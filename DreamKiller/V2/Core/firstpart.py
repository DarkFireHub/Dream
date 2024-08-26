import base64
import requests
import subprocess
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

def encode_base64(data):
    encoded_bytes = base64.b64encode(data.encode('utf-8'))
    encoded_str = encoded_bytes.decode('utf-8')
    return encoded_str

def send_to_webhook(webhook_url, message):
    data = {
        "content": message
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print(Fore.BLUE + "Message successfully sent.")
    else:
        print(Fore.BLUE + f"Failed to send message. Status code: {response.status_code}")

def main():
    print(Fore.BLUE + "Enter Discord ID: ", end='')
    discord_id = input()
    encoded_id = encode_base64(discord_id)
    
    # Display in blue
    print(Fore.BLUE + f"Discord User First Token Part : {encoded_id}.")
    
    print(Fore.BLUE + "Do you want to send the first token part to a Discord webhook? (yes/no): ", end='')
    send = input().strip().lower()
    
    if send == 'yes':
        print(Fore.BLUE + "Enter the Discord webhook URL: ", end='')
        webhook_url = input().strip()
        send_to_webhook(webhook_url, encoded_id)

    # Execute the dream.py script
    subprocess.run(["python", "dream2.py"])

if __name__ == "__main__":
    main()
