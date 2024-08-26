import json
import requests
from colorama import Fore, init
import subprocess
import phonenumbers
from phonenumbers import geocoder, carrier

# Initialize colorama
init(autoreset=True)

def lookup_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        if not phonenumbers.is_valid_number(parsed_number):
            return Fore.BLUE + "The provided phone number is not valid."

        country = geocoder.description_for_number(parsed_number, "en")
        operator = carrier.name_for_number(parsed_number, "en")

        # Simulated response data
        data = {
            "phone_number": phone_number,
            "country": country,
            "operator": operator,
            "valid": True
        }

        return data
    except Exception as e:
        return Fore.BLUE + f"An error occurred: {str(e)}"

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
    phone_number_to_lookup = input(Fore.BLUE + "Enter the phone number to lookup (in international format, e.g., +1234567890): ")
    info_data = lookup_phone_number(phone_number_to_lookup)

    if isinstance(info_data, dict):
        # Format the information
        info_text = (
            f"{Fore.BLUE}Information for the phone number: {info_data['phone_number']}\n"
            f"{Fore.BLUE}Country: {info_data['country']}\n"
            f"{Fore.BLUE}Operator: {info_data['operator']}\n"
            f"{Fore.BLUE}Valid: {info_data['valid']}"
        )
        print(info_text)

        send_webhook = input(Fore.BLUE + "Do you want to send this information to a webhook? (yes/no): ")
        if send_webhook.lower() == 'yes':
            webhook_url = input(Fore.BLUE + "Enter the webhook URL: ")
            result = send_to_webhook(webhook_url, info_data)
            print(result)

    else:
        print(info_data)

    # Execute the dream2.py script
    subprocess.run(["python", "dream2.py"])
