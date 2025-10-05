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

# === 各同盟設定 ===
ROLES = {
    1: {"name": "NFG", "emoji": "<:NFG:1423567563773972480>", "role_id": 1423254785938948226, "lang": "jp"},
    2: {"name": "1UP", "emoji": "<:1UP:1423549433173512202>", "role_id": 1423302704972824576, "lang": "en"},
    3: {"name": "HAP", "emoji": "<:HAP:1423549885931585556>", "role_id": 1423254452407894118, "lang": "jp"},
    4: {"name": "JST", "emoji": "<:JST:1423567512146018334>", "role_id": 1423254682498895964, "lang": "jp"},
    5: {"name": "N9Q", "emoji": "<:N9Q:1423549486617071648>", "role_id": None, "lang": "jp"},
    6: {"name": "sbz", "emoji": "<:sbz:1423548880468840560>", "role_id": None, "lang": "jp"},
    7: {"name": "BM1", "emoji": "<:BM1:1423567630995951636>", "role_id": None, "lang": "jp"},
    8: {"name": "MKW", "emoji": "<:MKW:1423549726086791188>", "role_id": None, "lang": "jp"},
    9: {"name": "Free Day", "emoji": "<:naisei:1424476127006818527>", "role_id": None, "lang": "free"},
    0: {"name": "Free Day", "emoji": "<:naisei:1424476127006818527>", "role_id": None, "lang": "free"},
}

# === Discord設定 ===
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

    # 通知対象メンバー
    if info["role_id"]:
        alliance_role = guild.get_role(info["role_id"])
        members_to_notify = [m for m in guild.members if hope_role in m.roles and alliance_role in m.roles]
    else:
        members_to_notify = [m for m in guild.members if hope_role in m.roles]

    mentions = " ".join(m.mention for m in members_to_notify)

    mm = f"{today.month:02d}"
    dd = f"{today.day:02d}"
    emoji = info["emoji"]
    alliance = info["name"]
    lang = info["lang"]

    # === 全同盟絵文字（フリーデー用） ===
    all_emojis = (
        "<:NFG:1423567563773972480> <:1UP:1423549433173512202> "
        "<:HAP:1423549885931585556> <:JST:1423567512146018334> "
        "<:N9Q:1423549486617071648> <:sbz:1423548880468840560> "
        "<:MKW:1423549726086791188> <:BM1:1423567630995951636>"
    )

    # === メッセージ分岐 ===
    if lang == "en":
        desc = (
            f"**📢 Chief on Duty: {alliance}**\n"
            f"📅 {mm}/{dd}\n\n"
            f"Let's do our best today! ✨\n\n"
            f"✉️ **Notification Target**\n"
            f"<:naisei:1424476127006818527> ＋\n"
            f"{emoji}"
        )

    elif lang == "free":
        desc = (
            f"**📢 本日の内政部長はフリー / Chief Free Day**\n"
            f"📅 {mm}/{dd}・{day_digit}のつく日\n\n"
            f"よろしくお願いします！\n\n"
            f"✉️ **通知対象**\n"
            f"<:naisei:1424476127006818527> ＋\n"
            f"{all_emojis}"
        )

    else:
        desc = (
            f"**📢 本日の内政部長は {alliance} さん**\n"
            f"📅 {mm}/{dd}・{day_digit}のつく日\n\n"
            f"よろしくお願いします🙇‍♂️✨\n\n"
            f"✉️ **通知対象**\n"
            f"<:naisei:1424476127006818527> ＋\n"
            f"{emoji}"
        )

    embed = discord.Embed(description=desc, color=0x9EC3FF)
    embed.set_footer(text="自動送信 by GitHub Actions 🤖")

    await channel.send(content=mentions, embed=embed)
    await bot.close()

bot.run(TOKEN)