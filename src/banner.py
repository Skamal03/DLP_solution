import os
from colorama import Fore, Style

def show_banner():
    """Displays the 'Zer0Leaks' ASCII banner in Sea Green."""
    
    # Clear terminal first
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
      {Style.RESET_ALL}
    """
    
    print(banner)
    print("="*110 + "\n")

if __name__ == "__main__":
    show_banner()
