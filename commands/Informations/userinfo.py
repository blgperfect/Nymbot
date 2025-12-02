import discord
from discord import app_commands
from discord.ext import commands
from config.config import CONFIG
from datetime import datetime

class UserInfoCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="userinfo",
        description="Affiche des informations détaillées sur un utilisateur."
    )
    @app_commands.describe(
        membre="Utilisateur à analyser (optionnel, vous par défaut)."
    )
    async def userinfo(self, interaction: discord.Interaction, membre: discord.User = None):
        user = membre or interaction.user
        preset = CONFIG.get("embed_default", {"color": 0x2F3136, "footer": "Bot"})
        member = interaction.guild.get_member(user.id) if interaction.guild else None

        try:
            # Statut utilisateur
            if member:
                status_map = {
                    discord.Status.online: "🟢 En ligne",
                    discord.Status.idle: "🌙 Inactif",
                    discord.Status.dnd: "⛔ Ne pas déranger",
                    discord.Status.offline: "⚪ Hors ligne",
                    discord.Status.invisible: "⚪ Invisible"
                }
                status = status_map.get(member.status, "⚪ Inconnu")
            else:
                status = "⚪ Hors serveur / inconnu"

            # Badges utilisateur
            flags = [flag.replace("_", " ").title() for flag, value in user.public_flags if value]
            badges = ", ".join(flags) if flags else "Aucun"

            # Rôles
            roles = (
                ", ".join([role.mention for role in member.roles if role.name != "@everyone"])
                if member and len(member.roles) > 1 else "Aucun"
            )

            # Dates
            created_at = user.created_at.strftime("%d/%m/%Y • %H:%M")
            joined_at = member.joined_at.strftime("%d/%m/%Y • %H:%M") if member and member.joined_at else "N/A"

            # Construction du texte esthétique
            text = (
                f"**👤 Informations sur {user.display_name}**\n\n"
                f"**• Tag :** `{user}`\n"
                f"**• ID :** `{user.id}`\n"
                f"**• Statut :** {status}\n\n"
                f"**🏅 Badges :** {badges}\n"
                f"**🛡️ Rôles :** {roles}\n\n"
                f"**📅 Compte créé :** {created_at}\n"
                f"**📅 Rejoint le serveur :** {joined_at}"
            )

            # Embed sobre mais lisible
            embed = discord.Embed(
                description=text,
                color=preset["color"],
                timestamp=datetime.utcnow()
            )
            embed.set_footer(text=preset["footer"])

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(
                "❌ Une erreur est survenue lors de la récupération des informations.",
                ephemeral=True
            )
            print(f"[ERROR] /userinfo command: {e}")


async def setup(bot: commands.Bot):
    await bot.add_cog(UserInfoCommand(bot))
