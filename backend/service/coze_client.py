# service/coze_client.py

import os
import time
from pathlib import Path
from dotenv import load_dotenv
from cozepy import Coze, Message, TokenAuth, WebOAuthApp, OAuthToken
from config import config

# 1) 自定义异常，必须在 _refresh_token() 里用之前定义
class NeedReauthorize(Exception):
    """Refresh Token 失效，需要用户重新授权"""

class CozeClient:
    def __init__(self):
        # 强烈推荐用 config 而不是 os.getenv 直接读
        self.oauth_app = WebOAuthApp(
            client_id     = config.CLIENT_ID,
            client_secret = config.CLIENT_SECRET,
            base_url      = config.API_BASE,
        )

        # 从环境读初始 token（第一次启动前，你必须先跑一次授权拿好这对 token）
        self.token = OAuthToken(
            access_token  = config.ACCESS_TOKEN,
            refresh_token = config.REFRESH_TOKEN,
            expires_in    = 900,
        )

        # 初始化 Coze 客户端
        self._init_client()
        # 记录上次刷新时间
        self.last_refresh = time.time()

    def _init_client(self):
        self.client = Coze(
            auth     = TokenAuth(self.token.access_token),
            base_url = config.API_BASE,
        )

    def _refresh_token(self) -> bool:
        try:
            # 用旧的 refresh_token 去刷新
            new_token = self.oauth_app.refresh_access_token(self.token.refresh_token)
            # 更新内存
            self.token = new_token
            self.last_refresh = time.time()
            # 持久化到 var.env
            self._update_env_tokens()
            # 用新的 access_token 重建 client
            self._init_client()
            return True

        except Exception as e:
            msg = str(e)
            # 如果是因为 refresh token 过期，就抛给上层处理
            if "invalid refresh token" in msg:
                raise NeedReauthorize(msg)
            # 其它异常仍然暴炸
            raise RuntimeError(f"Token refresh failed: {msg}")

    def _update_env_tokens(self):
        """把最新的 access_token/refresh_token 写回到 var.env，并 reload"""
        env_path = Path(__file__).parent.parent / "var.env"
        lines = env_path.read_text(encoding="utf-8").splitlines(keepends=True)

        for i, line in enumerate(lines):
            if line.startswith("COZE_ACCESS_TOKEN="):
                lines[i] = f"COZE_ACCESS_TOKEN={self.token.access_token}\n"
            elif line.startswith("COZE_REFRESH_TOKEN="):
                lines[i] = f"COZE_REFRESH_TOKEN={self.token.refresh_token}\n"

        env_path.write_text("".join(lines), encoding="utf-8")
        load_dotenv(env_path, override=True)

    def authorize_with_code(self, code: str):
        """
        前端回调得到 code 后，调用这里完成 OAuth 码→令牌 的交换
        """
        print(config.COZE_REDIRECT_URI)
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        token = self.oauth_app.get_access_token(
            redirect_uri = config.COZE_REDIRECT_URI,
            code         = code,
        )
        self.token = token
        self.last_refresh = time.time()
        self._update_env_tokens()
        self._init_client()

    def safe_chat(self, message: str, max_retries: int = 2) -> str:
        for attempt in range(max_retries):
            try:
                # 如果快到期，先刷新
                if time.time() - self.last_refresh > (self.token.expires_in - 60):
                    self._refresh_token()

                chat_poll = self.client.chat.create_and_poll(
                    bot_id   = config.BOT_ID,
                    user_id  = config.USER_ID,
                    additional_messages=[Message.build_user_question_text(message)],
                )
                # 找到第一个 answer 返回
                for msg in chat_poll.messages:
                    if msg.type == "answer":
                        return msg.content
                return "No answer received"

            except NeedReauthorize:
                # Refresh Token 真的失效，抛给路由去重授权
                raise
            except Exception:
                # 其它错误时再试一次
                if attempt < max_retries - 1:
                    self._refresh_token()
                    continue
                raise

# 全局单例
coze_client = CozeClient()
