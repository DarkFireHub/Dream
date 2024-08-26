import requests
import json
import random
import threading
import os
import subprocess
import sys
from colorama import init, Fore, Style

init(autoreset=False)
BLUE = Fore.BLUE
RESET = Style.RESET_ALL
print_lock = threading.Lock()  # Lock for synchronizing print statements

def current_time_hour():
    from datetime import datetime
    return datetime.now().strftime('%H:%M:%S')

def ErrorModule(e):
    with print_lock:
        print(f"{BLUE}[Error] {str(e)}{RESET}")

def Title(text):
    if sys.platform.startswith("win"):
        os.system(f'title {text}')
    else:
        sys.stdout.write(f'\33]0;{text}\a')
        sys.stdout.flush()

def CheckWebhook(url):
    with print_lock:
        print(f"{BLUE}[Webhook] Checking webhook URL: {url}{RESET}")

def ErrorNumber():
    with print_lock:
        print(f"{BLUE}[Error] Invalid number{RESET}")

try:
    with print_lock:
        print(f"{BLUE}IP Generator{RESET}")

    webhook = input(f"\n{BLUE}{current_time_hour()} Webhook ? (y/n) -> {RESET}")
    if webhook in ['y', 'Y', 'Yes', 'yes', 'YES']:
        webhook_url = input(f"{BLUE}{current_time_hour()} Webhook URL -> {RESET}")
        CheckWebhook(webhook_url)

    try:
        threads_number = int(input(f"{BLUE}{current_time_hour()} Threads Number -> {RESET}"))
    except:
        ErrorNumber()

    def send_webhook(embed_content):
        payload = {
            'embeds': [embed_content],
            'username': "IP Generator",
            'avatar_url': "https://cdn.discordapp.com/avatars/950507161946034246/e347d89423e13628f640f275518a78d8.png"
        }

        headers = {
            'Content-Type': 'application/json'
        }

        requests.post(webhook_url, data=json.dumps(payload), headers=headers)

    number_valid = 0
    number_invalid = 0
    file_txt_relative = "./Output/IpGenerator/IpValid.txt"
    file_txt = os.path.abspath(file_txt_relative)

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_txt), exist_ok=True)

    def ip_check():
        global number_valid, number_invalid
        number_1 = random.randint(1, 255)
        number_2 = random.randint(1, 255)
        number_3 = random.randint(1, 255)
        number_4 = random.randint(1, 255)
        ip = f"{number_1}.{number_2}.{number_3}.{number_4}"

        try:
            if sys.platform.startswith("win"):
                result = subprocess.run(['ping', '-n', '1', ip], capture_output=True, text=True, timeout=1)
            elif sys.platform.startswith("linux"):
                result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], capture_output=True, text=True, timeout=1)

            if result.returncode == 0:
                number_valid += 1
                with print_lock:
                    if webhook in ['y', 'Y', 'Yes', 'yes', 'YES']:
                        embed_content = {
                            'title': 'Ip Valid !',
                            'description': f"**__Ip:__**\n```{ip}```",
                            'color': 3447003,
                            'footer': {
                                "text": "IP Generator",
                                "icon_url": "https://cdn.discordapp.com/avatars/950507161946034246/e347d89423e13628f640f275518a78d8.png"
                            }
                        }
                        send_webhook(embed_content)
                        print(f"{BLUE} Valid | Ip: {ip}{RESET}")
                    else:
                        print(f"{BLUE} Valid | Ip: {ip}{RESET}")

                    with open(file_txt, 'a') as f:
                        f.write(f"{ip}\n")
            else:
                number_invalid += 1
                with print_lock:
                    print(f"{BLUE}{current_time_hour()} Invalid | Ip: {ip}{RESET}")
        except:
            number_invalid += 1
            with print_lock:
                print(f"{BLUE} Invalid | Ip: {ip}{RESET}")

        Title(f"Ip Generator - Invalid: {number_invalid} - Valid: {number_valid}")

    def request():
        threads = []
        try:
            for _ in range(int(threads_number)):
                t = threading.Thread(target=ip_check)
                t.start()
                threads.append(t)
        except:
            ErrorNumber()

        for thread in threads:
            thread.join()

    while True:
        request()
except Exception as e:
    ErrorModule(e)
