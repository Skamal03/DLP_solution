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

//    $$$$$$$$\                     $$$$$$\        $$\ $$\                          $$\                 
//    \____$$  |                   $$  __$$\      $$  |$$ |                         $$ |                
//        $$  / $$$$$$\   $$$$$$\  $$ /  $$ |    $$  / $$ |      $$$$$$\   $$$$$$\  $$ |  $$\  $$$$$$$\ 
//       $$  / $$  __$$\ $$  __$$\ $$ |  $$ |   $$  /  $$ |     $$  __$$\  \____$$\ $$ | $$  |$$  _____|
//      $$  /  $$$$$$$$ |$$ |  \__|$$ |  $$ |  $$  /   $$ |     $$$$$$$$ | $$$$$$$ |$$$$$$  / \$$$$$$\  
//     $$  /   $$   ____|$$ |      $$ |  $$ | $$  /    $$ |     $$   ____|$$  __$$ |$$  _$$<   \____$$\ 
//    $$$$$$$$\\$$$$$$$\ $$ |       $$$$$$  |$$  /     $$$$$$$$\\$$$$$$$\ \$$$$$$$ |$$ | \$$\ $$$$$$$  |
//    \________|\_______|\__|       \______/ \__/      \________|\_______| \_______|\__|  \__|\_______/ 
//                                                                                                      
//                                                                                                      
//                                                                                                                                                                                                            
                 
{Style.RESET_ALL}
      {Fore.WHITE}       -- Data Leakage Prevention System --{Style.RESET_ALL}
    """
    
    print(banner)
    print("="*60 + "\n")

if __name__ == "__main__":
    show_banner()
