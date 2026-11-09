import discord
import requests
import pyttsx3 as pyt
from discord.ext import commands

engine = pyt.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

for index, voice in enumerate(voices):
    print(f"Índice: {index} | Nome: {voice.name} | ID: {voice.id}")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.command()
async def start(ctx):
    texto = "olá, como vai, eu sou um meteorologista, digite /tempohoje e o nome de alguma cidade para começar a previsão. Ou /fato para eu falar um fato aleatório, um hobby meu."
    await ctx.send(f"olá, como vai, eu sou um meteorologista, digite `tempohoje (alguma cidade)` para começar a previsão(ou `/fato` para eu falar um fato aleatorio, num sei porque gosto disso, é um hobby meu)")
    engine.say(texto)
    engine.runAndWait()

@bot.command()
async def tempohoje(ctx, *, cidade):
    url = f"https://wttr.in/{cidade}?format=%C+%h+%2+%l+%m+%M"
    resposta = requests.get(url)
    
    if resposta.status_code == 200:
        texto_resposta = f"olá, mal dia, a previsão da localização que você citou é: {resposta.text}"
        await ctx.send(texto_resposta)
        engine.say(texto_resposta)
        engine.runAndWait()
    else:
        msg = "pelo amor de deus, a maldita conexão falhou, tente novamente mais tarde"
        await ctx.send(msg)
        engine.say(msg)
        engine.runAndWait()

@bot.command()
async def fato(ctx):
    url = "https://uselessfacts.jsph.pl/api/v2/facts/random"
    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados = resposta.json()
        fato_texto = dados.get('text', 'Não consegui ler o fato.')
        mensagem = f"um fato estranhamente aleatório: {fato_texto}"
        
        await ctx.send(mensagem)
        engine.say(mensagem)
        engine.runAndWait()
    else:
        await ctx.send("pelo amor de deus, a maldita conexão falhou, tente novamente mais tarde")

@bot.command()
async def voz_portugues(ctx):
    if len(voices) > 0:
        engine.setProperty('voice', voices[0].id)
        await ctx.send("agora minha voz está em português")
        engine.say("agora minha voz está em português")
        engine.runAndWait()

@bot.command()
async def voz_ingles(ctx):
    if len(voices) > 1:
        engine.setProperty('voice', voices[1].id)
        await ctx.send("agora minha voz está em inglês")
        engine.say("agora minha voz está em inglês")
        engine.runAndWait()
    else:
        await ctx.send("Não encontrei uma segunda voz configurada no sistema.")

@bot.command()
async def api_pokemon(ctx, pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id.lower()}"
    resposta = requests.get(url)
    
    if resposta.status_code == 200:
        dados = resposta.json()
        nome = dados['name']
        altura = dados['height']
        exp = dados['base_experience']
        
        texto_pk = f"TU DESCOBRIU MINHA OBSESSÃO! OK, aqui estão os dados do Pokémon: {nome}, altura {altura}, e experiência base {exp}."
        
        await ctx.send(texto_pk)
        engine.say(texto_pk)
        engine.runAndWait()
    else:
        await ctx.send("MEU DEUS, o maldito pokémon não encontrado ou a maldita conexão falhou!")


bot.run("TOKEN")
