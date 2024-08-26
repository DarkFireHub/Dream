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

   25 --> Multi Fonction Bot            |  26 --> Discord Id Lookup      |  27 --> Brawl Star Lookup            | 
   28 --> Soon ?                        |  29 --> Soon ?                 |  30 --> Soon ?                       |
   31 --> Soon ?                        |  32 --> Soon ?                 |  33 --> Soon ?                       |  
   34 --> Soon ?                        |  35 --> Soon ?                 |  << --> Previous Page                |
"""
    # Efface l'écran (Windows/Linux)
    os.system("cls" if os.name == "nt" else "clear")
    print(Fore.BLUE + banner_text)

def main():
    display_banner()
    choice = input(Fore.BLUE + "Dream ? : ").strip()

    if choice == "25":
        script_path = os.path.join("core", "nukerbot.py")

    elif choice == "26":
        script_path = os.path.join("core", "discordid.py")

    elif choice == "27":
        script_path = os.path.join("core", "brawlstarlookup.py.py")

    elif choice == "28":
        script_path = os.path.join("core", "soon.py")

    elif choice == "29":
        script_path = os.path.join("core", "soon.py")

    elif choice == "30":
        script_path = os.path.join("core", "soon.py")

    elif choice == "31":
        script_path = os.path.join("core", "soon.py")

    elif choice == "32":
        script_path = os.path.join("core", "soon.py")

    elif choice == "33":
        script_path = os.path.join("core", "soon.py")

    elif choice == "34":
        script_path = os.path.join("core", "soon.py")

    elif choice == "35":
        script_path = os.path.join("core", "soon.py")

    elif choice == "<<":
        script_path = os.path.join("dream2.py")
        
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
