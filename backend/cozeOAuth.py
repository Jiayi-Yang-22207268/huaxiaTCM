import requests
import json
import urllib.parse
import time
from typing import Dict, Optional

class CozeOAuthClient:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        """初始化Coze OAuth客户端"""
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.auth_code = "code_pulrZXwWMkzFPAOqkXIRviY4HSk7dpdLtHHtcljJ9AQwyEeI"
        
        # Coze API端点
        self.auth_base_url = "https://www.coze.cn/api/permission/oauth2"
        self.token_url = f"{self.auth_base_url}/token"
        self.authorize_url = f"{self.auth_base_url}/authorize"
        
        # 令牌信息
        self.access_token = None
        self.refresh_token = None
        self.token_expires_at = 0
    
    def get_authorization_url(self, state: str = None) -> str:
        """生成授权URL，引导用户访问此URL进行授权"""
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "state":state
        }
        
        # 对参数进行URL编码
        encoded_params = urllib.parse.urlencode(params)
        
        # 先获取授权跳转链接
        auth_redirect_response = requests.get(
            f"{self.authorize_url}?{encoded_params}"
        )
        print(auth_redirect_response.status_code)
        print(auth_redirect_response.headers.get("location"))

        if auth_redirect_response.status_code == 302:
            print("Correct")
        else:
            print("Fail")
        
        # # 从响应头中获取真正的跳转URL
        # if auth_redirect_response.status_code == 302:
        #     return auth_redirect_response.headers.get("location", "")
        # else:
        #     raise Exception(f"获取授权跳转链接失败: {auth_redirect_response.text}")
    
    def exchange_token(self) -> Dict:
        """用授权码交换访问令牌和刷新令牌"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.client_secret
        }
        
        data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "code": self.auth_code
        }
        
        response = requests.post(self.token_url, headers=headers, data=data)
        response_data = response.json()
        print(response.headers.get("X-Tt-Logid"))
        print(response_data)
        
        if response.status_code == 200:
            self._save_token_info(response_data)
            return response_data
        else:
            raise Exception(f"交换令牌失败: {response_data}")
    
    def refresh_access_token(self) -> Dict:
        """刷新访问令牌"""
        if not self.refresh_token:
            raise Exception("没有刷新令牌可用")
        
        headers = {
            "Authorization": f"Bearer {self.client_secret}",
            "Content-Type": "application/json"
        }
        
        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "refresh_token": self.refresh_token
        }
        
        response = requests.post(self.token_url, headers=headers, json=data)
        response_data = response.json()
        
        if response.status_code == 200:
            self._save_token_info(response_data)
            return response_data
        else:
            raise Exception(f"刷新令牌失败: {response_data}")
    
    def _save_token_info(self, token_data: Dict) -> None:
        """保存令牌信息并计算过期时间"""
        self.access_token = token_data.get("access_token")
        self.refresh_token = token_data.get("refresh_token")
        
        # 设置过期时间（提前1分钟，避免边界问题）
        expires_in = token_data.get("expires_in", 900)  # 默认15分钟
        self.token_expires_at = int(time.time()) + expires_in - 60
    
    def is_token_expired(self) -> bool:
        """检查令牌是否已过期"""
        return time.time() >= self.token_expires_at
    
    def call_agent_api(self, bot_id: str, endpoint: str, method: str = "GET", 
                      data: Optional[Dict] = None) -> Dict:
        """调用Coze智能体API，自动处理令牌刷新"""
        # 检查令牌是否过期，过期则刷新
        if self.is_token_expired() and self.refresh_token:
            self.refresh_access_token()
        
        if not self.access_token:
            raise Exception("没有有效的访问令牌")
        
        # 构建API请求
        base_api_url = "https://api.coze.cn/v1/bot"
        url = f"{base_api_url}/{endpoint}"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        # 根据请求方法发送请求
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, params=data)
        else:
            response = requests.post(url, headers=headers, json=data)
        
        return response.json()

# 使用示例
if __name__ == "__main__":
    # 填入你的应用信息
    CLIENT_ID = "01286810717636494777659388133804.app.coze"
    CLIENT_SECRET = "H6aEpPWcfEA1QpkGOh5lit8p9rBrcgxK3XmoBjOAuOgoKigx"
    REDIRECT_URI = "http://localhost:5173/zh/new-page"
    
    # 初始化客户端
    client = CozeOAuthClient(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    
    # 1. 生成授权URL
    # auth_url = client.get_authorization_url(state="random_state_123")
    # print(f"请访问以下URL进行授权: {auth_url}")
    
    # # 2. 用户授权后，获取回调URL中的code参数
    # # 注意：这一步需要在你的Web应用中实现，接收回调并提取code
    # # 这里仅作示例，实际使用时需替换为真实的code
    # auth_code = input("请输入授权码: ")
    
    # # 3. 交换令牌
    # code_NeqkcdWzH5JRuW8pnBEaDLJT7fhafPCueM5BUmmjeM34KbvK
    token_data = client.exchange_token()
    print(f"获取令牌成功: {token_data}")
    
    # # 4. 调用智能体API（示例：获取智能体配置）
    # BOT_ID = "你的智能体ID"
    # response = client.call_agent_api(
    #     bot_id=BOT_ID,
    #     endpoint="get_online_info",
    #     method="GET",
    #     data={"bot_id": BOT_ID}
    # )
    
    # print(f"API调用结果: {response}")