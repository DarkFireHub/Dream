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

   13 --> Soon ?    |  14 --> Soon ?    |  15 --> Soon ?    |  16 --> Soon ?
   17 --> Soon ?    |  18 --> Soon ?    |  19 --> Soon ?    |  20 --> Soon ?
   21 --> Soon ?    |  22 --> Soon ?    |  23 --> Soon ?    |  24 --> Soon ?
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
        script_path = os.path.join("core", "soon.py")

    elif choice == "15":
        script_path = os.path.join("core", "soon.py")

    elif choice == "16":
        script_path = os.path.join("core", "soon.py")

    elif choice == "17":
        script_path = os.path.join("core", "soon.py")

    elif choice == "18":
        script_path = os.path.join("core", "soon.py")

    elif choice == "19":
        script_path = os.path.join("core", "soon.py")

    elif choice == "20":
        script_path = os.path.join("core", "soon.py")

    elif choice == "21":
        script_path = os.path.join("core", "soon.py")

    elif choice == "22":
        script_path = os.path.join("core", "soon.py")

    elif choice == "23":
        script_path = os.path.join("core", "soon.py")

    elif choice == "24":
        script_path = os.path.join("core", "soon.py")
        
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
