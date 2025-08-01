import bittensor

STAKING_FEES = 0.0015 # Estimate of transaction fees

class WalletOperationFunctionality:
    def __init__(self, wallet, subtensor):
        self.WALLET = wallet
        self.SUBTENSOR = subtensor

        try:
            self.free_tao = float(self.SUBTENSOR.get_balance(address=self.WALLET.coldkeypub.ss58_address))
        except Exception as e:
            print(f"Error getting balance: {str(e)}")
            raise

        try:
            self.delegated_info = self.SUBTENSOR.get_delegated(coldkey_ss58=self.WALLET.coldkeypub.ss58_address)
        except Exception as e:
            print(f"Error getting delegated info: {str(e)}")
            raise

        self.delegated_info.sort(key=lambda info: info.netuid)
        self.root_stake = 0
        self.alpha_stake = 0
        self.raw_alpha_stakes_info = dict()
        self.duplicate_netuid_stakes = dict()

        for info in self.delegated_info:
            if info.netuid == 0:
                self.root_stake += float(info.stake) # Sums root stake
            else:
                if info.netuid in self.raw_alpha_stakes_info:
                    if info.netuid not in self.duplicate_netuid_stakes:
                        self.duplicate_netuid_stakes[info.netuid] = [(info.hotkey_ss58, info.owner_ss58)]
                    else:                        
                        self.duplicate_netuid_stakes[info.netuid].append((info.hotkey_ss58, info.owner_ss58))

                else:
                    try:
                        subnet_info = self.SUBTENSOR.subnet(netuid=info.netuid)
                    except Exception as e:
                        print(f"\nError getting subnet {info.netuid} info: {str(e)}")
                        raise

                    # Create dictionary of netuid keys and values of staking information
                    self.raw_alpha_stakes_info[info.netuid] = {
                        'netuid_name': subnet_info.subnet_name,
                        'price': float(subnet_info.price),
                        'delegator_hotkey': info.hotkey_ss58,
                        'delegator_owner': info.owner_ss58
                    }

                self.alpha_stake += float(info.stake) * float(subnet_info.price)


    def print_balances(self):
        print(f'\nFor coldkey: {self.WALLET.coldkeypub.ss58_address}')
        print(f'Free tao: τ{round(self.free_tao, 4)} | Root stake: τ{round(self.root_stake, 4)} | Alpha stake: τ{round(self.alpha_stake, 4)}')
        print(f'Total: τ{round(self.free_tao + self.root_stake + self.alpha_stake, 4)}')


    def config_stake_operations(self, stake_config):
        self.STAKE_CONFIG = stake_config
        self.stakes_to_make_info = dict()
        self.no_stake_netuids = []

        # Cycle through subnets to stake into
        for netuid, config in self.STAKE_CONFIG.items():
            if netuid in self.raw_alpha_stakes_info:
                self.stakes_to_make_info[netuid] = self.raw_alpha_stakes_info[netuid] # Append stake info to stakes to be made 
                stake_amount = config['default_stake']
                if config['sub_level_stakes'] is not None:
                    for level, stake in config['sub_level_stakes']:
                        if self.stakes_to_make_info[netuid]['price'] <= level:
                            stake_amount = stake
                self.stakes_to_make_info[netuid]['amount'] = stake_amount
            else:
                self.no_stake_netuids.append(netuid)


    def confirm_stake_operations(self):
        if self.no_stake_netuids:
            print(f'\nYou must manually make an initial stake on subnet(s) {self.no_stake_netuids} before using this program')
            exit()

        # Check this
        for netuid, hotkey_owner_pairs in self.duplicate_netuid_stakes.items():
            print(f'\nYou have multiple delegations on subnet {netuid}:')
            pairs_to_show = [(self.stakes_to_make_info[netuid]['delegator_hotkey'], self.stakes_to_make_info[netuid]['delegator_owner'])]
            for pair in hotkey_owner_pairs:
                pairs_to_show.append(pair)

            for i, pair in enumerate(pairs_to_show):
                try:
                    identity_info = self.SUBTENSOR.query_identity(pair[1])
                except Exception as e:
                    print(f"Error getting subnet {netuid} name: {str(e)}")
                    raise

                if identity_info is not None:
                    name = identity_info.name
                else:
                    name = '[Name not found]'
                    
                print(f'({i+1}) {name} ({pair[0][:6]}...)')

            delegator_index = int(input('What delegator would you like to use (enter the number): ')) - 1

            self.stakes_to_make_info[netuid]['delegator_hotkey'] = pairs_to_show[delegator_index][0]
            self.stakes_to_make_info[netuid]['delegator_owner'] = pairs_to_show[delegator_index][1]

        print(f'\nReady to stake into the following {len(self.stakes_to_make_info)} subnets:')
        self.total_stake_amount = 0

        # Print the list of stakes to be made
        for netuid, info in self.stakes_to_make_info.items(): 
            try:
                identity_info = self.SUBTENSOR.query_identity(info['delegator_owner'])
            except Exception as e:
                identity_info = None

            if identity_info is not None:
                info['delegator_name'] = identity_info.name
            else:
                info['delegator_name'] = '[Name not found]'

            print(f"({netuid}) {info['netuid_name']} delegated to {info['delegator_name']} ({info['delegator_hotkey'][:6]}...): τ{info['amount']}")
            self.total_stake_amount += info['amount']
        print(f'Requiring τ{round(self.total_stake_amount, 4)} total')


    # Check through this for errors, or possible improvements
    def check_balances_for_stake(self):
        alpha_stake_fees = len(self.stakes_to_make_info) * STAKING_FEES

        if self.total_stake_amount + alpha_stake_fees <= self.free_tao: # If free tao is sufficent amount required for stake
            print(f'\nYou have enough free tao to make this stake')

        # If possible, unstake required amount from root
        elif self.total_stake_amount + alpha_stake_fees < self.free_tao + self.root_stake:
            root_unstake_needed = self.total_stake_amount + alpha_stake_fees - self.free_tao
            print('\nNot enough free tao')
            continue_check(f'Would you like to unstake τ{round(root_unstake_needed, 10)} from root?')

            print('')
            root_unstake_made = 0
            i = 0
            # Error handling unstake operations (retry wrong password)
            while root_unstake_made < root_unstake_needed:
                # Check for subnet root and enough stake
                if self.delegated_info[i].netuid == 0 and float(self.delegated_info[i].stake) > STAKING_FEES:
                    this_stake_amount = float(self.delegated_info[i].stake)

                    # If this stake is more than needed, unstake required amount
                    if root_unstake_made + this_stake_amount > root_unstake_needed:
                        unstake_amount = root_unstake_needed - root_unstake_made
                    else:
                        unstake_amount = this_stake_amount

                    try:
                        unstake_successful = self.SUBTENSOR.unstake(
                            wallet=self.WALLET,
                            netuid=0,
                            hotkey_ss58=self.delegated_info[i].hotkey_ss58,
                            amount=bittensor.Balance(float(unstake_amount))
                        )
                    except Exception as e:
                        print(f"Unstake error: {str(e)}")
                        continue
                    else:
                        if unstake_successful:
                            root_unstake_made += (unstake_amount - STAKING_FEES)
                            print(f'τ{round(unstake_amount, 4)} unstaked from: {self.delegated_info[i].hotkey_ss58}')
                        else:
                            print(f'Unsuccessful unstaking τ{round(unstake_amount, 4)} from: {self.delegated_info[i].hotkey_ss58}')
                            quit()
                i += 1

        else:
            print(f'\nFree tao and root stake insufficient to make stake, please add more Tao!')
            exit()


    def make_stakes(self):
        # Cycle through subnet validator pairs
        print('')
        for netuid, info in self.stakes_to_make_info.items():
            try:
                stake_successful = self.SUBTENSOR.add_stake(
                    wallet=self.WALLET,
                    netuid=netuid,
                    hotkey_ss58=info['delegator_hotkey'],
                    amount=bittensor.Balance(float(info['amount']))
                )
            except Exception as e:
                # Need to fix formatting if error
                print(f"Stake error on subnet {netuid}: {str(e)}")
                continue_check('Would you like to continue?')
            else:
                if stake_successful:
                    print(f"Successfully staked on ({netuid}) {info['netuid_name']} to {info['delegator_name']} ({info['delegator_hotkey'][:6]}...): τ{info['amount']}")
                else:
                    print(f"Failed to make a stake on ({netuid}) {info['netuid_name']} to {info['delegator_name']} ({info['delegator_hotkey'][:6]}...)")
                    continue_check('Would you like to continue?')



# Gets user input to clarify continuation
def continue_check(message):
    continue_check = str(input(f'{message} (y/n): '))
    if not (continue_check.lower() == 'y'):
        exit()