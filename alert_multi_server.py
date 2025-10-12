# alert_multi_server.py
import os
import datetime
from zoneinfo import ZoneInfo
import discord
from discord.ext import commands

# === 基本設定 ===
TOKEN = os.environ["DISCORD_BOT_TOKEN"]
tz = ZoneInfo("Asia/Tokyo")

# === チャンネル①（メインサーバー）設定 ===
MAIN_CHANNEL_ID = 1422420392626098308
MAIN_ALERT_ROLE_ID = 1424477877071642707
MAIN_ROLES = {
    1: {"name": "NFG", "emoji": "<:NFG:1423572526730055782>", "role_id": 1423369997605929080, "lang": "jp"},
    2: {"name": "1UP", "emoji": "<:1UP:1423572427962581022>", "role_id": 1423381694286794764, "lang": "en"},
    3: {"name": "HAP", "emoji": "<:HAP:1423572292629303306>", "role_id": 1423381559813079186, "lang": "jp"},
    4: {"name": "JST", "emoji": "<:JST:1423572223934861342>", "role_id": 1423575093652754513, "lang": "jp"},
    5: {"name": "N9Q", "emoji": "<:N9Q:1423572353694044198>", "role_id": 1423576222537089124, "lang": "jp"},
    6: {"name": "sbz", "emoji": "<:sbz:1423548880468840560>", "role_id": 1423574916460056636, "lang": "jp"},
    7: {"name": "BM1", "emoji": "<:BM1:1423567630995951636>", "role_id": 1423574375029801020, "lang": "jp"},
    8: {"name": "MKW", "emoji": "<:MKW:1423572595831472223>", "role_id": 1423575677931622442, "lang": "jp"},
    9: {"name": "Free Day", "emoji": "<:naisei:1424476127006818527>", "role_id": None, "lang": "free"},
    0: {"name": "Free Day", "emoji": "<:naisei:1424476127006818527>", "role_id": None, "lang": "free"},
}

# === チャンネル②（サブサーバー）設定 ===
SUB_CHANNEL_ID = 1424451110160171028
SUB_ALERT_ROLE_ID = 1424450874649870427
SUB_ROLES = {
    "1UP": 1423302704972824576,
    "HAP": 1423254452407894118,
}

# === Bot設定 ===
intents = discord.Intents.default()
intents.members = True
intents.reactions = True
bot = commands.Bot(command_prefix="!", intents=intents)

# === 🛎 リアクションで通知ON/OFF ===
@bot.event
async def on_raw_reaction_add(payload):
    if payload.emoji.name == "🛎️":
        guild = bot.get_guild(payload.guild_id)
        role = guild.get_role(MAIN_ALERT_ROLE_ID) or guild.get_role(SUB_ALERT_ROLE_ID)
        member = guild.get_member(payload.user_id)
        if role and member:
            await member.add_roles(role)
            try:
                await member.send("🔔 通知ONにしました！")
            except:
                pass

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.emoji.name == "🛎️":
        guild = bot.get_guild(payload.guild_id)
        role = guild.get_role(MAIN_ALERT_ROLE_ID) or guild.get_role(SUB_ALERT_ROLE_ID)
        member = guild.get_member(payload.user_id)
        if role and member:
            await member.remove_roles(role)
            try:
                await member.send("🔕 通知OFFにしました。")
            except:
                pass

# === 自動投稿 ===
@bot.event
async def on_ready():
    today = datetime.datetime.now(tz).date()
    day_digit = int(str(today.day)[-1])
    info = MAIN_ROLES.get(day_digit, MAIN_ROLES[9])  # Free Day fallback

    emoji = info["emoji"]
    alliance = info["name"]
    alliance_role_id = info["role_id"]

    desc = (
        f"🗓️ {today:%m/%d} ・{day_digit}のつく日\n\n"
        f"**{emoji} 本日の内政部長は {alliance} さん {emoji}**\n\n"
        "よろしくお願いします🙇‍♂️✨\n\n"
        "─────────────────────\n"
        "⏰ UTC 0:00 投稿\n"
        "🔔 通知ロール＋同盟ロール持ちのみメンション"
    )

    embed = discord.Embed(description=desc, color=0x9EC3FF)
    embed.set_footer(text="自動送信 by GitHub Actions 🤖")

    # チャンネル①（メイン）通知
    await send_alert(MAIN_CHANNEL_ID, MAIN_ALERT_ROLE_ID, alliance_role_id, alliance, "メイン")

    # チャンネル②（サブ）通知（対象同盟が存在する場合のみ）
    sub_role_id = SUB_ROLES.get(alliance)
    if sub_role_id:
        await send_alert(SUB_CHANNEL_ID, SUB_ALERT_ROLE_ID, sub_role_id, alliance, "サブ")

    await bot.close()

# === 通知送信関数 ===
async def send_alert(channel_id, alert_role_id, alliance_role_id, alliance_name, label):
    channel = bot.get_channel(channel_id)
    if not channel:
        print(f"[WARN] {label}チャンネルが見つかりません。")
        return

    mentions = []
    for member in channel.guild.members:
        roles = [r.id for r in member.roles]
        if alert_role_id in roles and alliance_role_id in roles:
            mentions.append(member.mention)

    mention_text = " ".join(mentions) if mentions else "(通知対象なし)"
    embed = discord.Embed(
        description=f"**{label}通知**\n\n🔔 {alliance_name} 内政部長通知",
        color=0x9EC3FF
    )
    await channel.send(
        content=mention_text,
        embed=embed,
        allowed_mentions=discord.AllowedMentions(users=True)
    )

bot.run(TOKEN)