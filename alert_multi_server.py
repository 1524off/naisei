# alert_multi_server.
from zoneinfo import ZoneInfo
import datetime

# タイムゾーン設定
tz = ZoneInfo("Asia/Tokyo")

# 現在時刻を日本時間で取得
now = datetime.datetime.now(tz)
print("現在の日本時間:", now)
import os
import datetime
from zoneinfo import ZoneInfo
import discord
from discord.ext import commands

# === 設定 ===
TOKEN = os.environ["DISCORD_BOT_TOKEN"]
tz = ZoneInfo("Asia/Tokyo")

# ✅ 投稿先チャンネルを2つ指定（どちらにも同時送信）
CHANNEL_IDS = [
    1424451110160171028,  # メインサーバー
    1422420392626098308   # サブサーバー
]

# === 同盟設定 ===
ROLES = {
    1: {"name": "NFG", "emoji": "<:NFG:1423572526730055782>", "lang": "jp"},
    2: {"name": "1UP", "emoji": "<:1UP:1423572427962581022>", "lang": "en"},
    3: {"name": "HAP", "emoji": "<:HAP:1423572292629303306>", "lang": "jp"},
    4: {"name": "JST", "emoji": "<:JST:1423572223934861342>", "lang": "jp"},
    5: {"name": "N9Q", "emoji": "<:N9Q:1423572353694044198>", "lang": "jp"},
    6: {"name": "sbz", "emoji": "<:sbz:1423548880468840560>", "lang": "jp"},
    7: {"name": "BM1", "emoji": "<:BM1:1423567630995951636>", "lang": "jp"},
    8: {"name": "MKW", "emoji": "<:MKW:1423572595831472223>", "lang": "jp"},
    9: {"name": "Free Day", "emoji": "<:naisei:1424476127006818527>", "lang": "free"},
    0: {"name": "Free Day", "emoji": "<:naisei:1424476127006818527>", "lang": "free"},
}

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    today = datetime.datetime.now(tz).date()
    day_digit = int(str(today.day)[-1])
    info = ROLES[day_digit]

    mm = f"{today.month:02d}"
    dd = f"{today.day:02d}"
    emoji = info["emoji"]
    alliance = info["name"]
    lang = info["lang"]

    all_emojis = (
        "<:NFG:1423572526730055782> <:1UP:1423572427962581022> "
        "<:HAP:1423572292629303306> <:JST:1423572223934861342> "
        "<:N9Q:1423572353694044198> <:sbz:1423548880468840560> "
        "<:MKW:1423572595831472223> <:BM1:1423567630995951636> <:Other:1423595424501207070>"
    )

    # === メッセージ内容 ===
    if lang == "en":
        desc = (
            f"🗓️ {mm}/{dd} ・2’s Day\n\n"
            f"**{emoji} Chief on Duty: 1UP {emoji}**\n\n"
            f"🙇‍♂️🙇🙇✨\n\n"
            f"─────────────────────\n"
            f"⏰ UTC 0:00 投稿\n"
            f"✉️ Notification Target:\n"
            f"　Roles → <:naisei:1424476127006818527> <:1UP:1423572427962581022>\n\n"
            f"🔔 Toggle via role reaction!"
        )
    elif lang == "free":
        desc = (
            f"🗓️ {mm}/{dd} ・{day_digit}のつく日\n\n"
            f"**📢 本日の内政部長はフリー / Chief Free Day**\n\n"
            f"よろしくお願いします🙇‍♂️✨\n\n"
            f"─────────────────────\n"
            f"⏰ UTC 0:00 投稿\n"
            f"✉️ 通知対象：\n"
            f"　ロール → <:naisei:1424476127006818527> ＋\n"
            f"　{all_emojis}\n\n"
            f"🔔 ロール付与でON/OFF切り替え可能！"
        )
    else:
        desc = (
            f"🗓️ {mm}/{dd} ・{day_digit}のつく日\n\n"
            f"**{emoji} 本日の内政部長は {alliance} さん {emoji}**\n\n"
            f"よろしくお願いします🙇‍♂️✨\n\n"
            f"─────────────────────\n"
            f"⏰ UTC 0:00 投稿\n"
            f"✉️ 通知対象：\n"
            f"　ロール → <:naisei:1424476127006818527> {emoji}\n\n"
            f"🔔 ロール付与でON/OFF切り替え可能！"
        )

    embed = discord.Embed(description=desc, color=0x9EC3FF)
    embed.set_footer(text="自動送信 by GitHub Actions 🤖")

    for ch_id in CHANNEL_IDS:
        channel = bot.get_channel(ch_id)
        if channel:
            await channel.send(embed=embed)

    await bot.close()

bot.run(TOKEN)
