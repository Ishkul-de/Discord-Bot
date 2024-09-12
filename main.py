from thetoken import TOKEN
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

# Intents aktivieren, um Nachrichteninhalte und Mitglieder-Events zu erhalten
intents = discord.Intents.default()
intents.members = True  # Mitglieder-Ereignisse
intents.message_content = True  # Nachrichteninhalte

# Bot-Objekt mit Präfix und allen Intents
client = commands.Bot(command_prefix="!", intents=intents)

# Event, das ausgeführt wird, wenn der Bot bereit ist
@client.event
async def on_ready():
    print('The bot is now ready for use!')
    print('-----------------------------')

# bei !Hallo soll begrüßen
@client.command()
async def hallo(ctx):
    await ctx.send("Hello, I am the bot!")

@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has been kicked')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission for this")

@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'User {member} has been banned')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission for this")

# Event, das ausgeführt wird, wenn ein neues Mitglied dem Server beitritt
@client.event
async def on_member_join(member):
    # Begrüßungsnachricht an den Benutzer privat senden
    await member.send("Hello and welcome to the server!")
    
    # Channel-ID, in dem die Begrüßungsnachricht gesendet werden soll 
    channel_id = 1282636264608235565  # channel id
    channel = client.get_channel(channel_id)
    
    # Überprüfen, ob der Channel existiert
    if channel is not None:
        # Begrüßungsnachricht in den Channel senden
        await channel.send(f"Welcome to the server, {member.display_name}!")

@client.event 
async def on_member_remove(member):
    channel = client.get_channel(1282636264608235565)
    await channel.send(f"Goodbye, {member.display_name}!")

@client.event
async def on_message(message):
    # Verhindern, dass der Bot auf eigene Nachrichten reagiert
    if message.author == client.user:
        return

    # Liste der Schimpfwörter
    cursewords = [
    # Deutsch
    "poop", "poo", "abschaum", "affenschwanz", "ah du schwein", "alter muschi", "alter wichser",
    "am blitz geleckt haben", "analritter", "arsch", "arschficker", "arschfotze", "arschgeige",
    "arschgesicht", "arschkeks", "arschkriecher", "arschlecker", "arschloch", "auberfeiger",
    "aufgeilen", "backpfeifengesicht", "bastard", "bimbo", "blöde gans", "blöde stinkpot",
    "blödmann", "blödsinn", "bloede kuh", "blutige sau", "blvde fotze", "bonze", "bratze",
    "bruchbude", "bumsen", "das arschloch", "das ist mir scheißegal", "das miststück", "das schwein",
    "depp", "der dreckskerl", "der fotzenlecker", "der mist", "der mistkerl", "der wichser",
    "die drecksau", "die sau", "die verarsche", "dödel", "donnerwetter", "dreckige hure",
    "drecksack", "drecksau", "dreckskerl", "drecksnest", "du bastard", "du blöde kuh", "du fickfehler",
    "du hurensohn", "du sau", "du schwein", "du weichei", "dummbatz", "dumme", "dumme kuh",
    "dumme nuss", "dummkopf", "dumpfbacke", "erarschen", "fahr zur holle", "feigling", "fick",
    "fick deine mutter", "fick dich", "fick dich arschloch", "fick dich ins knie", "ficke", "ficken",
    "ficker", "filzlaus", "flachwichser", "flittchen", "fotze", "fratze", "geh zum teufel",
    "gottverdammt", "hackfresse", "halt deinen mund", "halt die fotze", "halt die klappe",
    "hat jemand dir ins gehirn geschissen", "hirnrissig", "homo", "hosenscheisser", "huhrensohn", "hure",
    "huren", "huren sohn", "hurensohn", "ich ficke deine mutter", "ich ficke deine schwester",
    "ich hasse dich", "ich will dich ficken", "ich will ficken", "idiot", "ische", "kackbratze",
    "kacke", "kacken", "kackwurst", "kampflesbe", "kanake", "kimme", "klugscheißer", "küss meinen arsch",
    "lech mien arsch", "leck mich", "leck mich am arsch", "lesbe", "lick", "lms", "lümmel", "lusche",
    "lutsch mein schwanz", "lutsch meine eier", "lutschen", "milf", "mist", "miststück", "möpse",
    "morgenlatte", "möse", "mufti", "muschi", "muschi lecker", "mutterficker", "nackt", "neger",
    "nigger", "nippel", "nutte", "ohne scheiß", "onanieren", "orgasmus", "penis", "penner", "pimmel",
    "pimpern", "pinkeln", "pisse", "pissen", "pisser", "popel", "poppen", "porno", "puff", "quatsch",
    "reudig", "rosette", "saugen", "schabracke", "scheiss", "scheissdreck", "scheisse", "scheiße",
    "scheissekopf", "scheissen", "scheisser", "scheisskerl", "scheisskopf", "schiesser", "schlampe",
    "schnackeln", "schnoodle noodle", "schwanz", "schwanzlutscher", "schweinebacke", "schweinehund",
    "schwuchtel", "schwuchtl", "shaisa", "sheisse", "sohn einer hündin", "spasti", "spießig",
    "spinnen", "spinner", "spinnst", "teufel", "tittchen", "titten", "trottel", "verdammt",
    "verdammte scheiße", "verdammter", "verdammter Scheiß", "verfluchter", "verpiss dich", "verrückter mann",
    "vögeln", "vollidiot", "vollpfosten", "vollscheißen", "volltrottel", "was zum teufel",
    "was zur hölle", "weichei", "wichse", "wichsen", "wichser", "witzbold", "zicke", "zur holle mit dir",

    # English
    "arse", "arsehole", "as useful as tits on a bull", "balls", "bastard", "beaver", "beef curtains",
    "bell", "bellend", "bent", "berk", "bint", "bitch", "blighter", "blimey", "blimey o'reilly",
    "bloodclaat", "bloody", "bloody hell", "blooming", "bollocks", "bonk", "bugger", "bugger me",
    "bugger off", "built like a brick shit-house", "bukkake", "bullshit", "cack", "cad", "chav",
    "cheese eating surrender monkey", "choad", "chuffer", "clunge", "cobblers", "cock", "cock cheese",
    "cock jockey", "cock-up", "cocksucker", "cockwomble", "codger", "cor blimey", "corey", "cow",
    "crap", "crikey", "cunt", "daft", "daft cow", "damn", "dick", "dickhead", "did he bollocks!",
    "did i fuck as like!", "dildo", "dodgy", "duffer", "fanny", "feck", "flaps", "fuck", "fuck me sideways!",
    "fucking cunt", "fucktard", "gash", "ginger", "git", "gob shite", "goddam", "gorblimey",
    "gordon bennett", "gormless", "he’s a knob", "hell", "hobknocker", "I'd rather snort my own cum",
    "jesus christ", "jizz", "knob", "knobber", "knobend", "knobhead", "ligger", "like fucking a dying man's handshake",
    "mad as a hatter", "manky", "minge", "minger", "minging", "motherfucker", "munter", "muppet", "naff",
    "nitwit", "nonce", "numpty", "nutter", "off their rocker", "penguin", "pillock", "pish", "piss off",
    "piss-flaps", "pissed", "pissed off", "play the five-fingered flute", "plonker", "ponce", "poof",
    "pouf", "poxy", "prat", "prick", "prickteaser", "punani", "punny", "pussy", "randy", "rapey",
    "rat arsed", "rotter", "rubbish", "scrubber", "shag", "shit", "shite", "shitfaced", "skank", "slag",
    "slapper", "slut", "snatch", "sod", "sod-off", "son of a bitch", "spunk", "stick it up your arse!",
    "swine", "taking the piss", "tart", "tits", "toff", "tosser", "trollop", "tuss", "twat", "twonk",
    "u fukin wanker", "wally", "wanker", "wankstain", "wazzack", "whore",
    "poop", "poo", "abschaum", "affenschwanz", "ah du schwein", "alter muschi", "alter wichser",
    "am blitz geleckt haben", "analritter", "arsch", "arschficker", "arschfotze", "arschgeige",
    "arschgesicht", "arschkrampe", "arschloch", "arschlöcher", "arschritze", "asylant",
    "axt im walde", "backfisch", "bauernlümmel", "beleidigte leberwurst", "bimbo", "blödmann",
    "braune brut", "bück dich", "bück dich hoch", "dachpappe", "dämliche drecksau",
    "dämliche pute", "dämlicher mistkäfer", "deppenhirn", "deppenschädel", "dödel", "dreckfink",
    "drecksau", "dreckschwein", "dumme drecksau", "dumme pute", "dummer mistkäfer",
    "durch den kakao gezogen", "durchfallhirn", "einfaltspinsel", "fick dich", "fick dich hart",
    "fick dich ins knie", "fick dich selbst", "fickfotze", "fickfresse", "ficker", "flachwichser",
    "fotzenlecker", "fotzenpisser", "fotzensohn", "gänsebrust", "gänserich", "geisteskranker",
    "gesichtsgrätsche", "hackfresse", "hakenkreuzträger", "halbschwanz", "hampelmann",
    "hinterwäldler", "hirnamputiert", "hodenlecker", "hurenbock", "hurensohn", "idiot", "in den arsch",
    "ischlampe", "judenschwein", "kanacke", "klofrau", "klolecker", "klugscheißer", "kollateralschaden",
    "kopp zu", "krankenhaus reif", "krüppel", "lutsch mein schwanz", "lümmel", "made", "miethure",
    "missgeburt", "mösenlecker", "muschifotze", "muschihaare", "nazischwein", "neger",
    "notgeil", "ochsenfrosch", "opfer", "penner", "pimmel", "pimmelficker", "pimmelkopp", "pisser",
    "pissflitsche", "pissnelke", "puffgänger", "ranzhirn", "rudelficker", "saftsack", "sau", "saupreuß",
    "scheißbirne", "scheiße", "scheißendreck", "scheißer", "schlampe", "schleimscheißer", "schwanz",
    "schwanzkopf", "schwanzlutscher", "schweinepriester", "sippenficker", "spast", "spastiker",
    "spatzenhirn", "untermensch", "vollpfosten", "wichsarsch", "wichsfresse", "wichser", "ziegenficker",
    "zipfelklatscher", "zonenwachtel",
    
    # Englische Schimpfwörter
    "fuck", "shit", "bastard", "asshole", "dumbass", "motherfucker", "dick", "dickhead", 
    "pussy", "slut", "whore", "bitch", "fucker", "jerk", "crap", "bollocks", "damn", "hell", 
    "cunt", "wanker", "twat", "prick", "shithead", "butthole", "arsehole", "douche", "douchebag", 
    "jackass", "idiot", "moron", "dumb", "loser", "sucker", "retard", "freak", "wimp", "chump", 
    "dipshit", "piss", "scumbag", "trash", "dickwad", "balls", "turd"

]


    # Überprüfen, ob die Nachricht ein Schimpfwort enthält
    for wort in cursewords:
        if wort in message.content.lower():
            await message.delete()
            await message.channel.send(f"{message.author.mention} keine bösen Wörter erlaubt!")
            break

    # Process commands if any
    await client.process_commands(message)

# Bot starten
client.run(TOKEN)
