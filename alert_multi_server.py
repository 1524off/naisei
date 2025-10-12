# alert_multi_server.py
import os
import datetime
from zoneinfo import ZoneInfo
import discord
from discord.ext import commands

# === 基本設定 ===
TOKEN = os.environ["DISCORD_BOT_TOKEN"]
tz = ZoneInfo("Asia/Tokyo")

# === チャンネル設定 ===
MAIN_CHANNEL_ID = 1422420392626098308  # メイン
SUB_CHANNEL_ID = 1424451110160171028   # サブ

# === メインサーバー ===
MAIN_NAISEI_ROLE = 1424477877071642707  # 内政部長
MAIN_ALLIANCE_ROLES = {
    "NFG": 1423369997605929080,
    "HAP": 1423381559813079186,
    "1UP": 1423381694286794764,
    "BM1": 1423574375029801020,
    "sbz": 1423574916460056636,
    "JST": 1423575093652754513,
    "N9Q": 1423576222537089124,
    "MKW": 1423575677931622442,
}

# === サブサーバー ===
SUB_NAISEI_ROLE = 1424450874649870427  # 内政部長
SUB_ALLIANCE_ROLES = {
    "1UP": 1423302704972824576,  # 1UPのみ
}

# === 日付ごとの担当設定 ===
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

# === BOT設定 ===
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    today = datetime.datetime.now(tz).date()
    day_digit = int(str(today.day)[-1])
    info = ROLES[day_digit]

    mm = f"{today.month:02d}"
    dd = f"{today.day:02d}"
    emoji = info["emoji"]
    alliance = info["name"]
    lang = info["lang"]

    # === 通知判定 ===
    notify = True
    if alliance not in MAIN_ALLIANCE_ROLES and lang != "free":
        print("ℹ️ 担当外の日 — 投稿のみ（通知なし）")
        notify = False

    # === Embed本文 ===
    if lang == "en" and alliance == "1UP":
        desc = (
            f"🗓️ {mm}/{dd} ・2’s Day\n\n"
            f"**{emoji} Chief on Duty: 1UP {emoji}**\n\n"
            f"🙇‍♂️🙇🙇✨\n\n"
            f"─────────────────────\n"
            f"⏰ UTC 0:00\n"
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
            f"✉️ 通知対象：全員（内政部長ロール）\n"
            f"🔔 ロール付与でON/OFF切り替え可能！"
        )
    else:
        desc = (
            f"🗓️ {mm}/{dd} ・{day_digit}のつく日\n\n"
            f"**{emoji} 本日の内政部長は {alliance} さん {emoji}**\n\n"
            f"よろしくお願いします🙇‍♂️✨\n\n"
            f"─────────────────────\n"
            f"⏰ UTC 0:00 投稿\n"
            f"✉️ 通知対象：@内政部長＋@{alliance}\n"
            f"（両方ロールを持つ人のみ）"
        )

    embed = discord.Embed(description=desc, color=0x9EC3FF)
    embed.set_footer(text="自動送信 by GitHub Actions 🤖")

    # === 各サーバー（メイン＋サブ）でチェック ===
    servers = [
        (MAIN_CHANNEL_ID, MAIN_NAISEI_ROLE, MAIN_ALLIANCE_ROLES),
        (SUB_CHANNEL_ID, SUB_NAISEI_ROLE, SUB_ALLIANCE_ROLES),
    ]

    for ch_id, naisei_role_id, alliance_roles in servers:
        channel = bot.get_channel(ch_id)
        if not channel:
            continue

        mention_text = None

        if notify:
            # Free Day → 内政部長全員メンション
            if lang == "free":
                mention_text = f"<@&{naisei_role_id}>"
            else:
                alliance_role_id = alliance_roles.get(alliance)
                if alliance_role_id:
                    mention_members = []
                    for guild in bot.guilds:
                        alliance_role = guild.get_role(alliance_role_id)
                        naisei_role = guild.get_role(naisei_role_id)
                        if not alliance_role or not naisei_role:
                            continue
                        for member in guild.members:
                            if alliance_role in member.roles and naisei_role in member.roles:
                                mention_members.append(member.mention)
                    if mention_members:
                        mention_text = " ".join(mention_members)
                    else:
                        print(f"📭 {alliance} の該当者なし — 通知なし投稿")

        # === 投稿処理 ===
        if mention_text:
            await channel.send(
                content=mention_text,
                embed=embed,
                allowed_mentions=discord.AllowedMentions(users=True)
            )
        else:
            await channel.send(embed=embed)

    print("✅ 投稿完了")
    await bot.close()


bot.run(TOKEN)