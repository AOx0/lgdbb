# bot.py
# https://discordpy.readthedocs.io/en/latest/api.html?highlight=guild.member#discord-models

import datetime
import json
import os
import random
import traceback

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILDID = 721616698477641749


class Bot:
    usuarios = {}

    class Conversacion:
        def __init__(self):
            self.tipo = 'default'
            self.cantidad = 0
            self.chat = 'default'
            self.id = 9999999999

        def luhnCheck(self, card_number):
            '''luhnCheck. Validates the CC with the last number'''
            num = list(map(int, str(card_number)))
            return sum(num[::-2] + [sum(divmod(d * 2, 10))
                                    for d in num[-2::-2]]) % 10 == 0

        def genID(self):

            while True:
                return1 = "9"
                return2 = ""
                ints1 = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
                for _ in range(9):
                    return1 += str(random.choice(ints1))
                for i in range(9):
                    if self.luhnCheck(f'{return1}{i}') is True:
                        return2 = f'{return1}{i}'
                        self.id = return2
                        return

        def reset(self):
            self.tipo = 'default'
            self.cantidad = 0
            self.chat = 'default'
            self.id = 9999999999

    def __init__(self):
        self.conversations = {}
        self.main_admin = 386927261
        self.admins = [386927261]

    def save2Log(self, content):
        self.usuarios["log"]["logs"] += 1
        self.usuarios["log"]["log"][self.usuarios["log"]["logs"]] = content
        self.saveUsr()

    def cobrarInteresTransfer(self, cuenta, cantidad):
        por = 0.05
        self.usuarios['users'][cuenta]['acid'] -= cantidad * por
        self.usuarios['users']['Legendary Bank']['acid'] += cantidad * por
        self.saveUsr()

    def cEstado(self, modo, usuario, cantidad):
        if modo == 1:
            self.usuarios['users'][usuario]['acid'] += cantidad
        else:
            self.usuarios['users'][usuario]['acid'] -= cantidad
        self.saveUsr()
        return

    def saveUsr(self):
        with open('objs.txt', 'w') as f:  # Python 3: open(..., 'wb')
            json.dump(self.usuarios, f)

    def loadUsr(self):
        with open('objs.txt', 'r') as f:  # Python 3: open(..., 'rb')
            bot.usuarios = json.load(f)

    def cobroCuota(self):
        self.saveUsr()
        self.loadUsr()
        for i in self.usuarios['users']:
            q = self.usuarios['users'][i]['acid'] * self.usuarios['cuota']
            self.usuarios['users'][i]['acid'] -= q
            self.usuarios['users']['Legendary Bank']['acid'] += q

        self.saveUsr()

    def cobroInteres(self):
        self.saveUsr()
        self.loadUsr()
        for i in self.usuarios['users']:
            if self.usuarios['users'][i]['pres'] != 0:
                q = self.usuarios['users'][i]['pres'] * self.usuarios['users'][i]['presNo']
                self.usuarios['users'][i]['pres'] += q

        self.saveUsr()

    def cobroTodo(self):
        self.cobroCuota()
        self.cobroInteres()

    def activar(self, usuario):
        bot.usuarios["users"][f"{usuario}"]["activado"] = True

    def desActivar(self, usuario):
        bot.usuarios["users"][f"{usuario}"]["activado"] = False

    def makeAdmin(self, usuario):
        self.activar(usuario)
        bot.usuarios["users"][f"{usuario}"]["admin"] = True

    def makeSuperAdmin(self, usuario):
        self.activar(usuario)
        self.makeAdmin(usuario)
        bot.usuarios["users"][f"{usuario}"]["superAdmin"] = True

    def unAdmin(self, usuario):
        bot.usuarios["users"][f"{usuario}"]["admin"] = False

    def unSuperAdmin(self, usuario):
        bot.usuarios["users"][f"{usuario}"]["superAdmin"] = False

    def prestamo(self,usuario, por, cant):
        bot.usuarios["users"][f"{usuario}"]["presNo"] += (por)
        bot.usuarios["users"][f"{usuario}"]["pres"] += (cant)

    def cuota(self, por):
        bot.usuarios["cuota"] = int(por)

    def mostarLog(self):
        toSend = ""
        for i in bot.usuarios["log"]["log"]:
            toSend += f" -- {bot.usuarios['log']['log'][i]}\n"
        return toSend


class Client(discord.Client):

    async def on_ready(self):
        print(f'{client.user} has connected to Discord!')
        for guild in client.guilds:
            if guild.name == GUILD:
                break

        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})\n'
        )

        members = '\n - '.join([member.name for member in guild.members])

        with open('objs.txt', 'r') as f:  # Python 3: open(..., 'rb')
            bot.usuarios = json.load(f)

        if str(bot.usuarios['date']) != str(datetime.date.today()):
            bot.usuarios['date'] = str(datetime.date.today())
            bot.cobroCuota()
            bot.cobroInteres()
        # bot.usuarios.append(bot.Usuario('NSH~Alejandro'))
        print(f'Guild Members:\n - {members}')
        print(f'{client}')

        for i in guild.members:
            if str(i.name) not in bot.usuarios["users"]:
                bot.usuarios["users"][f"{i.name}"] = {}
                bot.usuarios["users"][f"{i.name}"]["userID"] = str(i.id)
                bot.usuarios["users"][f"{i.name}"]["uMention"] = str(f"{i}")
                bot.usuarios["users"][f"{i.name}"]["activado"] = False
                bot.usuarios["users"][f"{i.name}"]["acid"] = 0
                bot.usuarios["users"][f"{i.name}"]["admin"] = False
                bot.usuarios["users"][f"{i.name}"]["superAdmin"] = False
                bot.usuarios["users"][f"{i.name}"]["presNo"] = 0
                bot.usuarios["users"][f"{i.name}"]["pres"] = 0

        bot.saveUsr()

        for p in bot.usuarios['users']:
            print(f"{p} : {bot.usuarios['users'][f'{p}']}")

    """async def on_member_join(self, member):
        print(member)
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, welcome to my Discord server!'
        )"""

    async def on_message(self, message):
        with open('objs.txt', 'r') as f:  # Python 3: open(..., 'rb')
            bot.usuarios = json.load(f)
            for p in bot.usuarios['users']:
                print(f"{p} : {bot.usuarios['users'][f'{p}']}")

        if bot.usuarios["debug"] is True or message.author == client.user:
            return

        if str(message.author.name) not in bot.usuarios["users"]:
            bot.usuarios["users"][f"{message.author.name}"] = {}
            bot.usuarios["users"][f"{message.author.name}"]["userID"] = str(message.author.id)
            bot.usuarios["users"][f"{message.author.name}"]["uMention"] = str(f"{message.author}")
            bot.usuarios["users"][f"{message.author.name}"]["activado"] = False
            bot.usuarios["users"][f"{message.author.name}"]["acid"] = 0
            bot.usuarios["users"][f"{message.author.name}"]["admin"] = False
            bot.usuarios["users"][f"{message.author.name}"]["superAdmin"] = False
            bot.usuarios["users"][f"{message.author.name}"]["presNo"] = 0
            bot.usuarios["users"][f"{message.author.name}"]["pres"] = 0

        if str(bot.usuarios['date']) != str(datetime.date.today()):
            bot.usuarios['date'] = str(datetime.date.today())
            bot.cobroCuota()
            bot.cobroInteres()

        if message.author.name in bot.conversations.keys():
            pass
        else:
            bot.conversations[message.author.name] = bot.Conversacion()

        print(f"Channel ID: {message.channel.id}")
        print(f"Keys: {bot.conversations.keys()}")
        print(f'Message from {message.author} (ID: {message.author.id}): {message.content}')

        if bot.usuarios["users"][message.author.name]["admin"] is True:
            a = discord.Client.get_channel(self=self, id=GUILDID)
            for i in bot.conversations:
                if bot.conversations[i].tipo == 're2' and str(bot.conversations[i].id) in str(message.content):
                    if 'cancelar' in str(message.content).lower():
                        try:
                            await a.send(f'<@{bot.usuarios["users"][i]["userID"]}>, su retiro de fondos, {bot.conversations[i].id}, fue denegado por un administrador.')
                        except:
                            await a.send(f'{i}, su retiro de fondos, {bot.conversations[i].id}, fue denegado por un administrador.')
                        bot.conversations[i].reset()
                        bot.saveUsr()
                        break
                    print('TERMINADO')
                    bot.cEstado(2, i, bot.conversations[i].cantidad)
                    await a.send(f'Transferencia {bot.conversations[i].id} exitosa.')
                    bot.save2Log(
                        f"RETIRO - Cantidad: {bot.conversations[i].cantidad} - ID: {bot.conversations[i].id} - User: {i}")
                    bot.conversations[i].tipo = 'default'
                    bot.saveUsr()
                elif bot.conversations[i].tipo == 'in2' and str(bot.conversations[i].id) in str(message.content):
                    if 'cancelar' in str(message.content).lower():
                        try:
                            await a.send(
                                f'<@{bot.usuarios["users"][i]["userID"]}>, su depósito de fondos, {bot.conversations[i].id}, fue denegado por un administrador.')
                        except:
                            await a.send(
                                f'{i}, su depósito de fondos, {bot.conversations[i].id}, fue denegado por un administrador.')
                        bot.conversations[i].reset()
                        bot.saveUsr()
                        break
                    print('TERMINADO')
                    bot.cEstado(1, i, bot.conversations[i].cantidad)
                    await a.send(f'Transferencia {bot.conversations[i].id} exitosa.')
                    bot.save2Log(
                        f"DEPOSITO - Cantidad: {bot.conversations[i].cantidad} - ID: {bot.conversations[i].id} - User: {i}")
                    bot.conversations[i].tipo = 'default'
                    bot.saveUsr()

        if bot.conversations[message.author.name].tipo == 're1':
            if "cancel" in message.content:
                bot.conversations[message.author.name].reset()
                bot.saveUsr()
            else:
                try:
                    bot.conversations[message.author.name].cantidad = int(message.content)
                    bot.conversations[message.author.name].genID()

                    await message.author.send(
                        f' ————————\n      LGD BANK\n ————————\n Solicitud Creada\n  ID : {bot.conversations[message.author.name].id}\n ————————\nAhora debes retirar\nel ácido @ físico en\n  una sucursal del\n         Banco.\n ————————\n    Entrega éste\nmensaje o el ID al\n encargado de la\n       sucursal.\n ————————'
                    )
                    bot.conversations[message.author.name].tipo = 're2'
                except:
                    bot.conversations[message.author.name].reset()
                    bot.saveUsr()
                    return
        elif bot.conversations[message.author.name].tipo == 'in1':
            if "cancel" in message.content:
                bot.conversations[message.author.name].reset()
                bot.saveUsr()
            else:
                try:
                    bot.conversations[message.author.name].cantidad = int(message.content)
                    bot.conversations[message.author.name].genID()

                    await message.author.send(
                        f' ————————\n      LGD BANK\n ————————\n Solicitud Creada\n  ID : {bot.conversations[message.author.name].id}\n ————————\nAhora debes llevar\nel ácido @ físico a\n  una sucursal del\n         Banco.\n ————————\n    Entrega éste\nmensaje o el ID al\n encargado de la\n       sucursal.\n ————————'
                    )
                    bot.conversations[message.author.name].tipo = 'in2'
                except:
                    bot.conversations[message.author.name].reset()
                    bot.saveUsr()
                    return
        elif bot.conversations[message.author.name].tipo == 'tr1':
            if "cancel" in message.content:
                bot.conversations[message.author.name].reset()
                bot.saveUsr()
            else:
                try:
                    bot.conversations[message.author.name].cantidad = int(message.content)
                    await message.channel.send(f'A quién deseas transferir {message.content}@, {message.author.name}?')
                    bot.conversations[message.author.name].tipo = 'tr2'
                except:
                    bot.conversations[message.author.name].reset()
                    bot.saveUsr()
                    return
        elif bot.conversations[message.author.name].tipo == 'tr2':
            try:
                if "cancel" in message.content:
                    bot.conversations[message.author.name].reset()
                    bot.saveUsr()
                else:
                    bot.conversations[message.author.name].genID()
                    user = message.content
                    for i in bot.usuarios['users']:
                        print(str(i).lower())
                        if str(i).lower() == user:
                            user = str(i)
                            break
                        else:
                            user1 = user.replace("<@", '')
                            user1 = user1.replace(">", '')
                            print(user1)
                            if bot.usuarios["users"][i]["userID"] == user1:
                                user = str(i)
                                break
                    if bot.usuarios['users'][message.author.name]["acid"] - bot.conversations[
                        message.author.name].cantidad >= 0:
                        bot.usuarios['users'][message.author.name]["acid"] -= bot.conversations[
                            message.author.name].cantidad
                        bot.usuarios['users'][user]["acid"] += bot.conversations[
                            message.author.name].cantidad
                        bot.cobrarInteresTransfer(user,
                                                  bot.conversations[message.author.name].cantidad)
                        print("Descontado interés")
                        a = discord.Client.get_channel(self=self, id=GUILDID)
                        await a.send(
                            f'Transferencia {bot.conversations[message.author.name].id} exitosa.')
                        bot.saveUsr()
                        bot.save2Log(
                            f"TRANSFERENCIA - Cantidad: {bot.conversations[message.author.name].cantidad} a {user} - ID: {bot.conversations[message.author.name].id} - User: {message.author.name}")
                        bot.conversations[message.author.name].reset()
                        bot.saveUsr()
                    else:
                        await message.channel.send(
                            f'Error al procesar la transferencia {bot.conversations[message.author.name].id}: pocos fondos'
                        )
                        bot.conversations[message.author.name].reset()
            except:
                bot.conversations[message.author.name].reset()
                return

        if ('su' in (str(message.content)).lower()) and bot.usuarios['users'][f'{message.author.name}'][
            'admin'] is True:
            print("Admin")
            if bot.usuarios['users'][f'{message.author.name}']['superAdmin'] is True:
                if 'su admin' in str(message.content).lower():
                    remove_text = 'su admin '
                    user = message.content.replace(remove_text, '')
                    for i in bot.usuarios['users']:
                        print(str(i).lower())
                        if str(i).lower() == user:
                            user = str(i)
                            break
                        else:
                            user1 = user.replace("<@", '')
                            user1 = user1.replace(">", '')
                            print(user1)
                            if bot.usuarios["users"][i]["userID"] == user1:
                                user = str(i)
                                break
                    try:
                        bot.makeAdmin(user)
                    except:
                        await message.channel.send("Usuario no encontrado")
                        return
                elif 'su superadmin' in str(message.content).lower():
                    remove_text = 'su superadmin '
                    user = message.content.replace(remove_text, '')
                    for i in bot.usuarios['users']:
                        print(str(i).lower())
                        if str(i).lower() == user:
                            user = str(i)
                            break
                        else:
                            user1 = user.replace("<@", '')
                            user1 = user1.replace(">", '')
                            print(user1)
                            if bot.usuarios["users"][i]["userID"] == user1:
                                user = str(i)
                                break
                    try:
                        bot.makeSuperAdmin(user)
                    except:
                        await message.channel.send("Usuario no encontrado")
                        return
                elif 'su noadmin' in str(message.content).lower():
                    remove_text = 'su noadmin '
                    user = message.content.replace(remove_text, '')
                    for i in bot.usuarios['users']:
                        print(str(i).lower())
                        if str(i).lower() == user:
                            user = str(i)
                            break
                        else:
                            user1 = user.replace("<@", '')
                            user1 = user1.replace(">", '')
                            print(user1)
                            if bot.usuarios["users"][i]["userID"] == user1:
                                user = str(i)
                                break
                    try:
                        bot.unAdmin(user)
                    except:
                        await message.channel.send("Usuario no encontrado")
                        return
                elif 'su nosuperadmin' in str(message.content).lower():
                    remove_text = 'su nosuperadmin '
                    user = message.content.replace(remove_text, '')
                    for i in bot.usuarios['users']:
                        print(str(i).lower())
                        if str(i).lower() == user:
                            user = str(i)
                            break
                        else:
                            user1 = user.replace("<@", '')
                            user1 = user1.replace(">", '')
                            print(user1)
                            if bot.usuarios["users"][i]["userID"] == user1:
                                user = str(i)
                                break
                    try:
                        bot.unSuperAdmin(user)
                    except:
                        await message.channel.send("Usuario no encontrado")
                elif 'su global' in str(message.content).lower():
                    bot.saveUsr()
                    await message.author.send(f"SU Global State:\n{json.dumps(bot.usuarios, indent=4)}")
                elif 'su log' in str(message.content).lower():
                    text = bot.mostarLog()
                    await message.author.send(f"LOG:\n{text}")
            if 'su estado' in str(message.content).lower():
                if 'todos' not in str(message.content):
                    remove_text = 'su estado '
                    text = message.content.replace(remove_text, '')
                    for i in bot.usuarios['users']:
                        print(str(i).lower())
                        if str(i).lower() == text:
                            text = str(i)
                            break
                        else:
                            user1 = text.replace("<@", '')
                            user1 = user1.replace(">", '')
                            print(user1)
                            if bot.usuarios["users"][i]["userID"] == user1:
                                text = str(i)
                                break
                    text1 = f'Nombre Cliente: {text}'
                    text2 = f'Ácido ahorrado: {bot.usuarios["users"][text]["acid"]}'
                    text3 = f'Prestamo: {bot.usuarios["users"][text]["pres"]} con {bot.usuarios["users"][text]["presNo"]} de interés diario'
                    if bot.usuarios["users"][text]["admin"] is True and bot.usuarios["users"][message.author.name][
                        "superAdmin"] is True:
                        await message.author.send(f' {text1}\n{text2}\n{text3}')
                    elif bot.usuarios["users"][text]["admin"] is True and bot.usuarios["users"][message.author.name][
                        "superAdmin"] is False:
                        await message.author.send(f'Nivel no autorizado')
                    elif bot.usuarios["users"][text]["admin"] is False:
                        await message.author.send(f' {text1}\n{text2}\n{text3}')
                else:
                    final = ' -- ADMIN: Estado general -- \n'
                    for i in bot.usuarios['users']:
                        text = f'Nombre Cliente: {i}'
                        text2 = f'Ácido ahorrado: {bot.usuarios["users"][i]["acid"]}'
                        text3 = f'Prestamo: {bot.usuarios["users"][i]["pres"]} con {bot.usuarios["users"][i]["presNo"]} de interés diario'

                        if bot.usuarios["users"][i]["admin"] is True and bot.usuarios["users"][message.author.name][
                            "superAdmin"] is True:
                            final += f'--------------------\n{text}\n{text2}\n{text3}\n'
                            # await message.author.send(f'--------------------\n{text}\n{text2}\n{text3}')
                        elif bot.usuarios["users"][i]["admin"] is True and \
                                bot.usuarios["users"][message.author.name][
                                    "superAdmin"] is False:
                            final += f'--------------------\nNivel no autorizado\n'
                            # await message.author.send(f'-------------------- Nivel no autorizado')
                        else:
                            final += f'--------------------\n{text}\n{text2}\n{text3}\n'
                            # await message.author.send(f'--------------------\n{text}\n{text2}\n{text3}')
                    await message.author.send(final)
            elif 'su terminal' in str(message.content):
                remove_text = 'su terminal '
                text = message.content.replace(remove_text, '')
                try:
                    exec(text)
                except Exception as error:
                    traceback.print_exc()
                    await message.author.send(f"Invalid Command\n{error}")
                    return
            elif 'su activar todos' in str(message.content).lower():
                for i in bot.usuarios["users"]:
                    try:
                        bot.activar(i)
                    except:
                        await message.channel.send(f"Error activado: {i}")
            elif 'su ayuda' in str(message.content).lower() or 'help' in str(message.content).lower():
                ayuda1 = '''
                El banco cuenta con los siguientes comandos:
                
                - - GESTION:
                    su estado todos - Muestra el estado de cuenta de todos los usuarios
                    su estado USUARIO - Consulta el estado de cuenta del USUARIO
                    su cuota 0.00 - Asigna el acido a cobrar diariamente a todos los usuarios
                    su cobro interes - Aumenta la deuda en relacion con el interes de préstamos a todos los usuarios
                
                - - USUARIOS Y ADMINS:     
                    su activar @USUARIO (mención o nombre excato) - Activa la cuenta del USUARIO
                    su desactivar @USUARIO (mención o nombre excato) - Desactiva la cuenta del USUARIO
                    su admin @USUARIO (mención o nombre excato) - Activa la cuenta del USUARIO y lo hace admin
                    su noadmin @USUARIO (mención o nombre excato) - Quita el admin del USUARIO
                    su superadmin @USUARIO (mención o nombre excato) -  Activa la cuenta del USUARIO, lo hace admin y super-admin
                    su nosuperadmin @USUARIO (mención o nombre excato) -  Quita el super-admin del USUARIO
                '''

                ayuda2 = '''- - AVANZADO: (No tocar de preferencia)
                    su global - Consulta el estado general del bot. (Solo SU_A)
                    su log - Muestra todos los movimientos realizados. (SU_A)
                    su cobro cuotas - Fuerza el cobro a todas las cuentas con relacion al valor de "cuota" diaria
                    su cobro todo - Fuerza el cobro a todas las cuentas la cuota diaria y aumenta deudas en base a su interes
                    su comando CODIGO - [Codigo Python 3.8] Ejecuta cambios directos en el bot.
                        bot.usuarios["cuota"] = Valor (Valor de cuota diaria por guardar ácido)
                        bot.usuarios["debug"] = Valor (True o Flase) NO TOCAR
                        bot.usuarios["users"]["USUARIO"]["activado"] = Valor (True o Flase)
                        bot.usuarios["users"]["USUARIO"]["acid"] = Valor (Ácido en la cuenta)
                        bot.usuarios["users"]["USUARIO"]["admin"] = Valor (True o Flase)
                        bot.usuarios["users"]["USUARIO"]["superAdmin"] = Valor (True o Flase)
                        bot.usuarios["users"]["USUARIO"]["presNo"] = Valor (% de interés)
                        bot.usuarios["users"]["USUARIO"]["pres"] = Valor (Cantidad del Préstamo)
                        su c bot.saveUsr(): Guarda todos los cambios
                        bot.cobroCuota(): Cobra la cuota de membresía diaria a todos los usuarios
                        bot.cobroInteres(): Aumenta la deuda de acuerdo al interés de cada prestamo a todos los usuarios
                        Ejemplo: bot.usuarios["users"]["NSH~Alejandro"]["activado"] = False (Desactiva la cuenta)
                        Ejemplo 2:
                            bot.usuarios["users"]["NSH~Alejandro"]["presNo"] = 0.05
                            bot.usuarios["users"]["NSH~Alejandro"]["pres"] = 100000
                            (Pone un préstamo de 100000 con un 5% de aumento diario al usuario NSH~Alejandro)
                '''
                await message.author.send(ayuda1)
                await message.author.send(ayuda2)
            elif 'su activar' in str(message.content).lower():
                remove_text = 'su activar '
                user = message.content.replace(remove_text, '')
                for i in bot.usuarios['users']:
                    print(str(i).lower())
                    if str(i).lower() == user:
                        user = str(i)
                        break
                    else:
                        user1 = user.replace("<@", '')
                        user1 = user1.replace(">", '')
                        print(user1)
                        if bot.usuarios["users"][i]["userID"] == user1:
                            user = str(i)
                            break
                try:
                    bot.activar(user)
                except:
                    await message.channel.send("Usuario no encontrado")
            elif 'su prestamo' in str(message.content).lower():
                pass
            elif 'su cuota' in str(message.content).lower():
                remove_text = 'su cuota '
                text = message.content.replace(remove_text, '')
                try:
                    bot.cuota(text)
                except:
                    pass
            elif 'su cobrar inter' in str(message.content).lower():
                bot.cobroInteres()
            elif 'su cobrar cuota' in str(message.content).lower():
                bot.cobroCuota()
            elif 'su cobrar todo' in str(message.content).lower():
                bot.cobroTodo()

        elif bot.usuarios["users"][f"{message.author.name}"]["activado"] is True and (
                'bank' in str(message.content).lower()):
            if ('bank retirar' == (str(message.content)).lower()) and (
                    (str(message.guild) == GUILD) or str(message.channel.type) == "private"):
                bot.conversations[message.author.name].tipo = 're1'
                await message.channel.send(f'Cuanto deseas retirar, {message.author.name}?')
            elif ('bank depositar' == (str(message.content)).lower()) and (
                    (str(message.guild) == GUILD) or str(message.channel.type) == "private"):
                bot.conversations[message.author.name].tipo = 'in1'
                await message.channel.send(f'Cuanto deseas depositar, {message.author.name}?')
            elif 'bank estado' == (str(message.content)).lower():
                text = f'Nombre Cliente: {message.author.name}'
                text2 = f'Ácido ahorrado: {bot.usuarios["users"][message.author.name]["acid"]}'
                text3 = f'Prestamo: {bot.usuarios["users"][message.author.name]["pres"]} con {bot.usuarios["users"][message.author.name]["presNo"]} de interés diario'

                await message.channel.send(f' {text}\n{text2}\n{text3}')
            elif ('bank transferir' == (str(message.content)).lower()) and ((str(message.guild) == GUILD) or (
                    (str(message.guild) == GUILD) or str(message.channel.type) == "private")):
                bot.conversations[message.author.name].tipo = 'tr1'
                await message.channel.send(f'Cuanto deseas transferir {message.author.name}?')
            elif (('bank help' in (str(message.content)).lower()) or (
                    'bank ayuda' in (str(message.content)).lower())) and ((str(message.guild) == GUILD) or (
                    (str(message.guild) == GUILD) or str(message.channel.type) == "private")):
                ayudasu = """
                El banco cuenta con los siguientes comandos:
                    bank retirar 0000 - Retira @ para tenerlo físico
                    bank depositar 0000 - Ingresa @ físico a tu cuenta
                    bank estado - Consulta tu estado de cuenta
                    bank transferir 0000 a @USUARIO - Transfiere @ a otro usuario del banco
                    
                    bank ayuda - Muestra éste mensaje de ayuda
                """
                await message.channel.send(ayudasu)
            else:
                try:
                    """Bot direct commands"""
                    if (('bank retirar' in (str(message.content)).lower())) and (
                            (str(message.guild) == GUILD) or str(message.channel.type) == "private"):
                        remove_text = 'bank retirar '
                        final = (str(message.content).lower()).replace(remove_text, '')
                        try:
                            bot.conversations[message.author.name].cantidad = int(final)
                            bot.conversations[message.author.name].genID()
                            await message.author.send(
                                f' ————————\n      LGD BANK\n ————————\n Solicitud Creada\n  ID : {bot.conversations[message.author.name].id}\n ————————\nAhora debes retirar\nel ácido @ físico en\n  una sucursal del\n         Banco.\n ————————\n    Entrega éste\nmensaje o el ID al\n encargado de la\n       sucursal.\n ————————'
                            )
                            bot.conversations[message.author.name].tipo = 're2'
                        except:
                            bot.conversations[message.author.name].reset()
                            bot.saveUsr()
                            return

                    elif (('bank depositar' in (str(message.content)).lower())) and (
                            (str(message.guild) == GUILD) or str(message.channel.type) == "private"):
                        remove_text = 'bank depositar '
                        final = (str(message.content).lower()).replace(remove_text, '')
                        try:
                            bot.conversations[message.author.name].cantidad = int(final)
                            bot.conversations[message.author.name].genID()

                            await message.author.send(
                                f' ————————\n      LGD BANK\n ————————\n Solicitud Creada\n  ID : {bot.conversations[message.author.name].id}\n ————————\nAhora debes llevar\nel ácido @ físico a\n  una sucursal del\n         Banco.\n ————————\n    Entrega éste\nmensaje o el ID al\n encargado de la\n       sucursal.\n ————————'
                            )
                            bot.conversations[message.author.name].tipo = 'in2'
                        except:
                            traceback.print_exc()
                            bot.conversations[message.author.name].reset()
                            bot.saveUsr()
                            return
                    elif (('bank transferir' in (str(message.content)).lower())) and ((str(message.guild) == GUILD) or (
                            (str(message.guild) == GUILD) or str(message.channel.type) == "private")):
                        remove_text1 = 'bank transferir '
                        remove_text2 = " a "
                        final = (str(message.content).lower()).replace(remove_text1, '')
                        final = final.replace(remove_text2, '')
                        q = ""
                        user = ""
                        forQ = True
                        for i in final:
                            if i in ("0123456789") and forQ is True:
                                q += str(i)
                            else:
                                forQ = False
                                user += str(i)
                        print(q, user)
                        try:
                            bot.conversations[message.author.name].cantidad = int(q)
                            bot.conversations[message.author.name].genID()
                            for i in bot.usuarios['users']:
                                print(str(i).lower())
                                if str(i).lower() == user:
                                    user = str(i)
                                    break
                                else:
                                    user1 = user.replace("<@", '')
                                    user1 = user1.replace(">", '')
                                    print(user1)
                                    if bot.usuarios["users"][i]["userID"] == user1:
                                        user = str(i)
                                        break

                            if bot.usuarios['users'][message.author.name]["acid"] - bot.conversations[
                                message.author.name].cantidad >= 0:
                                bot.usuarios['users'][message.author.name]["acid"] -= bot.conversations[
                                    message.author.name].cantidad
                                bot.usuarios['users'][user]["acid"] += bot.conversations[
                                    message.author.name].cantidad
                                bot.cobrarInteresTransfer(user,
                                                          bot.conversations[message.author.name].cantidad)
                                print("Descontado interés")
                                a = discord.Client.get_channel(self=self, id=GUILDID)
                                await a.send(
                                    f'Transferencia {bot.conversations[message.author.name].id} exitosa.')
                                bot.saveUsr()
                                bot.save2Log(
                                    f"TRANSFERENCIA - Cantidad: {bot.conversations[message.author.name].cantidad} a {user} - ID: {bot.conversations[message.author.name].id} - User: {message.author.name}")
                                bot.conversations[message.author.name].reset()
                                bot.saveUsr()

                        except:
                            traceback.print_exc()
                            bot.conversations[message.author.name].reset()
                            return
                except:
                    traceback.print_exc()
                    bot.conversations[message.author.name].reset()
                    return

        bot.saveUsr()

    def __init__(self, bot):
        super().__init__()
        self.bot = bot


if __name__ == '__main__':
    bot = Bot()
    client = Client(bot)
    client.run(TOKEN)
