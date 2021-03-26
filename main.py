# Il PeggioBot
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import keep_alive
import random
import asyncio
import variabili
from replit import db
import shlex
import typing

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=['! ', '!'], case_insensitive=True)


@bot.event
async def on_ready():
    print('Bot is ready!')


# aliases: lista di comandi che triggerano la funzione
@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')


@bot.command()
async def allineamento(ctx, *, messaggio=None):
    if messaggio:
        legge_caos = random.choice(variabili.legge_caos)
        bene_male = random.choice(variabili.bene_male)
        if legge_caos == bene_male == 'Neutrale':
            allineamento = 'Neutrale Puro'
        else:
            allineamento = legge_caos + ' ' + bene_male
        msg_out = f'L\'allineamento di {messaggio} è: {allineamento}.'

    else:
        msg_out = "Non so chi devo allineare."

    await ctx.send(msg_out)


@bot.command()
async def hug(ctx, *, arg: typing.Union[discord.Member, str] = None):
    if arg:
        if isinstance(arg, str):
            if arg == '@everyone':
                msg = f'{ctx.author.display_name} {random.choice(variabili.abbracci_tutti)}'
            else:
                msg = 'Non ho capito... :('
        else:
            msg = f'{ctx.author.display_name} ha mandato un abbraccio a {arg.mention}. {random.choice(variabili.abbracci)}'
    else:
        msg = f'Non mi hai detto chi vuoi abbracciare, quindi abbraccio te, {ctx.author.mention} :3'
    await ctx.send(msg)


@bot.command()
async def palla8(ctx, *, domanda=None):
    risposte = variabili.palla8
    if domanda:
        await ctx.send(
            f'**Domanda:** {domanda}\n**Risposta:** {random.choice(risposte)}, {ctx.author.display_name}'
        )
    else:
        await ctx.send(
            f'Non mi hai fatto la domanda, {ctx.author.display_name} >.<')


@bot.command()
async def nando(ctx, *, comando=None):
    flag = True
    if comando:
        comando = shlex.split(comando)
        if comando[0] == "aggiungi":
            parola = comando[2]
            if comando[1] == "soggetto":
                parola = parola[:1].upper() + parola[1:]
                if "soggetti" in db.keys():
                    soggetti = db["soggetti"]
                    if parola in soggetti:
                        await ctx.send('Hey, questo soggetto c\'è già!')
                        flag = not flag
                    else:
                        soggetti.append(parola)
                    db["soggetti"] = soggetti
                else:
                    db["soggetti"] = [parola]

            if comando[1] == "verbo":
                if "verbi" in db.keys():
                    verbi = db["verbi"]
                    if parola in verbi:
                        await ctx.send('Hey, questo verbo c\'è già!')
                        flag = not flag
                    else:
                        verbi.append(parola)
                    db["verbi"] = verbi
                else:
                    db["verbi"] = [parola]
            if comando[1] == "complemento":
                if "complementi" in db.keys():
                    complementi = db["complementi"]
                    if parola in complementi:
                        await ctx.send('Hey, questo complemento c\'è già!')
                        flag = not flag
                    else:
                        complementi.append(parola)
                    db["complementi"] = complementi
                else:
                    db["complementi"] = [parola]
            if flag:
              await ctx.send(f'*{parola}* aggiunto come *{comando[1]}*!')

        if comando[0] == "rimuovi":
            parola = comando[2]
            if comando[1] == "soggetto":
                soggetti = db['soggetti']
                try:
                    indice = soggetti.index(parola)
                    del soggetti[indice]
                    db['soggetti'] = soggetti
                    await ctx.send(f'Ho eliminato *{parola}*!')
                except ValueError:
                    await ctx.send(f'Non ho trovato la parola *{parola}*!')
            if comando[1] == "verbo":
                verbi = db['verbi']
                try:
                    indice = verbi.index(parola)
                    del verbi[indice]
                    db['verbi'] = verbi
                    await ctx.send(f'Ho eliminato *{parola}*!')
                except ValueError:
                    await ctx.send(f'Non ho trovato la parola *{parola}*!')
            if comando[1] == "complemento":
                complementi = db['complementi']
                try:
                    indice = complementi.index(parola)
                    del complementi[indice]
                    db['complementi'] = complementi
                    await ctx.send(f'Ho eliminato *{parola}*!')
                except ValueError:
                    await ctx.send(f'Non ho trovato la parola *{parola}*!')

        elif comando[0] == "lista":
            soggetti = variabili.soggetti
            if "soggetti" in db.keys():
                soggetti = soggetti + db["soggetti"]

            verbi = variabili.verbi
            if "verbi" in db.keys():
                verbi = verbi + db["verbi"]

            complementi = variabili.complementi
            if "complementi" in db.keys():
                complementi = complementi + db["complementi"]

            await ctx.send(f'**Soggetti:** {sorted(soggetti)}')
            await ctx.send(f'**Verbi:** {sorted(verbi)}')
            await ctx.send(f'**Complementi:** {sorted(complementi)}')
            await ctx.send(
                f'Per aggiungere elementi, usare il comando `!nando aggiungi soggetto|verbo|complemento \"elemento da inserire\"`\nPer rimuovere elementi, usare il comando `!nando rimuovi soggetto|verbo|complemento \"elemento da rimuovere\"`'
            )

    else:
        soggetti = variabili.soggetti
        if "soggetti" in db.keys():
            soggetti = soggetti + db["soggetti"]

        verbi = variabili.verbi
        if "verbi" in db.keys():
            verbi = verbi + db["verbi"]

        complementi = variabili.complementi
        if "complementi" in db.keys():
            complementi = complementi + db["complementi"]

        soggetto_sceltoA = random.choice(soggetti)
        soggetto_scelto = soggetto_sceltoA[:1].upper() + soggetto_sceltoA[1:]
        verbo_scelto = random.choice(verbi)
        complemento_scelto = random.choice(complementi)
        nandata = f'{soggetto_scelto} {verbo_scelto} {complemento_scelto}'

        if ' di il ' in nandata:
            nandata = nandata.replace(' di il ', ' del ')
        if ' di lo ' in nandata:
            nandata = nandata.replace(' di lo ', ' dello ')
        if ' di la ' in nandata:
            nandata = nandata.replace(' di la ', ' della ')
        if ' di i ' in nandata:
            nandata = nandata.replace(' di i ', ' dei ')
        if ' di gli ' in nandata:
            nandata = nandata.replace(' di gli ', ' degli ')
        if ' di le ' in nandata:
            nandata = nandata.replace(' di le ', ' delle ')
        if ' di l\'' in nandata:
            nandata = nandata.replace(' di l\'', ' dell\'')
        if ' a il ' in nandata:
            nandata = nandata.replace(' a il ', ' al ')
        if ' a lo ' in nandata:
            nandata = nandata.replace(' a lo ', ' allo ')
        if ' a la ' in nandata:
            nandata = nandata.replace(' a la ', ' alla ')
        if ' a i ' in nandata:
            nandata = nandata.replace(' a i ', ' ai ')
        if ' a gli ' in nandata:
            nandata = nandata.replace(' a gli ', ' agli ')
        if ' a le ' in nandata:
            nandata = nandata.replace(' a le ', ' alle ')
        if ' a l\'' in nandata:
            nandata = nandata.replace(' a l\'', ' all\'')
        if ' da il ' in nandata:
            nandata = nandata.replace(' da il ', ' dal ')
        if ' da lo ' in nandata:
            nandata = nandata.replace(' da lo ', ' dallo ')
        if ' da la ' in nandata:
            nandata = nandata.replace(' da la ', ' dalla ')
        if ' da i ' in nandata:
            nandata = nandata.replace(' dai ', ' dai ')
        if ' da gli ' in nandata:
            nandata = nandata.replace(' da gli ', ' dagli ')
        if ' da le ' in nandata:
            nandata = nandata.replace(' da le ', ' dalle ')
        if ' in il ' in nandata:
            nandata = nandata.replace(' in il ', ' nel ')
        if ' in lo ' in nandata:
            nandata = nandata.replace(' in lo ', ' nello ')
        if ' in la ' in nandata:
            nandata = nandata.replace(' in la ', ' nella ')
        if ' in i ' in nandata:
            nandata = nandata.replace(' in i ', ' nei ')
        if ' in gli ' in nandata:
            nandata = nandata.replace(' in gli ', ' negli ')
        if ' in le ' in nandata:
            nandata = nandata.replace(' in le ', ' nelle ')
        if ' in l\'' in nandata:
            nandata = nandata.replace(' in l\'', ' nell\'')
        if ' con il ' in nandata:
            nandata = nandata.replace(' con il ', ' col ')
        if ' con i ' in nandata:
            nandata = nandata.replace(' con i ', ' coi ')
        if ' su il ' in nandata:
            nandata = nandata.replace(' su il ', ' sul ')
        if ' su lo ' in nandata:
            nandata = nandata.replace(' su lo ', ' sullo ')
        if ' su la ' in nandata:
            nandata = nandata.replace(' su la ', ' sulla ')
        if ' su i ' in nandata:
            nandata = nandata.replace(' su i ', ' sui ')
        if ' su gli ' in nandata:
            nandata = nandata.replace(' su gli ', ' sugli ')
        if ' su le ' in nandata:
            nandata = nandata.replace(' su le ', ' sulle ')
        if ' ,' in nandata:
            nandata = nandata.replace(' ,', ',')

        await ctx.send(nandata)

        if str.lower(soggetto_scelto) == 'non è homo se':
            if "nohomo" in db.keys():
                nohomo = db["nohomo"]
                nohomo.append(nandata)
                db["nohomo"] = nohomo
            else:
                db["nohomo"] = [nandata]
            await ctx.send('Aggiunto alla lista delle regole no homo!')


@bot.command()
async def nohomo(ctx, *, comando=None):
    if comando:
        comando = shlex.split(comando)
        if comando[0] == "aggiungi":
            fraseA = comando[1]
            frase = fraseA[:1].upper() + frase[1:]
            if "nohomo" in db.keys():
                nohomo_db = db["nohomo"]
                nohomo_db.append(frase)
                db["nohomo"] = nohomo_db
            else:
                db["nohomo"] = [frase]
            await ctx.send(f'Ho aggiunto *{frase}*!')

        if comando[0] == "rimuovi":
            frase = comando[1]
            nohomo_db = db['nohomo']
            try:
                indice = nohomo_db.index(frase)
                del nohomo_db[indice]
                db['nohomo'] = nohomo_db
                await ctx.send(f'Ho eliminato *{frase}*!')
            except ValueError:
                await ctx.send(f'Non ho trovato la frase *{frase}*!')

        if comando[0] == 'lista':
            nohomo_rules = variabili.nohomo
            if "nohomo" in db.keys():
                nohomo_rules = nohomo_rules + db["nohomo"]
            await ctx.send(sorted(nohomo_rules))

    else:
        nohomo_rules = variabili.nohomo
        if "nohomo" in db.keys():
            nohomo_rules = nohomo_rules + db["nohomo"]

        nohomo_outA = random.choice(nohomo_rules)
        nohomo_out = nohomo_outA[:1].upper() + nohomo_outA[1:]
        await ctx.send(f'Il saggio dice:\n*{nohomo_out}*')


@bot.listen('on_message')
async def hey_bot(message):
    if message.author == bot.user:
        return

    msg = message.content.lower()
    if msg.startswith('hey bot') or msg.startswith('hey culo'):
        if message.author.name == "Rufus Loacker":
            response = "Hey papà!"
        elif message.author.name == "Kanmuri":
            response = "Hey admin del mondo!"
        elif message.author.name == "CowardKnight":
            response = "Hey persona con gatti belli!"
        else:
            response = f'Hey {message.author.display_name}!'
        await message.channel.send(response)


@bot.command()
async def indovina(ctx):
    await ctx.send(
        "Scegli un numero fra 1 e 10. Hai 15 secondi per indovinare!")

    # generates a random number and turns it into a string
    number = random.randint(1, 10)
    print(number)
    tries = 0
    smartass_lvl = 0

    while tries < 3:

        def check(m):
            return m.channel == ctx.channel

        try:
            messaggio = await bot.wait_for('message', check=check, timeout=15)
            try:
                msg_numero = int(messaggio.content)
                if msg_numero == number:
                    risposta = f'Hai indovinato il numero, {messaggio.author.display_name}!'
                    await ctx.send(risposta)
                    break
                elif msg_numero < number:
                    tries += 1
                    risposta = f'Il numero che hai scelto è troppo basso, ti rimangono {3-tries} tentativi'
                elif msg_numero > number and msg_numero <= 10:
                    tries += 1
                    risposta = f'Il numero che hai scelto è troppo alto, ti rimangono {3-tries} tentativi'
                elif msg_numero > 10:
                    risposta = "Leggi meglio le regole..."

            except:
                if smartass_lvl == 0:
                    risposta = "In numero, non in parola >.<"
                    smartass_lvl += 1
                elif smartass_lvl == 1:
                    risposta = "Hey, te l'ho già detto, in numero!"
                    smartass_lvl += 1
                elif smartass_lvl == 2:
                    risposta = "Non voglio dirtelo un'altra volta..."
                    smartass_lvl += 1
                else:
                    risposta = f'Mo però me so rotto i coglioni eh. Il numero era {number}.'
                    await ctx.send(risposta)
                    break

            await ctx.send(risposta)

        except asyncio.TimeoutError:
            risposta = f'Tempo scaduto! Il numero era {number}'
            await ctx.send(risposta)
            break

    await ctx.send("Grazie per aver giocato :)")


keep_alive.keep_alive()
bot.run(TOKEN)
