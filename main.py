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
import tracemalloc
from collections import Counter
from itertools import chain

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=['! ', '!'], case_insensitive=True)

# FLAG globali
flagDuplicato = False
flagEliminazione = True


@bot.event
async def on_ready():
	print('PeggioBot è pronto!')

alias_kali = ['tettedikali', 'tette', 'kali']
@bot.command(aliases = alias_kali)
async def gatto(ctx, *, comando=None):
	global flagDuplicato
	global flagEliminazione

	flagDuplicato = False
	flagEliminazione = True
	flagLista = False

	msg_gatto = ''
	embed = discord.Embed()
	embed.set_image(url='https://c.tenor.com/ociZpU8b_Q8AAAAj/cat-meme.gif')
	if ctx.message.attachments:
		if comando:
			gatto_pic = ctx.message.attachments[0].url
			comando = comando.lower()
			nomi_gatti = shlex.split(comando)
			for nome_gatto in nomi_gatti:
				# aggiunge l'url della foto gatto al database del gatto
				aggiungi_nandata(ctx, nome_gatto, gatto_pic)
				aggiungi_nandata(ctx, 'gatti_db', nome_gatto)
				msg_gatto += f'foto di {nome_gatto.capitalize()} aggiunta al database!\n'
			msg_gatto += f'Non cancellare questo messaggio pls'

		else:
			msg_gatto = "Rimanda la foto dicendomi chi è questo gatto!"

	elif comando:
		comando = comando.lower()

		if 'rimuovi' in comando:
			comandi = shlex.split(comando)
			nome_gatto = comandi[1]
			url_gatto = comandi[2]

			if nome_gatto in db.keys():
				# rimuovo la foto dal database del gatto
				gatto_db = db[nome_gatto]
				indice = gatto_db.index(url_gatto)
				del gatto_db[indice]
				if gatto_db:
					db[nome_gatto] = gatto_db
				else:
					del db[nome_gatto]

				msg_gatto = f'Foto di {nome_gatto.capitalize()} eliminata!'
			else:
				msg_gatto = f'Non ho trovato la foto di {nome_gatto.capitalize()} da eliminare!'
			
		
		elif 'lista' in comando:
			if 'gatti_db' in db.keys():
				msg_bot = await ctx.send("Sto compilando la lista, pazienta un poco!")
				gatti_db = sorted(db['gatti_db'])
				tot_gatti = 0
				nuova_lista_gatti = []
				msg_gatto += "Ecco la lista dei Peggiogatti:\n\n"
				for gatto in gatti_db:
					gatto_db = db[gatto]
					quante_foto = len(gatto_db)
					tot_gatti += quante_foto
					msg_gatto += f'**{gatto.capitalize()}**: {quante_foto} foto\n'


				for gatto in gatti_db:
					for pic_gatto in db[gatto]:
						if pic_gatto not in nuova_lista_gatti:
							nuova_lista_gatti.append(pic_gatto)

				tot_gatti = len(nuova_lista_gatti)
				msg_gatto += f'\nIn totale ci sono {tot_gatti} foto!'
				await msg_bot.edit(content=msg_gatto)
				flagLista = True

			else:
				msg_gatto = "Hey, non ci sono ancora foto di gatti!"

		elif 'foto'	in comando:
			comandi = shlex.split(comando)
			nome_gatto = comandi[0].lower()
			if nome_gatto in db.keys():
				flagLista = True
				
				foto_gatto = db[nome_gatto]
				pic_index = 0
				embed.set_image(url=foto_gatto[pic_index])
				msg_pics = await ctx.send(f'**{nome_gatto}** foto {(pic_index % len(foto_gatto))+1}/{len(foto_gatto)}', embed=embed)

				emoji_list = ['⏮️', '⬅️', '➡️', '⏭️', '❌']
				for emoji in emoji_list:
					await msg_pics.add_reaction(emoji)

				def check(reaction, user):
					return user == ctx.author and str(reaction.emoji) in emoji_list
				
				while True:
					try:
						reaction, user = await bot.wait_for('reaction_add', timeout=30, check=check)

						if str(reaction.emoji) == '⏮️':
							pic_index -= 10
						elif str(reaction.emoji) == '⬅️':
							pic_index -= 1
						elif str(reaction.emoji) == '➡️':
							pic_index += 1
						elif str(reaction.emoji) == '⏭️':
							pic_index += 10
						elif str(reaction.emoji) == '❌':
							await msg_pics.edit(content=f'Grazie per aver guardato le foto di {nome_gatto.capitalize()}!', embed=None)
							for emoji in emoji_list:
								await msg_pics.clear_reaction(emoji)
							break

						pic_index = pic_index % len(foto_gatto)
						print('fuori ', pic_index)

						await msg_pics.remove_reaction(reaction, ctx.author)	

						embed.set_image(url=foto_gatto[pic_index])
						await msg_pics.edit(content=f'**{nome_gatto}** foto {pic_index+1}/{len(foto_gatto)}', embed=embed)

					except asyncio.TimeoutError:
						await msg_pics.edit(content=f'Grazie per aver guardato le foto di {nome_gatto.capitalize()}!', embed=None)
						for emoji in emoji_list:
							await msg_pics.clear_reaction(emoji)
						break

				

			else:
				msg_gatto = f'Non ho ancora foto di {nome_gatto.capitalize()}!'

		# il 'comando' sarà quindi il nome di un gatto. 
		else:
			nome_gatto = comando
			# Se il nome del gatto è nel db...
			if nome_gatto in db.keys():
				gatto_url = random.choice(db[nome_gatto])
				msg_gatto = f'Ecco una foto di {nome_gatto.capitalize()}:'
				embed.set_image(url=gatto_url)
			else:
				msg_gatto = f'Non ho ancora foto di {nome_gatto.capitalize()}!'

	# se non c'è nome di gatto, prende un gatto a caso
	else:
		if 'gatti_db' in db.keys():
			#scelgo un nome di gatto a caso
			gatti_db = db['gatti_db']
			gatto_casuale = random.choice(gatti_db)

			#dal database del gatto scelto a caso, prendo una foto a caso
			gatto_db = db[gatto_casuale]
			foto_casuale = random.choice(gatto_db)

			msg_gatto = f'Ecco una foto a caso di {gatto_casuale.capitalize()}:'
			embed.set_image(url=foto_casuale)

		else:
			msg_gatto = "Hey, non ci sono ancora foto di gatti!"
	
	if any(x in ctx.invoked_with for x in alias_kali):
		lista_kali = [
			'Volevi vedere una gattona hot, eh? Ecco qui:',
			'Tieni, sporcaccione ;',
			'Sei proprio un pervertito...'
			]
		msg_gatto = random.choice(lista_kali)
	if not flagLista:
		await ctx.send(msg_gatto, embed=embed)			

# aliases: lista di comandi che triggerano la funzione
@bot.command()
async def ping(ctx):
	await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

@bot.command()
async def sgrigna(ctx):
	await ctx.send("La sgrigna (termine dialettale romagnolo) è una risata incontenibile, una ridarella. È quando inizi a ridere e non riesci a smettere e ridi per qualsiasi cosa.\n- *Alessandra Guardigli*")

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
async def lore(ctx, *, messaggio_in=None):
	global flagDuplicato
	global flagEliminazione

	flagDuplicato = False
	flagEliminazione = True

	if messaggio_in:
		
		print("if messaggio_in: ", messaggio_in)
		messaggio = shlex.split(messaggio_in)
		print("if messaggio_in split: ", messaggio)

		if len(messaggio) >= 3:

			print("if len msg = 3: ", messaggio_in)
			print("if len msg = 3: ", messaggio)

			comando = messaggio[0].lower()
			argomento = messaggio[1]
			argomento = argomento.strip('"')
			lore = messaggio[2]

			if comando == "aggiungi":
				print("aggiungi - argomento: ", argomento)
				print("aggiungi - lore: ", lore)
				aggiungi_nandata(ctx, argomento, lore)
				aggiungi_nandata(ctx, 'argomenti_lore', argomento)
				if not flagDuplicato:
					msg_out = f'Aggiunta la lore su **{argomento}**'
					print("db[argomento] \n", db[argomento])
					print("db[argomenti_lore \n", db['argomenti_lore'])
				else:
					msg_out = f'Hey, questa lore c\'è già!'
			
			else:
				msg_out = "Sembra tu voglia aggiungere qualcosa. Usa le virgolette, pls!\n`!lore aggiungi \"argomento della lore\" \"testo della lore\"`"

		elif len(messaggio) == 2:

			comando = messaggio[0].lower()
			argomento = messaggio[1]
			print("argomento: ", argomento)
			argomento = argomento.strip('"')
			print("argomento stripped: ", argomento)

			if comando == 'rimuovi':
				print("rimuovi - argomento: ", argomento)
				if argomento in db.keys():
					del db[argomento]
					print("db[argomento] cancellato")
					rimuovi_nandata(ctx, 'argomenti_lore', argomento)
					if flagEliminazione:
						msg_out = f'Ho eliminato la lore su {argomento}!'
						print(db['argomenti_lore'])
					else:
						print("Non è stato eliminato")
						msg_out = f'Non ho trovato la lore su {argomento}!'
				else:
					print("Non c'era l'argomento in db")
					msg_out = f'Non ho trovato la lore su {argomento}!'
			
			else:
				msg_out = "Sembra tu voglia rimuovere qualcosa. Usa le virgolette, pls!\n`!lore rimuovi \"argomento della lore\"`"

		elif len(messaggio) == 1:

			comando = messaggio_in
			print("if len msg = 1", comando)

			if comando == 'lista':
				if 'argomenti_lore' in db.keys():
					argomenti = sorted(db['argomenti_lore'])
					msg_out = '**Ecco una lista della lore PN:**\n'
					for argomento in argomenti:
						if argomento in db.keys():
							msg_out += f'{argomento}\n'
					msg_out += "\n*Scrivi fra virgolette l'argomento che vuoi sapere!*"

				else:
					msg_out = 'Non ci sono ancora argomenti di cui parlare!'	

			else:
				argomento = comando
				print("argomento: ", argomento)
				argomento = argomento.strip('"')
				print("argomento stripped: ", argomento)
				if argomento in db['argomenti_lore']:
					print("argomento c'è nella lista args")
					lore = db[argomento]
					lore = ''.join(lore)
					print(lore, type(lore))
					msg_out = f'Ecco la lore su **{argomento}**:\n{lore}'
				else:
					msg_out = 'Non ho trovato la lore su questo argomento!'

		else:
			msg_out = "Non sono sicuro di quello che mi hai chiesto, prova a usare le virgolette!"

	else:
		msg_out = 'Devi scrivere l\'argomento su cui vuoi sapere la lore!'

	await ctx.send(msg_out)
	print()


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
	if ctx.invoked_with == 'nando':
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
	if ctx.invoked_with == 'nando':
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

async def split_lista(ctx, lista, nome_lista):
	n = 10 # maximum chars
	lista = sorted(lista)
	chunks = [lista[i:i+n] for i in range(0, len(lista), n)]

	for index, chunk in enumerate(chunks):
		if not index:
			await ctx.send(f'**{nome_lista}**\n{chunk}')
		else:
			await ctx.send(chunk)

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
			await ctx.send("Stiamo lavorando per voi!")

			contesti, soggetti, verbi, complementi = costruisci_liste()

			print(f'**Contesti**: {sorted(contesti)}')
			print(f'**Soggetti**: {sorted(soggetti)}')
			print(f'**Verbi**: {sorted(verbi)}')
			print(f'**Complementi**: {sorted(complementi)}')

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
		non_importa, soggetti, verbi, complementi = costruisci_liste()

		if random.choice([True, False]):
			contesti = variabili.contesti
		else:
			contesti = db["contesti"]

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
		if ' da l\'' in nandata:
			nandata = nandata.replace(' da l\'', ' dall\'')
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
		if ' su l\'' in nandata:
			nandata = nandata.replace(' su l\'', ' sull\'')		
		if ' ,' in nandata:
			nandata = nandata.replace(' ,', ',')

		if 'nandate' in db.keys():
			num_nandate = db['nandate']
			num_nandate += 1
			db['nandate'] = num_nandate
		else:
			db['nandate'] = 1

		await ctx.send(nandata)

		gatti_db = db['gatti_db']
		if any(nome_gatto.lower() in nandata.lower() for nome_gatto in gatti_db):
			nome_gatto = [nome_gatto for nome_gatto in gatti_db if nome_gatto.lower() in nandata.lower()]
			cmd = bot.get_command("gatto")
			for elem in nome_gatto:
				await cmd(ctx, comando=elem)

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

@bot.listen('on_message')
async def hey_bot(ctx):
		if ctx.author == bot.user:
				return

		msg = ctx.content.lower()
		if msg.startswith('hey bot') or msg.startswith('hey culo'):
				if ctx.author.name == "Rufus Loacker":
						response = "Hey papà!"
				elif ctx.author.name == "Kanmuri":
						response = "Hey admin del mondo!"
				elif ctx.author.name == "CowardKnight":
						response = "Hey persona con gatti belli!"
				else:
						response = f'Hey {ctx.author.display_name}!'
				await ctx.channel.send(response)
		
		lista_good = ['good bot', 'goodbot', 'bravo bot']
		if any(x in msg for x in lista_good):
			await ctx.channel.send(f'Awwww, grazie {ctx.author.display_name} <3 <3 <3')
		
		lista_bad = ['bad bot', 'badbot', 'cattivo bot']
		if any(x in msg for x in lista_bad):
			await ctx.channel.send(f'Così ferisci i miei sentimenti {ctx.author.display_name}... :(')
		
		lista_grazie = ['thanks bot', 'thanksbot', 'grazie bot', 'grazie culo']
		if any(x in msg for x in lista_grazie):
			await ctx.channel.send("Prego! ^_^")

		lista_oliver = ['vero oliver']
		if any(x in msg for x in lista_oliver):
			await ctx.channel.send("Il vero Oliver? Quello di Rufus, ovviamente.")
		
		gatti_db = db['gatti_db']
		lista_comandi = ['!gatto', '! gatto']
		if any(nome_gatto.lower() in msg for nome_gatto in gatti_db) and not any(comando in msg for comando in lista_comandi):
			embed = discord.Embed()
			nome_gatto = [nome_gatto for nome_gatto in gatti_db if nome_gatto.lower() in msg]
			for elem in nome_gatto:
				gatto_url = random.choice(db[elem])
				msg_gatto = f'Ecco una foto di {elem.capitalize()}:'
				embed.set_image(url=gatto_url)
				await ctx.channel.send(msg_gatto, embed=embed)

keep_alive.keep_alive()
bot.run(TOKEN)