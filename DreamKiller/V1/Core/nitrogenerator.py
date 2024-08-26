import random
import msvcrt
import string
import json
import requests
import threading
from colorama import init, Fore
import subprocess

# Initialize colorama
init(autoreset=True)

# Codes ANSI pour la coloration du texte dans la console
BLUE = '\033[94m'
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

# Chemin du fichier de sortie pour les liens valides
VALID_NITRO_FILE = "Output/Nitro/ValidNitro.txt"

def ErrorModule(e):
    print(Fore.BLUE + f"Error in module: {e}\n")

def Title(title):
    print(Fore.BLUE + f"Title: {title}\n")

def CheckWebhook(webhook_url):
    print(Fore.BLUE + f"Checking webhook: {webhook_url}\n")

def ErrorNumber():
    print(Fore.BLUE + "Error in number input\n")

def send_webhook(embed_content, webhook_url, username_webhook, avatar_webhook):
    payload = {
        'embeds': [embed_content],
        'username': username_webhook,
        'avatar_url': avatar_webhook
    }

    headers = {
        'Content-Type': 'application/json'
    }

    requests.post(webhook_url, data=json.dumps(payload), headers=headers)

def nitro_check(webhook, webhook_url, threads_number, color_webhook):
    try:
        code_nitro = ''.join([random.choice(string.ascii_uppercase + string.digits) for _ in range(16)])
        url_nitro = f'https://discord.gift/{code_nitro}'
        response = requests.get(f'https://discordapp.com/api/v6/entitlements/gift-codes/{code_nitro}?with_application=false&with_subscription_plan=true', timeout=1)
        if response.status_code == 200:
            if webhook in ['y', 'Y', 'Yes', 'yes', 'YES']:
                embed_content = {
                    'title': f'Nitro Valid !',
                    'description': f"{Fore.BLUE}**__Nitro:__**\n```{url_nitro}```",
                    'color': color_webhook,
                    'footer': {
                        "text": username_webhook,
                        "icon_url": avatar_webhook,
                    }
                }
                send_webhook(embed_content, webhook_url, username_webhook, avatar_webhook)
                print(f"{Fore.GREEN}Valid Nitro: {url_nitro}\n")

                # Écrit le lien valide dans le fichier
                with open(VALID_NITRO_FILE, 'a') as file:
                    file.write(f"{url_nitro}\n")
            else:
                print(f"{Fore.GREEN}Valid Nitro: {url_nitro}\n")
        else:
            print(Fore.BLUE + f"Invalid Nitro: {url_nitro}\n")
    except Exception as e:
        print(Fore.BLUE + f"Error in nitro check: {e}\n")

def request(webhook, webhook_url, threads_number, color_webhook, username_webhook, avatar_webhook):
    threads = []
    try:
        for _ in range(int(threads_number)):
            t = threading.Thread(target=nitro_check, args=(webhook, webhook_url, threads_number, color_webhook))
            t.start()
            threads.append(t)
    except Exception as e:
        print(Fore.BLUE + f"Error in threading: {e}\n")

    for thread in threads:
        thread.join()

def main():
    try:
        webhook_choice = input(Fore.BLUE + "Use webhook for notifications? (y/n) -> ").lower()
        if webhook_choice not in ['y', 'n']:
            print(Fore.BLUE + "Invalid choice. Please enter 'y' or 'n'.")
            return

        if webhook_choice == 'y':
            webhook_url = input(Fore.BLUE + "Webhook URL -> ")
            username_webhook = input(Fore.BLUE + "Webhook Username -> ")
            avatar_webhook = input(Fore.BLUE + "Webhook Avatar URL -> ")
        else:
            webhook_url = None
            username_webhook = None
            avatar_webhook = None

        while True:
            threads_number = input(Fore.BLUE + "Threads Number -> ")
            try:
                threads_number = int(threads_number)
                break  # Sort de la boucle si la conversion en entier est réussie
            except ValueError:
                print(Fore.BLUE + "Invalid input. Please enter a number.\n")

        color_webhook = input(Fore.BLUE + "Webhook Color (e.g., blue, green, red) -> ")

        request(webhook_choice, webhook_url, threads_number, color_webhook, username_webhook, avatar_webhook)

    except KeyboardInterrupt:
        print(Fore.BLUE + "\nScript interrupted.\n")
    except Exception as e:
        print(Fore.BLUE + f"Unexpected error: {e}\n")

# Exécute le script principal
if __name__ == "__main__":
    main()

subprocess.run(["python", "dream.py"])

print(Fore.BLUE + "Script terminated.\n")
