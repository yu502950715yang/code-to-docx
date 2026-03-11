import sys
import os
import tkinter as tk
from tkinter import filedialog
import streamlit
import streamlit.web.cli as stcli
import webbrowser
import threading
import time

def resolve_path(path):
    if getattr(sys, "frozen", False):
        basedir = sys._MEIPASS
    else:
        basedir = os.path.dirname(__file__)
    return os.path.join(basedir, path)

def open_browser():
    # 等待服务器启动
    time.sleep(5)
    webbrowser.open("http://localhost:8501")

if __name__ == "__main__":
    app_path = resolve_path("app.py")
    
    # 在后台线程中打开浏览器
    threading.Thread(target=open_browser, daemon=True).start()
    
    # 模拟命令行参数
    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--global.developmentMode=false",
        "--server.headless=true",
        "--browser.gatherUsageStats=false",
        "--server.enableCORS=false",
        "--server.enableXsrfProtection=false",
        "--server.port=8501",
    ]
    
    sys.exit(stcli.main())
