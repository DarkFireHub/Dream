import subprocess
import requests
import json
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

def get_public_ip():
    response = requests.get('https://api.ipify.org?format=json')
    return response.json().get('ip')

def get_ip_info(ip):
    url = f'http://ipinfo.io/{ip}/json'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(Fore.BLUE + f"Error: Unable to retrieve IP information. Status Code: {response.status_code}")
        return None

def send_to_webhook(data, webhook_url):
    headers = {'Content-Type': 'application/json'}
    
    # Format the payload for Discord webhook
    payload = {
        "embeds": [
            {
                "title": f"IP Information for {data.get('ip', 'N/A')}",
                "fields": [
                    {"name": "IP", "value": data.get("ip", "N/A")},
                    {"name": "Hostname", "value": data.get("hostname", "N/A")},
                    {"name": "City", "value": data.get("city", "N/A")},
                    {"name": "Region", "value": data.get("region", "N/A")},
                    {"name": "Country", "value": data.get("country", "N/A")},
                    {"name": "Location", "value": data.get("loc", "N/A")},
                    {"name": "Organization", "value": data.get("org", "N/A")},
                    {"name": "Postal", "value": data.get("postal", "N/A")},
                    {"name": "Timezone", "value": data.get("timezone", "N/A")}
                ]
            }
        ]
    }

    response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        print(Fore.BLUE + "Information successfully sent to the webhook.")
    else:
        print(Fore.BLUE + f"Error: Unable to send information to the webhook. Status Code: {response.status_code}")
        print(Fore.BLUE + f"Response: {response.text}")

def print_ip_info(ip_info):
    print(Fore.BLUE + "IP Information:")
    for key, value in ip_info.items():
        print(Fore.BLUE + f"{key.capitalize()}: {value}")

def main():
    ip = get_public_ip()
    if ip:
        ip_info = get_ip_info(ip)
        if ip_info:
            print_ip_info(ip_info)

            send_to_webhook_choice = input(Fore.BLUE + "Do you want to send this information to a webhook? (yes/no): ").strip().lower()
            
            yes_responses = {"yes", "y", "ye", "yup", "yep", "oui", "o"}
            no_responses = {"no", "n", "nope", "non"}
            
            if send_to_webhook_choice in yes_responses:
                webhook_url = input(Fore.BLUE + "Enter the webhook URL: ")
                send_to_webhook(ip_info, webhook_url)
            elif send_to_webhook_choice in no_responses:
                print(Fore.BLUE + "Information was not sent to the webhook.")
            else:
                print(Fore.BLUE + "Invalid response. Please enter yes or no.")
        
        else:
            print(Fore.BLUE + "No information retrieved.")
    else:
        print(Fore.BLUE + "Unable to retrieve public IP address.")

    # Attendre une entrée de l'utilisateur avant d'exécuter dream.py
    subprocess.run(["python", "dream.py"])

if __name__ == "__main__":
    main()
