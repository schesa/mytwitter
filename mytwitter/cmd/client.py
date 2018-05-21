import argparse

import mytwitter.config

from mytwitter.client import rpc
from mytwitter import log

CONF = mytwitter.config.CONF

parser = argparse.ArgumentParser(description='mytwitter RPC client.')
parser.add_argument('--config-path', required=True,
                    help='The config file path.')


def main():
    args = parser.parse_args()

    CONF.load_config(args.config_path)
    log.configure_logging()

    rpc_server = rpc.MyTwitterClientRPCAPI()  # noqa

    # Ran out of time before adding some CLI. Here, have
    # a PDB breakpoint instead.
    from mytwitter.db import api  # noqa
    import pdb; pdb.set_trace()  # noqa

    # rpc_server.call()  # noqa
