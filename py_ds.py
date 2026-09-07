from openai import OpenAI

# 配置 API 信息
API_KEY = "sk-1d54b35405d64478b12cf7b3bbf7fe49"  # 替换为你的 API Key
BASE_URL = "https://api.deepseek.com"

# 初始化 OpenAI 客户端
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# 初始化对话历史
conversation_history = []

def chat_with_deepseek(user_input):
    """
    调用 DeepSeek API 进行对话。
    :param user_input: 用户输入的消息
    :return: 模型返回的回复
    """
    global conversation_history

    # 将用户输入添加到对话历史中
    conversation_history.append({"role": "user", "content": user_input})

    try:
        # 调用 DeepSeek API
        response = client.chat.completions.create(
            model="deepseek-chat",  # 使用 DeepSeek-V3 模型
            messages=conversation_history,
            stream=False  # 非流式输出
        )

        # 提取模型回复
        assistant_reply = response.choices[0].message.content

        # 将模型回复添加到对话历史中
        conversation_history.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply

    except Exception as e:
        print(f"请求失败: {e}")
        return None

def main():
    print("欢迎使用 DeepSeek 聊天机器人！输入 'exit' 退出程序。")
    while True:
        # 获取用户输入
        user_input = input("\n你: ")
        if user_input.lower() == "exit":
            print("再见！")
            break

        # 调用 API 并获取回复
        reply = chat_with_deepseek(user_input)
        if reply:
            print(f"DeepSeek: {reply}")

if __name__ == "__main__":
    main()