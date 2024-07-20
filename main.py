import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import pytz

intents = discord.Intents.default()
intents.presences = True
intents.members = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()

bot = MyBot()

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.tree.command(name="spotify", description="Retrieve Spotify activity of a user")
@app_commands.describe(user="The user to check")
async def spotify(interaction: discord.Interaction, user: discord.User):
    member = interaction.guild.get_member(user.id)
    if member is None:
        await interaction.response.send_message("User not found in this server.")
        return

    activity = None
    for act in member.activities:
        if isinstance(act, discord.Spotify):
            activity = act
            break

    if activity is None:
        await interaction.response.send_message("This user is not listening to Spotify.")
        return

    # Convert start time to Japan Standard Time
    jst = pytz.timezone('Asia/Tokyo')
    start_time_utc = activity.start
    start_time_jst = start_time_utc.astimezone(jst)
    start_time_str = start_time_jst.strftime('%Y-%m-%d %H:%M:%S')

    embed = discord.Embed(
        title=f"{member.name} がSpotifyを再生中",
        description=f"**{activity.title}** by **{activity.artist}**",
        color=0x331f44
    )
    embed.set_thumbnail(url=activity.album_cover_url)
    embed.add_field(name="アルバム", value=activity.album, inline=True)
    embed.add_field(name="再生時間", value=f"{activity.duration.seconds // 60}:{activity.duration.seconds % 60:02d}", inline=True)
    embed.set_footer(text=f"再生開始時刻： {start_time_str} 日本時間")

    # Log the information to the console
    print(f"ユーザー名: {member.name}")
    print(f"タイトル: {activity.title}")
    print(f"アーティスト: {activity.artist}")
    print(f"アルバム: {activity.album}")
    print(f"再生時間: {activity.duration.seconds // 60}:{activity.duration.seconds % 60:02d}")
    print(f"再生開始時刻: {start_time_str} JST")
    print(f"アルバムカバーＵＲＬ: {activity.album_cover_url}")

    await interaction.response.send_message(embed=embed)

bot.run('YOUR_BOT_TOKEN')
