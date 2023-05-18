# Bulk Run Bridges LayerZero

<a href="https://imgbb.com/"><img src="https://i.ibb.co/wQQHdZ7/gui.png" alt="gui" border="0"></a>

## Functional
* Bridges currently supported: Stargate, Aptos Bridge
* Supported networks: Arbitrum, Optimism, Avalanche, Polygon, Fantom, BSC, Ethereum, Aptos (бридж только в аптос).
* Supported networks: Ethereum (only between Eth mainnet, Arbitrum, Optimism), USDC, USDT.
* Random selection of the number of tokens for the bridge.
* Bridge from all wallets to one address.

## Config 
You can run the script through the gui interface or directly with the settings from the config file (config.yaml).

Config:
* Address to send - an optional choice if you want to bridge from all cartoons to one wallet. You can enter the e-mail address or aptos if you bridge into it.
* Min amount и max amount to bridge - the range in which the amount for the bridge is randomly selected. If you do not need a random, then simply enter the same values \u200b\u200bin both fields.
* Slippage - Slipper selection in percent (ex: 0.5 = 0.5%)
* Gas limit - each network needs a different gas limit, but you can set a large value in advance, in the end, the gas_estimate required by the network will be used **gas_limit * 1.5**
* Gas price - the default is automatic, but if the network is loaded at the moment it can throw errors, so you can select it manually
* Test mode - You can run it in test mode, the script will check the correctness of the transaction and show estimate gas.
* Choose RPC - put random public rpc. In case of a rate limit, you can replace it manually via **contracts/rpcs.py**

## Wallets
All addresses and privates are inserted into the file from a new line.

* We throw privates from evm wallets into a file **evm_wallets.txt** (only 0х...)

* Addresses aptos wallets into a file **aptos_wallets.txt**

P.S. The number of aptos and eum wallets should be the same if you want each eum address bridged to a separate aptos wallet.

## Running a script

```bash
pip install -r req.txt
```

## Using

```cmd
python run_gui.py

```
Launch via gui interface 
```cmd
python run_config.py

```
Launch via config file (config.yaml)

## Bridge process

! For the first time, I recommend running everything in **test mode**

The script will first check the approvals (if you are not bridging on air), if there are no approvals, then it will approve everything itself and only then start the bridge.

Before the bridge, you can check the table of commissions of the stargate itself in the table on the bridge page (Transfer Gas Estimator). Therefore, for the bridge, throw in the native token for the approval, the coms of the bridge and the transaction itself.
