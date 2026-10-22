# Flask-LangChain-Agent-Demo

基于 Flask + LangChain + 智谱大模型（GLM-4-Flash）开发的本地知识库（RAG）问答后端接口。

## 🌟 项目功能
- 将本地 txt 文件（如员工手册）切分并构建为本地知识库。
- 通过 LangChain 封装自定义 Tool，让大模型具备检索本地知识的能力。
- 提供标准的 Flask POST HTTP 接口，供前端或其他系统调用。
- 实现 RAG（检索增强生成），解决大模型无法回答私有数据的问题。

## 🛠️ 技术栈
- **Web 框架**: Flask
- **Agent 框架**: LangChain (v1.x)
- **大语言模型**: 智谱 GLM-4-Flash (免费)
- **文本处理**: LangChain Text Splitters

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install flask langchain langchain-openai langchain-community langchain-text-splitters
```

### 2. 设置智谱 API Key
去 [智谱开放平台](https://open.bigmodel.cn) 免费申请 API Key。

**Windows (CMD):**
```cmd
set ZHIPU_API_KEY=你的完整API_KEY
```

**Mac/Linux:**
```bash
export ZHIPU_API_KEY=你的完整API_KEY
```

### 3. 启动后端服务
```bash
python app.py
```
*服务启动后会运行在 `http://127.0.0.1:5000`*

## 📝 接口测试

使用 `curl` 发送 POST 请求进行测试：

```bash
curl -X POST http://127.0.0.1:5000/chat \
-H "Content-Type: application/json" \
-d "{\"message\": \"我们公司出差住宿标准是多少？\"}"
```

**返回示例:**
```json
{
  "reply": "根据公司规定，出差住宿标准如下：一线城市每晚不超过 600 元，二线城市不超过 400 元。"
}
```