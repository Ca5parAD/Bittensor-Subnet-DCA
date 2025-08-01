import bittensor

MINIMUM_TAO_BALANCE = 0.0000005

class WalletOperationFunctionality:
    def __init__(self, wallet, subtensor):
        self.wallet = wallet
        self.subtensor = subtensor

        try:
            self.free_tao = float(self.subtensor.get_balance(address=self.wallet.coldkeypub.ss58_address))
        except Exception as e:
            print(f"Error getting balance: {str(e)}")
            raise
        
        try:
            self.delegated_info = self.subtensor.get_delegated(coldkey_ss58=self.wallet.coldkeypub.ss58_address)
            self.delegated_info.sort(key=lambda info: info.netuid)
        except Exception as e:
            print(f"Error getting delegated info: {str(e)}")
            raise

        self.root_stake = 0
        self.alpha_stake = 0
        for info in self.delegated_info:
            if info.netuid == 0:
                self.root_stake += float(info.stake) # Sums root stake
            else:
                try:
                    subnet_info = self.subtensor.subnet(netuid=info.netuid)
                    self.alpha_stake += float(info.stake) * float(subnet_info.price)
                except Exception as e:
                    print(f"Error getting subnet {info.netuid} info: {str(e)}")
                    continue

    def print_balances(self):
        print(f'\nFor coldkey: {self.wallet.coldkeypub.ss58_address}')
        print(f'Free tao: τ{round(self.free_tao, 4)} | Root stake: τ{round(self.root_stake, 4)} | Alpha stake: τ{round(self.alpha_stake, 4)}')
        print(f'Total: τ{self.free_tao + self.root_stake + self.alpha_stake}')

    def check_netuids_to_stake(self, netuids_to_stake, stake_amount):
        self.netuids_to_stake = netuids_to_stake
        self.stake_amount = stake_amount
        print(f'\nYou would like to stake τ{stake_amount} into the following {len(self.netuids_to_stake)} subnets:')
        # Print the list of subnets to stake into
        for netuid in self.netuids_to_stake:
            print(netuid)
        print(f'Requiring τ{self.stake_amount*len(netuids_to_stake)} total')

    def check_balances_for_stake(self):
        self.total_stake_amount = self.stake_amount * len(self.netuids_to_stake)
        if self.total_stake_amount <= (self.free_tao - MINIMUM_TAO_BALANCE): # If free tao is sufficent amount required for stake
            pass

        # If possible, unstake required amount from root
        elif self.total_stake_amount < (self.free_tao - MINIMUM_TAO_BALANCE) + (self.root_stake - MINIMUM_TAO_BALANCE):
            root_unstake_needed = self.total_stake_amount - (max(self.free_tao - MINIMUM_TAO_BALANCE, 0))
            print('\nNot enough free tao')
            continue_check(f'Would you like to unstake τ{round(root_unstake_needed, 4)} from root?')

            print('\n')
            root_unstake_made = 0
            i = 0
            while root_unstake_made < root_unstake_needed:
                # Check for subnet root and enough stake
                if self.delegated_info[i].netuid == 0 and float(self.delegated_info[i].stake) > (2 * MINIMUM_TAO_BALANCE):
                    this_stake_amount = float(self.delegated_info[i].stake - MINIMUM_TAO_BALANCE)

                    # Stake more then needed, unstake required amount
                    if root_unstake_made + this_stake_amount > root_unstake_needed:
                        unstake_amount = root_unstake_needed - root_unstake_made
                    else:
                        unstake_amount = this_stake_amount

                    try:
                        unstake_successful = self.subtensor.unstake(
                            wallet=self.wallet,
                            netuid=0,
                            hotkey_ss58=self.delegated_info[i].hotkey_ss58,
                            amount=bittensor.Balance(float(unstake_amount))
                        )
                    except Exception as e:
                        print(f"Unstake error: {str(e)}")
                        continue
                    else:
                        if unstake_successful:
                            root_unstake_made += unstake_amount
                            print(f'τ{round(unstake_amount, 4)} unstaked from: {self.delegated_info[i].hotkey_ss58}')
                        else:
                            print(f'Unsuccessful unstaking τ{round(unstake_amount, 4)} from: {self.delegated_info[i].hotkey_ss58}')
                            quit()
                i += 1

        else:
            print(f'\nFree tao and root stake insufficient to make stake')
            exit()
                
    def organise_hotkeys_to_stake(self):
        self.netuid_hotkey_pairs = []
        self.no_stake_flag = False

        # Cycle through subnets to stake into
        for netuid in self.netuids_to_stake:
            found_flag = False

            # Cycle through delegate info
            for info in self.delegated_info:
                if netuid == info.netuid:
                    print(f'Subnet {netuid} staked to: {info.hotkey_ss58}')
                    self.netuid_hotkey_pairs.append((netuid, info.hotkey_ss58)) # Create list of tuples of subnets and validators
                    found_flag = True
                    break
            if not found_flag:
                print(f'No stake for subnet: {netuid}')
                self.no_stake_flag = True

        if self.no_stake_flag:
            print('\nNeed to make an initial stake on each subnet before using this program')
            exit()

    def make_stakes(self):
        # Cycle through subnet validator pairs
        for netuid, hotkey in self.netuid_hotkey_pairs:
            try:
                stake_successful = self.subtensor.add_stake(
                    wallet=self.wallet,
                    netuid=netuid,
                    hotkey_ss58=hotkey,
                    amount=bittensor.Balance(float(self.stake_amount))
                )
            except Exception as e:
                print(f"Stake error on subnet {netuid}: {str(e)}")
                continue_check('Would you like to continue?')
            else:
                if stake_successful:
                    print(f'Stake on subnet {netuid} to {hotkey} successful')
                else:
                    print(f'Failed to make a stake on subnet {netuid} to {hotkey}')
                    continue_check('Would you like to continue?')

# Gets user input to clarify continuation
def continue_check(message):
    continue_check = str(input(f'{message} (y/n): '))
    if not (continue_check.lower() == 'y'):
        exit()