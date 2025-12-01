import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
from config.config import CONFIG
import re


class ServerInfoCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ------------------------------------------------------------
    # EXTRACT CODE FROM INVITE (link or raw code)
    # ------------------------------------------------------------
    def extract_invite_code(self, invite: str) -> str | None:
        invite = invite.strip()

        # Raw code (most common)
        if "/" not in invite and len(invite) <= 32:
            return invite

        patterns = [
            "discord.gg/",
            "discord.com/invite/",
            "www.discord.gg/",
            "www.discord.com/invite/"
        ]

        for p in patterns:
            if p in invite:
                return invite.split(p)[-1].split("?")[0]

        return None

    # ------------------------------------------------------------
    # VALIDATE INVITE CODE FORMAT
    # ------------------------------------------------------------
    def is_valid_invite_code(self, code: str) -> bool:
        return bool(re.fullmatch(r"[A-Za-z0-9-_]{2,32}", code))

    # ------------------------------------------------------------
    # MAIN COMMAND
    # ------------------------------------------------------------
    @app_commands.command(
        name="serverinfo",
        description="Affiche les informations du serveur, ou d'un autre via une invitation."
    )
    @app_commands.describe(invite="Lien ou code d'invitation Discord")
    async def serverinfo(self, interaction: discord.Interaction, invite: str | None = None):

        # ------------------------------------------------------------
        # CASE 1 — NO INVITE → LOCAL SERVER INFO
        # ------------------------------------------------------------
        if invite is None:
            await self.send_local_server_info(interaction)
            return

        # ------------------------------------------------------------
        # CASE 2 — INVITE PROVIDED → VALIDATE FORMAT
        # ------------------------------------------------------------
        code = self.extract_invite_code(invite)
        if code is None or not self.is_valid_invite_code(code):
            return await interaction.response.send_message(
                "❌ Veuillez fournir une invitation Discord valide.",
                ephemeral=True
            )

        # ------------------------------------------------------------
        # FETCH INVITE SAFELY
        # ------------------------------------------------------------
        try:
            invite_obj = await self.bot.fetch_invite(code, with_counts=True)
        except discord.NotFound:
            return await interaction.response.send_message(
                "❌ Cette invitation n'existe pas ou a expiré.",
                ephemeral=True
            )
        except discord.HTTPException:
            return await interaction.response.send_message(
                "❌ Erreur lors de la récupération de l'invitation.",
                ephemeral=True
            )

        # ------------------------------------------------------------
        # SEND PREVIEW INFO FOR EXTERNAL SERVER
        # ------------------------------------------------------------
        await self.send_external_server_info(interaction, invite_obj)

    # ------------------------------------------------------------
    # FULL INFO FOR LOCAL SERVER
    # ------------------------------------------------------------
    async def send_local_server_info(self, interaction: discord.Interaction):
        guild = interaction.guild
        preset = CONFIG["embed_default"]

        total_members = guild.member_count
        humans = sum(not m.bot for m in guild.members)
        bots = total_members - humans

        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)

        owner = guild.owner
        created_at = guild.created_at.strftime("%d/%m/%Y • %H:%M")

        embed = discord.Embed(
            title=f"📘 Informations du serveur : {guild.name}",
            description="Voici les informations principales du serveur.",
            color=preset["color"]
        )

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

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

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        embed.set_footer(text=preset["footer"])

        await interaction.response.send_message(embed=embed)

    # ------------------------------------------------------------
    # PUBLIC PREVIEW FOR AN EXTERNAL SERVER
    # ------------------------------------------------------------
    async def send_external_server_info(self, interaction: discord.Interaction, invite: discord.Invite):
        guild = invite.guild  # PartialInviteGuild
        preset = CONFIG["embed_default"]

        embed = discord.Embed(
            title=f"🌐 Aperçu du serveur : {guild.name}",
            description=guild.description or "Aucune description fournie.",
            color=preset["color"]
        )

        # Icône
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        # Champs adaptés aux PartialInviteGuild
        fields = [
            ("🆔 ID", str(guild.id), True),
            (
                "👥 Membres",
                f"En ligne : {invite.approximate_presence_count}\n"
                f"Total : {invite.approximate_member_count}",
                True
            ),
            ("📄 Description", guild.description or "Aucune description", False),
            ("✨ Boost / Niveau", "Non disponible via une invitation", True),
            (
                "📚 Infos supplémentaires",
                f"Niveau NSFW : {guild.nsfw_level}\n"
                f"Vérification : {guild.verification_level}",
                True
            ),
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        # Bannière si disponible
        if guild.banner:
            embed.set_image(url=guild.banner.url)

        embed.set_footer(text=preset["footer"])

        # Bouton pour rejoindre
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Rejoindre le serveur", url=invite.url))

        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(ServerInfoCommand(bot))
