import os
import threading
import requests
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")

def get_input(prompt):
    """Get user input with a prompt and strip any extra whitespace."""
    return input(Fore.BLUE + prompt).strip()

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
        print(Fore.RED + f'[ERROR] Exception occurred: {e}')

def channel_spammer():
    """Main function to execute the channel spammer."""
    tokens_input = get_input("Enter Account Tokens (comma-separated): ")
    message = get_input('Your Message: ')
    group_id = get_input('Group ID: ')
    
    # Validate inputs
    if not tokens_input or not message or not group_id:
        print(Fore.RED + 'Error: All fields are required.')
        return
    
    tokens = [token.strip() for token in tokens_input.split(',')]
    url = f'https://discord.com/api/v10/channels/{group_id}/messages'
    num_repeats = 3  # Number of times to send the message per token
    
    clear_screen()
    
    # Using ThreadPoolExecutor for managing threads
    with ThreadPoolExecutor(max_workers=len(tokens) * num_repeats) as executor:
        futures = []
        for token in tokens:
            for _ in range(num_repeats):
                future = executor.submit(send_message, token, url, message)
                futures.append(future)

        # Wait for all futures to complete
        for future in futures:
            future.result()

if __name__ == "__main__":
    channel_spammer()
