import discord
from discord import app_commands
from discord.ext import commands
from config.config import CONFIG
from datetime import datetime


class ServerInfoCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="serverinfo",
        description="Affiche les informations du serveur."
    )
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        preset = CONFIG["embed_default"]

        # Compteurs membres
        total_members = guild.member_count
        humans = sum(not m.bot for m in guild.members)
        bots = total_members - humans

        # Salons
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)

        # Informations complémentaires
        owner = guild.owner
        created_at = guild.created_at.strftime("%d/%m/%Y • %H:%M")

        embed = discord.Embed(
            title=f"📘 Informations du serveur : {guild.name}",
            description="Voici les informations principales du serveur.",
            color=preset["color"]
        )

        # Icône du serveur
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        # Liste des champs pour un code plus propre
        fields = [
            ("🏷️ Nom", guild.name, True),
            ("🆔 ID", str(guild.id), True),
            ("👑 Propriétaire", owner.mention if owner else "Inconnu", True),
            (
                "👥 Membres",
                f"**Total :** {total_members}\n"
                f"**Humains :** {humans}\n"
                f"**Bots :** {bots}",
                True
            ),
            (
                "📚 Salons",
                f"📄 Textuels : {text_channels}\n"
                f"🔊 Vocaux : {voice_channels}\n"
                f"📁 Catégories : {categories}",
                True
            ),
            ("📆 Créé le", created_at, False),
            (
                "✨ Boost",
                f"Niveau : {guild.premium_tier}\n"
                f"Boosts : {guild.premium_subscription_count}",
                True
            ),
            (
                "😀 Emojis",
                f"{len(guild.emojis)} emojis",
                True
            ),
        ]

        # Ajout des champs dans l'embed
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        # Footer depuis preset
        embed.set_footer(text=preset["footer"])

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(ServerInfoCommand(bot))

