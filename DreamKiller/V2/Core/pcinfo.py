import platform
import psutil
import requests
import subprocess
import getpass
import GPUtil

def get_pc_info():
    gpus = GPUtil.getGPUs()
    gpu_info = "None"
    if gpus:
        gpu = gpus[0]
        gpu_info = f"{gpu.name}, {gpu.memoryTotal} MB"
    
    info = {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Platform": platform.platform(),
        "Processor": platform.processor(),
        "RAM": f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB",
        "CPU Cores": psutil.cpu_count(logical=False),
        "CPU Threads": psutil.cpu_count(logical=True),
        "Disk Usage": f"{psutil.disk_usage('/').percent}%",
        "User": getpass.getuser(),
        "GPU": gpu_info
    }
    return info

def display_info(info):
    print("\033[34m")  # Set text color to blue
    for key, value in info.items():
        print(f"{key}: {value}")
    print("\033[0m")  # Reset text color to default

def send_to_webhook(info, url):
    response = requests.post(url, json=info)
    return response.status_code, response.text

def execute_script(script_name):
    subprocess.run(["python", script_name])

def main():
    info = get_pc_info()
    display_info(info)
    
    choice = input("Do you want to send this information to a webhook? (yes/no): ")
    if choice.lower() == 'yes':
        webhook_url = input("Please enter the webhook URL: ")
        status, response = send_to_webhook(info, webhook_url)
        print(f"Webhook response status: {status}")
        print(f"Webhook response: {response}")
    
    execute_script("dream.py")

if __name__ == "__main__":
    main()
