import discord
from discord.ext import commands
from deep_translator import GoogleTranslator
import os
from flask import Flask
import threading
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# Flask 服务器（防止 Render 休眠）
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Discord 机器人
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
target_languages = ['zh-cn', 'ja', 'ko', 'th']

@bot.event
async def on_ready():
    logger.info(f'机器人已登录：{bot.user}')

@bot.event
async def on_message(message):
    # 忽略机器人自己的消息
    if message.author == bot.user:
        return

    # 获取消息内容
    original_text = message.content.strip()
    if not original_text:
        logger.info("收到空消息，跳过翻译")
        await bot.process_commands(message)
        return

    logger.info(f"收到消息：{original_text}")

    # 翻译消息
    translations = []
    for lang in target_languages:
        try:
            translated = GoogleTranslator(source='auto', target=lang).translate(original_text)
            if translated:
                translations.append(f"[{lang.upper()}]: {translated}")
                logger.info(f"翻译到 {lang}: {translated}")
            else:
                translations.append(f"[{lang.upper()}]: 翻译为空")
                logger.warning(f"翻译到 {lang} 返回空结果")
        except Exception as e:
            translations.append(f"[{lang.upper()}]: 翻译失败 ({str(e)})")
            logger.error(f"翻译到 {lang} 失败: {str(e)}")

    # 分段发送消息（避免超过 2000 字符限制）
    if translations:
        reply = "\n".join(translations)
        logger.info(f"总回复长度：{len(reply)} 字符")
        if len(reply) <= 2000:
            await message.channel.send(reply)
        else:
            # 分段发送
            current_message = ""
            for line in translations:
                if len(current_message) + len(line) + 1 <= 2000:
                    current_message += line + "\n"
                else:
                    if current_message:
                        await message.channel.send(current_message.strip())
                        logger.info(f"发送分段消息：{len(current_message)} 字符")
                        current_message = line + "\n"
            if current_message:
                await message.channel.send(current_message.strip())
                logger.info(f"发送最后分段消息：{len(current_message)} 字符")

    # 继续处理命令
    await bot.process_commands(message)

# 启动 Flask 和 Discord 机器人
threading.Thread(target=run_flask, daemon=True).start()
bot.run(os.getenv('DISCORD_BOT_TOKEN'))
