from wxpy import Bot, Message
import requests
import json
import sqlite3
from openai.lib.azure import AzureOpenAI
import trafilatura

# 初始化微信机器人，扫码登录
bot = Bot()

# 初始化 Azure OpenAI 客户端
client = AzureOpenAI(
    azure_endpoint="https://onewo-sweden-central.openai.azure.com",
    api_key="",
    api_version="2024-02-01"
)

# 数据库连接
conn = sqlite3.connect("gpt-35-turbo-instruct.db")
cursor = conn.cursor()


# 工具函数
def web_crawl(url: str) -> str:
    downloaded = trafilatura.fetch_url(url)
    return trafilatura.extract(downloaded)


def get_city_code(arguments: dict) -> str:
    code_map = {
        "深圳市": "440300",
        "广州市": "440100",
        "北京市": "110000",
    }
    return code_map.get(arguments["city"])


def get_weather(arguments: dict) -> str:
    response = requests.get("https://restapi.amap.com/v3/weather/weatherInfo",
                            params={"key": "",
                                    "city": arguments["adcode"]})
    return response.text


tool_map = {
    "get_city_code": get_city_code,
    "get_weather": get_weather,
}


def chat(prompt: str) -> str:
    # 获取聊天历史记录
    cursor.execute("""
        SELECT id AS chat_id FROM chat WHERE name = 'gpt-35-turbo-instruct' ORDER BY id DESC LIMIT 1
    """)
    row = cursor.fetchone()
    chat_id = row[0] if row else None

    messages = [{"role": "user", "content": prompt}]

    while True:
        completions = client.chat.completions.create(
            model="gpt-35-turbo-instruct",
            messages=messages,
            tools=[
                {"name": "get_city_code", "function": get_city_code},
                {"name": "get_weather", "function": get_weather},
            ]
        )

        choice = completions.choices[0]
        if choice.finish_reason == "tool_calls":
            messages.append(choice.message)
            for tc in choice.message.tool_calls:
                tool = tool_map.get(tc.function.name)
                if tool:
                    arguments = json.loads(tc.function.arguments)
                    content = tool(arguments)
                    messages.append({
                        "role": "tool",
                        "content": json.dumps({"content": content}, ensure_ascii=False),
                        "tool_call_id": tc.id,
                    })
        elif choice.finish_reason == "stop":
            break

    return choice.message.content


@bot.register()
def reply_message(msg: Message):
    reply = chat(msg.text)
    msg.reply(reply)


# 保持机器人在线
bot.join()
