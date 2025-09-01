import os
import json
import requests

# 可选：如果你有 xhs_state.json，可提取 Cookie。不过下文假设直接使用环境变量
def get_cookie_from_env():
    cookie = os.getenv("XHS_COOKIE")
    if not cookie:
        print("❌ 未提供 XHS_COOKIE")
        exit(1)
    return cookie

def push_cookie_to_coze(cookie_str: str):
    coze_token = os.getenv("COZE_TOKEN")
    bot_id = os.getenv("COZE_BOT_ID")
    if not all([coze_token, bot_id]):
        print("❌ 缺少 COZE_TOKEN 或 COZE_BOT_ID")
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

    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code == 200:
        print("✅ Cookie 成功推送到 Coze Bot")
    else:
        print(f"❌ 推送失败 [{resp.status_code}]:", resp.text)

def main():
    cookie = get_cookie_from_env()
    print("Cookie:", cookie)
    push_cookie_to_coze(cookie)

if __name__ == "__main__":
    main()
