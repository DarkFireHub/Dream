import json
import requests
from colorama import Fore, init
from validate_email_address import validate_email
import subprocess

# Initialize colorama
init(autoreset=True)

def lookup_email(email):
    if not validate_email(email):
        return Fore.BLUE + "The provided email is not valid."

    # Simulated lookup function - replace this with an actual API call if needed
    def simulated_lookup(email):
        # Simulated response data
        data = {
            "email": email,
            "domain": email.split('@')[-1],
            "valid": True,
            "organization": "Tech Solutions Inc.",
            "location": "San Francisco, USA"
        }
        return data

    # Get email information
    info = simulated_lookup(email)

    # Format the information
    result = (
        f"{Fore.BLUE}Information for the email: {info['email']}\n"
        f"{Fore.BLUE}Domain: {info['domain']}\n"
        f"{Fore.BLUE}Valid: {info['valid']}\n"
        f"{Fore.BLUE}Organization: {info['organization']}\n"
        f"{Fore.BLUE}Location: {info['location']}"
    )

    return result, info

def send_to_webhook(url, data):
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return Fore.BLUE + "Information sent successfully to the webhook."
        else:
            return Fore.BLUE + f"Failed to send information. Status code: {response.status_code}"
    except Exception as e:
        return Fore.BLUE + f"An error occurred: {str(e)}"

# Example usage
if __name__ == "__main__":
    email_to_lookup = input(Fore.BLUE + "Enter the email to lookup: ")
    info_text, info_data = lookup_email(email_to_lookup)
    print(info_text)

    send_webhook = input(Fore.BLUE + "Do you want to send this information to a webhook? (yes/no): ")
    if send_webhook.lower() == 'yes':
        webhook_url = input(Fore.BLUE + "Enter the webhook URL: ")
        result = send_to_webhook(webhook_url, info_data)
        print(result)

    # Execute the dream2.py script
    subprocess.run(["python", "dream2.py"])
