import PyInstaller.__main__
import os
import shutil
import streamlit

def build():
    # 清理旧的构建文件
    if os.path.exists('build'):
        try:
            shutil.rmtree('build')
        except:
            print("无法清理 build 目录，可能是正在使用中。")
    if os.path.exists('dist'):
        try:
            shutil.rmtree('dist')
        except:
            print("无法清理 dist 目录，可能是正在使用中。")

    # 获取 streamlit 安装路径
    streamlit_path = os.path.dirname(streamlit.__file__)
    static_path = os.path.join(streamlit_path, "static")
    print(f"Streamlit path: {streamlit_path}")
    print(f"Static path: {static_path}")

    # 定义打包参数
    args = [
        'run_app.py',               # 入口脚本
        '--name=代码提取工具',        # 生成的 exe 名称
        '--onedir',                 # 生成文件夹模式（比 onefile 快得多）
        '--clean',                  # 清理临时文件
        # '--noconsole',              # 运行时不显示控制台窗口
        
        # 添加主程序文件
        '--add-data=app.py;.',
        '--add-data=CodeToDocx.py;.',
        f'--add-data={static_path};streamlit/static',
        
        # 收集元数据 (Streamlit 运行必须)
        '--copy-metadata=streamlit',
        '--copy-metadata=packaging',
        '--collect-all=streamlit',
        
        # 排除不需要的大型库以极大加快打包速度
        '--exclude-module=matplotlib',
        '--exclude-module=bokeh',
        '--exclude-module=pydeck',
        '--exclude-module=altair',
        '--exclude-module=sklearn',
        '--exclude-module=scipy',
        '--exclude-module=notebook',
        '--exclude-module=jupyter',
        '--exclude-module=jupyter_client',
        '--exclude-module=ipykernel',
        '--exclude-module=ipython',
        # '--exclude-module=pandas',   # Streamlit 可能依赖
        # '--exclude-module=numpy',    # Streamlit 可能依赖
        # '--exclude-module=pyarrow',  # Streamlit 可能依赖
        # '--exclude-module=PIL',      # Streamlit 可能依赖
        
        # 确保包含必要的隐藏导入
        '--hidden-import=streamlit',
        '--hidden-import=streamlit.web.cli',
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.filedialog',
        '--hidden-import=docx',
        '--hidden-import=pywin32_ctypes',
    ]
    
    # 执行打包
    print("开始打包... (这可能需要几分钟，请耐心等待)")
    PyInstaller.__main__.run(args)
    print("打包完成！请查看 dist 目录。")

if __name__ == "__main__":
    build()
