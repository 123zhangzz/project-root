import os
import requests
import json
import time
from datetime import datetime

def get_xhs_cookie():
    """
    获取小红书Cookie的实际实现
    这里需要您根据实际情况填写具体的获取逻辑
    """
    # 示例实现 - 请替换为您的实际Cookie获取逻辑
    # 可能是通过Selenium自动化、API调用或其他方式
    
    # 模拟获取Cookie的过程
    print("正在获取Cookie...")
    
    # 这里应该是您实际的Cookie获取代码
    # 例如：
    # cookie = your_cookie_getting_function()
    
    # 示例中使用模拟数据
    cookie = f"xhs_token=example_{int(time.time())}; user_id=123456; session={int(time.time())}"
    
    return cookie

def send_to_feishu_directly(content, token, receive_id, receive_id_type="chat_id"):
    """
    直接使用飞书API发送消息，绕过Coze平台
    
    :param content: 要发送的内容
    :param token: 飞书API访问令牌
    :param receive_id: 接收者ID（可以是chat_id, user_id, open_id, email）
    :param receive_id_type: 接收者ID类型，默认为chat_id
    :return: 是否成功
    """
    # 飞书消息API端点
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 构建消息内容
    payload = {
        "receive_id": receive_id,
        "msg_type": "text",
        "content": json.dumps({"text": content})
    }
    
    # 添加查询参数指定ID类型
    params = {"receive_id_type": receive_id_type}
    
    try:
        response = requests.post(
            url, 
            headers=headers, 
            json=payload, 
            params=params,
            timeout=30
        )
        
        print(f"飞书API响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("消息成功发送到飞书!")
            print(f"消息ID: {result.get('data', {}).get('message_id')}")
            return True
        else:
            print(f"飞书API错误: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"请求飞书API失败: {e}")
        return False

def main():
    # 从环境变量获取配置
    feishu_token = os.getenv("FEISHU_ACCESS_TOKEN")
    receive_id = os.getenv("FEISHU_RECEIVE_ID")
    receive_id_type = os.getenv("FEISHU_RECEIVE_ID_TYPE", "chat_id")  # 默认使用chat_id
    
    if not all([feishu_token, receive_id]):
        print("错误: 缺少必要的环境变量")
        print("请设置 FEISHU_ACCESS_TOKEN 和 FEISHU_RECEIVE_ID")
        return
    
    # 获取Cookie
    cookie = get_xhs_cookie()
    if not cookie:
        print("未能获取到Cookie")
        return
    
    print(f"获取到的Cookie: {cookie}")
    
    # 格式化消息内容
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"【自动推送】小红书Cookie更新\n时间: {current_time}\nCookie内容:\n{cookie}"
    
    # 直接发送到飞书
    success = send_to_feishu_directly(
        content=message,
        token=feishu_token,
        receive_id=receive_id,
        receive_id_type=receive_id_type
    )
    
    if success:
        print("Cookie已成功发送到飞书")
    else:
        print("发送到飞书失败")

if __name__ == "__main__":
    main()
