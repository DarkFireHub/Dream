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

   13 --> Get Someone First Token Part  |  14 --> Email Lookup           |  15 --> Phone Number Lookup          | 
   16 --> Bot Id To Invite              |  17 --> Token Checker          |  18 --> Discord Account Nuker        |
   19 --> Channel Spammer               |  20 --> Spam Dm With One Token |  21 --> Group Spammer Token Input    |  
   22 --> Group Spammer With Token List |  >> --> Next Page              |  << --> First Page                   |
"""
    # Efface l'écran (Windows/Linux)
    os.system("cls" if os.name == "nt" else "clear")
    print(Fore.BLUE + banner_text)

def main():
    display_banner()
    choice = input(Fore.BLUE + "Dream ? : ").strip()

    if choice == "13":
        script_path = os.path.join("core", "firstpart.py")

    elif choice == "14":
        script_path = os.path.join("core", "emaillookup.py")

    elif choice == "15":
        script_path = os.path.join("core", "phonenumber.py")

    elif choice == "16":
        script_path = os.path.join("core", "idtoinv.py")

    elif choice == "17":
        script_path = os.path.join("core", "tokenchecker.py")

    elif choice == "18":
        script_path = os.path.join("core", "accountnuker.py")

    elif choice == "19":
        script_path = os.path.join("core", "channelspammer.py")

    elif choice == "20":
        script_path = os.path.join("core", "spamdm.py")

    elif choice == "21":
        script_path = os.path.join("core", "groupspammer.py")

    elif choice == "22":
        script_path = os.path.join("core", "groupspammer2.py")

    elif choice == ">>":
        script_path = os.path.join("dream3.py")

    elif choice == "<<":
        script_path = os.path.join("dream.py")
        
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
