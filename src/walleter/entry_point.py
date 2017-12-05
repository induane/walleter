"""Walleter command line entry point."""
# Standard
import argparse
import errno
import logging
import os
import pkg_resources
import sys
import time
from logging.config import dictConfig

# Boltons
from boltons.iterutils import windowed_iter
from log_color import ColorFormatter, ColorStripper

# Project
from walleter.utils.arg_format import ArgFormatter
from walleter.utils.blockchain import BlockchainInfo
from walleter.utils.wallet import Wallet

LOG = logging.getLogger(__name__)
DEST_ADDRESS = '16Mfp5hjBmro5p4Kg6z4XqvVmrWbzq17px'

# Setup the version string globally
try:
    pkg_version = "%(prog)s {0}".format(
        pkg_resources.get_distribution("walleter").version
    )
except pkg_resources.DistributionNotFound:
    pkg_version = '%(prog)s Development'
except Exception:
    pkg_version = '%(prog)s Unknown'

# Py Compat
if sys.version_info[0] == 3:
    xrange = range


def logging_init(level, logfile=None, verbose=False):
    """
    Given the log level and an optional logging file location, configure
    all logging.
    """
    # Get logging related arguments & the configure logging
    if logfile:
        logfile = os.path.abspath(logfile)

    # Don't bother with a file handler if we're not logging to a file
    handlers = ['console', 'filehandler'] if logfile else ['console', ]

    # If the main logging level is any of these, set librarys to WARNING
    lib_warn_levels = ('DEBUG', 'INFO', 'WARNING', )

    # The base logging configuration
    BASE_CONFIG = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'ConsoleFormatter': {
                '()': ColorFormatter,
                'format': '%(levelname)s: %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
            'FileFormatter': {
                '()': ColorStripper,
                'format': ("%(levelname)-8s: %(asctime)s '%(message)s' "
                           '%(name)s:%(lineno)s'),
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG' if verbose else level,
                'class': 'logging.StreamHandler',
                'formatter': 'ConsoleFormatter',
            },
        },
        'loggers': {
            'walleter': {
                'handlers': handlers,
                'level': 'DEBUG' if verbose else level,
                'propagate': False,
            },
            'requests': {
                'handlers': handlers,
                'level': 'WARNING' if level in lib_warn_levels else level,
                'propagate': False,
            },
        }
    }

    # If we have a log file, modify the dict to add in the filehandler conf
    if logfile:
        BASE_CONFIG['handlers']['filehandler'] = {
            'level': 'DEBUG' if verbose else level,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': logfile,
            'formatter': 'FileFormatter',
        }

    # Setup the loggers
    dictConfig(BASE_CONFIG)



def cli():
    parser = argparse.ArgumentParser(
        description="Wallet exploration tool",
        formatter_class=ArgFormatter,
    )
    parser.add_argument(
        "-i",
        "--iterations",
        dest="iterations",
        type=int,
        default=1,
        help="Number of iterations to derive"
    )
    parser.add_argument(
        "-b",
        "--bypass-iterations",
        dest="bypass",
        action='store_true',
        help="Skip interstitial iterations"
    )
    parser.add_argument(
        "-V",
        "--version",
        dest="version",
        action="version",
        version=pkg_version,
        help="Display the version number."
    )
    parser.add_argument(
        '-l',
        '--log-level',
        default='INFO',
        choices=('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'),
        help='Logging level for command output.',
        dest='log_level'
    )
    parser.add_argument(
        '-L',
        '--logfile',
        dest='logfile',
        default=None,
        help='Location to place a log of the process output'
    )
    parser.add_argument(
        '-s',
        '--seed',
        dest='seed',
        default=None,
        help='Use a specific seed instead of core dataset'
    )
    parsed_args = parser.parse_args()
    logging_init(parsed_args.log_level, logfile=parsed_args.logfile)
    run(parsed_args.iterations,
        force_seed=parsed_args.seed, bypass=parsed_args.bypass)
    LOG.debug(u"#g<\u2713> Complete! Dataset exhausted.")


def iter_wallets(wallet, iterations):
    """Iterate a wallet feeding it's address into the next iteration."""
    prev = None
    for idx in xrange(iterations):
        if not prev:
            prev = wallet.address
            yield wallet
        else:
            try:
                new = Wallet(prev)
            except Exception:
                break
            else:
                prev = new.address
                yield new


def main():
    try:
        cli()
    except KeyboardInterrupt:
        # Write a nice message to stderr
        sys.stderr.write(
            u"\n\033[91m\u2717 Operation canceled by user.\033[0m\n"
        )
        sys.exit(errno.EINTR)


def run(iterations, force_seed=None, bypass=False):
    """Actual code shit."""

    home_folder = os.path.expanduser('~')
    config_dir = os.path.join(home_folder, '.walleter')

    if not os.path.exists(config_dir):
        os.mkdir(config_dir)

    cache_file = os.path.join(config_dir, 'check_cache')
    found_file = os.path.join(config_dir, 'found_coins')

    block_info = BlockchainInfo()
    LOG.info("Opening BlockchainInfo session")
    block_info.open_session()
    LOG.info("Session open")

    cache = []
    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            cache = [x.strip().strip('\r\n').strip('\n') for x
                     in f.readlines()]

    # If given a specific seed, conjure a dataset from that
    if force_seed is not None:
        if force_seed in ('""', '\'\''):
            force_seed = ''
        all_data = [force_seed]
        LOG.info('Using custom seed: {0}'.format(force_seed))
    else:
        from data import all_data_iter as all_data

    tried = set()
    for dict_word in all_data:
        dict_word = dict_word.strip()

        if dict_word in tried:
            continue  # already did that this session

        tried.add(dict_word)
        LOG.debug('Dict word: "{0}"'.format(dict_word))

        # Create initial wallet
        try:
            wallet = Wallet(dict_word)
        except Exception:
            continue

        for idx, wallet in enumerate(iter_wallets(wallet, iterations)):

            if bypass and idx + 1 != iterations:
                continue

            if wallet.address in cache:
                LOG.debug('Skipping cached address')
                continue

            LOG.debug('Checking address: {0}'.format(wallet.address))

            # Get received bitcoins
            retry = 0
            while retry < 5:
                try:
                    received_bitcoins = block_info.get_received(wallet.address)
                    break
                except Exception:
                    LOG.warning('Response invalid for received bitcoins. '
                                'Retrying in 5 seconds.')
                    time.sleep(5)
                    retry += 1
            if retry == 5:
                LOG.error('Retries exceeded; Skipping.')
                continue

            if not received_bitcoins:
                LOG.info('Wallet never had any coins. Moving along...')

                # Write address to cache file
                with open(cache_file, 'a') as f:
                    f.write("{0}\n".format(wallet.address))
                continue

            # Get current balance
            for _ in xrange(5):
                try:
                    balance = block_info.get_balance(wallet.address)
                    break
                except Exception:
                    LOG.warning('Response invallid for balance. Retrying in '
                                '5seconds.')
                    time.sleep(5)
                    retry += 1
            else:
                LOG.error('Retries exceeded; skipping.'.format(retry_count))
                continue

            if balance == 0.00:
                balance_str = '#y<{:.8f}>'.format(balance)
            else:
                balance_str = '#g<{:.8f}>'.format(balance)


            # Output results
            output = (
                'Wallet found: {}; Received: {:.8f}; Address: {}; Private '
                'Key: {}; Balance: {}'.format(
                    wallet.passphrase,
                    received_bitcoins,
                    wallet.address,
                    wallet.private_key_wif,
                    balance_str
                )
            )

            LOG.info(output)
            with open(found_file, 'a') as f:
                f.write(output)
                f.write("\n")


if __name__ == "__main__":
    main()
