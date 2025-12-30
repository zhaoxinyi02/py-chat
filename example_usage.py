from chatbot import CustomerServiceChatbot
import os


def example_basic_usage():
    print("=== 示例 1: 基础使用 ===\n")
    
    chatbot = CustomerServiceChatbot()
    
    response1 = chatbot.chat("你好，我想了解你们的产品")
    print(f"用户: 你好，我想了解你们的产品")
    print(f"客服: {response1}\n")
    
    response2 = chatbot.chat("价格是多少？")
    print(f"用户: 价格是多少？")
    print(f"客服: {response2}\n")


def example_custom_prompt():
    print("=== 示例 2: 自定义系统提示词 ===\n")
    
    chatbot = CustomerServiceChatbot()
    
    custom_prompt = """你是一个专业的技术支持工程师，
专门帮助用户解决软件使用问题。
请用专业但易懂的语言回答，必要时提供步骤说明。"""
    
    chatbot.set_system_prompt(custom_prompt)
    
    response = chatbot.chat("我的软件无法启动，怎么办？")
    print(f"用户: 我的软件无法启动，怎么办？")
    print(f"技术支持: {response}\n")


def example_conversation_management():
    print("=== 示例 3: 对话管理 ===\n")
    
    chatbot = CustomerServiceChatbot()
    
    chatbot.chat("我叫张三")
    chatbot.chat("我想买一台笔记本电脑")
    
    history = chatbot.get_conversation_history()
    print(f"当前对话轮数: {len(history)}\n")
    
    filename = chatbot.save_conversation("example_conversation.json")
    print(f"对话已保存到: {filename}\n")
    
    chatbot.reset_conversation()
    print("对话已重置\n")
    
    chatbot.load_conversation("example_conversation.json")
    print("对话已加载\n")
    
    response = chatbot.chat("你还记得我的名字吗？")
    print(f"用户: 你还记得我的名字吗？")
    print(f"客服: {response}\n")


def example_multi_turn_context():
    print("=== 示例 4: 多轮对话上下文 ===\n")
    
    chatbot = CustomerServiceChatbot()
    
    questions = [
        "我想买一部手机",
        "预算在3000-5000元",
        "主要用来拍照",
        "有什么推荐吗？",
        "第一个的详细参数是什么？"
    ]
    
    for question in questions:
        response = chatbot.chat(question)
        print(f"用户: {question}")
        print(f"客服: {response}\n")


def example_error_handling():
    print("=== 示例 5: 错误处理 ===\n")
    
    try:
        chatbot = CustomerServiceChatbot(api_key="invalid_key")
    except ValueError as e:
        print(f"捕获到错误: {e}\n")
    
    if os.getenv("OPENAI_API_KEY"):
        chatbot = CustomerServiceChatbot()
        print("API Key 验证成功\n")


if __name__ == "__main__":
    print("=" * 60)
    print("智能客服机器人 - 使用示例")
    print("=" * 60)
    print()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  警告: 未设置 OPENAI_API_KEY 环境变量")
        print("请先设置 API Key 才能运行示例\n")
        print("设置方法:")
        print("  Windows: set OPENAI_API_KEY=your_key")
        print("  Linux/Mac: export OPENAI_API_KEY=your_key")
        print()
    else:
        try:
            example_basic_usage()
            
            example_custom_prompt()
            
            example_conversation_management()
            
            example_multi_turn_context()
            
            example_error_handling()
            
        except Exception as e:
            print(f"运行示例时出错: {e}")
    
    print("=" * 60)
    print("示例运行完成")
    print("=" * 60)
