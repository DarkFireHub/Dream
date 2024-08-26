import subprocess
import msvcrt
import requests
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

def delete_webhook(webhook_url):
    response = requests.delete(webhook_url)
    if response.status_code == 204:
        print(Fore.BLUE + "Webhook successfully deleted.")
    else:
        print(Fore.BLUE + f"Error: Unable to delete webhook. Status Code: {response.status_code}")
        print(Fore.BLUE + f"Response: {response.text}")

def main():
    webhook_url = input(Fore.BLUE + "Enter the webhook URL: ")
    delete_webhook(webhook_url)
    subprocess.run(["python", "dream.py"])

if __name__ == "__main__":
    main()
