# Bittensor Subnet DCA

A Python program to execute multiple subnet DCA's at once; intended to save time by eliminating the need to individually stake into each subnet you are DCAing into.

## Features
- Stakes a user-defined TAO amount into specified subnets.
- Checks wallet balances (free TAO, root stake, alpha stake) before staking.
- Supports unstaking from root subnet if free TAO is insufficient.
- Validates subnet delegation and prompts user confirmation.

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
Edit auto_dca.py to set:
- YOUR_WALLET_PATH: Path to your Bittensor wallet.
- YOUR_WALLET_NAME: Wallet name.
- YOUR_NETWORK: 'finney' for mainnet or 'test' for testnet.
- STAKE_AMOUNT: TAO to stake per subnet.
- NETUIDS_TO_STAKE: List of subnet IDs.

### Example
```py
YOUR_WALLET_PATH = '/Users/<user>/.bittensor/wallets'
YOUR_WALLET_NAME = 'MyWallet'
YOUR_NETWORK = 'finney'

STAKE_AMOUNT = 0.1
NETUIDS_TO_STAKE = [1, 3, 56, 64]
```

## Run the script:
```bash
python auto_dca.py
```
**Confirm staking details and proceed as prompted**

## Notes
- Requires an initial stake on each subnet.
- Root unstaking option available if free TAO is insufficient.
- Use testnet for safe testing before mainnet.

## Contributing
Contributions welcome! Open an issue or submit a pull request.

## License
MIT License (LICENSE)
