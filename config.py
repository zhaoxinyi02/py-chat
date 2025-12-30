import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    
    DEFAULT_PROVIDER = "openai"
    
    OPENAI_DEFAULT_MODEL = "gpt-3.5-turbo"
    DEEPSEEK_DEFAULT_MODEL = "deepseek-chat"
    
    OPENAI_MODELS = [
        "gpt-3.5-turbo",
        "gpt-4",
        "gpt-4-turbo-preview"
    ]
    
    DEEPSEEK_MODELS = [
        "deepseek-chat",
        "deepseek-coder"
    ]
    
    DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
    
    DEFAULT_TEMPERATURE = 0.7
    
    MAX_TOKENS = 1000
    
    DEFAULT_SYSTEM_PROMPT = """你是一个专业的智能客服机器人。你的职责是：
1. 友好、专业地回答用户的问题
2. 提供准确、有帮助的信息
3. 在不确定时，诚实地告知用户
4. 保持礼貌和耐心
5. 记住对话上下文，提供连贯的多轮对话体验

请用中文回答用户的问题。"""
    
    CONVERSATION_SAVE_DIR = "conversations"
    
    @classmethod
    def ensure_save_dir(cls):
        if not os.path.exists(cls.CONVERSATION_SAVE_DIR):
            os.makedirs(cls.CONVERSATION_SAVE_DIR)
