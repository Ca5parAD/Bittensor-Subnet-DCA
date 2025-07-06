# Bittensor Subnet DCA

A Python program to automate Dollar-Cost Averaging (DCA) staking into Bittensor subnets, supporting both testnet and mainnet.

## Features
- Stakes a user-defined TAO amount into specified subnets.
- Checks wallet balances (free TAO, root stake, alpha stake) before staking.
- Supports unstaking from root subnet if free TAO is insufficient.
- Validates subnet delegation and prompts user confirmation.

## Prerequisites
- Python 3.8+
- Bittensor library
- A configured Bittensor wallet with TAO (testnet or mainnet)

## Installation
Clone the repo:
```bash
git clone https://github.com/Ca5parAD/Bittensor-Subnet-DCA.git
cd Bittensor-Subnet-DCA
```

## Usage
Edit auto_dca.py to set:
- your_wallet_path: Path to your Bittensor wallet.
- your_wallet_name: Wallet name.
- your_network: 'finney' for mainnet or 'test' for testnet.
- stake_amount: TAO to stake per subnet.
- netuids_to_stake: List of subnet IDs.

### Example
```py
your_wallet_path = '/Users/<user>/.bittensor/wallets'
your_wallet_name = 'MyWallet'
your_network = 'finney'
stake_amount = 0.1
netuids_to_stake = [1, 3, 56, 64]
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
