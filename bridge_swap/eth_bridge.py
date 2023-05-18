import time

from bridge_swap.base_bridge import BridgeBase
from src.files_manager import read_evm_wallets_from_file
from web3_checksum.get_checksum_address import get_checksum_address
from src.schemas.config import ConfigSchema
from src.config import print_config

from web3 import Web3
from loguru import logger


def eth_mass_transfer(config_data: ConfigSchema):
    print_config(config=config_data,
                 log_text="Starting ETH bridge in 5 sec")

    eth_bridge = EthBridgeManual(config=config_data)
    wallets = read_evm_wallets_from_file()
    wallet_number = 1
    for wallet in wallets:
        eth_bridge.transfer(private_key=wallet, wallet_number=wallet_number)
        get_address = get_checksum_address(private_key=wallet)
        wallet_number += 1


class EthBridgeManual(BridgeBase):
    def __init__(self, config: ConfigSchema):
        super().__init__(config=config)

    def transfer(self, private_key, wallet_number):
        source_wallet_address = self.get_wallet_address(private_key=private_key)
        wallet_eth_balance = self.get_eth_balance(source_wallet_address)
        wallet_address = self.get_wallet_address(private_key=private_key)
        eth_amount_out = self.get_random_amount_out(min_amount=self.min_bridge_amount,
                                                    max_amount=self.max_bridge_amount)

        if wallet_eth_balance < eth_amount_out:
            logger.error(f"[{wallet_number}] [{source_wallet_address}] - not enough native"
                         f" ({Web3.from_wei(eth_amount_out, 'ether')} ETH) "
                         f"to bridge. Balance: {Web3.from_wei(wallet_eth_balance, 'ether')} ETH")
            return

        if self.config_data.send_to_one_address is True:
            dst_wallet_address = Web3.to_checksum_address(self.config_data.address_to_send)
        else:
            dst_wallet_address = wallet_address

        txn = self.build_eth_bridge_tx(wallet_address=wallet_address,
                                       dst_wallet_address=dst_wallet_address,
                                       amount_out=eth_amount_out,
                                       chain_id=self.target_chain.chain_id)
        try:
            estimated_gas_limit = self.get_estimate_gas(transaction=txn)

            if self.config_data.gas_limit > estimated_gas_limit:
                txn['gas'] = int(estimated_gas_limit + (estimated_gas_limit * 0.3))

            if self.config_data.test_mode is True:
                logger.info(f"[{wallet_number}] [{source_wallet_address}] - Estimated gas limit for {self.source_chain.name} → "
                            f"{self.target_chain.name} "
                            f"ETH bridge: {estimated_gas_limit}")
                return

            signed_txn = self.web3.eth.account.sign_transaction(txn, private_key=private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            logger.info(f"[{wallet_number}] [{source_wallet_address}] - Transaction sent: {tx_hash.hex()}")
        except Exception as e:
            logger.error(f"[{wallet_number}] [{source_wallet_address}] - Error while sending ETH bridge txn: {e}")
            return
