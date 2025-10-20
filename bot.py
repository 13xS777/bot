import discord
from discord.ext import commands
from deep_translator import GoogleTranslator
import os

# 创建机器人实例
bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())
bot.intents.message_content = True

# 目标语言列表
target_languages = ['zh-cn', 'ja', 'ko', 'th']

@bot.event
async def on_ready():
    print(f'机器人已登录：{bot.user}')

@bot.event
async def on_message(message):
    # 忽略机器人自己的消息
    if message.author == bot.user:
        return

    # 翻译消息
    original_text = message.content
    if not original_text.strip():  # 检查空消息
        await bot.process_commands(message)
        return

    translations = []
    for lang in target_languages:
        try:
            translated = GoogleTranslator(source='auto', target=lang).translate(original_text)
            translations.append(f"[{lang.upper()}]: {translated}")
        except Exception as e:
            translations.append(f"[{lang.upper()}]: 翻译失败 ({str(e)})")

    # 发送翻译结果
    if translations:
        reply = "\n".join(translations)
        await message.channel.send(reply)

    # 继续处理命令
    await bot.process_commands(message)

# 从环境变量获取 token
bot.run(os.getenv('DISCORD_BOT_TOKEN'))
