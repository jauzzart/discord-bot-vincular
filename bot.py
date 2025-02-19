{\rtf1\ansi\ansicpg1252\cocoartf2639
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;\f1\fnil\fcharset0 AppleColorEmoji;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import discord\
from discord.ui import Button, View\
from discord.ext import commands\
from discord import app_commands\
import sqlite3  # Para armazenar os dados do formul\'e1rio\
import asyncio\
\
# Configura\'e7\'f5es do bot\
intents = discord.Intents.default()\
intents.members = True  # Necess\'e1rio para gerenciar membros e roles\
\
bot = commands.Bot(command_prefix="!", intents=intents)\
\
# Conex\'e3o com o banco de dados SQLite\
conn = sqlite3.connect('formulario.db')\
cursor = conn.cursor()\
\
# Cria\'e7\'e3o da tabela no banco de dados (caso n\'e3o exista)\
cursor.execute('''\
CREATE TABLE IF NOT EXISTS formul\'e1rios (\
    discord_id INTEGER PRIMARY KEY,\
    email TEXT,\
    nick_minecraft TEXT,\
    idade INTEGER,\
    nick_discord TEXT\
)\
''')\
conn.commit()\
\
# Classe de View para o bot\'e3o de vincula\'e7\'e3o\
class VincularView(View):\
    def __init__(self):\
        super().__init__(timeout=None)\
\
    @discord.ui.button(label="Vincular-se", style=discord.ButtonStyle.green)\
    async def vincular(self, button: discord.ui.Button, interaction: discord.Interaction):\
        # Enviar uma mensagem de formul\'e1rio para o usu\'e1rio preencher\
        await interaction.response.send_message("Por favor, preencha o formul\'e1rio com seu email, nick do Minecraft, idade e nick do Discord.", ephemeral=True)\
        \
        # Criar um formul\'e1rio interativo (exemplo simples)\
        await interaction.followup.send("Preencha o formul\'e1rio respondendo as perguntas a seguir:")\
\
        # Esperar a resposta do usu\'e1rio\
        def check(m):\
            return m.author == interaction.user and m.channel == interaction.channel\
\
        try:\
            # Perguntar e salvar os dados\
            await interaction.followup.send("Qual seu email?")\
            email_msg = await bot.wait_for('message', check=check)\
            email = email_msg.content\
\
            await interaction.followup.send("Qual seu nick no Minecraft?")\
            nick_minecraft_msg = await bot.wait_for('message', check=check)\
            nick_minecraft = nick_minecraft_msg.content\
\
            await interaction.followup.send("Qual sua idade?")\
            idade_msg = await bot.wait_for('message', check=check)\
            idade = int(idade_msg.content)\
\
            await interaction.followup.send("Qual seu nick no Discord?")\
            nick_discord_msg = await bot.wait_for('message', check=check)\
            nick_discord = nick_discord_msg.content\
\
            # Armazenar os dados no banco de dados\
            cursor.execute('''\
            INSERT OR REPLACE INTO formul\'e1rios (discord_id, email, nick_minecraft, idade, nick_discord)\
            VALUES (?, ?, ?, ?, ?)\
            ''', (interaction.user.id, email, nick_minecraft, idade, nick_discord))\
            conn.commit()\
\
            # Enviar confirma\'e7\'e3o\
            await interaction.followup.send("Formul\'e1rio enviado com sucesso! Voc\'ea agora ser\'e1 vinculado.")\
\
            # Atribuir o cargo e liberar os canais\
            role = discord.utils.get(interaction.guild.roles, name="Vinculado")\
            await interaction.user.add_roles(role)\
\
            # Enviar uma mensagem no canal restrito para os administradores\
            admin_channel = discord.utils.get(interaction.guild.text_channels, name="
\f1 \uc0\u55357 \u57056 
\f0 \uc0\u9475 chat-staff")\
            await admin_channel.send(f"Novo formul\'e1rio recebido de \{interaction.user.name\} (\{interaction.user.id\}):\\nEmail: \{email\}\\nNick do Minecraft: \{nick_minecraft\}\\nIdade: \{idade\}\\nNick no Discord: \{nick_discord\}")\
\
        except asyncio.TimeoutError:\
            await interaction.followup.send("Voc\'ea demorou muito para responder. Tente novamente.", ephemeral=True)\
\
# Comando /vinculo para ver as informa\'e7\'f5es de um usu\'e1rio\
@bot.tree.command(name="vinculo", description="Ver informa\'e7\'f5es de vincula\'e7\'e3o de uma conta")\
@app_commands.describe(user="Usu\'e1rio a ser verificado")\
async def vinculo(interaction: discord.Interaction, user: discord.User):\
    # Buscar os dados do banco de dados\
    cursor.execute('SELECT * FROM formul\'e1rios WHERE discord_id = ?', (user.id,))\
    dados = cursor.fetchone()\
\
    if dados:\
        email, nick_minecraft, idade, nick_discord = dados[1], dados[2], dados[3], dados[4]\
        await interaction.response.send_message(\
            f"Formul\'e1rio de \{user.name\}:\\nEmail: \{email\}\\nNick do Minecraft: \{nick_minecraft\}\\nIdade: \{idade\}\\nNick no Discord: \{nick_discord\}",\
            ephemeral=True\
        )\
    else:\
        await interaction.response.send_message("N\'e3o encontrei nenhum formul\'e1rio vinculado para esse usu\'e1rio.", ephemeral=True)\
\
# Evento on_ready para indicar que o bot est\'e1 online\
@bot.event\
async def on_ready():\
    print(f'Bot \{bot.user\} est\'e1 online!')\
\
# Evento on_member_join para enviar a mensagem com o bot\'e3o assim que o usu\'e1rio entrar no servidor\
@bot.event\
async def on_member_join(member: discord.Member):\
    # Canal de boas-vindas ou qualquer canal onde voc\'ea queira que o bot envie a mensagem\
    channel = discord.utils.get(member.guild.text_channels, name="
\f1 \uc0\u55357 \u56395 
\f0 \uc0\u9475 bem-vindo")  # Substitua pelo nome do seu canal\
\
    if channel:\
        # Cria o bot\'e3o de vincula\'e7\'e3o\
        view = VincularView()\
        await channel.send(f"Bem-vindo ao servidor, \{member.mention\}! Para se vincular, clique no bot\'e3o abaixo:", view=view)\
\
# Rodando o bot\
bot.run('MTMzMDkxNTg5OTkyMTkyODI0NA.GFb2p_.8FQ5SNMQA0aI0n6cOHRQOHJfrpH2cjzZZk0gFY')\
}