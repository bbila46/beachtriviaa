import discord
from discord.ext import commands
from discord import app_commands
import json
import random
import os

XP_FILE = "xp_data.json"

XP_ROLES = [
    (0, "🏖️ Beach First-Aid Trainee"),
    (75, "🩹 Sandy Bandage Applier"),
    (150, "☀️ Sunburn Relief Specialist"),
    (225, "🪼 Jellyfish Sting Soother"),
    (300, "🌊 Tidal Wound Healer"),
    (375, "🐚 Seashell Scrapes Medic"),
    (450, "🚤 Ocean Lifesaver"),
    (525, "🪸 Coral Cut Caretaker"),
    (600, "🏥 Beach ER Doctor"),
    (675, "🩺 Chief of Coastal Medicine"),
    (750, "🌟🏄 Legendary Surf Medic")
]

QUESTIONS = [
    ("What is the most common medical issue faced by beachgoers?", "B"),
    ("Which vitamin is primarily produced by sun exposure?", "C"),
    ("What is the best way to treat a jellyfish sting?", "B"),
    ("What SPF is recommended for effective sun protection?", "B"),
    ("Which of these can prevent swimmer’s ear?", "A"),
    ("What is a symptom of heat exhaustion?", "B"),
    # Add more questions here as needed
]

def load_xp():
    if os.path.exists(XP_FILE):
        with open(XP_FILE, "r") as f:
            return json.load(f)
    return {}

def save_xp(data):
    with open(XP_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_rank(xp):
    for amount, role in reversed(XP_ROLES):
        if xp >= amount:
            return role
    return XP_ROLES[0][1]

class BeachTrivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.xp_data = load_xp()

    @app_commands.command(name="beachtrivia", description="Start a beach medical trivia question!")
    async def beachtrivia(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=discord.Embed(
            title="🌴 Welcome to BeachTrivia! ☀️",
            description="Each correct answer earns you **25 XP**. Let's begin!",
            color=0x00BFFF
        ), ephemeral=True)

        question, answer = random.choice(QUESTIONS)
        await interaction.followup.send(f"**❓ Question:** {question}\nA, B, C or D? (Type your answer)", ephemeral=True)

        def check(m):
            return m.author.id == interaction.user.id and m.channel == interaction.channel

        try:
            msg = await self.bot.wait_for("message", timeout=30.0, check=check)
            if msg.content.strip().upper() == answer.upper():
                user_id = str(interaction.user.id)
                self.xp_data[user_id] = self.xp_data.get(user_id, 0) + 25
                save_xp(self.xp_data)
                role = get_rank(self.xp_data[user_id])
                await interaction.followup.send(f"✅ Correct! Total XP: {self.xp_data[user_id]} • Rank: **{role}**", ephemeral=True)
            else:
                await interaction.followup.send("❌ Incorrect answer.", ephemeral=True)
        except:
            await interaction.followup.send("⌛ Time’s up!", ephemeral=True)

    @app_commands.command(name="leaderboard", description="View the BeachTrivia leaderboard")
    async def leaderboard(self, interaction: discord.Interaction):
        sorted_xp = sorted(self.xp_data.items(), key=lambda x: x[1], reverse=True)
        embed = discord.Embed(title="🏖️ BeachTrivia Leaderboard", color=0xFFA500)
        for i, (user_id, xp) in enumerate(sorted_xp[:10], 1):
            user = await self.bot.fetch_user(int(user_id))
            embed.add_field(name=f"#{i} - {user.name}", value=f"XP: {xp} • {get_rank(xp)}", inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(BeachTrivia(bot))
