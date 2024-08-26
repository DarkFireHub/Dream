import requests
import json
from datetime import datetime
from colorama import init, Fore
import subprocess

# Initialize colorama
init(autoreset=True)

def get_user_id_by_username(username):
    url = "https://users.roblox.com/v1/usernames/users"
    payload = {"usernames": [username]}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        data = response.json()
        if data["data"]:
            return data["data"][0]["id"]
        else:
            print(Fore.BLUE + "Error: No user found with that username.")
            return None
    else:
        print(Fore.BLUE + f"Error: Unable to retrieve user ID. Status code: {response.status_code}")
        return None

def get_roblox_user_info(user_id):
    url = f"https://users.roblox.com/v1/users/{user_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(Fore.BLUE + f"Error: Unable to retrieve user information. Status code: {response.status_code}")
        return None

def send_to_webhook(data, webhook_url):
    headers = {'Content-Type': 'application/json'}
    content = (
        f"Display Name: {data.get('displayName', 'N/A')}\n"
        f"Username: {data.get('name', 'N/A')}\n"
        f"Description: {data.get('description', 'N/A')}\n"
        f"Account Created: {format_date(data.get('created', 'N/A'))}\n"
        f"Is Banned: {'Yes' if data.get('isBanned') else 'No'}\n"
        f"User ID: {data.get('id', 'N/A')}\n"
        f"Is Verified: {'Yes' if data.get('isVerified') else 'No'}\n"
    )
    payload = {
        "content": content
    }
    print(Fore.BLUE + f"Payload to be sent: {payload}")  # Log the payload
    
    try:
        response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            print(Fore.BLUE + "Information successfully sent to the webhook.")
        else:
            print(Fore.BLUE + f"Error: Unable to send information to the webhook. Status code: {response.status_code}")
            print(Fore.BLUE + f"Response: {response.text}")  # Log the response text for more details
    except requests.exceptions.RequestException as e:
        print(Fore.BLUE + f"Error: {e}")

def format_date(date_string):
    try:
        date_obj = datetime.fromisoformat(date_string)
        return date_obj.strftime("%d/%m/%Y")
    except ValueError:
        return "Invalid date format"

def main():
    username = input(Fore.BLUE + "Please enter the Roblox username: ")
    user_id = get_user_id_by_username(username)
    
    if user_id:
        user_info = get_roblox_user_info(user_id)
        
        if user_info:
            print(Fore.BLUE + "User Information:")
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
            
            for key in info_order:
                value = user_info.get(key, "N/A")
                if key == "created" and value != "N/A":
                    value = format_date(value)
                if isinstance(value, bool):
                    value = "Yes" if value else "No"
                info_string = f"{info_labels[key]}: {value}"
                print(Fore.BLUE + info_string)
            
            send_to_webhook_choice = input(Fore.BLUE + "Do you want to send this information to a webhook? (yes/no): ").strip().lower()
            yes_responses = {"yes", "y", "oui", "o"}
            no_responses = {"no", "n", "non"}
            
            if send_to_webhook_choice in yes_responses:
                webhook_url = input(Fore.BLUE + "Please enter the webhook URL: ")
                send_to_webhook(user_info, webhook_url)
            elif send_to_webhook_choice in no_responses:
                print(Fore.BLUE + "Information was not sent to the webhook.")
            else:
                print(Fore.BLUE + "Invalid response. Please enter yes or no.")
        else:
            print(Fore.BLUE + "No information retrieved.")
    else:
        print(Fore.BLUE + "Unable to retrieve user ID.")

    # Run dream.py using subprocess
    subprocess.run(["python", "dream.py"])

if __name__ == "__main__":
    main()
