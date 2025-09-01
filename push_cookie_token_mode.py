import json
import os
import requests

LOGIN_STATE_FILE = "xhs_state.json"  # 文件名固定或自定义

def extract_cookie_string_from_json(json_file: str) -> str:
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    cookies = data.get("cookies", [])
    cookie_str = "; ".join(f"{cookie['name']}={cookie['value']}" for cookie in cookies)
    return cookie_str

def push_cookie_to_coze(cookie_str: str):
    coze_token = os.getenv("COZE_TOKEN")
    bot_id = os.getenv("COZE_BOT_ID")

    if not all([coze_token, bot_id]):
        print("❌ 缺少 COZE_TOKEN 或 COZE_BOT_ID 环境变量")
        return

    url = "https://api.coze.cn/open_api/v2/chat"
    headers = {
        "Authorization": f"Bearer {coze_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "bot_id": bot_id,
        "query": f"/cookie {cookie_str}",
        "stream": False
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("✅ Cookie 已成功推送至 Coze")
    else:
        print(f"❌ 推送失败 [{response.status_code}]: {response.text}")

def main():
    if not os.path.exists(LOGIN_STATE_FILE):
        print("❌ 未找到文件:", LOGIN_STATE_FILE)
        return

    try:
        print("✔ 读取并解析 Cookie 文件...")
        cookie_str = extract_cookie_string_from_json(LOGIN_STATE_FILE)
        print("✔ Cookie 字符串构造完成")

        push_cookie_to_coze(cookie_str)

    except Exception as e:
        print("❌ 执行失败:", str(e))

if __name__ == "__main__":
    main()
