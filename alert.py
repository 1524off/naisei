# alert.py
import os
import datetime
from zoneinfo import ZoneInfo
import discord
from discord.ext import commands

TOKEN = os.environ["DISCORD_BOT_TOKEN"]
CHANNEL_ID = int(os.environ["DISCORD_CHANNEL_ID"])
HOPE_ROLE_ID = 1424450874649870427  # 内政部長通知ロール
tz = ZoneInfo("Asia/Tokyo")

# 各同盟の絵文字・言語・ロールID
ROLES = {
    1: {"name": "NFG", "emoji": ":NFG:", "role_id": 1423254785938948226, "lang": "jp"},
    2: {"name": "1UP", "emoji": ":1UP:", "role_id": 1423302704972824576, "lang": "en"},  # 1UPは英語書式
    3: {"name": "HAP", "emoji": ":HAP:", "role_id": 1423254452407894118, "lang": "jp"},
    4: {"name": "JST", "emoji": ":JST:", "role_id": 1423254682498895964, "lang": "jp"},
    5: {"name": "N9Q", "emoji": ":N9Q:", "role_id": None, "lang": "jp"},
    6: {"name": "sbz", "emoji": ":sbz:", "role_id": None, "lang": "jp"},
    7: {"name": "BM1", "emoji": ":BM1:", "role_id": None, "lang": "jp"},
    8: {"name": "MKW", "emoji": ":MKW:", "role_id": None, "lang": "jp"},
    9: {"name": "Free Day", "emoji": ":naisei:", "role_id": None, "lang": "free"},
    0: {"name": "Free Day", "emoji": ":naisei:", "role_id": None, "lang": "free"},
}

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    today = datetime.datetime.now(tz).date()
    day_digit = int(str(today.day)[-1])
    info = ROLES[day_digit]

    channel = bot.get_channel(CHANNEL_ID)
    guild = channel.guild
    hope_role = guild.get_role(HOPE_ROLE_ID)

    # 通知対象（メンション）抽出
    if info["role_id"]:
        alliance_role = guild.get_role(info["role_id"])
        members_to_notify = [m for m in guild.members if hope_role in m.roles and alliance_role in m.roles]
    else:
        members_to_notify = [m for m in guild.members if hope_role in m.roles]  # 9/0は希望者全員

    mentions = " ".join(m.mention for m in members_to_notify)

    mm = f"{today.month:02d}"
    dd = f"{today.day:02d}"
    emoji = info["emoji"]
    name = info["name"]
    lang = info["lang"]

    # ===== 1行フォーマット作成 =====
    if lang == "en":
        # 1UPの日（英語）
        # 例: 📢 chief:1UP: 1UP 📅Today 10/07⏰ UTC 0:00 ✉️ 　:naisei:＋:1UP:
        text = f"📢 chief{emoji} {name} 📅Today {mm}/{dd}⏰ UTC 0:00 ✉️ 　:naisei:＋{emoji}"
    elif lang == "free":
        # 9/0 フリー
        # 例: 📢 本日の内政部長はフリー/Free Day📅 今日は 10/09⏰ 毎朝 9:00/UTC 0:00✉️ 通知対象　:naisei:
        text = f"📢 本日の内政部長はフリー/Free Day📅 今日は {mm}/{dd}⏰ 毎朝 9:00/UTC 0:00✉️ 通知対象　:naisei:"
    else:
        # 通常（日本語）
        # 例: 📢 内政部長アラート:NFG: 担当：NFG さん📅 今日は 10/01⏰ 毎朝 9:00✉️ 通知対象　:naisei:＋ :NFG:
        text = f"📢 内政部長アラート{emoji} 担当：{name} さん📅 今日は {mm}/{dd}⏰ 毎朝 9:00✉️ 通知対象　:naisei:＋ {emoji}"

    # 送信（本文のみ・埋め込みなし）
    await channel.send(content=(mentions + " " + text if mentions else text))
    await bot.close()

bot.run(TOKEN)