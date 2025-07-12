# ********** Please fill: **********

# E.g.
# YOUR_WALLET_PATH = '/enter/your/wallet/path'
# YOUR_WALLET_NAME = 'Wallet Name'
# YOUR_NETWORK = 'finney' # or 'test' for testnet
#
# STAKE_AMOUNT = 0.1 # Amount (tao) to stake per subnet
# NETUIDS_TO_STAKE = [1, 3, 56, 64] # List of subnets to stake into

YOUR_WALLET_PATH = ''
YOUR_WALLET_NAME = ''
YOUR_NETWORK = 'finney'

STAKE_AMOUNT = 0.1
NETUIDS_TO_STAKE = []

# **********************************

import bittensor
import auto_dca_utils as custom 

# Setup wallet and subtensor
try:
    wallet = bittensor.wallet(path=YOUR_WALLET_PATH, name=YOUR_WALLET_NAME)
    subtensor = bittensor.subtensor(network=YOUR_NETWORK)

except:
    print('Something went connecting to the Bittensor network')
    
wallet_info = custom.WalletOperationFunctionality(wallet, subtensor) # Create wallet functionality object

wallet_info.print_balances()
wallet_info.check_netuids_to_stake(NETUIDS_TO_STAKE, STAKE_AMOUNT)

custom.continue_check('Correct?')

wallet_info.check_balances_for_stake(STAKE_AMOUNT*len(NETUIDS_TO_STAKE))
wallet_info.organise_hotkeys_to_stake()

custom.continue_check('\nContinue?')

wallet_info.make_stakes()

wallet_info.__init__(wallet, subtensor) # Re-initialise wallet
wallet_info.print_balances()