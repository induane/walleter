import logging

from coinkit import BitcoinKeypair

LOG = logging.getLogger(__name__)


class Wallet(object):

    def __init__(self, passphrase, private_key=False):
        self.passphrase = passphrase
        if private_key:
            self.keypair = BitcoinKeypair.from_private_key(
                self.passphrase.encode('ascii')
            )
        else:
            try:
                self.keypair = BitcoinKeypair.from_passphrase(self.passphrase)
            except Exception:
                LOG.exception(u'Failed to generate keypair from {0}'.format(
                    self.passphrase
                ))
                raise

    @property
    def address(self):
        return self.keypair.address()

    @property
    def private_key(self):
        return self.keypair.private_key()

    @property
    def private_key_wif(self):
        return self.keypair.private_key(format='wif')

    @property
    def private_key_bin(self):
        return self.keypair.private_key(format='bin')

    @property
    def public_key(self):
        return self.keypair.public_key()
