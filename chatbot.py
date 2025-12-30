import openai
from typing import List, Dict, Optional
import json
import os
from datetime import datetime
import requests


class CustomerServiceChatbot:
    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo", 
                 provider: str = "openai", base_url: Optional[str] = None):
        """
        初始化智能客服机器人
        
        Args:
            api_key: API密钥（OpenAI或DeepSeek）
            model: 模型名称
            provider: API提供商 ("openai" 或 "deepseek")
            base_url: 自定义API基础URL（可选）
        """
        self.provider = provider.lower()
        
        if self.provider == "openai":
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass it directly.")
            openai.api_key = self.api_key
            if base_url:
                openai.api_base = base_url
        elif self.provider == "deepseek":
            self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
            if not self.api_key:
                raise ValueError("DeepSeek API key is required. Set DEEPSEEK_API_KEY environment variable or pass it directly.")
            self.base_url = base_url or "https://api.deepseek.com/v1"
        else:
            raise ValueError(f"Unsupported provider: {provider}. Use 'openai' or 'deepseek'.")
        
        self.model = model
        self.conversation_history: List[Dict[str, str]] = []
        self.system_prompt = """你是一个专业的智能客服机器人。你的职责是：
1. 友好、专业地回答用户的问题
2. 提供准确、有帮助的信息
3. 在不确定时，诚实地告知用户
4. 保持礼貌和耐心
5. 记住对话上下文，提供连贯的多轮对话体验

请用中文回答用户的问题。"""
        
        self.conversation_history.append({
            "role": "system",
            "content": self.system_prompt
        })
    
    def chat(self, user_message: str) -> str:
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            if self.provider == "openai":
                assistant_message = self._chat_openai()
            elif self.provider == "deepseek":
                assistant_message = self._chat_deepseek()
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
            
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
        
        except Exception as e:
            error_message = f"抱歉，发生了错误：{str(e)}"
            return error_message
    
    def _chat_openai(self) -> str:
        """使用OpenAI API进行对话"""
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.conversation_history,
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    
    def _chat_deepseek(self) -> str:
        """使用DeepSeek API进行对话"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.model,
            "messages": self.conversation_history,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"DeepSeek API error: {response.status_code} - {response.text}")
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
    
    def reset_conversation(self):
        self.conversation_history = [{
            "role": "system",
            "content": self.system_prompt
        }]
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        return [msg for msg in self.conversation_history if msg["role"] != "system"]
    
    def save_conversation(self, filename: str = None):
        conversations_dir = "conversations"
        if not os.path.exists(conversations_dir):
            os.makedirs(conversations_dir)
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(conversations_dir, f"conversation_{timestamp}.json")
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)
        
        return filename
    
    def load_conversation(self, filename: str):
        with open(filename, 'r', encoding='utf-8') as f:
            self.conversation_history = json.load(f)
    
    def set_system_prompt(self, prompt: str):
        self.system_prompt = prompt
        self.conversation_history[0] = {
            "role": "system",
            "content": prompt
        }


if __name__ == "__main__":
    print("=== 智能客服机器人 (命令行版本) ===")
    print("输入 'quit' 或 'exit' 退出")
    print("输入 'reset' 重置对话")
    print("输入 'save' 保存对话历史")
    print("=" * 40)
    
    openai_key = os.getenv("OPENAI_API_KEY")
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    
    if openai_key:
        print("\n检测到 OpenAI API Key，使用 OpenAI")
        provider = "openai"
        model = "gpt-3.5-turbo"
    elif deepseek_key:
        print("\n检测到 DeepSeek API Key，使用 DeepSeek")
        provider = "deepseek"
        model = "deepseek-chat"
    else:
        print("\n错误: 未找到 API Key")
        print("请设置 OPENAI_API_KEY 或 DEEPSEEK_API_KEY 环境变量")
        exit(1)
    
    try:
        chatbot = CustomerServiceChatbot(provider=provider, model=model)
        print(f"使用模型: {model}")
        print("=" * 40)
        
        while True:
            user_input = input("\n你: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("\n感谢使用智能客服机器人！再见！")
                break
            
            if user_input.lower() == 'reset':
                chatbot.reset_conversation()
                print("\n对话已重置。")
                continue
            
            if user_input.lower() == 'save':
                filename = chatbot.save_conversation()
                print(f"\n对话已保存到: {filename}")
                continue
            
            response = chatbot.chat(user_input)
            print(f"\n客服: {response}")
    
    except ValueError as e:
        print(f"\n错误: {e}")
    except KeyboardInterrupt:
        print("\n\n程序已终止。再见！")
