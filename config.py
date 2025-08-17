WALLET_PATH = "/enter/your/wallet/path"
WALLET_NAME = "Wallet Name"
NETWORK = "finney"

STAKE_AMOUNT_SIMPLE = 0.1
NETUIDS_TO_STAKE_SIMPLE = [19, 56, 64]

STAKE_CONFIG_ADVANCED = {
    19: {"default_stake": 0.1, "sub_level_stakes": None},
    56: {"default_stake": 0.2, "sub_level_stakes": [[0.047, 0.25]]},
    64: {"default_stake": 0.3, "sub_level_stakes": [[0.1386, 0.5], [0.1179, 0.6]]}
}
