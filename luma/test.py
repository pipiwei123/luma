import requests
import time

# 定义常量
BASE_URL = "https://luma.super-api.cn/api/photon/v1/generations/"
CREATE_URL = BASE_URL + "?andrew=true"
HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Content-Type": "application/json",
    "Cookie": "_gcl_au=1.1.1625405224.1718366624; _ga=GA1.1.603950015.1718366885; _clck=hmcbd2%7C2%7Cfmn%7C0%7C1626; access_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOnsidXNlcl91dWlkIjoiMmQxY2M1YzEtNmQ4MC00NGYyLTk4ZTEtYzMyY2RiMjcwOGViIiwiY2xpZW50X2lkIjoiIn0sImV4cCI6MTcxOTA3OTE0MX0.VhUWUPxgE6CfKw3bI77RPn1QAbMVAn5upxqvrcxt8L0; refresh_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOnsidXNlcl91dWlkIjoiMmQxY2M1YzEtNmQ4MC00NGYyLTk4ZTEtYzMyY2RiMjcwOGViIiwiY2xpZW50X2lkIjoiIn0sImV4cCI6MTcxOTA3OTE0MX0.VhUWUPxgE6CfKw3bI77RPn1QAbMVAn5upxqvrcxt8L0; _clsk=16aiv64%7C1718475436884%7C9%7C1%7Cq.clarity.ms%2Fcollect; _ga_67JX7C10DX=GS1.1.1718474336.3.1.1718475436.0.0.0",
    "Origin": "https://lumalabs.ai",
    "Referer": "https://lumalabs.ai/",
    "Sec-Ch-Ua": '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
}

# 创建任务的负载
payload = {
    "user_prompt": "一个猫咪在吃鱼",
    "aspect_ratio": "16:9",
    "expand_prompt": True
}

def create_task():
    response = requests.post(CREATE_URL, headers=HEADERS, json=payload)
    if response.status_code == 201:
        data = response.json()
        print(data)
        return data[0]['id']
    else:
        print("Failed to create task")
        return None

def check_task_status(task_id):
    url = BASE_URL + task_id
    response = requests.get(url, headers=HEADERS)
    print(response.json())
    if response.status_code == 200:
        return response.json()

    else:
        print("Failed to check task status")
        return None

def main():
    task_id = create_task()
    if not task_id:
        return

    print(f"Task created with ID: {task_id}")

    while True:
        task_status = check_task_status(task_id)
        if task_status:
            if task_status['state'] == 'completed':
                print("Task completed!")
                print("Video URL:", task_status['video']['url'])
                break
            else:
                print("Task still pending...")
        time.sleep(1)

if __name__ == "__main__":
    main()
