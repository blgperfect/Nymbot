import discord
from discord import app_commands
from discord.ext import commands
import random

# ---------- View pour pagination ----------
class CommandListView(discord.ui.View):
    def __init__(self, embeds):
        super().__init__(timeout=None)
        self.embeds = embeds
        self.current_page = 0

    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.secondary)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = (self.current_page - 1) % len(self.embeds)
        await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = (self.current_page + 1) % len(self.embeds)
        await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)

# ---------- Cog avec la commande /ss ----------
class SSCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ss", description="Affiche un aperçu de toutes les commandes possibles")
    async def ss(self, interaction: discord.Interaction):
        # Liste extrêmement large de commandes possibles pour un bot Discord
        commands_list = [
            # Informations & utilitaires
            {"name": "ping", "description": "Test la latence du bot"},
            {"name": "info", "description": "Affiche des informations sur le serveur"},
            {"name": "serverinfo", "description": "Infos détaillées du serveur"},
            {"name": "roleinfo", "description": "Affiche les infos d'un rôle"},
            {"name": "userinfo", "description": "Infos détaillées d'un utilisateur"},
            {"name": "avatar", "description": "Affiche l'avatar d'un utilisateur"},
            {"name": "serverroles", "description": "Liste tous les rôles du serveur"},
            {"name": "serveremojis", "description": "Liste tous les émojis du serveur"},
            {"name": "invite", "description": "Donne le lien d'invitation du bot"},
            {"name": "uptime", "description": "Temps d'activité du bot"},
            {"name": "stats", "description": "Statistiques générales du bot"},

            # Modération
            {"name": "ban", "description": "Bannir un utilisateur"},
            {"name": "kick", "description": "Kick un utilisateur"},
            {"name": "mute", "description": "Rendre un utilisateur muet"},
            {"name": "unmute", "description": "Rendre la parole à un utilisateur"},
            {"name": "warn", "description": "Avertir un utilisateur"},
            {"name": "clear", "description": "Supprimer un nombre de messages"},
            {"name": "lock", "description": "Verrouiller un salon"},
            {"name": "unlock", "description": "Déverrouiller un salon"},
            {"name": "slowmode", "description": "Configurer le slowmode d'un salon"},

            # Fun / Divertissement
            {"name": "say", "description": "Faire parler le bot"},
            {"name": "joke", "description": "Raconter une blague"},
            {"name": "meme", "description": "Envoyer un meme aléatoire"},
            {"name": "8ball", "description": "Répondre à une question style boule 8 magique"},
            {"name": "coinflip", "description": "Lancer une pièce (pile ou face)"},
            {"name": "dice", "description": "Lancer un dé"},
            {"name": "quote", "description": "Afficher une citation aléatoire"},
            {"name": "hug", "description": "Faire un câlin à un utilisateur"},
            {"name": "kiss", "description": "Faire un bisou à un utilisateur"},
            {"name": "pat", "description": "Frapper doucement un utilisateur"},
            {"name": "slap", "description": "Gif d'une claque à un utilisateur"},

            # Jeux & interaction
            {"name": "rps", "description": "Pierre-papier-ciseaux contre le bot"},
            {"name": "trivia", "description": "Poser une question trivia"},
            {"name": "wordgame", "description": "Jeu de mots rapide"},
            {"name": "guessnumber", "description": "Devine le nombre choisi par le bot"},
            {"name": "hangman", "description": "Jeu du pendu"},

            # Économie fictive / expérience
            {"name": "balance", "description": "Voir son solde"},
            {"name": "daily", "description": "Réclamer sa récompense quotidienne"},
            {"name": "pay", "description": "Envoyer de l'argent à un autre utilisateur"},
            {"name": "leaderboard", "description": "Afficher le classement des membres"},

            # Outils / utilitaires supplémentaires
            {"name": "timer", "description": "Lancer un minuteur"},
            {"name": "remind", "description": "Créer un rappel"},
            {"name": "translate", "description": "Traduire un texte"},
            {"name": "weather", "description": "Afficher la météo d'une ville"},
            {"name": "news", "description": "Afficher les dernières nouvelles"},
            {"name": "math", "description": "Résoudre une expression mathématique"},

            # Divers
            {"name": "poll", "description": "Créer un sondage"},
            {"name": "suggest", "description": "Envoyer une suggestion au staff"},
            {"name": "feedback", "description": "Envoyer un feedback sur le bot"},
            {"name": "report", "description": "Signaler un problème ou utilisateur"},
        ]

        # Pagination automatique
        embeds = []
        page_size = 6
        for i in range(0, len(commands_list), page_size):
            embed = discord.Embed(title="📜 Liste des commandes possibles", color=discord.Color.blurple())
            for cmd in commands_list[i:i+page_size]:
                embed.add_field(name=f"/{cmd['name']}", value=cmd["description"], inline=False)
            embed.set_footer(text=f"Page {len(embeds)+1} / {(len(commands_list)-1)//page_size+1}")
            embeds.append(embed)

        view = CommandListView(embeds)
        await interaction.response.send_message(embed=embeds[0], view=view, ephemeral=False)

# ---------- Setup ----------
async def setup(bot):
    await bot.add_cog(SSCommand(bot))
