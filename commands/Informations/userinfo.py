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
        preset = CONFIG["embed_default"]

        try:
            member = interaction.guild.get_member(user.id) if interaction.guild else None

            # Statut : seulement si membre du serveur
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

            # Badges / flags
            flags = [flag.replace("_", " ").title() for flag, has in user.public_flags if has]
            badges = ", ".join(flags) if flags else "Aucun"

            # Rôles du serveur
            roles = ", ".join([role.mention for role in member.roles[1:]]) if member else "N/A"

            # Dates
            created_at = user.created_at.strftime("%d/%m/%Y • %H:%M")
            joined_at = member.joined_at.strftime("%d/%m/%Y • %H:%M") if member and member.joined_at else "N/A"

            # Embed structuré et lisible
            embed = discord.Embed(
                title=f"👤 Informations sur {user}",
                color=preset["color"],
                description=f"Informations textuelles sur {user.display_name}."
            )

            # Infos de base
            embed.add_field(name="Tag", value=str(user), inline=True)
            embed.add_field(name="ID", value=str(user.id), inline=True)
            embed.add_field(name="Statut", value=status, inline=True)

            # Badges et rôles
            embed.add_field(name="Badges", value=badges, inline=False)
            embed.add_field(name="Rôles", value=roles, inline=False)

            # Dates importantes
            embed.add_field(name="Compte Discord créé le", value=created_at, inline=True)
            embed.add_field(name="A rejoint ce serveur le", value=joined_at, inline=True)

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
