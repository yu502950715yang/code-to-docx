import streamlit as st
import os
import tkinter as tk
from tkinter import filedialog
from CodeToDocx import generate_docx, DEFAULT_PROJECT_NAME, DEFAULT_VERSION, DEFAULT_SOURCE_CONFIGS
import time

st.set_page_config(page_title="代码提取工具 - 软著申请材料生成", layout="wide")

# CSS to align buttons with input fields (skipping the label height)
st.markdown("""
    <style>
    .align-button-with-label {
        margin-top: 28px;
    }
    </style>
    """, unsafe_allow_html=True)

# Helper function to open directory dialog
def select_folder(key):
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    folder_selected = filedialog.askdirectory(master=root)
    root.destroy()
    if folder_selected:
        st.session_state[f"path_{key}"] = folder_selected

st.title("📄 代码提取工具")
st.markdown("快速生成软件著作权申请所需的程序鉴别材料（源代码文档）。")

# Sidebar for global settings
with st.sidebar:
    st.header("项目信息")
    project_name = st.text_input("项目名称", DEFAULT_PROJECT_NAME)
    version = st.text_input("版本号", DEFAULT_VERSION)
    
    st.header("生成设置")
    max_pages = st.number_input("目标页数", min_value=1, max_value=200, value=60)
    mode = st.selectbox("生成模式", ["start_end", "sequential"], 
                        format_func=lambda x: "前后各半 (start_end)" if x == "start_end" else "连续读取 (sequential)")
    
    # 输出目录选择
    if "path_output" not in st.session_state:
        st.session_state["path_output"] = os.getcwd()

    col_out1, col_out2 = st.columns([4, 1])
    with col_out1:
        # 使用 key="path_output" 绑定，但不直接使用 st.session_state["path_output"] 作为 value 参数，
        # 因为当 key 存在时，value 参数只在首次渲染有效。
        # 但我们需要处理用户手动修改输入框的情况，以及点击按钮更新的情况。
        # 如果 text_input 有 key，它的值会自动同步到 session_state[key]。
        # 如果外部代码更新了 session_state[key] 并 rerun，输入框会显示新值。
        output_dir = st.text_input("输出目录", key="path_output")
    with col_out2:
        st.markdown('<div class="align-button-with-label"></div>', unsafe_allow_html=True)
        st.button("📁", key="btn_output_dir", help="选择输出文件夹", on_click=select_folder, args=("output",))

    output_filename = f"《{project_name}{version}》程序鉴别材料.docx"
    output_path = os.path.join(output_dir, output_filename)

# Main area for source configurations
st.header("🔍 源码配置")
st.info("配置需要扫描的源代码目录和文件类型。")

if 'source_configs' not in st.session_state:
    st.session_state.source_configs = [c.copy() for c in DEFAULT_SOURCE_CONFIGS]

# Initialize paths in session state if not already present
for i, config in enumerate(st.session_state.source_configs):
    key = f"path_{i}"
    if key not in st.session_state:
        st.session_state[key] = config['path']

# Display and edit source configs
updated_configs = []
to_delete = []

for i, config in enumerate(st.session_state.source_configs):
    with st.expander(f"配置项 {i+1}: {config['name']}", expanded=True):
        # 4-column layout for better alignment
        col1, col2, col3, col4 = st.columns([2, 4, 1.5, 0.5])
        
        with col1:
            name = st.text_input(f"名称", config['name'], key=f"name_input_{i}")
        
        with col2:
            path = st.text_input(f"源码路径", key=f"path_{i}")
            
        with col3:
            # Spacer for label height
            st.markdown('<div class="align-button-with-label"></div>', unsafe_allow_html=True)
            st.button(f"📁 选择文件夹", key=f"btn_{i}", use_container_width=True, on_click=select_folder, args=(i,))
                
        with col4:
            # Spacer for label height
            st.markdown('<div class="align-button-with-label"></div>', unsafe_allow_html=True)
            if st.button("🗑️", key=f"del_{i}", use_container_width=True):
                to_delete.append(i)
        
        ext_str = st.text_input(f"文件后缀 (逗号分隔)", ",".join(config['extensions']), key=f"ext_{i}")
        extensions = [e.strip() for e in ext_str.split(",") if e.strip()]
        
        updated_configs.append({
            "name": name,
            "path": st.session_state[f"path_{i}"],
            "extensions": extensions
        })

# Remove items marked for deletion
if to_delete:
    for index in sorted(to_delete, reverse=True):
        st.session_state.source_configs.pop(index)
        # Clean up path session state by shifting remaining ones
        # Actually it's better to just clear all path_ keys and re-initialize them
        # to avoid mismatch if we delete from the middle.
        for j in range(index, len(st.session_state.source_configs) + 1):
            key = f"path_{j}"
            next_key = f"path_{j+1}"
            if next_key in st.session_state:
                st.session_state[key] = st.session_state[next_key]
            elif key in st.session_state:
                del st.session_state[key]
    st.rerun()

if st.button("➕ 添加新源码目录"):
    new_idx = len(st.session_state.source_configs)
    st.session_state.source_configs.append({"name": "新项目", "path": "", "extensions": [".java"]})
    st.session_state[f"path_{new_idx}"] = ""
    st.rerun()

if st.button("🗑️ 清空所有配置"):
    st.session_state.source_configs = []
    # Clear path related session state
    for key in list(st.session_state.keys()):
        if key.startswith("path_"):
            del st.session_state[key]
    st.rerun()

st.session_state.source_configs = updated_configs

# Execution section
st.divider()
if st.button("🚀 开始生成文档", type="primary", use_container_width=True):
    if not updated_configs:
        st.error("请至少添加一个源码配置项！")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        def update_progress(text, progress):
            status_text.text(text)
            progress_bar.progress(progress)

        try:
            start_time = time.time()
            result_path = generate_docx(
                max_pages=max_pages,
                mode=mode,
                project_name=project_name,
                version=version,
                output_file=output_path,
                source_configs=updated_configs,
                progress_callback=update_progress
            )
            end_time = time.time()
            
            st.success(f"✅ 生成成功！耗时 {end_time - start_time:.2f} 秒")
            st.info(f"文件保存路径: `{result_path}`")
            
            with open(result_path, "rb") as f:
                st.download_button(
                    label="📥 点击下载生成的文档",
                    data=f,
                    file_name=output_filename,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
        except Exception as e:
            st.error(f"❌ 生成过程中发生错误: {str(e)}")
            st.exception(e)

st.markdown("---")
st.caption("Built with Streamlit & python-docx")
