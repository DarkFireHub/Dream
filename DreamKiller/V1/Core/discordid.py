import subprocess
import requests
import json
from datetime import datetime
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

def get_discord_user_info(user_id, bot_token):
    # Discord API URL to fetch user information
    url = f"https://discord.com/api/v9/users/{user_id}"
    headers = {
        'Authorization': f'Bot {bot_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(Fore.BLUE + f"Error: Unable to retrieve user information. Status Code: {response.status_code}")
        return None

def send_to_webhook(data, webhook_url):
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Format the payload for Discord webhook
    payload = {
        "embeds": [
            {
                "title": "Discord User Information",
                "fields": [
                    {"name": "Username", "value": data.get("username", "N/A")},
                    {"name": "Discriminator", "value": data.get("discriminator", "N/A")},
                    {"name": "User ID", "value": data.get("id", "N/A")},
                    {"name": "Avatar URL", "value": f"https://cdn.discordapp.com/avatars/{data.get('id')}/{data.get('avatar')}.png" if data.get("avatar") else "N/A"},
                    {"name": "Bio", "value": data.get("bio", "N/A")},
                    {"name": "Locale", "value": data.get("locale", "N/A")},
                    {"name": "Premium Type", "value": "Nitro Classic" if data.get("premium_type") == 1 else "Nitro" if data.get("premium_type") == 2 else "None"},
                    {"name": "Email Verified", "value": "Yes" if data.get("verified") else "No"},
                    {"name": "MFA Enabled", "value": "Yes" if data.get("mfa_enabled") else "No"}
                ]
            }
        ]
    }

    response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 204:
        print(Fore.BLUE + "Information successfully sent to the webhook.")
    else:
        print(Fore.BLUE + f"Error: Unable to send information to the webhook. Status Code: {response.status_code}")
        print(Fore.BLUE + f"Response: {response.text}")

def format_date(timestamp):
    # Discord timestamps are in Unix milliseconds
    date_obj = datetime.utcfromtimestamp(timestamp / 1000.0)
    return date_obj.strftime("%d/%m/%Y")

def main():
    # Ask for the Discord user ID and bot token
    user_id = input(Fore.BLUE + "Please enter the Discord user ID: ")
    bot_token = input(Fore.BLUE + "Please enter the Discord bot token: ")
    
    # Retrieve user information
    user_info = get_discord_user_info(user_id, bot_token)
    
    if user_info:
        print(Fore.BLUE + "User Information:")

        # Display user information in a formatted way
        info_labels = {
            "username": "Username",
            "discriminator": "Discriminator",
            "id": "User ID",
            "avatar": "Avatar URL",
            "banner": "Banner URL",
            "bio": "Bio",
            "locale": "Locale",
            "premium_type": "Premium Type",
            "public_flags": "Public Flags",
            "flags": "Flags",
            "email": "Email",
            "verified": "Email Verified",
            "mfa_enabled": "MFA Enabled"
        }
        
        for key, label in info_labels.items():
            value = user_info.get(key, "N/A")
            if key == "avatar" or key == "banner":
                value = f"https://cdn.discordapp.com/{key}s/{user_id}/{value}.png"
            elif key == "premium_type":
                value = "Nitro Classic" if value == 1 else "Nitro" if value == 2 else "None"
            elif key == "verified" or key == "mfa_enabled":
                value = "Yes" if value else "No"
            elif isinstance(value, int):
                value = str(value)
            info_string = f"{label}: {value}"
            print(Fore.BLUE + info_string)
        
        # Ask if the user wants to send the information to a webhook
        send_to_webhook_choice = input(Fore.BLUE + "Do you want to send this information to a webhook? (yes/no): ").strip().lower()
        
        yes_responses = {"yes", "yop", "yup", "y", "ye", "oui", "oi", "oe"}
        no_responses = {"no", "n", "nope", "nop", "nty", "nt", "non"}
        
        if send_to_webhook_choice in yes_responses:
            webhook_url = input(Fore.BLUE + "Please enter the webhook URL: ")
            send_to_webhook(user_info, webhook_url)
        elif send_to_webhook_choice in no_responses:
            print(Fore.BLUE + "Information was not sent to the webhook.")
        else:
            print(Fore.BLUE + "Invalid response. Please enter yes or no.")
    
    else:
        print(Fore.BLUE + "No information retrieved.")

    subprocess.run(["python", "dream.py"])

if __name__ == "__main__":
    main()
