import os
import subprocess
import time
import threading
import requests
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def read_tokens(file_path):
    with open(file_path) as f:
        return f.read().splitlines()

def send_message(token, url, message):
    headers = {'authorization': token}
    data = {'content': f'`{message}`'}

    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code in [200, 201, 204]:
        print(Fore.GREEN + '[SUCCESS] Message Sent Successfully!')
    else:
        print(Fore.RED + f'[FAILURE] An Error Occurred: {response.status_code}')

def channel_spammer():
    
    tokens = input("Enter Account Token : ")
    message = input(Fore.BLUE + 'Your Message : ')
    channel_id = input(Fore.BLUE + 'Channel ID : ')
    clear()

    url = f'https://discord.com/api/v9/channels/{channel_id}/messages'

    threads = []

    for token in tokens:
        for _ in range (3):  # Adjust the range as needed
            thread = threading.Thread(target=send_message, args=(token, url, message))
            thread.start()
            threads.append(thread)


    for thread in threads:
        thread.join()
    
if __name__ == "__main__":
    channel_spammer()
