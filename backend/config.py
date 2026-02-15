import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')

# JWT configuration
JWT_SECRET_KEY = 'your_secret_key'

client = OpenAI(api_key="sk-6b2c67a266834cb7a373f5ee07f510ba", base_url="https://api.deepseek.com")

headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer sk-YZlZxvQyIzmoBWXN6QcmADwFohBLcrJZL6fJzEXD0mYlzG1I',
    'Content-Type': 'application/json'
}

def load_config():
    env_path = Path(__file__).parent / "var.env"
    if not env_path.exists():
        print('------------------------------------------------------------')
        raise FileNotFoundError(f".env file not found at {env_path}")
    
    load_dotenv(env_path, encoding='utf-8')

    # 验证变量是否加载成功
    test_var = os.getenv("COZE_CLIENT_ID")
    print(f"测试变量 COZE_CLIENT_ID: {test_var}")  # 应显示您的真实ID

class Config:
    def __init__(self):
        load_config()
        self.CLIENT_ID = os.getenv('COZE_CLIENT_ID')
        self.CLIENT_SECRET = os.getenv('COZE_CLIENT_SECRET')
        self.ACCESS_TOKEN = os.getenv('COZE_ACCESS_TOKEN')
        self.REFRESH_TOKEN = os.getenv('COZE_REFRESH_TOKEN')
        self.API_BASE = os.getenv('COZE_API_BASE', 'https://api.coze.cn')
        self.BOT_ID = os.getenv('COZE_BOT_ID')
        self.USER_ID = os.getenv('COZE_DEFAULT_USER_ID', 'default_user')
        self.COZE_REDIRECT_URI = os.getenv('COZE_REDIRECT_URI', 'http://localhost:5000/api/chat/oauth/callback')
        self.COZE_SUCCESS_REDIRECT_URI = os.getenv('COZE_SUCCESS_REDIRECT_URI', 'http://localhost:5000/zh/home')

config = Config()

