import requests
from prettytable import PrettyTable
import subprocess  # Pour exécuter un autre script

# Replace 'YOUR_API_KEY' with your actual API key obtained from the Brawl Stars Developer Portal
API_KEY = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImE5ZDY0MDRkLWQyM2EtNDlhYy1hZjMzLWQyMWI1MDEyNzczMCIsImlhdCI6MTcyMTI0NDk4MCwic3ViIjoiZGV2ZWxvcGVyLzBmMjA0MTc1LTA1MWItYzk0My1mNjYzLWU0ZGFmNDQ4YWEyZSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiNzAuMzYuNC45OCJdLCJ0eXBlIjoiY2xpZW50In1dfQ.G874F37zZOHfLXyrY6XipKgCrq_V-mRdMaO94ijdfFEl2zfPIdz5CIMvJAbboeSYsciBeuJZKa9AHLJsqwVUaA'
BASE_URL = 'https://api.brawlstars.com/v1/players/'

# Function to get Brawl Stars account information
def get_brawl_stars_account_info(player_id):
    # Replace special characters in the player's ID
    player_id = player_id.replace('#', '%23')
    
    # Define the request headers
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    
    # Make the GET request to the API
    response = requests.get(f'{BASE_URL}{player_id}', headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to display account information in a formatted table
def display_account_info(account_info):
    table = PrettyTable()
    table.field_names = ["Attribute", "Value"]
    
    # Add rows to the table
    table.add_row(["Name", account_info.get('name', 'N/A')])
    table.add_row(["Tag", account_info.get('tag', 'N/A')])
    table.add_row(["Trophies", account_info.get('trophies', 'N/A')])
    table.add_row(["Experience Level", account_info.get('expLevel', 'N/A')])
    table.add_row(["Club", account_info.get('club', {}).get('name', 'N/A')])
    
    # Display the table
    print(table)

# Function to ask if user wants to send info to webhook
def ask_send_to_webhook():
    answer = input("Do you want to send this information to a webhook? (yes/no): ").strip().lower()
    return answer == 'yes'

# Example usage
if __name__ == "__main__":
    player_id = input("Enter the Brawl Stars player ID (e.g., #2PP): ")
    account_info = get_brawl_stars_account_info(player_id)
    
    if account_info:
        print("Brawl Stars account information:")
        display_account_info(account_info)
        
        # Ask if user wants to send info to webhook
        if ask_send_to_webhook():
            # Here you can add code to send data to webhook
            print("Sending information to webhook... (placeholder)")
        else:
            print("Not sending information to webhook.")
            
        # Run another script at the end
        print("Executing dream2.py...")
        subprocess.run(['python', 'dream2.py'])  # Replace with appropriate command if needed
    else:
        print("Unable to get account information. Please check the ID and try again.")
