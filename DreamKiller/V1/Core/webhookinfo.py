import requests
import time
from colorama import init, Fore
import subprocess  # Added for subprocess.run()

# Initialize colorama
init(autoreset=True)

def get_webhook_info(webhook_url):
    response = requests.get(webhook_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(Fore.BLUE + f"Error: Unable to retrieve webhook information. Status Code: {response.status_code}")
        print(Fore.BLUE + f"Response: {response.text}")
        return None

def print_webhook_info(webhook_info):
    print(Fore.BLUE + "Webhook Information:")
    for key, value in webhook_info.items():
        print(Fore.BLUE + f"{key.capitalize()}: {value}")

def main():
    webhook_url = input(Fore.BLUE + "Enter the webhook URL: ")

    webhook_info = get_webhook_info(webhook_url)
    if webhook_info:
        print_webhook_info(webhook_info)
    else:
        print(Fore.BLUE + "No information retrieved.")

    # Example subprocess.run() call
    time.sleep(5)
    subprocess.run(["python", "dream.py"])

if __name__ == "__main__":
    main()
