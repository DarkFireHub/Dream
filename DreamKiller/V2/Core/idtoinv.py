import json
import requests
from colorama import Fore, init
import subprocess
import pyperclip

# Initialize colorama
init(autoreset=True)

def send_to_webhook(url, data):
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return Fore.BLUE + "Information sent successfully to the webhook."
        else:
            return Fore.BLUE + f"Failed to send information. Status code: {response.status_code}"
    except Exception as e:
        return Fore.BLUE + f"An error occurred: {str(e)}"

# Function to handle webhook sending
def send_info_to_webhook():
    webhook_url = input(Fore.BLUE + "Enter the webhook URL: ")
    info_data = {
        "message": "Example message sent to webhook"
    }
    result = send_to_webhook(webhook_url, info_data)
    print(result)

# Example usage
if __name__ == "__main__":
    # Execute the Discord bot ID script
    id = input(Fore.BLUE + "Enter Bot ID: ")
    discord_url = f"https://discord.com/oauth2/authorize?client_id={id}&permissions=8&integration_type=0&scope=bot"
    print(Fore.BLUE + f"Authorization URL: {discord_url}")

    # Define valid responses for yes and no
    valid_yes_responses = ["yes", "yup", "yop", "ye", "yiipe", "y"]
    valid_no_responses = ["no", "nope", "nty", "nt", "n"]

    # Prompt to copy the Discord bot authorization link
    copy_link = input(Fore.BLUE + "Do you want to copy the authorization URL to clipboard? (yes/no): ").lower()
    if copy_link in valid_yes_responses:
        pyperclip.copy(discord_url)
        print(Fore.BLUE + "Authorization URL copied to clipboard.")
    elif copy_link not in valid_no_responses:
        print(Fore.BLUE + "Invalid response. Skipping copying the URL.")

    # Prompt to send information to webhook
    send_webhook = input(Fore.BLUE + "Do you want to send information to a webhook? (yes/no): ").lower()
    if send_webhook in valid_yes_responses:
        send_info_to_webhook()
    elif send_webhook not in valid_no_responses:
        print(Fore.BLUE + "Invalid response. Skipping sending information to webhook.")

    # Execute the dream2.py script at the end
    subprocess.run(["python", "dream2.py"])
