import subprocess
import requests
import msvcrt
import time
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

def send_message_to_webhook(webhook_url, message, delay, num_messages):
    headers = {'Content-Type': 'application/json'}
    payload = {
        "content": message
    }

    for _ in range(num_messages):
        response = requests.post(webhook_url, headers=headers, json=payload)
        
        if response.status_code == 204:
            print(Fore.BLUE + "Message successfully sent.")
        elif response.status_code == 429:
            retry_after = response.json().get('retry_after', 1) / 1000.0
            print(Fore.BLUE + f"Rate limited. Retrying after {retry_after} seconds.")
            time.sleep(retry_after)
            continue
        else:
            print(Fore.BLUE + f"Error: Unable to send message. Status Code: {response.status_code}")
            print(Fore.BLUE + f"Response: {response.text}")

        time.sleep(delay)

def main():
    webhook_url = input(Fore.BLUE + "Enter the webhook URL: ")
    message = input(Fore.BLUE + "Enter the message to send: ")
    delay = float(input(Fore.BLUE + "Enter the delay between messages (minimum 0.1): "))
    num_messages = int(input(Fore.BLUE + "Enter the number of messages to send: "))

    if delay < 0.1:
        print(Fore.BLUE + "The delay is too short. Setting it to 0.1 seconds.")
        delay = 0.1

    send_message_to_webhook(webhook_url, message, delay, num_messages)
    
    print(Fore.BLUE + "All messages sent.")
    
    subprocess.run(["python", "dream.py"])

if __name__ == "__main__":
    main()
