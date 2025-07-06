import bittensor

class FullWalletInfo:
    def __init__(self, wallet, subtensor):
        self.wallet = wallet
        self.subtensor = subtensor
        self.free_tao = self.subtensor.get_balance(address=self.wallet.coldkeypub.ss58_address) # Gets free tao balance
        
        self.delegated_info = self.subtensor.get_delegated(coldkey_ss58=self.wallet.coldkeypub.ss58_address)
        self.delegated_info.sort(key=lambda info: info.netuid)  # Sort by subnet ID

        self.root_stake = 0
        self.alpha_stake = 0
        for info in self.delegated_info:
            if info.netuid == 0:
                self.root_stake += info.stake # Sums root stake

            else:
                subnet_info = self.subtensor.subnet(netuid=info.netuid)
                self.alpha_stake += bittensor.Balance(float(info.stake) * float(subnet_info.price)) # Converts alpha stake to tao and sums


    def check_balances(self, total_stake_amount):
        print(total_stake_amount)
        if total_stake_amount < float(self.free_tao):
            pass
        elif total_stake_amount < float(self.free_tao) + float(self.root_stake):
            root_unstake_needed = total_stake_amount - float(self.free_tao)
            print('Not enough free tao')
            continue_check = str(input(f'Would you like to unstake {root_unstake_needed} from root? (y/n): '))
            if (continue_check == 'y' or continue_check == 'Y'):
                self.subtensor.unstake(wallet=self.wallet, netuid=0, amount=root_unstake_needed)
            else:
                exit()
        else:
            print(f'Free tao and root stake insufficient to make stake')
            exit()
                
    def organise_hotkeys_to_stake(self, netuids_to_stake):
        self.hotkeys_to_stake = []
        self.no_stake_flag = False

        for netuid in netuids_to_stake:
            for i in range(len(self.delegated_info)):
                if netuid == self.delegated_info[i].netuid:
                    print(f'Subnet {netuid} staked to: {self.delegated_info[i].hotkey_ss58}')
                    self.hotkeys_to_stake.append(self.delegated_info[i].hotkey_ss58)
                    break
                elif i == len(self.delegated_info) - 1:
                    print(f'No stake for subnet: {netuid}')
                    self.no_stake_flag = True
        

