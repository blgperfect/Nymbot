import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from config.config import CONFIG
import logging
import random

# ------------------------------------------------------------
# Logging : désactiver les infos Discord si tu veux
# ------------------------------------------------------------
for name in ["discord", "discord.client", "discord.gateway", "discord.http"]:
    logging.getLogger(name).setLevel(logging.WARNING)

# ------------------------------------------------------------
# Charger le TOKEN depuis .env
# ------------------------------------------------------------
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# ------------------------------------------------------------
# Intents
# ------------------------------------------------------------
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.presences = True        # <-- indispensable pour les statuts
intents.message_content = True

# ------------------------------------------------------------
# Classe principale du bot
# ------------------------------------------------------------
class NymBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.config = CONFIG
        self.status_index = 0  # index pour la rotation
        self.presence_messages = [
            "Nyym c'est la meilleure ❤️",
            "Joue dans {guild_count} serveurs",
            "Observe {member_count} membres"
        ]

    async def setup_hook(self):
        # Charger commands et events
        await self.load_all_extensions("commands")
        await self.load_all_extensions("events")

        # Synchroniser les slash commands
        await self.tree.sync()
        print("Slash commands synchronisées.")

        # Démarrer la rotation de statut
        self.presence_rotation.start()

    # --------------------------------------------------------
    # Rotation automatique du statut / activité
    # --------------------------------------------------------
    @tasks.loop(seconds=20)
    async def presence_rotation(self):
        guild_count = len(self.guilds)
        member_count = sum(g.member_count for g in self.guilds)

        # Récupération du message suivant
        texte_template = self.presence_messages[self.status_index]
        texte = texte_template.format(guild_count=guild_count, member_count=member_count)

        # Changer la présence
        await self.change_presence(
            activity=discord.Game(name=texte),
            status=discord.Status.dnd
        )

        # Passage au message suivant
        self.status_index = (self.status_index + 1) % len(self.presence_messages)

    @presence_rotation.before_loop
    async def before_presence_rotation(self):
        await self.wait_until_ready()

    # --------------------------------------------------------
    # Fonction utilitaire : charger tous les fichiers .py d’un dossier
    # --------------------------------------------------------
    async def load_all_extensions(self, base_folder: str):
        if not os.path.isdir(base_folder):
            print(f"[INFO] Le dossier '{base_folder}' n'existe pas, ignoré.")
            return

        for root, dirs, files in os.walk(base_folder):
            for filename in files:
                if filename.endswith(".py"):
                    path = os.path.join(root, filename)
                    module = path[:-3].replace("/", ".").replace("\\", ".")

                    try:
                        await self.load_extension(module)
                        print(f"[OK] Extension chargée : {module}")
                    except Exception as e:
                        print(f"[ERREUR] Échec du chargement de {module} : {e}")

# ------------------------------------------------------------
# Instancier le bot
# ------------------------------------------------------------
bot = NymBot()

# ------------------------------------------------------------
# Event : bot connecté
# ------------------------------------------------------------
@bot.event
async def on_ready():
    print(f"NymBot connecté en tant que {bot.user}")

# ------------------------------------------------------------
# Démarrer le bot
# ------------------------------------------------------------
bot.run(TOKEN)
