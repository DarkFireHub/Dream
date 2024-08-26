import os
import requests
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")

def read_tokens(file_path):
    """Read tokens from a file and return as a list."""
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        print(Fore.RED + f'[ERROR] File not found: {file_path}')
        return []
    except Exception as e:
        print(Fore.RED + f'[ERROR] An unexpected error occurred: {e}')
        return []

def send_message(token, url, message):
    """Send a message to the specified URL using the given token."""
    headers = {'Authorization': token}
    data = {'content': f'`{message}`'}
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code in [200, 201, 204]:
            print(Fore.GREEN + '[SUCCESS] Message sent successfully!')
        else:
            print(Fore.RED + f'[FAILURE] Error occurred: {response.status_code}')
    except requests.RequestException as e:
        print(Fore.RED + f'[ERROR] Request exception: {e}')

def channel_spammer():
    """Main function to execute the channel spammer."""
    tokens = read_tokens("valid.txt")
    if not tokens:
        print(Fore.RED + 'No tokens available. Exiting.')
        return

    message = input(Fore.BLUE + 'Your Message: ').strip()
    channel_id = input(Fore.BLUE + 'Group ID: ').strip()
    
    if not message or not channel_id:
        print(Fore.RED + 'Message and Group ID are required.')
        return

    clear_screen()
    
    url = f'https://discord.com/api/v10/channels/{channel_id}/messages'
    
 
    with ThreadPoolExecutor(max_workers=len(tokens) * 3) as executor:
        futures = [executor.submit(send_message, token, url, message) for token in tokens for _ in range(3)]
        for future in futures:
            future.result()  

if __name__ == "__main__":
    channel_spammer()
