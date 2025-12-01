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

        # Compteurs
        total_members = guild.member_count
        humans = sum(1 for m in guild.members if not m.bot)
        bots = total_members - humans

        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)

        # Date de création
        created_at = guild.created_at.strftime("%d/%m/%Y • %H:%M")

        embed = discord.Embed(
            title=f"📘 Informations du serveur : {guild.name}",
            description="Voici les informations principales du serveur.",
            color=preset["color"]
        )

        # Icône du serveur
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        # Champs principaux
        embed.add_field(
            name="🏷️ Nom",
            value=guild.name,
            inline=True
        )

        embed.add_field(
            name="🆔 ID",
            value=str(guild.id),
            inline=True
        )

        embed.add_field(
            name="👑 Propriétaire",
            value=f"<@{guild.owner_id}>",
            inline=True
        )

        embed.add_field(
            name="👥 Membres",
            value=f"**Total :** {total_members}\n**Humains :** {humans}\n**Bots :** {bots}",
            inline=True
        )

        embed.add_field(
            name="📚 Salons",
            value=(
                f"📄 Textuels : {text_channels}\n"
                f"🔊 Vocaux : {voice_channels}\n"
                f"📁 Catégories : {categories}"
            ),
            inline=True
        )

        embed.add_field(
            name="📆 Créé le",
            value=f"{created_at}",
            inline=False
        )

        # Footer via preset obligatoire
        embed.set_footer(text=preset["footer"])

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(ServerInfoCommand(bot))
