# ********** Please fill: **********

# E.g.
# your_wallet_path = '/enter/your/wallet/path'
# your_wallet_name = 'Wallet Name'
# your_network = 'finney' # or 'test' for testnet
#
# stake_amount = 0.1 # Amount (tao) to stake per subnet
# netuids_to_stake = [1, 3, 56, 64] # List of subnets to stake into

your_wallet_path = ''
your_wallet_name = ''
your_network = 'finney'

stake_amount = 0.1
netuids_to_stake = []

# **********************************

import bittensor
import auto_dca_utils as custom 

# Setup wallet and subtensor
wallet = bittensor.wallet(path=your_wallet_path, name=your_wallet_name)
subtensor = bittensor.subtensor(network=your_network)

wallet_info = custom.WalletOperationFunctionality(wallet, subtensor) # Create wallet functionality object

wallet_info.print_balances()

wallet_info.check_netuids_to_stake(netuids_to_stake, stake_amount)

custom.continue_check('Correct?')

wallet_info.check_balances_for_stake(stake_amount*len(netuids_to_stake))
wallet_info.organise_hotkeys_to_stake()

custom.continue_check('\nContinue?')

wallet_info.make_stakes()

wallet_info.__init__(wallet, subtensor) # Re-initialise wallet
wallet_info.print_balances()