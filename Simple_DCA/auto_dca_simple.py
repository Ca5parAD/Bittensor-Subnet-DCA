import bittensor
import auto_dca_utils_simple as utils

# ********** Please fill: **********

'''E.g.
YOUR_WALLET_PATH = '/enter/your/wallet/path'
YOUR_WALLET_NAME = 'Wallet Name'
YOUR_NETWORK = 'finney' # or 'test' for testnet

STAKE_AMOUNT = 0.1 # Amount (tao) to stake per subnet
NETUIDS_TO_STAKE = [1, 3, 56, 64] # List of subnets to stake into'''

YOUR_WALLET_PATH = '/Users/caspar/Bittensor/.bittensor/wallets'
YOUR_WALLET_NAME = 'Chrome (5CXr)'
YOUR_NETWORK = 'finney'

STAKE_AMOUNT = 0.75
NETUIDS_TO_STAKE = [1, 3, 4, 8, 13, 19, 37, 56, 64, 75]

# **********************************

# Setup wallet and subtensor
try:
    wallet = bittensor.wallet(path=YOUR_WALLET_PATH, name=YOUR_WALLET_NAME)
    subtensor = bittensor.subtensor(network=YOUR_NETWORK)

except:
    print('Something went wrong connecting to the Bittensor network')
    
wallet_info = utils.WalletOperationFunctionality(wallet, subtensor) # Create wallet functionality object

wallet_info.print_balances()
wallet_info.check_netuids_to_stake(NETUIDS_TO_STAKE, STAKE_AMOUNT)

utils.continue_check('Correct?')

wallet_info.check_balances_for_stake()
wallet_info.organise_hotkeys_to_stake()

utils.continue_check('Continue?')

wallet_info.make_stakes()

wallet_info.__init__(wallet, subtensor) # Re-initialise wallet
wallet_info.print_balances()

