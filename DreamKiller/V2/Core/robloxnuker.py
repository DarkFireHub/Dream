import requests

# URL de l'API Roblox pour les messages privés
message_url = 'https://privatemessages.roblox.com/v1/messages/send'

# Session requests
session = requests.Session()

def get_csrf_token():
    response = session.post('https://auth.roblox.com/v2/logout')
    if 'x-csrf-token' in response.headers:
        session.headers.update({'x-csrf-token': response.headers['x-csrf-token']})
        print("CSRF token obtained")
    else:
        print("Failed to obtain CSRF token")

def get_user_info():
    response = session.get('https://users.roblox.com/v1/users/authenticated')
    if response.status_code == 200:
        user_info = response.json()
        username = user_info.get('name')
        print(f"Logged in as: {username}")
        return user_info
    else:
        print("Failed to retrieve user info")
        print(response.json())
        return None

def get_friends(user_id):
    response = session.get(f'https://friends.roblox.com/v1/users/{user_id}/friends')
    if response.status_code == 200:
        friends_data = response.json()['data']
        print("Friends data:", friends_data)
        return friends_data
    else:
        print("Failed to retrieve friends")
        print(response.json())
        return []

def send_message(recipient_id, message):
    payload = {
        'recipientId': recipient_id,
        'subject': 'Message from Python Script',
        'body': message
    }
    get_csrf_token()
    response = session.post(message_url, json=payload)
    if response.status_code == 200:
        print(f"Message sent to user {recipient_id}")
    else:
        print(f"Failed to send message to user {recipient_id}")
        print(response.json())

def main():
    roblosecurity_cookie = input("Enter your .ROBLOSECURITY cookie: ")
    session.cookies.update({'.ROBLOSECURITY': roblosecurity_cookie})
    
    user_info = get_user_info()
    if user_info:
        user_id = user_info['id']
        friends = get_friends(user_id)
        
        message = input("Enter the message you want to send to your friends on Roblox: ")
        
        for friend in friends:
            friend_id = friend['id']
            send_message(friend_id, message)

if __name__ == "__main__":
    main()
