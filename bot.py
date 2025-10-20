import discord
from discord.ext import commands
from googletrans import Translator
import os

# 创建机器人实例
bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())
bot.intents.message_content = True

# 初始化翻译器
translator = Translator()

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

    # 检测原消息语言
    original_text = message.content
    detected_lang = translator.detect(original_text).lang

    # 如果消息是纯英文或其他不支持的语言，跳过
    if detected_lang not in ['zh-cn', 'ja', 'ko', 'th']:
        await bot.process_commands(message)
        return

    # 为每个目标语言生成翻译（除了原语言）
    translations = []
    for lang in target_languages:
        if lang != detected_lang:  # 不翻译回原语言
            translated = translator.translate(original_text, dest=lang).text
            translations.append(f"[{lang.upper()}]: {translated}")

    # 如果有翻译，发送到频道
    if translations:
        reply = "\n".join(translations)
        await message.channel.send(reply)

    # 继续处理命令
    await bot.process_commands(message)

# 从环境变量获取token
bot.run(os.getenv('DISCORD_BOT_TOKEN'))
