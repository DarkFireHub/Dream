import subprocess
import requests
import json
from datetime import datetime
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

def get_roblox_user_info(user_id):
    # Roblox API URL to fetch user information
    url = f"https://users.roblox.com/v1/users/{user_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(Fore.BLUE + "Error: Unable to retrieve user information.")
        return None

def send_to_webhook(data, webhook_url):
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Ensure the data is not empty and has a content field for Discord
    if not data or 'content' not in data or not data['content'].strip():
        print(Fore.BLUE + "Error: The message content is empty.")
        return
    
    try:
        response = requests.post(webhook_url, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad status codes
        print(Fore.BLUE + "Information successfully sent to the webhook.")
    except requests.exceptions.RequestException as e:
        print(Fore.BLUE + f"Error: Unable to send information to the webhook. Exception: {e}")

def format_date(date_string):
    date_obj = datetime.fromisoformat(date_string)
    return date_obj.strftime("%d/%m/%Y")

def main():
    # Ask for the Roblox user ID
    user_id = input(Fore.BLUE + "Please enter the Roblox user ID: ")
    
    # Retrieve user information
    user_info = get_roblox_user_info(user_id)
    
    if user_info:
        print(Fore.BLUE + "User Information:")

        # Display user information in a formatted way
        info_order = ["displayName", "name", "description", "created", "isBanned", "id", "isVerified"]
        info_labels = {
            "displayName": "Display Name",
            "name": "Username",
            "description": "Description",
            "created": "Account Created",
            "isBanned": "Is Banned",
            "id": "User ID",
            "isVerified": "Is Verified"
        }
        
        message_content = ""
        for key in info_order:
            value = user_info.get(key, "N/A")
            if key == "created" and value != "N/A":
                value = format_date(value)
            if isinstance(value, bool):
                value = "Yes" if value else "No"
            info_string = f"{info_labels[key]}: {value}"
            print(Fore.BLUE + info_string)
            message_content += f"{info_string}\n"
        
        # Prepare the data to be sent to the webhook
        webhook_data = {"content": message_content.strip()}
        
        # Ask if the user wants to send the information to a webhook
        send_to_webhook_choice = input(Fore.BLUE + "Do you want to send this information to a webhook? (yes/no): ").strip().lower()
        
        yes_responses = {"yes", "yop", "yup", "y", "ye", "oui", "oi", "oe"}
        no_responses = {"no", "n", "nope", "nop", "nty", "nt", "non"}
        
        if send_to_webhook_choice in yes_responses:
            webhook_url = input(Fore.BLUE + "Please enter the webhook URL: ")
            send_to_webhook(webhook_data, webhook_url)
        elif send_to_webhook_choice in no_responses:
            print(Fore.BLUE + "Information was not sent to the webhook.")
        else:
            print(Fore.BLUE + "Invalid response. Please enter yes or no.")
    
    else:
        print(Fore.BLUE + "No information retrieved.")

    input(Fore.BLUE + "Press Enter to exit...")

    # Run the subprocess after user interaction
    subprocess.run(["python", "dream.py"])

if __name__ == "__main__":
    main()