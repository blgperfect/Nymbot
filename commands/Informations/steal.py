import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
from config.config import CONFIG
from datetime import datetime, timezone
import re

class StealEmojiCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="steal",
        description="Ajoute un emoji à votre serveur à partir d'un autre serveur ou message."
    )
    @app_commands.describe(
        emoji="Emoji à voler (coller le code ou envoyer l'emoji)",
        name="Nom que vous voulez donner à l'emoji (optionnel)"
    )
    async def steal(self, interaction: discord.Interaction, emoji: str, name: str = None):
        preset = CONFIG.get("embed_default", {"color": 0x2F3136, "footer": "Bot"})
        
        # Vérifier permissions
        if not interaction.guild:
            return await interaction.response.send_message("❌ Cette commande doit être utilisée dans un serveur.", ephemeral=True)
        if not interaction.guild.me.guild_permissions.manage_emojis_and_stickers:
            return await interaction.response.send_message("❌ Je n'ai pas la permission de gérer les emojis ici.", ephemeral=True)
        
        # Regex pour détecter un emoji Discord <:name:id> ou <a:name:id>
        match = re.match(r'<(a?):(\w+):(\d+)>', emoji)
        if not match:
            return await interaction.response.send_message("❌ Emoji invalide. Assurez-vous d'envoyer un emoji personnalisé.", ephemeral=True)

        animated_flag, emoji_name, emoji_id = match.groups()
        animated = bool(animated_flag)
        emoji_url = f"https://cdn.discordapp.com/emojis/{emoji_id}.{'gif' if animated else 'png'}"

        # Utiliser le nom fourni si disponible
        emoji_name = name or emoji_name

        # Vérifier limite du serveur
        if len(interaction.guild.emojis) >= interaction.guild.emoji_limit:
            return await interaction.response.send_message("❌ Le serveur a atteint le nombre maximum d'emojis.", ephemeral=True)

        # Télécharger l'image
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(emoji_url) as resp:
                    if resp.status != 200:
                        return await interaction.response.send_message("❌ Impossible de récupérer l'image de l'emoji.", ephemeral=True)
                    image_bytes = await resp.read()

            # Créer l'emoji
            new_emoji = await interaction.guild.create_custom_emoji(name=emoji_name, image=image_bytes)
            
            embed = discord.Embed(
                title="✅ Emoji ajouté avec succès !",
                description=f"**Nom :** {new_emoji.name}\n**Emoji :** {str(new_emoji)}",
                color=preset["color"],
                timestamp=datetime.now(timezone.utc)
            )
            embed.set_footer(text=preset["footer"])
            await interaction.response.send_message(embed=embed)

        except discord.HTTPException as e:
            await interaction.response.send_message(f"❌ Une erreur est survenue : {e}", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(StealEmojiCommand(bot))
