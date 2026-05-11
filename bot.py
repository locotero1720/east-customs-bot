# ╔══════════════════════════════════════════════════════════════╗
#                     EAST CUSTOMS BOT
#                    FiveM Discord Bot
# ╚══════════════════════════════════════════════════════════════╝
#
# FEATURES:
# ✅ Willkommen System
# ✅ Ticket System (Rabatt / Fragen / Sonstiges / Bewerbung)
# ✅ Ankündigungen (/an)
# ✅ Anti Spam
# ✅ Status Rotation (FiveM Themed)
# ✅ Logs für alles
# ✅ Ticket schließen Button

import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import time
import random
import os

# ──────────────────────────────────────────────
# 🔧 BOT SETUP
# ──────────────────────────────────────────────

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ──────────────────────────────────────────────
# 📌 CHANNEL IDS EINTRAGEN
# ──────────────────────────────────────────────

WELCOME_CHANNEL_ID       = 1379078861983318160   # Willkommen-Channel
LOG_CHANNEL_ID           = 1503227957995376680   # Log-Channel
TICKET_CATEGORY_ID       = 1503227912298692648   # Kategorie für Tickets
ANNOUNCEMENT_CHANNEL_ID  = 1503227860549369927   # Ankündigungs-Channel
SUPPORT_ROLE_ID          = 1503227860549369927   # Support-Rolle

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ──────────────────────────────────────────────
# 🚗 STATUS ROTATION
# ──────────────────────────────────────────────

statuses = [
    "🏎️ EAST Customs macht Träume auf vier Rädern wahr",
    "🔥 Heute wird wieder Leistung gebaut statt geredet",
    "⚙️ EAST Customs arbeitet am nächsten Drift-Biest",
    "💨 Der Prüfstand glüht schon wieder",
    "🛞 Neue Felgen? EAST hat da was vorbereitet",
    "🚗 Jeder Umbau erzählt seine eigene Geschichte",
    "🔩 EAST Customs kennt keine halben Sachen",
    "💥 Das nächste Projekt wird komplett eskalieren",
    "🛠️ EAST bringt jedes Auto auf das nächste Level",
    "🎁 IC Special Deal heute nur bei EAST Customs",
    "🚗 EAST Customs baut wieder brutale Cars",
    "🔥 Neue Umbauten in Arbeit bei EAST Customs",
    "⚙️ Motor wird gerade abgestimmt",
    "🛠️ EAST Customs ist wieder in der Werkstatt",
    "💨 Turbo pfeift schon wieder verdächtig",
    "🏁 Neue Projekte warten auf ihre Auslieferung",
    "🚘 Felgen werden gerade montiert",
    "🔧 EAST Customs tuned bis spät in die Nacht",
    "🔥 Mehr Leistung? EAST regelt das",
    "⚡ ECU wird neu abgestimmt",
    "🛞 Frische Reifen für das nächste Monster",
    "🚔 Bitte keine illegalen Straßenrennen 😶",
    "💥 Auspuff klingt wieder viel zu krank",
    "🏎️ EAST Customs liefert reine Power",
    "🔩 Schrauben locker? EAST fixt das",
    "🚗 Der nächste Widebody ist fast fertig",
    "🔥 EAST Customs bringt die Straßen zum beben",
    "💨 Turbo + Popcorn Mapping aktiviert",
    "⚙️ Performance zuerst – alles andere später",
    "🎁 Heute Rabatt auf IC-Umbauten bei EAST Customs",
]

async def rotate_status():
    await bot.wait_until_ready()
    while not bot.is_closed():
        status = random.choice(statuses)
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=status
            )
        )
        await asyncio.sleep(30)

# ──────────────────────────────────────────────
# 👋 WILLKOMMEN SYSTEM
# ──────────────────────────────────────────────

@bot.event
async def on_member_join(member):

    channel = member.guild.get_channel(WELCOME_CHANNEL_ID)

    if channel:
        embed = discord.Embed(
            title="🚗 Willkommen bei EAST Customs",
            description=(
                f"Willkommen {member.mention} auf dem Server! 🔥\n\n"
                f"Schau dich um, stell deine Fragen und werde Teil der EAST Customs Family."
            ),
            color=discord.Color.gold()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text="EAST Customs | FiveM Werkstatt")
        await channel.send(embed=embed)

    log_channel = member.guild.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        embed = discord.Embed(
            title="📥 Member beigetreten",
            description=f"{member} (`{member.id}`) ist dem Server beigetreten.",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Account erstellt: {member.created_at.strftime('%d.%m.%Y')}")
        await log_channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    log_channel = member.guild.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        embed = discord.Embed(
            title="📤 Member verlassen",
            description=f"{member} (`{member.id}`) hat den Server verlassen.",
            color=discord.Color.red()
        )
        await log_channel.send(embed=embed)

# ──────────────────────────────────────────────
# 🎫 TICKET SYSTEM
# ──────────────────────────────────────────────

class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="🔒 Ticket schließen",
        style=discord.ButtonStyle.danger,
        custom_id="close_ticket"
    )
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel = interaction.channel

        log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(
                title="🔒 Ticket geschlossen",
                description=(
                    f"Ticket **{channel.name}** wurde von "
                    f"{interaction.user.mention} geschlossen."
                ),
                color=discord.Color.dark_red()
            )
            await log_channel.send(embed=embed)

        await interaction.response.send_message("🔒 Ticket wird geschlossen...")
        await asyncio.sleep(3)
        await channel.delete()


class TicketPanel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="💸 Rabatt",
        style=discord.ButtonStyle.success,
        custom_id="ticket_rabatt"
    )
    async def rabatt(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, "rabatt")

    @discord.ui.button(
        label="❓ Fragen",
        style=discord.ButtonStyle.primary,
        custom_id="ticket_fragen"
    )
    async def fragen(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, "fragen")

    @discord.ui.button(
        label="🛠️ Sonstiges",
        style=discord.ButtonStyle.secondary,
        custom_id="ticket_sonstiges"
    )
    async def sonstiges(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, "sonstiges")

    @discord.ui.button(
        label="📋 Bewerbung",
        style=discord.ButtonStyle.danger,
        custom_id="ticket_bewerbung"
    )
    async def bewerbung(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction, "bewerbung")


async def create_ticket(interaction: discord.Interaction, typ: str):
    guild = interaction.guild
    member = interaction.user
    support_role = guild.get_role(SUPPORT_ROLE_ID)

    existing = discord.utils.get(guild.text_channels, name=f"{typ}-{member.name.lower()}")
    if existing:
        await interaction.response.send_message(
            f"❌ Du hast bereits ein offenes {typ}-Ticket: {existing.mention}",
            ephemeral=True
        )
        return

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
    }
    if support_role:
        overwrites[support_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

    channel = await guild.create_text_channel(
        name=f"{typ}-{member.name}",
        category=guild.get_channel(TICKET_CATEGORY_ID),
        overwrites=overwrites
    )

    descriptions = {
        "rabatt": (
            f"Hey {member.mention}! 💸\n\n"
            "Schreib uns kurz:\n"
            "**1.** Welches Auto / Welche Dienstleistung?\n"
            "**2.** Warum möchtest du einen Rabatt?\n"
            "**3.** Dein FiveM Name"
        ),
        "fragen": (
            f"Hey {member.mention}! ❓\n\n"
            "Stell deine Frage – das Team meldet sich so schnell wie möglich."
        ),
        "sonstiges": (
            f"Hey {member.mention}! 🛠️\n\n"
            "Beschreibe dein Anliegen so genau wie möglich.\n"
            "Wir helfen dir weiter!"
        ),
        "bewerbung": (
            f"Hey {member.mention}! 📋\n\n"
            "Bitte beantworte folgende Fragen:\n"
            "**1.** Dein FiveM Name?\n"
            "**2.** Wie alt bist du?\n"
            "**3.** Wie lange spielst du schon auf dem Server?\n"
            "**4.** Warum willst du bei EAST Customs arbeiten?\n"
            "**5.** Was bringst du mit?"
        ),
    }

    embed = discord.Embed(
        title=f"🎫 {typ.capitalize()} Ticket",
        description=descriptions.get(typ, f"Hallo {member.mention}, beschreibe dein Anliegen."),
        color=discord.Color.blurple()
    )
    embed.set_footer(text="EAST Customs | Ticket System")

    await channel.send(
        content=f"{member.mention}" + (f" | {support_role.mention}" if support_role else ""),
        embed=embed,
        view=CloseTicketView()
    )

    await interaction.response.send_message(
        f"✅ Dein Ticket wurde erstellt: {channel.mention}",
        ephemeral=True
    )

    log_channel = guild.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        embed = discord.Embed(
            title="🎫 Ticket erstellt",
            description=f"{member.mention} hat ein **{typ}** Ticket geöffnet → {channel.mention}",
            color=discord.Color.orange()
        )
        await log_channel.send(embed=embed)


@bot.tree.command(name="ticket-panel", description="Sendet das Ticket Panel")
@app_commands.checks.has_permissions(administrator=True)
async def ticket_panel(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎫 EAST Customs Support",
        description=(
            "Brauchst du Hilfe oder hast eine Frage?\n"
            "Wähle unten die passende Kategorie aus!\n\n"
            "💸 **Rabatt** – Fragen zu Rabatten & Angeboten\n"
            "❓ **Fragen** – Allgemeine Fragen zum Shop\n"
            "🛠️ **Sonstiges** – Alles andere\n"
            "📋 **Bewerbung** – Bewirb dich bei EAST Customs"
        ),
        color=discord.Color.gold()
    )
    embed.set_footer(text="EAST Customs | FiveM Werkstatt")
    await interaction.channel.send(embed=embed, view=TicketPanel())
    await interaction.response.send_message("✅ Ticket Panel gesendet.", ephemeral=True)

# ──────────────────────────────────────────────
# 📢 ANKÜNDIGUNGEN
# ──────────────────────────────────────────────

@bot.tree.command(name="an", description="Sende eine Ankündigung")
@app_commands.describe(text="Deine Ankündigung")
@app_commands.checks.has_permissions(administrator=True)
async def an(interaction: discord.Interaction, text: str):
    channel = interaction.guild.get_channel(ANNOUNCEMENT_CHANNEL_ID)

    if not channel:
        await interaction.response.send_message("❌ Ankündigungs-Channel nicht gefunden.", ephemeral=True)
        return

    embed = discord.Embed(
        title="📢 EAST Customs",
        description=text,
        color=discord.Color.gold()
    )
    embed.set_footer(text=f"EAST Customs | {interaction.user.display_name}")

    await channel.send(content="@everyone", embed=embed)
    await interaction.response.send_message("✅ Ankündigung gesendet.", ephemeral=True)

    log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        embed2 = discord.Embed(
            title="📢 Ankündigung gesendet",
            description=f"{interaction.user.mention} hat eine Ankündigung gemacht.\n\n>>> {text[:500]}",
            color=discord.Color.blue()
        )
        await log_channel.send(embed=embed2)

# ──────────────────────────────────────────────
# 💀 ANTISPAM SYSTEM
# ──────────────────────────────────────────────

user_messages: dict[int, list[float]] = {}

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    user_id = message.author.id
    now = time.time()

    if user_id not in user_messages:
        user_messages[user_id] = []

    user_messages[user_id].append(now)
    user_messages[user_id] = [t for t in user_messages[user_id] if now - t < 8]

    if len(user_messages[user_id]) >= 5:
        await message.channel.send(
            f"{message.author.mention} 🚨 Chill Bruder, der Chat läuft nicht weg 💀"
        )

        log_channel = message.guild.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(
                title="💀 Spam erkannt",
                description=(
                    f"{message.author.mention} (`{message.author.id}`) hat gespammt "
                    f"in {message.channel.mention}."
                ),
                color=discord.Color.red()
            )
            await log_channel.send(embed=embed)

        user_messages[user_id] = []

    await bot.process_commands(message)

# ──────────────────────────────────────────────
# ✅ BOT READY
# ──────────────────────────────────────────────

@bot.event
async def on_ready():
    bot.add_view(TicketPanel())
    bot.add_view(CloseTicketView())
    await bot.tree.sync()
    print(f"✅ EAST Customs Bot online als {bot.user}")
    bot.loop.create_task(rotate_status())

# ──────────────────────────────────────────────
# 🚀 BOT STARTEN
# ──────────────────────────────────────────────

bot.run(BOT_TOKEN)
