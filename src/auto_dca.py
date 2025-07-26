import bittensor
import auto_dca_utils as utils 

# ********** Please fill: **********

'''E.g.
YOUR_WALLET_PATH = '/enter/your/wallet/path'
YOUR_WALLET_NAME = 'Wallet Name'
YOUR_NETWORK = 'finney' # or 'test' for testnet

STAKE_AMOUNT = 0.1 # Amount (tao) to stake per subnet
NETUIDS_TO_STAKE = [1, 3, 56, 64] # List of subnets to stake into'''

YOUR_WALLET_PATH = ''
YOUR_WALLET_NAME = ''
YOUR_NETWORK = 'finney'

STAKE_CONFIG = {
    3: {'default_stake': 0.4, 'sub_level_stakes': [(0.012, 1.5), (0.0114, 1.8)]},
    8: {'default_stake': 0.5, 'sub_level_stakes': None},
    64: {'default_stake': 1, 'sub_level_stakes': [(0.138, 1.5), (0.114, 2.0)]},
    75: {'default_stake': 0.6, 'sub_level_stakes': [(0.104, 1.3), (0.0885, 1.5)]}
} # Make sure multiplier levels are in descending order

# Look to impliment threading functionality to front run confirmations by start doing slow operations (access the network)
# aswell as multiple delegation checks ()
# **********************************

# Setup wallet and subtensor
try:
    wallet = bittensor.wallet(path=YOUR_WALLET_PATH, name=YOUR_WALLET_NAME)
    subtensor = bittensor.subtensor(network=YOUR_NETWORK)

except:
    print('Something went wrong connecting to the Bittensor network')
    quit()

else:
    print('Connection to Bittensor network successful')
    
# Create wallet functionality object
wallet_operations = utils.WalletOperationFunctionality(wallet, subtensor) 

wallet_operations.print_balances()
utils.continue_check('Correct?')

wallet_operations.config_stake_operations(STAKE_CONFIG)
wallet_operations.confirm_stake_operations()
utils.continue_check('Correct?')

wallet_operations.check_balances_for_stake()
utils.continue_check('Continue?')

wallet_operations.make_stakes()

wallet_operations.__init__(wallet, subtensor) # Re-initialise wallet
wallet_operations.print_balances()
