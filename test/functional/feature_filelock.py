#!/usr/bin/env python3
# Copyright (c) 2018-2022 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Check that it's not possible to start a second bitcoind instance using the same datadir or wallet."""
import random
import string

from test_framework.test_framework import BitcoinTestFramework
from test_framework.test_node import (
    BAXIUM_PID_FILENAME_DEFAULT,
    ErrorMatch,
)

class FilelockTest(BitcoinTestFramework):
    def set_test_params(self):
        self.setup_clean_chain = True
        self.num_nodes = 2
        self.uses_wallet = None

    def setup_network(self):
        self.add_nodes(self.num_nodes, extra_args=None)
        self.nodes[0].start()
        self.nodes[0].wait_for_rpc_connection()

    def run_test(self):
        datadir = self.nodes[0].chain_path
        blocksdir = self.nodes[0].blocks_path
        self.log.info(f"Using datadir {datadir}")
        self.log.info(f"Using blocksdir {blocksdir}")

        self.log.info("Check that we can't start a second bitcoind instance using the same datadir")
        expected_msg = f"Error: Cannot obtain a lock on directory {datadir}. {self.config['environment']['CLIENT_NAME']} is probably already running."
        self.nodes[1].assert_start_raises_init_error(extra_args=[f'-datadir={self.nodes[0].datadir_path}', '-noserver'], expected_msg=expected_msg)

        self.log.info("Check that we can't start a second bitcoind instance using the same blocksdir")
        expected_msg = f"Error: Cannot obtain a lock on directory {blocksdir}. {self.config['environment']['CLIENT_NAME']} is probably already running."
        self.nodes[1].assert_start_raises_init_error(extra_args=[f'-blocksdir={self.nodes[0].datadir_path}', '-noserver'], expected_msg=expected_msg)

        self.log.info("Check that cookie and PID file are not deleted when attempting to start a second bitcoind using the same datadir/blocksdir")
        cookie_file = datadir / ".cookie"
        assert cookie_file.exists()  # should not be deleted during the second bitcoind instance shutdown
        pid_file = datadir / BAXIUM_PID_FILENAME_DEFAULT
        assert pid_file.exists()

        if self.is_wallet_compiled():
            wallet_name = ''.join([random.choice(string.ascii_lowercase) for _ in range(6)])
            self.nodes[0].createwallet(wallet_name=wallet_name)
            wallet_dir = self.nodes[0].wallets_path
            self.log.info("Check that we can't start a second bitcoind instance using the same wallet")
            expected_msg = f"Error: SQLiteDatabase: Unable to obtain an exclusive lock on the database, is it being used by another instance of {self.config['environment']['CLIENT_NAME']}?"
            self.nodes[1].assert_start_raises_init_error(extra_args=[f'-walletdir={wallet_dir}', f'-wallet={wallet_name}', '-noserver'], expected_msg=expected_msg, match=ErrorMatch.PARTIAL_REGEX)

if __name__ == '__main__':
    FilelockTest(__file__).main()
