#!/bin/python

import argparse
import sys

from bitfeeds.exchange import ExchangeGateway
# from bitfeeds.broker.bitmex import ExchGwBitmex
# from bitfeeds.broker.btcc import ExchGwBtccSpot, ExchGwBtccFuture
# from bitfeeds.broker.bitfinex import ExchGwBitfinex
# from bitfeeds.broker.okcoin import ExchGwOkCoin
# from bitfeeds.broker.kraken import ExchGwKraken
# from bitfeeds.broker.gdax import ExchGwGdax
from bitfeeds.broker.bitstamp import BitstampGateway
# from bitfeeds.broker.gatecoin import ExchGwGatecoin
# from bitfeeds.broker.quoine import ExchGwQuoine
# from bitfeeds.broker.poloniex import ExchGwPoloniex
# from bitfeeds.broker.bittrex import ExchGwBittrex
# from bitfeeds.broker.yunbi import ExchGwYunbi
# from bitfeeds.broker.liqui import ExchGwLiqui
from bitfeeds.broker.binance import BinanceGateway
# from bitfeeds.broker.cryptopia import ExchGwCryptopia
# from bitfeeds.broker.cryptopia import CryptopiaBroker

from bitfeeds.storage.kdbplus import KdbPlusStorage
from bitfeeds.storage.sqlite import SqliteStorage
from bitfeeds.storage.zeromq import ZmqStorage
from bitfeeds.storage.mysql import MysqlStorage
from bitfeeds.storage.file import FileStorage

from bitfeeds.subscription import SubscriptionManager
from bitfeeds.util import Logger


def main():
    parser = argparse.ArgumentParser(description='Bitcoin exchange market data feed handler.')
    parser.add_argument('-instmts', action='store', help='Instrument subscription file.', default='subscriptions.ini')
    parser.add_argument('-exchtime', action='store_true', help='Use exchange timestamp.')
    parser.add_argument('-kdb', action='store_true', help='Use Kdb+ as database.')
    parser.add_argument('-csv', action='store_true', help='Use csv file as database.')
    parser.add_argument('-sqlite', action='store_true', help='Use SQLite database.')
    parser.add_argument('-mysql', action='store_true', help='Use MySQL.')
    parser.add_argument('-zmq', action='store_true', help='Use zmq publisher.')
    parser.add_argument('-mysqldest', action='store', dest='mysqldest',
                        help='MySQL destination. Formatted as <name:pwd@host:port>',
                        default='')
    parser.add_argument('-mysqlschema', action='store', dest='mysqlschema',
                        help='MySQL schema.',
                        default='')
    parser.add_argument('-kdbdest', action='store', dest='kdbdest',
                        help='Kdb+ destination. Formatted as <host:port>',
                        default='')
    parser.add_argument('-zmqdest', action='store', dest='zmqdest',
                        help='Zmq destination. For example \"tcp://127.0.0.1:3306\"',
                        default='')
    parser.add_argument('-sqlitepath', action='store', dest='sqlitepath',
                        help='SQLite database path',
                        default='')
    parser.add_argument('-csvpath', action='store', dest='csvpath',
                        help='Csv file path',
                        default='')
    parser.add_argument('-output', action='store', dest='output',
                        help='Verbose output file path')
    args = parser.parse_args()

    Logger.init_log(args.output)

    storages = []
    is_database_defined = False
    
    if args.sqlite:
        storage = SqliteStorage()
        storage.connect(path=args.sqlitepath)
        storages.append(storage)
        is_database_defined = True

    if args.mysql:
        storage = MysqlStorage()
        mysqldest = args.mysqldest
        logon_credential = mysqldest.split('@')[0]
        connection = mysqldest.split('@')[1]
        
        storage.connect(host=connection.split(':')[0],
                          port=int(connection.split(':')[1]),
                          user=logon_credential.split(':')[0],
                          pwd=logon_credential.split(':')[1],
                          schema=args.mysqlschema)
        
        storages.append(storage)
        is_database_defined = True

    if args.csv:
        if args.csvpath != '':
            storage = FileStorage(dir=args.csvpath)
        else:
            storage = FileStorage()

        storages.append(storage)
        is_database_defined = True
    
    if args.kdb:
        storage = KdbPlusStorage()
        storage.connect(host=args.kdbdest.split(':')[0], port=int(args.kdbdest.split(':')[1]))
        storages.append(storage)
        is_database_defined = True

    if args.zmq:
        storage = ZmqStorage()
        storage.connect(addr=args.zmqdest)
        storages.append(storage)
        is_database_defined = True

    if not is_database_defined:
        print('Error: Please define which database is used.')
        parser.print_help()
        sys.exit(1)

    # Subscription instruments
    if args.instmts is None or len(args.instmts) == 0:
        print('Error: Please define the instrument subscription list. You can refer to subscriptions.ini.')
        parser.print_help()
        sys.exit(1)
        
    # Use exchange timestamp rather than local timestamp
    if args.exchtime:
        ExchangeGateway.is_local_timestamp = False
    
    # Initialize subscriptions
    subscription_instmts = SubscriptionManager(args.instmts).get_subscriptions()
    
    if len(subscription_instmts) == 0:
        print('Error: No instrument is found in the subscription file. ' +
              'Please check the file path and the content of the subscription file.')
        
        parser.print_help()
        sys.exit(1)        
    
    # Initialize snapshot destination
    ExchangeGateway.init_snapshot_table(storages)
    Logger.info(__name__, 'Subscription file = %s' % args.instmts)
    log_str = 'Exchange/Instrument/InstrumentCode:\n'
    
    for instmt in subscription_instmts:
        log_str += '%s/%s/%s\n' % (instmt.exchange_name, instmt.instmt_name, instmt.instmt_code)
    
    Logger.info(__name__, log_str)
    
    gateways = []
    # gateways.append(ExchGwBtccSpot(storages))
    # gateways.append(ExchGwBtccFuture(storages))
    # gateways.append(ExchGwBitmex(storages))
    # gateways.append(ExchGwBitfinex(storages))
    # gateways.append(ExchGwOkCoin(storages))
    # gateways.append(ExchGwKraken(storages))
    # gateways.append(ExchGwGdax(storages))
    gateways.append(BitstampGateway(storages))
    # gateways.append(ExchGwGatecoin(storages))
    # gateways.append(ExchGwQuoine(storages))
    # gateways.append(ExchGwPoloniex(storages))
    # gateways.append(ExchGwBittrex(storages))
    # gateways.append(ExchGwYunbi(storages))
    # gateways.append(ExchGwLiqui(storages))
    gateways.append(BinanceGateway(storages))
    # gateways.append(ExchGwCryptopia(storages))

    threads = []

    for item in gateways:
        for instmt in subscription_instmts:
            if instmt.get_exchange_name() == item.get_exchange_name():
                Logger.info(__name__, "Starting instrument %s-%s..." % \
                    (instmt.get_exchange_name(), instmt.get_instmt_name()))
                threads += item.start(instmt)

if __name__ == '__main__':
    main()
