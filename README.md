# Sidekick Personal Co-Worker

Sidekick 是一个基于 LangChain 和 Gradio 构建的智能助手应用，它能够通过自然语言与用户交互，并使用各种工具来完成任务。

## 功能特点

- 🤖 基于 GPT-4 的智能对话
- 🌐 网页浏览和搜索能力
- 📚 维基百科查询
- 📝 文件管理
- 🔔 推送通知
- 🐍 Python 代码执行
- 📊 任务评估和反馈

## 环境要求

- Python 3.12+
- uv 包管理器
- Playwright 浏览器

## 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/Sidekick-Personal-Co-worker.git
cd Sidekick-Personal-Co-worker
```

2. 创建并激活虚拟环境：
```bash
uv venv
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
uv pip install -r requirements.txt
```

4. 安装 Playwright 浏览器：
```bash
playwright install
```

5. 配置环境变量：
创建 `.env` 文件并添加以下内容：
```
SERPER_API_KEY=你的serper_api_key
PUSHOVER_TOKEN=你的pushover_token
PUSHOVER_USER=你的pushover_user
OPENAI_API_KEY=你的openai_api_key
```

## 使用方法

1. 启动应用：
```bash
python app.py
```

2. 在浏览器中访问：
应用会自动在浏览器中打开，默认地址为 http://127.0.0.1:7860

3. 使用界面：
   - 在输入框中输入您的问题或任务
   - 在成功标准框中输入您期望的结果
   - 点击 "Go!" 按钮或按回车键提交
   - 使用 "Reset" 按钮重置对话

## 项目结构

```
Sidekick-Personal-Co-worker/
├── app.py              # Gradio 界面和主应用
├── sidekick.py         # Sidekick 核心逻辑
├── sidekick_tools.py   # 工具集实现
├── requirements.txt    # 项目依赖
└── .env               # 环境变量配置
```

## 工具集

Sidekick 集成了多种工具：
- 网页浏览和搜索
- 维基百科查询
- 文件管理
- 推送通知
- Python 代码执行

## 注意事项

- 确保所有必要的 API 密钥都已正确配置
- 保持 `.env` 文件的安全性，不要将其提交到版本控制系统
- 在使用文件管理功能时，文件会保存在 `sandbox` 目录中

