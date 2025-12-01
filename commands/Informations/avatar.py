import discord
from discord import app_commands
from discord.ext import commands
from config.config import CONFIG


class AvatarButton(discord.ui.View):
    def __init__(self, url: str):
        super().__init__(timeout=None)  # bouton permanent
        self.add_item(
            discord.ui.Button(
                label="Télécharger",
                url=url
            )
        )


class AvatarCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="avatar",
        description="Affiche l'avatar principal d'un utilisateur."
    )
    @app_commands.describe(
        membre="Utilisateur dont vous souhaitez afficher l'avatar (optionnel)."
    )
    async def avatar(self, interaction: discord.Interaction, membre: discord.User = None):
        user = membre or interaction.user
        preset = CONFIG["embed_default"]

        try:
            avatar = user.display_avatar
            avatar_url = avatar.replace(size=4096).url

            # Détection avatar par défaut
            if avatar_url == user.default_avatar.url:
                description = "Avatar par défaut de l’utilisateur."
            # Détection avatar animé
            elif avatar.is_animated():
                description = "Avatar animé."
            else:
                description = "Voici l'avatar demandé."

            embed = discord.Embed(
                title=f"Avatar de {user.display_name}",
                description=description,
                color=preset["color"]
            )

            embed.set_image(url=avatar_url)
            embed.set_footer(text=preset["footer"])

            # Bouton de téléchargement permanent
            view = AvatarButton(avatar_url)

            await interaction.response.send_message(embed=embed, view=view)

        except Exception as e:
            await interaction.response.send_message(
                "❌ Une erreur est survenue lors de l'affichage de l'avatar.",
                ephemeral=True
            )
            # Optionnel : log interne pour debug
            print(f"[ERROR] /avatar command: {e}")


async def setup(bot: commands.Bot):
    await bot.add_cog(AvatarCommand(bot))
