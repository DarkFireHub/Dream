import requests
import os
import time
import subprocess
from colorama import Fore, init

init()  # Initialisation de Colorama pour la coloration du texte

def checker(token, tested_tokens, valid_tokens):
    session = requests.Session()
    headers = {
        'Authorization': token
    }

    try:
        r = session.get('https://discord.com/api/v9/users/@me', headers=headers)
        if r.status_code == 200:
            print(f"{Fore.BLUE}  Valid {Fore.BLUE}| {Fore.RESET}{token}")
            valid_tokens.append(token)  # Ajouter le token à la liste des tokens valides
            tested_tokens.append(token)  # Ajouter le token à la liste des tokens testés
        elif r.status_code == 429:
            print(f"{Fore.YELLOW}  Rate Limited {Fore.YELLOW}[{Fore.RESET}429{Fore.YELLOW}] {Fore.CYAN}| {Fore.RESET}{token}")
        else:
            print(f"{Fore.RED}  Invalid {Fore.RED}| {Fore.RESET}{token}")
            tested_tokens.append(token)  # Ajouter le token à la liste des tokens testés même s'il est invalide
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}  Error: {Fore.RESET}{e}")

def read_tokens_from_file(file_path):
    with open(file_path, 'r') as file:
        tokens = file.read().splitlines()
    return tokens

def save_valid_tokens(file_path, tokens):
    with open(file_path, 'w') as file:
        for token in tokens:
            file.write(f'{token}\n')

if __name__ == "__main__":
    tokens_file_path = 'Input/tokens.txt'  # Chemin vers le fichier contenant les tokens
    valid_tokens_file = 'valid.txt'  # Chemin vers le fichier où enregistrer les tokens valides
    
    tokens = read_tokens_from_file(tokens_file_path)
    tested_tokens = []
    valid_tokens = []
    
    for token in tokens:
        checker(token, tested_tokens, valid_tokens)
    
    save_valid_tokens(valid_tokens_file, valid_tokens)
    
    time.sleep(2)
    subprocess.run(["python", "dream2.py"])