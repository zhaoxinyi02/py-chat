from chatbot import CustomerServiceChatbot
import os

print("=" * 50)
print("DeepSeek API 测试")
print("=" * 50)

api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    print("\n❌ 错误: 未找到 DEEPSEEK_API_KEY 环境变量")
    print("请先设置: $env:DEEPSEEK_API_KEY='your_key'")
    exit(1)

print(f"\n✅ API Key 已配置: {api_key[:20]}...")

try:
    print("\n正在初始化 DeepSeek 聊天机器人...")
    chatbot = CustomerServiceChatbot(
        provider="deepseek",
        model="deepseek-chat"
    )
    print("✅ 初始化成功！")
    
    print("\n正在发送测试消息...")
    response = chatbot.chat("你好，请用一句话介绍你自己。")
    
    print("\n" + "=" * 50)
    print("DeepSeek 回复:")
    print("=" * 50)
    print(response)
    print("\n" + "=" * 50)
    print("✅ DeepSeek API 测试成功！")
    print("=" * 50)
    
except Exception as e:
    print(f"\n❌ 错误: {e}")
    print("\n请检查:")
    print("1. API Key 是否正确")
    print("2. 网络连接是否正常")
    print("3. DeepSeek API 服务是否可用")
