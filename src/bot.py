import discord
import json
import os
import re
import requests

from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# URL do arquivo list.json no repositório GitHub
GITHUB_URL = 'https://raw.githubusercontent.com/Discord-AntiScam/scam-links/refs/heads/main/list.json'

# Caminho para o arquivo de configuração persistente
CONFIG_FILE = 'notification_channels.json'

# Função para carregar dados persistentes
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

# Função para salvar dados persistentes
def save_config():
    with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
        json.dump(notification_channels, file, ensure_ascii=False, indent=4)

# Carrega canais de notificação previamente configurados
notification_channels = load_config()

# Carrega a lista de links bloqueados do arquivo list.json
def load_blocked_links():
    try:
        response = requests.get(GITHUB_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erro ao baixar a lista de links bloqueados: {e}")
        # Carrega a lista localmente como fallback
        file_path = os.path.join(os.path.dirname(__file__), 'utils', 'list.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

blocked_links = load_blocked_links()

@bot.event
async def on_ready():
    print(f'Bot {bot.user} está online!')

@bot.command()
@commands.has_permissions(administrator=True)
async def definir_canal_notificar(ctx, channel: discord.TextChannel):
    """Comando para definir o canal de notificação."""
    guild_id = str(ctx.guild.id)  # Converta para string para compatibilidade com JSON
    notification_channels[guild_id] = channel.id

    save_config()  # Salva a configuração no arquivo
    await ctx.send(f"Canal de notificação definido para: {channel.mention}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    for link in blocked_links:
        pattern = re.compile(re.escape(link), re.IGNORECASE)

        if pattern.search(message.content):
            print(f'Link bloqueado encontrado: {link}')
            try:
                await message.delete()
                guild_id = str(message.guild.id)
                notification_channel_id = notification_channels.get(guild_id)

                # Notifica no canal configurado, se existir
                if notification_channel_id:
                    channel = bot.get_channel(notification_channel_id)
                    if channel:
                        await channel.send(
                            f"🔴 Link suspeito detectado e apagado em {message.channel.mention}.\n"
                            f"**Usuário:** {message.author.mention}\n"
                            f"**Conteúdo:** {message.content}"
                        )
                else:
                    await message.channel.send(
                        "Mensagem removida com link bloqueado. Canal de notificação não configurado."
                    )
            except discord.Forbidden:
                print("Permissão negada para apagar a mensagem.")
            except discord.HTTPException as e:
                print(f"Erro ao apagar a mensagem: {e}")
            break

    await bot.process_commands(message)

# Substitua 'YOUR_TOKEN_HERE' pelo token do seu bot
bot.run('YOUR_TOKEN_HERE')