import requests
import json
import subprocess

def get_private_server_links(game_id):
    url = f"https://discord-gg-keybypass.unblocked.eu.org/api/private-servers/{game_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        try:
            data = response.json()
            if isinstance(data, list):
                return data
            elif 'links' in data:
                links = data['links']
                return links
            else:
                print("No 'links' key found in the response.")
                return []
        except json.JSONDecodeError:
            print("Failed to decode JSON response.")
            return []
    else:
        print(f"Error during the request. Status: {response.status_code}")
        return []

def send_to_discord(webhook_url, links):
    max_length = 2000
    # Create chunks of links where each chunk's length is under max_length
    message = "\n".join(links)
    
    while len(message) > max_length:
        # Find the maximum number of characters that can fit in the chunk
        split_index = message.rfind('\n', 0, max_length)
        if split_index == -1:
            split_index = max_length
        
        chunk = message[:split_index]
        message = message[split_index:].lstrip()
        
        payload = {
            "content": chunk
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
        
        if response.status_code == 204:
            print("Successfully sent a chunk of links.")
        else:
            print(f"Failed to send chunk. Status: {response.status_code}")
            print(f"Response: {response.text}")
    
    # Send the remaining part of the message
    if message:
        payload = {
            "content": message
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
        
        if response.status_code == 204:
            print("Successfully sent the last chunk of links.")
        else:
            print(f"Failed to send the last chunk. Status: {response.status_code}")
            print(f"Response: {response.text}")

def main():
    game_id = input("Game Id : ")
    links = get_private_server_links(game_id)
    
    if links:
        for link in links:
            print(link)
        
        send_to_webhook = input("Do you want to send the links to a Discord webhook? (yes/no): ")
        if send_to_webhook.lower() == 'yes':
            webhook_url = input("Please enter the Discord webhook URL: ")
            send_to_discord(webhook_url, links)
    else:
        print("No private server links found.")
    
    # Execute dream.py
    subprocess.run(["python", "dream.py"])

if __name__ == "__main__":
    main()
