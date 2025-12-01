import discord
from discord import app_commands
from discord.ext import commands
from config.config import CONFIG


class AvatarButton(discord.ui.View):
    def __init__(self, url: str):
        super().__init__(timeout=None)
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

        # Utilisation stricte de ton preset existant
        preset = CONFIG["embed_default"]

        # Avatar HD (Discord gère automatiquement les formats)
        avatar_url = user.display_avatar.replace(size=4096).url

        embed = discord.Embed(
            title=f"Avatar de {user.display_name}",
            description="Voici l'avatar demandé.",
            color=preset["color"]
        )

        embed.set_image(url=avatar_url)
        embed.set_footer(text=preset["footer"])

        # Bouton de téléchargement
        view = AvatarButton(avatar_url)

        try:
            await interaction.response.send_message(embed=embed, view=view)
        except discord.HTTPException:
            await interaction.response.send_message(
                "Une erreur est survenue lors de l'envoi de l'avatar.",
                ephemeral=True
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(AvatarCommand(bot))
