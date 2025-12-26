import os
from colorama import Fore, Style

def show_banner(clear_screen=True):
    """Displays the 'Zer0Leaks' ASCII banner in Sea Green."""
    
    # Clear terminal first
    if clear_screen:
        os.system('cls' if os.name == 'nt' else 'clear')
    
    # Sea Green is best approximated by CYAN in standard terminals
    color = Fore.CYAN 
    
    # Using a clearer 'Big' font style
    banner = f"""
{color}

//    $$$$$$$$\                     $$$$$$\        $$\ $$\                 $$$$$$\  $$\                 
//    \____$$  |                   $$  __$$\      $$  |$$ |               $$  __$$\ $$ |                
//        $$  / $$$$$$\   $$$$$$\  $$ /  $$ |    $$  / $$ |      $$$$$$\  $$ /  $$ |$$ |  $$\  $$$$$$$\ 
//       $$  / $$  __$$\ $$  __$$\ $$ |  $$ |   $$  /  $$ |     $$  __$$\ $$$$$$$$ |$$ | $$  |$$  _____|
//      $$  /  $$$$$$$$ |$$ |  \__|$$ |  $$ |  $$  /   $$ |     $$$$$$$$ |$$  __$$ |$$$$$$  / \$$$$$$\  
//     $$  /   $$   ____|$$ |      $$ |  $$ | $$  /    $$ |     $$   ____|$$ |  $$ |$$  _$$<   \____$$\ 
//    $$$$$$$$\\$$$$$$$\ $$ |       $$$$$$  |$$  /     $$$$$$$$\\$$$$$$$\ $$ |  $$ |$$ | \$$\ $$$$$$$  |
//    \________|\_______|\__|       \______/ \__/      \________|\_______|\__|  \__|\__|  \__|\_______/ 
{Style.RESET_ALL}{Fore.WHITE}              
             +-+-+ +-+-+-+-+ +-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+-+-+ +-+-+-+-+-+-+ +-+-+
             |-|-| |D|a|t|a| |L|e|a|k|a|g|e| |P|r|e|v|e|n|t|i|o|n| |S|y|s|t|e|m| |-|-|
             +-+-+ +-+-+-+-+ +-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+-+-+ +-+-+-+-+-+-+ +-+-+
             
                                    -- ctrl + c for menu --
    {Style.RESET_ALL}
    """
    print(banner)
    # Legend
    print(f"            {Fore.RED}[RED] Local Files{Style.RESET_ALL} | {Fore.YELLOW}[YEL] Clipboard{Style.RESET_ALL} | {Fore.MAGENTA}[PUR] USB{Style.RESET_ALL} | {Fore.BLUE}[BLU] Info{Style.RESET_ALL} | {Fore.GREEN}[GRN] Status{Style.RESET_ALL}")
    print("="*110 + "\n")

if __name__ == "__main__":
    show_banner()
