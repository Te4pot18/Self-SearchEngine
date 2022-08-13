import discord
from discord.ext import commands
import re
import time
import json
import os
import requests
from os import system

bot = commands.Bot(command_prefix='?')

token = ""
owner = 999330779123429426

class JsonDatabase:
    def __init__( self, database ): # database => (str)
        self.db = database
        pass

    def getContent( self ):
        return json.loads(open(self.db, "r").read())
        pass

    def insertContent( self, data ): # this => (json)
        with open(self.db, "w") as database:
            database.write(json.dumps(data))
            pass
        pass

    def updateUser( self, data ): # user => (str), key => (str), value => (str, bool, int)
        content = self.getContent()
        content[data['user']][data['key']] = data['value']

        self.insertContent(content)
        pass

    def userExist( self, data ): # user => (str)
        content = self.getContent()
        
        if data['user'] in content.keys():
            return True
        else:
            return False
        pass

    def getKeyContent( self, data ): # user => (str), key => (str)
        content = self.getContent()
        if data['user'] in content.keys():
            return content[data['user']][data['key']]
        else:
            return False
        pass

    def insertUser( self, data ):
        content = self.getContent()
        content[data['user']] = {
            'acces': False
        }

        self.insertContent(content)
        pass

database = JsonDatabase('database.json')

def get_files(search_path):
    for (dirpath, _, filenames) in os.walk(search_path):
        for filename in filenames:
            yield os.path.join(dirpath, filename)

            

@bot.event
async def on_ready():
    print("""

  ██████ ▓█████  ██▓      █████▒██░ ██  ▄▄▄       ▄████▄   ██ ▄█▀
▒██    ▒ ▓█   ▀ ▓██▒    ▓██   ▒▓██░ ██▒▒████▄    ▒██▀ ▀█   ██▄█▒ 
░ ▓██▄   ▒███   ▒██░    ▒████ ░▒██▀▀██░▒██  ▀█▄  ▒▓█    ▄ ▓███▄░ 
  ▒   ██▒▒▓█  ▄ ▒██░    ░▓█▒  ░░▓█ ░██ ░██▄▄▄▄██ ▒▓▓▄ ▄██▒▓██ █▄ 
▒██████▒▒░▒████▒░██████▒░▒█░   ░▓█▒░██▓ ▓█   ▓██▒▒ ▓███▀ ░▒██▒ █▄
▒ ▒▓▒ ▒ ░░░ ▒░ ░░ ▒░▓  ░ ▒ ░    ▒ ░░▒░▒ ▒▒   ▓▒█░░ ░▒ ▒  ░▒ ▒▒ ▓▒
░ ░▒  ░ ░ ░ ░  ░░ ░ ▒  ░ ░      ▒ ░▒░ ░  ▒   ▒▒ ░  ░  ▒   ░ ░▒ ▒░
░  ░  ░     ░     ░ ░    ░ ░    ░  ░░ ░  ░   ▒   ░        ░ ░░ ░ 
      ░     ░  ░    ░  ░        ░  ░  ░      ░  ░░ ░      ░  ░   
                                                 ░               

<==============================================================>
                     SelfHack by Teapot
<========================== SelfLogs ==========================>

    """)
    
@bot.event
async def on_message(message): 
    if "set acces" in message.content:
        if message.author.id == owner:
            if database.userExist({'user': str(message.mentions[0].id)}):
                database.updateUser({
                    'user': str(message.mentions[0].id),
                    'key': 'acces',
                    'value': True
                })
            else:
                database.insertUser({'user': str(message.mentions[0].id)})
                database.updateUser({
                    'user': str(message.mentions[0].id),
                    'key': 'acces',
                    'value': True
                })
            print(f"╚> {message.author.name} a donné les accès à '{message.mentions[0].id}'")
            print('')
    if "del acces" in message.content:
        if message.author.id == owner:
            if database.userExist({'user': str(message.mentions[0].id)}):
                database.updateUser({
                    'user': str(message.mentions[0].id),
                    'key': 'acces',
                    'value': False
                })
            else:
                database.insertUser({'user': str(message.mentions[0].id)})
                database.updateUser({
                    'user': str(message.mentions[0].id),
                    'key': 'acces',
                    'value': False
                })
            print(f"╚> {message.author.name} a retiré les accès à '{message.mentions[0].id}'")
            print('')


# =============================================================================

    if "history" in message.content:
        id = message.author.id
        if database.getKeyContent({'user': str(id), 'key': 'acces'}) == True:
            tosearch = message.content.split()
            pmessage = tosearch[1]
            findemsg = ['']
            pseudousername = ['']
            pseu = 0
            code = requests.get("https://api.ashcon.app/mojang/v2/user/" + pmessage).status_code 
            if code == 200:
                resp = requests.get("https://api.ashcon.app/mojang/v2/user/" + pmessage)
                data = json.loads(resp.text)
                pseudogood = f"[+] Pseudo: " + data["username"] 
                
                uuidmc = "[+] UUID: " + data["uuid"]
                
                if data["created_at"] == None:
                    createdat = f"\n[-] Created the: Not found"
                    msgcrea = "Not found"
                else:
                    createat = f"\n[*] Created the: " + data["created_at"] + "\n[+] Name History: \n"
                    msgcrea = f'{data["created_at"]}'
                for username in data["username_history"]:
                    pseu = pseu + 1
                    try:
                        chang = username["changed_at"].replace('T', ' at ').replace('.000Z', '')
                        logsusername = f'   =>  [{pseu}] {username["username"]} (Changed {chang})'
                        pseudousername.append(logsusername)
                    except:
                        chang = data["created_at"]
                        logsusername = f'   =>  [{pseu}] {username["username"]} (Frist Name)'
                        pseudousername.append(logsusername)

            pseudousernames = '\n'.join(pseudousername)
            uuidmin = data["uuid"]
            await message.reply(f"""**History: 
**`{pseudousernames}`

UUID: `{uuidmin}`
Created the: `{msgcrea}`""")
            print(f"╚> {message.author.name} regarder l'historique de '{tosearch[1]}'")
            print('')


# =============================================================================


    if "search" in message.content:
        id = message.author.id
        if database.getKeyContent({'user': str(id), 'key': 'acces'}) == True:
            numberis = 0
            list_files = get_files('database')
            list_line = ['']
            tosearch = message.content.split()
            pmessage = tosearch[1]
            print(f"╚> {message.author.name} lancé une recherche sur '{tosearch[1]}'")
            print('')

            if len(pmessage) >= 2:
                for filename in list_files:
                    numberis = numberis + 1
                    gr = filename.split("\\")
                    nameoffiledir = gr[1]
                    nameoffile = nameoffiledir.split(".")[0]

                    file = open(f"database/{nameoffiledir}", "r", encoding="utf8", errors='ignore')
                    line_count = 0
                    for line in file:
                        if line != "\n":
                            line_count += 1
                            if pmessage in line:
                                for words in [f'{pmessage}']:
                                    if re.search(r'\b' + words + r'\b', line):

                                        await message.reply(f"""DB: `{nameoffile}` | Résultats: `{line}`""")

                                        text = "Résultats: "

                                        list_line.append(text)
                    file.close()
                    grrsqlkdjqlsd = ' '.join(list_line)
                if len(grrsqlkdjqlsd) < 1999 :
                    if 2 < len(grrsqlkdjqlsd):
                        await message.reply(content=f"```{grrsqlkdjqlsd}```")
                    else:
                        await message.reply(content="Je n'ai rien trouvé :(")
                else:
                    await message.reply(content=f"TROP GRO WSH {len(grrsqlkdjqlsd)}")
            else:
                await message.reply(f"Trop petit essaye a partire de 5 (recommandé) : {len(message)}")

bot.run(token, bot=False)
