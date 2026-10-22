import os
from flask import Flask, request, jsonify
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

app = Flask(__name__)

# ================= 1. 读取本地员工手册 =================
print("正在加载本地员工手册...")
loader = TextLoader("employee_handbook.txt", encoding="utf-8")
docs = loader.load()

# 把长长的员工手册切成小段
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
splits = text_splitter.split_documents(docs)

@tool
def search_handbook(query: str) -> str:
    """当用户询问考勤、报销、请假、福利等公司规章制度时，使用此工具检索员工手册。"""
    results = []
    # 简单的关键词匹配：如果问题里的词和文档里的词对上了，就返回那段文本
    for doc in splits:
        # 为了让匹配更准一点，我们把问题拆成单个字去匹配（虽然粗糙，但对中文管用）
        if any(char in doc.page_content for char in query if char.strip()):
            results.append(doc.page_content)
    
    if not results:
        return "未在员工手册中找到相关规定，请咨询 HR。"
    
    # 去重后拼接返回
    return "\n---\n".join(set(results))

# ================= 2. 初始化 Agent =================
model = ChatOpenAI(
    model="glm-4-flash",
    api_key=os.environ.get("ZHIPU_API_KEY", "你的Key填在这里"), 
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)

agent = create_agent(
    model=model,
    tools=[search_handbook],
    system_prompt="你是一个专业的人力资源助手。请严格根据 search_handbook 工具检索到的内容回答员工的问题。如果查不到，就直说不知道。"
)

# ================= 3. 编写 Flask 路由 =================
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({"error": "请输入内容"}), 400

    print(f"员工提问: {user_message}")
    
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": user_message}]
        })
        reply = result["messages"][-1].content
        return jsonify({"reply": reply})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)