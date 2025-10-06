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

# 同盟設定（名称・絵文字・ロールID・言語）
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

    # 通知対象抽出（通常日は 内政部長通知＋担当同盟、フリー日は 内政部長通知のみ）
    if info["role_id"]:
        alliance_role = guild.get_role(info["role_id"])
        members_to_notify = [m for m in guild.members if hope_role in m.roles and alliance_role in m.roles]
    else:
        members_to_notify = [m for m in guild.members if hope_role in m.roles]

    mentions = " ".join(m.mention for m in members_to_notify)

    # 表示用
    mm = f"{today.month:02d}"
    dd = f"{today.day:02d}"
    emoji = info["emoji"]
    alliance = info["name"]
    lang = info["lang"]

    # フリーデーに並べる全同盟絵文字
    all_emojis = (
        "<:NFG:1423567563773972480> <:1UP:1423549433173512202> "
        "<:HAP:1423549885931585556> <:JST:1423567512146018334> "
        "<:N9Q:1423549486617071648> <:sbz:1423548880468840560> "
        "<:MKW:1423549726086791188> <:BM1:1423567630995951636>"
    )

    # ── 埋め込み本文（ご指定レイアウト） ──
    if lang == "en":
        # 1UPの日（英語）
        desc = (
            f"🗓️ {mm}/{dd} ・ 2’s Day\n\n"
            f"**{emoji} Chief on Duty: 1UP {emoji}**\n\n"
            f"Let's do our best 🙇‍♂️✨\n\n"
            f"─────────────────────\n"
            f"⏰ Posts at 9:00 JST  \n"
            f"✉️ Notification Target:\n"
            f"　Roles → <:naisei:1424476127006818527> <:1UP:1423549433173512202>\n\n"
            f"🔔 Toggle via role reaction!"
        )
    elif lang == "free":
        # 9・0 のつく日（フリー）
        desc = (
            f"🗓️ {mm}/{dd} ・{day_digit}のつく日\n\n"
            f"**📢 本日の内政部長はフリー / Chief Free Day**\n\n"
            f"よろしくお願いします🙇‍♂️✨\n\n"
            f"─────────────────────\n"
            f"⏰ 毎朝 9:00 投稿  \n"
            f"✉️ 通知対象：\n"
            f"　ロール → <:naisei:1424476127006818527> ＋\n"
            f"　{all_emojis}\n\n"
            f"🔔 ロール付与でON/OFF切り替え可能！"
        )
    else:
        # 通常日（日本語）例：ご指定のBM1ケース
        desc = (
            f"🗓️ {mm}/{dd} ・{day_digit}のつく日\n\n"
            f"**{emoji} 本日の内政部長は {alliance}さん {emoji}**\n\n"
            f"よろしくお願いします🙇‍♂️✨\n\n"
            f"─────────────────────\n"
            f"⏰ 毎朝 9:00 投稿  \n"
            f"✉️ 通知対象：\n"
            f"　ロール → <:naisei:1424476127006818527> {emoji}\n\n"
            f"🔔 ロール付与でON/OFF切り替え可能！"
        )

    embed = discord.Embed(description=desc, color=0x9EC3FF)
    embed.set_footer(text="自動送信 by GitHub Actions 🤖")

    await channel.send(content=mentions, embed=embed)
    await bot.close()

bot.run(TOKEN)