import streamlit as st
from chatbot import CustomerServiceChatbot
import os
from datetime import datetime
from dotenv import load_dotenv
import glob
import json
import html
import markdown

load_dotenv()

CONVERSATIONS_DIR = "conversations"
if not os.path.exists(CONVERSATIONS_DIR):
    os.makedirs(CONVERSATIONS_DIR)


st.set_page_config(
    page_title="智能客服机器人",
    page_icon="💬",
    layout="wide"
)

# 隐藏 Streamlit 默认的菜单和 Deploy 按钮，添加气泡样式
custom_style = """
<style>
/* 基础设置 */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display: none;}

/* 全局字体 */
html, body, [class*="css"] {
    font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
}

/* 消息行容器 */
.message-row {
    display: flex;
    margin-bottom: 24px;
    align-items: flex-start;
    animation: fadeIn 0.4s ease-out;
}

.message-row.user {
    flex-direction: row-reverse;
}

.message-row.assistant {
    flex-direction: row;
}

/* 头像样式 */
.avatar {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    flex-shrink: 0;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    transition: transform 0.2s;
}

.avatar:hover {
    transform: scale(1.05);
}

.avatar.user {
    background: #95ec69;
    color: white;
    margin-left: 16px;
    border: none;
}

.avatar.assistant {
    background: #ffffff;
    color: #4a5568;
    margin-right: 16px;
    border: 1px solid #e2e8f0;
}

/* 消息内容容器 */
.message-content {
    max-width: 75%;
    display: flex;
    flex-direction: column;
}

/* 消息标签（名字） */
.message-label {
    font-size: 13px;
    color: #718096;
    margin-bottom: 6px;
    font-weight: 500;
}

.message-row.user .message-label {
    text-align: right;
    margin-right: 4px;
}

.message-row.assistant .message-label {
    text-align: left;
    margin-left: 4px;
}

/* 气泡样式 */
.message-bubble {
    padding: 14px 18px;
    border-radius: 16px;
    position: relative;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    line-height: 1.6;
    font-size: 15px;
    overflow-wrap: break-word;
}

.message-bubble.user {
    background: #95ec69;
    color: #000000;
    border-top-right-radius: 2px;
}

.message-bubble.assistant {
    background: #ffffff;
    color: #2d3748;
    border-top-left-radius: 2px;
    border: 1px solid #edf2f7;
}

/* Markdown 内容样式优化 */
.message-bubble.assistant p {
    margin: 0 0 10px 0;
}

.message-bubble.assistant p:last-child {
    margin-bottom: 0;
}

.message-bubble.assistant pre {
    background: #f7fafc !important;
    border-radius: 8px !important;
    border: 1px solid #e2e8f0 !important;
    margin: 10px 0 !important;
    padding: 12px !important;
}

.message-bubble.assistant code {
    font-family: 'JetBrains Mono', Consolas, monospace !important;
    font-size: 13px !important;
    background: rgba(0,0,0,0.05);
    padding: 2px 4px;
    border-radius: 4px;
}

.message-bubble.assistant pre code {
    background: transparent;
    padding: 0;
}

/* 动画定义 */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
"""
st.markdown(custom_style, unsafe_allow_html=True)


def init_session_state():
    if 'chatbot' not in st.session_state:
        openai_key = os.getenv("OPENAI_API_KEY")
        deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        
        if openai_key:
            try:
                st.session_state.chatbot = CustomerServiceChatbot(
                    api_key=openai_key, 
                    provider="openai",
                    model="gpt-3.5-turbo"
                )
                st.session_state.messages = []
                st.session_state.api_key_valid = True
                st.session_state.provider = "openai"
            except Exception as e:
                st.session_state.api_key_valid = False
                st.session_state.error_message = str(e)
        elif deepseek_key:
            try:
                st.session_state.chatbot = CustomerServiceChatbot(
                    api_key=deepseek_key,
                    provider="deepseek",
                    model="deepseek-chat"
                )
                st.session_state.messages = []
                st.session_state.api_key_valid = True
                st.session_state.provider = "deepseek"
            except Exception as e:
                st.session_state.api_key_valid = False
                st.session_state.error_message = str(e)
        else:
            st.session_state.api_key_valid = False
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'provider' not in st.session_state:
        st.session_state.provider = None


def main():
    init_session_state()
    
    st.title("智能客服机器人")
    st.markdown("基于 ChatGPT/DeepSeek 的多轮对话客服系统")
    
    with st.sidebar:
        st.header("设置")
        
        if not st.session_state.get('api_key_valid', False):
            st.warning("请配置 API Key")
            
            provider_choice = st.radio(
                "选择 API 提供商",
                ["OpenAI", "DeepSeek"],
                help="选择要使用的 API 提供商"
            )
            
            api_key_input = st.text_input(
                f"{provider_choice} API Key",
                type="password",
                help=f"请输入您的 {provider_choice} API Key"
            )
            
            if st.button("保存 API Key"):
                if api_key_input:
                    try:
                        provider = provider_choice.lower()
                        model = "gpt-3.5-turbo" if provider == "openai" else "deepseek-chat"
                        st.session_state.chatbot = CustomerServiceChatbot(
                            api_key=api_key_input,
                            provider=provider,
                            model=model
                        )
                        st.session_state.messages = []
                        st.session_state.api_key_valid = True
                        st.session_state.provider = provider
                        st.success("API Key 已保存")
                        st.rerun()
                    except Exception as e:
                        st.error(f"错误: {str(e)}")
                else:
                    st.error("请输入 API Key")
        else:
            provider_display = st.session_state.get('provider', 'unknown').upper()
            st.success(f"API Key 已配置 ({provider_display})")
        
        st.divider()
        
        if st.session_state.get('api_key_valid', False):
            current_provider = st.session_state.get('provider', 'openai')
            
            if current_provider == "openai":
                model_options = ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"]
                default_model = "gpt-3.5-turbo"
            else:
                model_options = ["deepseek-chat", "deepseek-coder"]
                default_model = "deepseek-chat"
            
            current_model = st.session_state.chatbot.model if hasattr(st.session_state.chatbot, 'model') else default_model
            model_index = model_options.index(current_model) if current_model in model_options else 0
            
            model_choice = st.selectbox(
                "选择模型",
                model_options,
                index=model_index,
                help=f"选择要使用的 {current_provider.upper()} 模型"
            )
        
        if st.session_state.get('api_key_valid', False):
            st.session_state.chatbot.model = model_choice
        
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("重置对话", use_container_width=True):
                if st.session_state.get('api_key_valid', False):
                    st.session_state.chatbot.reset_conversation()
                    st.session_state.messages = []
                    st.success("对话已重置")
                    st.rerun()
        
        with col2:
            if st.button("保存对话", use_container_width=True):
                if st.session_state.get('api_key_valid', False) and st.session_state.messages:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = os.path.join(CONVERSATIONS_DIR, f"conversation_{timestamp}.json")
                    st.session_state.chatbot.save_conversation(filename)
                    st.success(f"对话已保存")
        
        st.divider()
        
        with st.expander("历史对话"):
            if st.session_state.get('api_key_valid', False):
                conversation_files = sorted(glob.glob(os.path.join(CONVERSATIONS_DIR, "conversation_*.json")), reverse=True)
                
                if conversation_files:
                    st.markdown(f"共 {len(conversation_files)} 条历史记录")
                    
                    for conv_file in conversation_files[:10]:
                        filename = os.path.basename(conv_file)
                        timestamp_str = filename.replace("conversation_", "").replace(".json", "")
                        try:
                            dt = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                            display_name = dt.strftime("%Y-%m-%d %H:%M:%S")
                        except:
                            display_name = timestamp_str
                        
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            if st.button(display_name, key=f"load_{filename}", use_container_width=True):
                                try:
                                    st.session_state.chatbot.load_conversation(conv_file)
                                    with open(conv_file, 'r', encoding='utf-8') as f:
                                        history = json.load(f)
                                    st.session_state.messages = [msg for msg in history if msg["role"] != "system"]
                                    st.success(f"已加载对话")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"加载失败: {str(e)}")
                        with col2:
                            if st.button("删除", key=f"del_{filename}"):
                                try:
                                    os.remove(conv_file)
                                    st.success("已删除")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"删除失败: {str(e)}")
                else:
                    st.info("暂无历史对话")
            else:
                st.info("请先配置 API Key")
        
        with st.expander("自定义系统提示词"):
            custom_prompt = st.text_area(
                "系统提示词",
                value=st.session_state.chatbot.system_prompt if st.session_state.get('api_key_valid', False) else "",
                height=150,
                help="自定义客服机器人的行为和角色"
            )
            
            if st.button("应用提示词"):
                if st.session_state.get('api_key_valid', False):
                    st.session_state.chatbot.set_system_prompt(custom_prompt)
                    st.success("提示词已更新")
        
        st.divider()
        
        st.markdown("### 对话统计")
        if st.session_state.get('api_key_valid', False):
            msg_count = len(st.session_state.messages)
            st.metric("消息数量", msg_count)
    
    if not st.session_state.get('api_key_valid', False):
        st.info("请在侧边栏配置 API Key 以开始使用")
        
        st.markdown("""
        ### 使用说明
        
        1. 在左侧边栏选择 API 提供商并输入 API Key
        2. 配置完成后，在下方输入框中输入您的问题
        3. 系统会记住对话历史，支持上下文理解
        4. 可以随时保存对话记录或加载历史对话
        
        ### 功能特点
        
        - 支持 OpenAI 和 DeepSeek 双 API
        - 支持多轮对话，记忆上下文
        - 可自定义系统提示词
        - 支持多种模型选择
        - 对话历史保存和加载
        - 简洁的 Web 界面
        
        ### 获取 API Key
        
        - OpenAI: 访问 [OpenAI Platform](https://platform.openai.com/api-keys)
        - DeepSeek: 访问 [DeepSeek Platform](https://platform.deepseek.com/api_keys)
        """)
        return
    
    # 显示对话历史
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            label = "您"
            avatar = """
            <svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" class="css-i6hzaj">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
            </svg>
            """
            # 用户消息：转义HTML
            escaped_content = html.escape(content).replace('\n', '<br>')
            
            st.markdown(f'''
            <div class="message-row user">
                <div class="avatar user">{avatar}</div>
                <div class="message-content">
                    <div class="message-label">{label}</div>
                    <div class="message-bubble user">{escaped_content}</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        else:
            label = "AI助手"
            avatar = """
            <svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" class="css-i6hzaj">
                <path d="M12 2a2 2 0 0 1 2 2v2a2 2 0 0 1-2 2 2 2 0 0 1-2-2V4a2 2 0 0 1 2-2z"></path>
                <path d="M12 16a2 2 0 0 1 2 2v2a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-2a2 2 0 0 1 2-2z"></path>
                <line x1="12" y1="8" x2="12" y2="16"></line>
                <path d="M20 12a8 8 0 1 1-16 0"></path>
            </svg>
            """
            # AI消息：渲染Markdown
            md_content = markdown.markdown(content, extensions=['tables', 'fenced_code', 'codehilite'])
            
            st.markdown(f'''
            <div class="message-row assistant">
                <div class="avatar assistant">{avatar}</div>
                <div class="message-content">
                    <div class="message-label">{label}</div>
                    <div class="message-bubble assistant">{md_content}</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    if prompt := st.chat_input("请输入您的问题..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.spinner("思考中..."):
            response = st.session_state.chatbot.chat(prompt)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()


if __name__ == "__main__":
    main()
