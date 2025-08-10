# Bittensor Subnet DCA
A Python program to execute multiple Bittensor subnet staking operations at once for the purpose of DCAing, intended to save time by eliminating the need to individually stake into each subnet being 'DCAd' into; incorporating 2 program options for different staking configurations.

### Features
- Checks wallet balances (free TAO, root stake, alpha stake) before staking
- Checks subnet delegation, confirms which delegator to use if multiple and prompts user confirmation
- Supports unstaking from root if free TAO is insufficient to make stakes
- Performs user-defined staking operations into specified subnets


## Prerequisites
- Python 3.8+
- Bittensor library
- A configured Bittensor wallet with TAO


## Installation
Clone the repo:
```bash
git clone https://github.com/Ca5parAD/Bittensor-Subnet-DCA.git
cd Bittensor-Subnet-DCA
```


## Usage
The file includes 2 program options for different levels of staking configuration complexity:

- **simple_dca** uses the same stake amount for all subnets
- **advanced_dca** allows for different stake amounts on each subnet and under specified price levels

### For both programs
Edit config.json to declar wallet path, name and network to be used:
- wallet_path: Path to your Bittensor wallet
- wallet_name: Wallet name
- network: 'finney' for mainnet or 'test' for testnet

#### Example
```json
"wallet_path": "/Users/<user>/.bittensor/wallets",
"wallet_name": "MyWallet",
"network": "finney",
```

### For simple_dca
Edit simple_dca.py to set:
- stake_amount_simple: Stake amount per subnet
- netuids_to_stake_simple: list of netuids to stake into

#### Example
```json
"stake_amount_simple": 0.1,
"netuids_to_stake_simple": [19, 56, 64],
```

### For advanced_dca
Edit advanced_dca.py to set:
- STAKE_CONFIG: Staking configuration - default stake and stake amount under price levels

#### Example
```json
"stake_config_advanced": {
        "19": {"default_stake": 0.8, "sub_level_stakes": null},
        "56": {"default_stake": 1, "sub_level_stakes": [[0.047, 2], [0.0366, 3]]},
        "64": {"default_stake": 0.75, "sub_level_stakes": [[0.1386, 1.5]]}
    }
```

### Run the script:
```bash
python dca_simple.py
```
or
```bash
python dca_advanced.py
```

> [!IMPORTANT]
> - Requires an initial stake on each subnet
> - Use testnet for safe testing before mainnet


## Contributing
Contributions welcome! Open an issue or submit a pull request

## License
MIT License (LICENSE)