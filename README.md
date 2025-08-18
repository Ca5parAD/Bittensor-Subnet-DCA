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
Edit `config.py` to declare wallet path, name, and network to be used:
- WALLET_PATH: Path to your Bittensor wallet
- WALLET_NAME: Wallet name
- NETWORK: 'finney' for mainnet or 'test' for testnet

#### Example
```python
WALLET_PATH = "/Users/<user>/.bittensor/wallets"
WALLET_NAME = "MyWallet"
NETWORK = "finney"
```

### For simple_dca
Edit `config.py` to set:
- STAKE_AMOUNT_SIMPLE: Stake amount per subnet
- NETUIDS_TO_STAKE_SIMPLE: list of netuids to stake into

#### Example
```python
STAKE_AMOUNT_SIMPLE = 0.1
NETUIDS_TO_STAKE_SIMPLE = [19, 56, 64]
```

### For advanced_dca
Edit `config.py` to set:
- STAKE_CONFIG_ADVANCED: Staking configuration - default stake and stake amount under price levels

#### Example
```python
STAKE_CONFIG_ADVANCED = {
    19: {"default_stake": 0.2, "sub_level_stakes": None},
    56: {"default_stake": 0.1, "sub_level_stakes": [[0.047, 0.2], [0.0366, 0.3]]},
    64: {"default_stake": 0.15, "sub_level_stakes": [[0.1386, 0.2]]}
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