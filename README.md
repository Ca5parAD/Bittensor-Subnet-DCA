# Bittensor Subnet DCA
A Python program to execute multiple Bittensor subnet staking operations at once for the purpose of DCAing, intended to save time by eliminating the need to individually stake into each subnet being 'DCAd' into; incorporating 2 program options for different staking configurations.

### Features
- Checks wallet balances (free TAO, root stake, alpha stake) before staking.
- Validates subnet delegation and prompts user confirmation.
- Supports unstaking from root if free TAO is insufficient to make stake.
- Performs user-defined staking operations into specified subnets.

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

- **auto_dca_simple** uses the same stake amount for all subnets

- **Auto_DCA_Advanced** allows for different stake amounts on each subnet and under specified price levels


### For auto_dca_simple
Edit auto_dca_simple.py to set:
- YOUR_WALLET_PATH: Path to your Bittensor wallet.
- YOUR_WALLET_NAME: Wallet name.
- YOUR_NETWORK: 'finney' for mainnet or 'test' for testnet.
  
- STAKE_AMOUNT: TAO to stake per subnet.
- NETUIDS_TO_STAKE: List of subnet IDs.

#### Example
```py
YOUR_WALLET_PATH: Final = '/Users/<user>/.bittensor/wallets'
YOUR_WALLET_NAME: Final = 'MyWallet'
YOUR_NETWORK: Final = 'finney'

STAKE_AMOUNT: Final = 0.1
NETUIDS_TO_STAKE: Final = [1, 3, 56, 64]
```

### For auto_dca_advanced
Edit auto_dca_advanced.py to set:
- YOUR_WALLET_PATH: Path to your Bittensor wallet.
- YOUR_WALLET_NAME: Wallet name.
- YOUR_NETWORK: 'finney' for mainnet or 'test' for testnet.

- STAKE_CONFIG: Staking configuration - default stake and stake amount under price levels

#### Example
```py
YOUR_WALLET_PATH = '/Users/<user>/.bittensor/wallets'
YOUR_WALLET_NAME = 'MyWallet'
YOUR_NETWORK = 'finney'

STAKE_CONFIG = { # Make sure multiplier levels are in descending order
    1: {'default_stake': 0.3, 'sub_level_stakes': [(0.0275, 0.4), (0.0193, 0.5)]},
    4: {'default_stake': 0.25, 'sub_level_stakes': None},
    64: {'default_stake': 0.75, 'sub_level_stakes': [(0.1386, 1.5), (0.1179, 2)]}
}
```


### Run the script:
```bash
python auto_dca.py
```
or
```bash
python auto_dca_simple.py
```

> [!NOTE]
> - Requires an initial stake on each subnet.
> - Use testnet for safe testing before mainnet.

## Contributing
Contributions welcome! Open an issue or submit a pull request.

## License
MIT License (LICENSE)
