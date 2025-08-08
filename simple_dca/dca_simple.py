import bittensor
import auto_dca_utils_simple as utils
import json

# Load config
with open('../config.json', 'r') as config_file:
    config = json.load(config_file)

# Populate personal info
WALLET_PATH = config['wallet_path']
WALLET_NAME = config['wallet_name']
NETWORK = config['network']

STAKE_AMOUNT_SIMPLE = config['stake_amount_simple']
NETUIDS_TO_STAKE_SIMPLE = config['netuids_to_stake_simple']


# Setup wallet and subtensor
try:
    wallet = bittensor.wallet(path=WALLET_PATH, name=WALLET_NAME)
    subtensor = bittensor.subtensor(network=NETWORK)

except:
    print('Something went wrong connecting to the Bittensor network')
    
wallet_info = utils.WalletOperationFunctionality(wallet, subtensor) # Create wallet functionality object

wallet_info.print_balances()
wallet_info.check_netuids_to_stake(NETUIDS_TO_STAKE_SIMPLE, STAKE_AMOUNT_SIMPLE)

utils.continue_check('Correct?')

wallet_info.check_balances_for_stake()
wallet_info.organise_hotkeys_to_stake()

utils.continue_check('Continue?')

wallet_info.make_stakes()

wallet_info.__init__(wallet, subtensor) # Re-initialise wallet
wallet_info.print_balances()

