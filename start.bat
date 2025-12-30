@echo off
chcp 65001 >nul
title 智能客服机器人启动器



:: 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到Python，请先安装Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/3] 检测到Python环境
python --version
echo.

:: 安装依赖
echo [2/3] 正在安装所需库...
echo.
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if %errorlevel% neq 0 (
    echo.
    echo [警告] 部分库安装失败，尝试使用默认源重新安装...
    pip install -r requirements.txt
)
echo.

:: 检查.env文件
if not exist .env (
    echo [提示] 未找到.env文件，请配置API Key
    echo 您可以在Web界面中配置，或者创建.env文件
    echo.
)

:: 启动应用
echo [3/3] 正在启动应用...
echo.
echo ========================================
echo  应用启动中，请稍候...
echo  浏览器将自动打开 http://localhost:8501
echo  按 Ctrl+C 可停止服务
echo ========================================
echo.

streamlit run app.py

:: 如果streamlit命令失败，尝试使用python -m streamlit
if %errorlevel% neq 0 (
    echo.
    echo [提示] 尝试使用备用启动方式...
    python -m streamlit run app.py
)

pause
