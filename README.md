# 代码提取工具 (Code-to-Docx)

本项目是一个高效、易用的代码提取与文档生成工具，专门用于快速生成**软件著作权申请**所需的“程序鉴别材料”（即源代码 Word 文档）。

## 🌟 核心功能

- **自动化扫描**：支持多路径递归扫描，按需过滤文件扩展名（如 `.py`, `.java`, `.vue`, `.js`, `.cpp` 等）。
- **软著专用模式**：
  - **前后各半 (start_end)**：自动提取代码库的前 30 页和后 30 页，符合软著申请的典型要求。
  - **连续读取 (sequential)**：从头开始按顺序提取指定页数的代码。
- **专业格式排版**：
  - 自动生成**标题页**（项目名、版本号）。
  - **页眉页脚**：页眉显示项目信息，页脚自动生成居中页码。
  - **字体优化**：代码使用 `Consolas` (英文) 和 `宋体` (中文) 混合排版，五号字体，12磅行间距。
  - **行号支持**：可开启 Word 原生页面行号，支持每页重新编号。
- **智能防冲突**：保存文档时若文件已被打开，会自动创建副本保存，避免程序崩溃。
- **多端支持**：提供直观的 **Web UI 界面** 和灵活的 **命令行 (CLI)** 操作。

## 🛠️ 环境准备

确保您的计算机已安装 Python 3.8+。

安装项目所需的依赖库：

```bash
pip install -r requirements.txt
```

## 🚀 使用方法

### 方式一：Web UI 界面（推荐）

提供最直观的操作体验，支持文件夹选择器。

1.  在项目根目录下运行：
    ```bash
    streamlit run app.py
    ```
2.  浏览器将自动打开 `http://localhost:8501`。
3.  在界面中配置：
    - **项目信息**：名称、版本号。
    - **生成设置**：目标页数（默认 60 页）、提取模式、是否开启行号。
    - **源码配置**：点击 `➕ 添加新源码目录`，选择路径并设置过滤后缀。
4.  点击 `🚀 开始生成文档`，完成后可直接点击下载。

### 方式二：命令行 (CLI)

适合自动化脚本或高级用户。

```bash
# 基本用法：生成 60 页，使用前后截取模式，启用行号
python CodeToDocx.py --name "我的项目" --version "V1.0" --pages 60 --mode start_end --line-numbers
```

**可用参数：**
- `--pages`: 目标页数 (默认 60)
- `--mode`: 提取模式 `sequential` 或 `start_end` (默认 `start_end`)
- `--name`: 项目名称
- `--version`: 版本号
- `--line-numbers`: 启用页面行号
- `--output`: 指定输出文件路径

### 方式三：打包为独立可执行文件 (EXE)

如果您希望在没有 Python 环境的电脑上运行，可以将其打包：

1.  运行打包脚本：
    ```bash
    python build_exe.py
    ```
2.  打包完成后，在 `dist/代码提取工具/` 目录下找到 `代码提取工具.exe` 即可运行。

## 📂 项目结构

- [CodeToDocx.py](file:///e:/code/code-to-docx/CodeToDocx.py)：核心逻辑，负责代码收集与 Word 生成。
- [app.py](file:///e:/code/code-to-docx/app.py)：基于 Streamlit 的 Web 交互界面。
- [run_app.py](file:///e:/code/code-to-docx/run_app.py)：用于打包 EXE 的启动入口。
- [build_exe.py](file:///e:/code/code-to-docx/build_exe.py)：PyInstaller 打包脚本。
- [requirements.txt](file:///e:/code/code-to-docx/requirements.txt)：项目依赖列表。
- [verify_line_numbers.py](file:///e:/code/code-to-docx/verify_line_numbers.py)：辅助验证脚本。

---
*注：本项目生成的文档仅作为辅助材料，请在提交前仔细检查内容是否符合相关机构的具体要求。*
