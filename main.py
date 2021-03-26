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

# FLAG globali
flagDuplicato = False
flagEliminazione = True


@bot.event
async def on_ready():
	print('Bot is ready!')


# aliases: lista di comandi che triggerano la funzione
@bot.command()
async def ping(ctx):
	await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')


@bot.command()
async def allineamento(ctx, *, messaggio_in=None):
	global flagDuplicato
	global flagEliminazione

	flagDuplicato = False
	flagEliminazione = True

	if messaggio_in:
		messaggio = shlex.split(messaggio_in)
		comando = messaggio[0]
		if comando == "aggiungi":
			subcomando = messaggio[1]
			parola = messaggio[2]
			if subcomando == "bene" or subcomando == "legge":
				aggiungi_nandata(ctx, subcomando, parola)
			else:
				await ctx.send('Non conosco il comando :(')
				flagDuplicato = not flagDuplicato

			if not flagDuplicato:
				msg_out = f'*{parola}* aggiunto come allineamento!'
			else:
				msg_out = f'Hey, questo allineamento c\'è già!'

		elif comando == "rimuovi":
			subcomando = messaggio[1]
			parola = messaggio[2]
			if subcomando == "bene" or subcomando == "legge":
				rimuovi_nandata(ctx, subcomando, parola)
			else:
				await ctx.send('Non conosco il comando :(')
				flagDuplicato = not flagDuplicato
				
			if flagEliminazione:
				msg_out = f'Ho eliminato *{parola}*!'
			else:
				msg_out = f'Non ho trovato *{parola}*!'

		else:
			legge_caos = variabili.legge_caos
			if "legge" in db.keys():
				legge_caos = legge_caos + db["legge"]

			bene_male = variabili.bene_male
			if "bene" in db.keys():
				bene_male = bene_male + db["bene"]

			legge_caos_scelta = random.choice(legge_caos)
			bene_male_scelta = random.choice(bene_male)
			if legge_caos_scelta == bene_male_scelta == 'Neutrale':
				allineamento = 'Neutrale Puro'
			else:
				allineamento = legge_caos_scelta + ' ' + bene_male_scelta
			msg_out = f'L\'allineamento di {messaggio_in} è: {allineamento}.'

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

def aggiungi_nandata(ctx, comando_in, parola):
	global flagDuplicato
	if ctx.invoked_with != 'allineamento':
		nome_db = comando_in[:-1] + comando_in[-1].replace('o', 'i')
	else:
		nome_db = comando_in
	parola_interna = parola
	if nome_db in db.keys():
		database = db[nome_db]
		if parola_interna in database:
			flagDuplicato = not flagDuplicato
		else:
			database.append(parola_interna)
	else:
		database = [parola_interna]
	db[nome_db] = database

def rimuovi_nandata(ctx, comando_in, parola):
	global flagEliminazione
	if ctx.invoked_with != 'allineamento':
		nome_db = comando_in[:-1] + comando_in[-1].replace('o', 'i')
	else:
		nome_db = comando_in
	parola_interna = parola
	database = db[nome_db]
	try:
		indice = database.index(parola_interna)
		del database[indice]
		db[nome_db] = database
	except ValueError:
		flagEliminazione = not flagEliminazione

def costruisci_liste():
	contesti = variabili.contesti
	if "contesti" in db.keys():
		contesti = contesti + db["contesti"]

	soggetti = variabili.soggetti
	if "soggetti" in db.keys():
		soggetti = soggetti + db["soggetti"]

	verbi = variabili.verbi
	if "verbi" in db.keys():
		verbi = verbi + db["verbi"]

	complementi = variabili.complementi
	if "complementi" in db.keys():
		complementi = complementi + db["complementi"]
	
	return contesti, soggetti, verbi, complementi

@bot.command()
async def nando(ctx, *, messaggio_in=None):
	global flagDuplicato
	global flagEliminazione

	flagDuplicato = False
	flagEliminazione = True

	if messaggio_in:
		messaggio = shlex.split(messaggio_in)
		comando = messaggio[0]
		if comando == "aggiungi":
			subcomando = messaggio[1]
			parola = messaggio[2]
			if subcomando == "soggetto" or subcomando == "verbo" or subcomando == "complemento" or subcomando == "contesto":
				aggiungi_nandata(ctx, subcomando, parola)
			else:
				await ctx.send('Non conosco il comando :(')
				flagDuplicato = not flagDuplicato

			if not flagDuplicato:
				await ctx.send(f'*{parola}* aggiunto come *{subcomando}*!')
			else:
				await ctx.send(f'Hey, questo {subcomando} c\'è già!')

		elif comando == "rimuovi":
			subcomando = messaggio[1]
			parola = messaggio[2]
			if subcomando == "soggetto" or subcomando == "verbo" or subcomando == "complemento" or subcomando == "contesto":
				rimuovi_nandata(ctx, subcomando, parola)
			else:
				await ctx.send('Non conosco il comando :(')
				flagEliminazione = not flagEliminazione
			
			if flagEliminazione:
				await ctx.send(f'Ho eliminato *{parola}*!')
			else:
				await ctx.send(f'Non ho trovato *{parola}*!')

		elif comando == "lista":
			contesti, soggetti, verbi, complementi = costruisci_liste()

			await ctx.send(f'**Contesti:** {sorted(contesti)}')
			await ctx.send(f'**Soggetti:** {sorted(soggetti)}')
			await ctx.send(f'**Verbi:** {sorted(verbi)}')
			await ctx.send(f'**Complementi:** {sorted(complementi)}')
			await ctx.send(
					f'Per aggiungere elementi, usare il comando `!nando aggiungi soggetto|verbo|complemento \"elemento da inserire\"`\nPer rimuovere elementi, usare il comando `!nando rimuovi soggetto|verbo|complemento \"elemento da rimuovere\"`'
					)			
		elif comando == "stats":
			contesti, soggetti, verbi, complementi = costruisci_liste()
			combinazioni = len(contesti) * len(soggetti) * len(verbi) * len(complementi)

			if 'nandate' in db.keys():
				num_nandate = db['nandate']
			else:
				num_nandate = 0
			await ctx.send(f'**Contesti:** {len(contesti):,}\n**Soggetti:** {len(soggetti):,}\n**Verbi:** {len(verbi):,}\n**Complementi:** {len(complementi):,}\nLe combinazioni possibili sono ben {combinazioni:,}. Accipicchia!\nSono state generate addirittura {num_nandate:,} nandate!')

	else:
		contesti, soggetti, verbi, complementi = costruisci_liste()

		contesto_sceltoA = random.choice(contesti)
		contesto_scelto = contesto_sceltoA[:1].upper() + contesto_sceltoA[1:]
		soggetto_scelto = random.choice(soggetti)
		if not contesto_scelto:
			soggetto_scelto = soggetto_scelto[:1].upper() + soggetto_scelto[1:]
		verbo_scelto = random.choice(verbi)
		complemento_scelto = random.choice(complementi)
		nandata = f'{contesto_scelto} {soggetto_scelto} {verbo_scelto} {complemento_scelto}'

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
			nandata = nandata.replace(' da i ', ' dai ')
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

		if 'nandate' in db.keys():
			num_nandate = db['nandate']
			num_nandate += 1
			db['nandate'] = num_nandate
		else:
			db['nandate'] = 1

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
						frase = fraseA[:1].upper() + fraseA[1:]
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
