import discord
from discord.ext import commands
from googletrans import Translator

# 创建机器人实例，prefix是命令前缀（这里不用命令，所以随意）
bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())
bot.intents.message_content = True  # 启用消息内容读取

# 初始化翻译器
translator = Translator()

# 目标语言列表：中文('zh-cn')、日文('ja')、韩文('ko')、泰文('th')
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

    # 如果消息是纯英文或其他不支持的，就跳过（可选，根据需要调整）
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

    # 继续处理命令（如果有）
    await bot.process_commands(message)

# 运行机器人，替换YOUR_TOKEN_HERE为你从步骤1复制的TOKEN
bot.run('YOUR_TOKEN_HERE')