# WeChat Bot

这是一个简单的微信机器人，使用 wxpy 库和 Azure OpenAI API 来实现自动回复，并集成了自定义功能。

## 安装

首先，克隆此仓库并进入项目目录：

```bash
git clone https://github.com/jiayx01/chat_bot.git
cd wechat-bot
```


## 安装

### 克隆仓库

首先，克隆此仓库并进入项目目录：

```bash
git clone https://github.com/yourusername/wechat-bot.git
cd wechat-bot
```
## 使用
### 配置
在 main.py 文件中，替换以下部分中的 your_tuling_api_key 为您申请的图灵机器人 API Key。
```bash
tuling = Tuling(api_key='your_tuling_api_key')
```
### 运行微信机器人
```bash
python main.py
```
