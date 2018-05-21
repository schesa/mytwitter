import argparse

import mytwitter.config

from mytwitter.db import api as db_api
from mytwitter.server import rpc
from mytwitter import log

CONF = mytwitter.config.CONF

parser = argparse.ArgumentParser(description='mytwitter RPC server.')
parser.add_argument('--config-path', required=True,
                    help='The config file path.')


def main():
    args = parser.parse_args()

    CONF.load_config(args.config_path)
    log.configure_logging()

    db_api.initialize()
    db_api.create_tables()

    rpc_server = rpc.MyTwitterServerRPCAPI()
    rpc_server.accept()
