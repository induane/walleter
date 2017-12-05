from abc import ABCMeta, abstractmethod
import requests
import logging
import time


class BaseBlockExplorer(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.session = None
        self._base_url = None
        self._base_url_received = None
        self._base_url_balance = None
        self._received_suffix = '' #allow derived classes not to set this
        self._balance_suffix = ''

    @abstractmethod
    def open_session(self):
        logging.info("Opening new session to {}".format(self._base_url))
        self.session = requests.Session()
        open_session = self.session.get(self._base_url)
        if open_session.status_code != requests.codes.ok:
            raise Exception("Error: Failed to open connection to {}. Error: {}".format(self._base_url,
                                                                                       open_session.text))

    @abstractmethod
    def close_session(self):
        logging.debug("Closing session")
        self.session.close()
        self.session = None

    @abstractmethod
    def get_received(self, public_address):
        logging.debug("Getting received bitcoins for public address {}".format(public_address))
        if not self.session:
            raise Exception("Error: Need to open_session first before executing get_received")
        received_url = "{}/{}{}".format(self._base_url_received, public_address, self._received_suffix)
        logging.debug("requesting data from {}".format(received_url))
        bitcoins_received_text = self.session.get(received_url).text
        try:
            bitcoins_received = self.text_to_float(bitcoins_received_text)
        except Exception as e:
            logging.error("Got invalid received bitcoins response: '{}'".format(bitcoins_received_text))
            raise
        return bitcoins_received

    @abstractmethod
    def get_balance(self, public_address):
        logging.debug("Getting balance for public address {}".format(public_address))
        if not self.session:
            raise Exception("Error: Need to open_session before executing get_balance")
        balance_url = "{}/{}{}".format(self._base_url_balance, public_address, self._balance_suffix)
        logging.debug("requesting data from {}".format(balance_url))
        bitcoin_balance_text = self.session.get(balance_url).text
        try:
            bitcoin_balance = self.text_to_float(bitcoin_balance_text)
        except Exception as e:
            logging.error("Got invalid bitcoin balance response: '{}'".format(bitcoin_balance_text))
            raise
        return bitcoin_balance

    @staticmethod
    def text_to_float(text):
        try:
            return float(text)
        except Exception:
            raise

    @staticmethod
    def satoshi_to_btc(value):
        try:
            return value / 100000000.00000000
        except Exception:
            raise


class BlockchainInfo(BaseBlockExplorer):
    STRING_TYPE = "blockchaininfo"

    def __init__(self):
        BaseBlockExplorer.__init__(self)
        self._api_limit_seconds = 10
        logging.info("Note there is a {} second wait between each API call to respect posted limits".format(self._api_limit_seconds))
        self._base_url = "http://blockchain.info"
        self._base_url_received = "{}/q/getreceivedbyaddress".format(self._base_url)
        self._base_url_balance = "{}/q/addressbalance".format(self._base_url)

    def open_session(self):
        return BaseBlockExplorer.open_session(self)

    def close_session(self):
        return BaseBlockExplorer.close_session(self)

    def get_balance(self, public_address):
        logging.debug("Sleeping {} seconds before making API call".format(self._api_limit_seconds))
        time.sleep(self._api_limit_seconds)
        try:
            balance = BaseBlockExplorer.get_balance(self, public_address)
            btc_balance = self.satoshi_to_btc(balance)
        except Exception as e:
            raise
        return btc_balance

    def get_received(self, public_address):
        logging.debug("Sleeping {} seconds before making API call".format(self._api_limit_seconds))
        time.sleep(self._api_limit_seconds)
        try:
            received = BaseBlockExplorer.get_received(self, public_address)
            btc_received = self.satoshi_to_btc(received)
        except Exception as e:
            raise
        return btc_received
