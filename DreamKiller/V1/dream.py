import subprocess
import os
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

def display_banner():
    # Texte de la bannière
    banner_text = r"""
               ________                                
               \______ \_______   ____ _____    _____  
                |    |  \_  __ \_/ __ \\__  \  /     \ 
                |    `   \  | \/\  ___/ / __ \|  Y Y  \
               /_______  /__|    \___  >____  /__|_|  /
                       \/            \/     \/      \/ 

   1 --> Get Pc Info     |  2 --> Roblox Id Info    |  3 --> Roblox User Info |  4 --> Discord Id Info
   5 --> Ip Generator    |  6 --> IpLookup          |  7 --> Get Your Ip      |  8 --> Nitro Generator
   9 --> Webhook Info    | 10 --> Webhook Deleter   | 11 --> Webhook Spammer  | 12 --> Get Someone First Token Part ?
"""
    # Efface l'écran (Windows/Linux)
    os.system("cls" if os.name == "nt" else "clear")
    print(Fore.BLUE + banner_text)

def main():
    display_banner()
    choice = input(Fore.BLUE + "Your Choice : ").strip()

    if choice == "1":
        script_path = os.path.join("core", "pcinfo.py")

    elif choice == "2":
        script_path = os.path.join("core", "robloxid.py")

    elif choice == "3":
        script_path = os.path.join("core", "robloxuser.py")

    elif choice == "4":
        script_path = os.path.join("core", "discordid.py")

    elif choice == "5":
        script_path = os.path.join("core", "ipgen.py")

    elif choice == "6":
        script_path = os.path.join("core", "iplookup.py")

    elif choice == "7":
        script_path = os.path.join("core", "getyourip.py")

    elif choice == "8":
        script_path = os.path.join("core", "nitrogenerator.py")

    elif choice == "9":
        script_path = os.path.join("core", "webhookinfo.py")

    elif choice == "10":
        script_path = os.path.join("core", "webhookdeleter.py")

    elif choice == "11":
        script_path = os.path.join("core", "webhookspammer.py")

    elif choice == "12":
        script_path = os.path.join("core", "firstpart.py")
        
    else:
        print(Fore.RED + "Invalid choice. Exiting...")
        return

    if os.path.exists(script_path):
        try:
            subprocess.run(["python", script_path], check=True)
        except subprocess.CalledProcessError as e:
            print(Fore.RED + f"An error occurred while executing the script: {e}")
    else:
        print(Fore.RED + f"Script not found: {script_path}")

if __name__ == "__main__":
    main()
