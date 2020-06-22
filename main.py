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
            """Inicializa la clase conversación"""
            self.tipo = 'default'
            self.cantidad = 0
            self.chat = 'default'
            self.id = 9999999999

        @staticmethod
        def luhn_check(card_number):
            """luhn_check. Validates the CC with the last number"""
            num = list(map(int, str(card_number)))
            return sum(num[::-2] + [sum(divmod(d * 2, 10))
                                    for d in num[-2::-2]]) % 10 == 0

        def gen_id(self):
            while True:
                return1 = "9"
                ints1 = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
                for _ in range(9):
                    return1 += str(random.choice(ints1))
                for i in range(9):
                    if self.luhn_check(f'{return1}{i}') is True:
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

    def save_log(self, content):
        self.usuarios["log"]["logs"] += 1
        self.usuarios["log"]["log"][self.usuarios["log"]["logs"]] = content
        self.save_usr()

    def cobrar_interes_transfer(self, cuenta, cantidad):
        por = 0.05
        self.usuarios['users'][cuenta]['acid'] -= cantidad * por
        self.usuarios['users']['Legendary Bank']['acid'] += cantidad * por
        self.save_usr()

    def c_estado(self, modo, usuario, cantidad):
        if modo == 1:
            self.usuarios['users'][usuario]['acid'] += cantidad
        else:
            self.usuarios['users'][usuario]['acid'] -= cantidad
        self.save_usr()
        return

    def save_usr(self):
        with open('objs.txt', 'w') as f:  # Python 3: open(..., 'wb')
            json.dump(self.usuarios, f)

    def load_usr(self):
        with open('objs.txt', 'r') as f:  # Python 3: open(..., 'rb')
            self.usuarios = json.load(f)

    def cobro_cuota(self):
        # self.usuarios['date'] = str(datetime.date.today())
        self.save_usr()
        self.load_usr()
        for i in self.usuarios['users']:
            q = self.usuarios['users'][i]['acid'] * self.usuarios['cuota']
            self.usuarios['users'][i]['acid'] -= q
            self.usuarios['users']['Legendary Bank']['acid'] += q

        self.save_usr()

    def cobro_interes(self):
        # self.usuarios['date'] = str(datetime.date.today())
        self.save_usr()
        self.load_usr()
        for i in self.usuarios['users']:
            if self.usuarios['users'][i]['pres'] != 0:
                q = self.usuarios['users'][i]['pres'] * self.usuarios['users'][i]['presNo']
                self.usuarios['users'][i]['pres'] += q

        self.save_usr()

    def cobro_todo(self):
        self.usuarios['date'] = str(datetime.date.today())
        self.cobro_cuota()
        self.cobro_interes()

    def activar(self, usuario):
        self.usuarios["users"][f"{usuario}"]["activado"] = True

    def desactivar(self, usuario):
        self.usuarios["users"][f"{usuario}"]["activado"] = False

    def make_admin(self, usuario):
        self.activar(usuario)
        self.usuarios["users"][f"{usuario}"]["admin"] = True

    def make_super_admin(self, usuario):
        self.activar(usuario)
        self.make_admin(usuario)
        self.usuarios["users"][f"{usuario}"]["superAdmin"] = True

    def un_admin(self, usuario):
        self.usuarios["users"][f"{usuario}"]["admin"] = False

    def un_super_admin(self, usuario):
        self.usuarios["users"][f"{usuario}"]["superAdmin"] = False

    def prestamo(self, usuario, por, cant):
        self.usuarios["users"][f"{usuario}"]["presNo"] += por
        self.usuarios["users"][f"{usuario}"]["pres"] += cant

    def cuota(self, por):
        self.usuarios["cuota"] = int(por)

    def mostar_log(self):
        to_send = ""
        for i in self.usuarios["log"]["log"]:
            to_send += f" -- {self.usuarios['log']['log'][i]}\n"
        return to_send

    def add_usuario(self, i):
        self.usuarios["users"][f"{i.name}"] = {}
        elements = {"userID": str(i.id), "uMention": str(f"{i}"), "activado": False, "acid": 0, "admin": False,
                    "superAdmin": False, "presNo": 0, "pres": 0}
        user = self.usuarios["users"][f"{i.name}"]
        for element in elements:
            user[f"{element}"] = elements[element]

    def alternative_search(self, user):
        for i in self.usuarios['users']:
            print(str(i).lower())
            if str(i).lower() == user:
                user = str(i)
                return user
            else:
                user1 = user
                user1 = user1.replace("<@", '')
                user1 = user1.replace(">", '')
                print(user1)
                if self.usuarios["users"][i]["userID"] == user1:
                    user = str(i)
                    return user
                else:
                    print("Hasta aca")
                    user1 = user
                    user1 = user1.replace("<@", '')
                    user1 = user1.replace("!", '')
                    user1 = user1.replace(">", '')
                    if self.usuarios["users"][i]["userID"] == user1:
                        user = str(i)
                        return user
        return user


class Client(discord.Client):

    async def on_ready(self):
        # print(f'{client.user} has connected to Discord!')
        for guild in client.guilds:
            if guild.name == GUILD:
                break

        print(
            f'{client.user} is conectado:\n'
            f'Guild - {guild.name}(id: {guild.id})\n'
        )

        bot.load_usr()

        if str(bot.usuarios['date']) != str(datetime.date.today()):
            bot.cobro_todo()

        # members = '\n - '.join([member.name for member in guild.members])
        # bot.usuarios.append(bot.Usuario('NSH~Alejandro'))
        # print(f'Guild Members:\n - {members}')
        # print(f'{client}')

        for i in guild.members:
            if str(i.name) not in bot.usuarios["users"]:
                id_change: bool = False
                for j in bot.usuarios['users']:
                    if str(i.id) == str(bot.usuarios['users'][f'{j}']['userID']):
                        bot.usuarios['users'][f'{i.name}'] = bot.usuarios['users'].pop(f'{j}')
                        bot.usuarios["users"][f"{i.name}"]['uMention'] = str(f'{i}')
                        id_change = True
                        break
                if id_change is False:
                    bot.add_usuario(i)

        bot.save_usr()

        for p in bot.usuarios['users']:
            print(f"{p} : {bot.usuarios['users'][f'{p}']}")

    """async def on_member_join(self, member):
        print(member)
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, welcome to my Discord server!'
        )"""

    async def on_message(self, message):
        bot.load_usr()
        for p in bot.usuarios['users']:
            print(f"{p} : {bot.usuarios['users'][f'{p}']}")

        if bot.usuarios["debug"] is True or message.author == client.user:
            return
        if str(message.author.name) not in bot.usuarios["users"]:
            id_change = False
            for i in bot.usuarios['users']:
                if str(message.author.id) == str(bot.usuarios['users'][f'{i}']['userID']):
                    bot.usuarios['users'][f'{message.author.name}'] = bot.usuarios['users'].pop(f'{i}')
                    bot.usuarios["users"][f"{message.author.name}"]['uMention'] = str(f'{i}')
                    id_change = True
                    break
            if id_change is False:
                bot.add_usuario(message.author)
        if str(bot.usuarios['date']) != str(datetime.date.today()):
            bot.cobro_todo()
        if message.author.name not in bot.conversations.keys():
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
                            await a.send(
                                f'<@{bot.usuarios["users"][i]["userID"]}>, su retiro de fondos, {bot.conversations[i].id}, fue denegado por un administrador.')
                        except:
                            await a.send(
                                f'{i}, su retiro de fondos, {bot.conversations[i].id}, fue denegado por un administrador.')
                        bot.conversations[i].reset()
                        bot.save_usr()
                        break
                    print('TERMINADO')
                    bot.c_estado(2, i, bot.conversations[i].cantidad)
                    await a.send(f'Transferencia {bot.conversations[i].id} exitosa.')
                    bot.save_log(
                        f"RETIRO - Cantidad: {bot.conversations[i].cantidad} - ID: {bot.conversations[i].id} - User: {i}")
                    bot.conversations[i].tipo = 'default'
                    bot.save_usr()
                elif bot.conversations[i].tipo == 'in2' and str(bot.conversations[i].id) in str(message.content):
                    if 'cancelar' in str(message.content).lower():
                        try:
                            await a.send(
                                f'<@{bot.usuarios["users"][i]["userID"]}>, su depósito de fondos, {bot.conversations[i].id}, fue denegado por un administrador.')
                        except:
                            await a.send(
                                f'{i}, su depósito de fondos, {bot.conversations[i].id}, fue denegado por un administrador.')
                        bot.conversations[i].reset()
                        bot.save_usr()
                        break
                    print('TERMINADO')
                    bot.c_estado(1, i, bot.conversations[i].cantidad)
                    await a.send(f'Transferencia {bot.conversations[i].id} exitosa.')
                    bot.save_log(
                        f"DEPOSITO - Cantidad: {bot.conversations[i].cantidad} - ID: {bot.conversations[i].id} - User: {i}")
                    bot.conversations[i].tipo = 'default'
                    bot.save_usr()

        if bot.conversations[message.author.name].tipo == 're1':
            if "cancel" in message.content:
                bot.conversations[message.author.name].reset()
                bot.save_usr()
            else:
                try:
                    bot.conversations[message.author.name].cantidad = int(message.content)
                    bot.conversations[message.author.name].gen_id()

                    await message.author.send(
                        f' ————————\n      LGD BANK\n ————————\n Solicitud Creada\n  ID : {bot.conversations[message.author.name].id}\n ————————\nAhora debes retirar\nel ácido @ físico en\n  una sucursal del\n         Banco.\n ————————\n    Entrega éste\nmensaje o el ID al\n encargado de la\n       sucursal.\n ————————'
                    )
                    bot.conversations[message.author.name].tipo = 're2'
                except:
                    bot.conversations[message.author.name].reset()
                    bot.save_usr()
                    return
        elif bot.conversations[message.author.name].tipo == 'in1':
            if "cancel" in message.content:
                bot.conversations[message.author.name].reset()
                bot.save_usr()
            else:
                try:
                    bot.conversations[message.author.name].cantidad = int(message.content)
                    bot.conversations[message.author.name].gen_id()

                    await message.author.send(
                        f' ————————\n      LGD BANK\n ————————\n Solicitud Creada\n  ID : {bot.conversations[message.author.name].id}\n ————————\nAhora debes llevar\nel ácido @ físico a\n  una sucursal del\n         Banco.\n ————————\n    Entrega éste\nmensaje o el ID al\n encargado de la\n       sucursal.\n ————————'
                    )
                    bot.conversations[message.author.name].tipo = 'in2'
                except:
                    bot.conversations[message.author.name].reset()
                    bot.save_usr()
                    return
        elif bot.conversations[message.author.name].tipo == 'tr1':
            if "cancel" in message.content:
                bot.conversations[message.author.name].reset()
                bot.save_usr()
            else:
                try:
                    bot.conversations[message.author.name].cantidad = int(message.content)
                    await message.channel.send(f'A quién deseas transferir {message.content}@, {message.author.name}?')
                    bot.conversations[message.author.name].tipo = 'tr2'
                except:
                    bot.conversations[message.author.name].reset()
                    bot.save_usr()
                    return
        elif bot.conversations[message.author.name].tipo == 'tr2':
            try:
                if "cancel" in message.content:
                    bot.conversations[message.author.name].reset()
                    bot.save_usr()
                else:
                    bot.conversations[message.author.name].gen_id()
                    user = message.content
                    user = bot.alternative_search(user)
                    if bot.usuarios['users'][message.author.name]["acid"] - bot.conversations[message.author.name].cantidad >= 0:
                        bot.usuarios['users'][message.author.name]["acid"] -= bot.conversations[
                            message.author.name].cantidad
                        bot.usuarios['users'][user]["acid"] += bot.conversations[
                            message.author.name].cantidad
                        bot.cobrar_interes_transfer(user,
                                                    bot.conversations[message.author.name].cantidad)
                        print("Descontado interés")
                        a = discord.Client.get_channel(self=self, id=GUILDID)
                        await a.send(
                            f'Transferencia {bot.conversations[message.author.name].id} exitosa.')
                        bot.save_usr()
                        bot.save_log(
                            f"TRANSFERENCIA - Cantidad: {bot.conversations[message.author.name].cantidad} a {user} - ID: {bot.conversations[message.author.name].id} - User: {message.author.name}")
                        bot.conversations[message.author.name].reset()
                        bot.save_usr()
                    else:
                        await message.channel.send(
                            f'Error al procesar la transferencia {bot.conversations[message.author.name].id}: pocos fondos'
                        )
                        bot.conversations[message.author.name].reset()
            except:
                bot.conversations[message.author.name].reset()
                return

        if ('su' in (str(message.content)).lower()) and bot.usuarios['users'][f'{message.author.name}']['admin'] is True:
            print("Admin")
            if bot.usuarios['users'][f'{message.author.name}']['superAdmin'] is True:
                if 'su admin' in str(message.content).lower():
                    remove_text = 'su admin '
                    user = message.content.replace(remove_text, '')
                    user = bot.alternative_search(user)
                    try:
                        bot.make_admin(user)
                    except:
                        await message.channel.send("Usuario no encontrado")
                        return
                elif 'su superadmin' in str(message.content).lower():
                    remove_text = 'su superadmin '
                    user = message.content.replace(remove_text, '')
                    user = bot.alternative_search(user)
                    try:
                        bot.make_super_admin(user)
                    except:
                        await message.channel.send("Usuario no encontrado")
                        return
                elif 'su noadmin' in str(message.content).lower():
                    remove_text = 'su noadmin '
                    user = message.content.replace(remove_text, '')
                    user = bot.alternative_search(user)
                    try:
                        bot.un_admin(user)
                    except:
                        await message.channel.send("Usuario no encontrado")
                        return
                elif 'su nosuperadmin' in str(message.content).lower():
                    remove_text = 'su nosuperadmin '
                    user = message.content.replace(remove_text, '')
                    user = bot.alternative_search(user)
                    try:
                        bot.un_super_admin(user)
                    except:
                        await message.channel.send("Usuario no encontrado")
                elif 'su global' in str(message.content).lower():
                    bot.save_usr()
                    await message.author.send(f"SU Global State:\n{json.dumps(bot.usuarios, indent=4)}")
                elif 'su log' in str(message.content).lower():
                    text = bot.mostar_log()
                    await message.author.send(f"LOG:\n{text}")
                elif 'su cuota' in str(message.content).lower():
                    remove_text = 'su cuota '
                    text = message.content.replace(remove_text, '')
                    try:
                        bot.cuota(text)
                    except:
                        pass
                elif 'su terminal' in str(message.content):
                    remove_text = 'su terminal '
                    text = message.content.replace(remove_text, '')
                    try:
                        exec(text)
                    except Exception as error:
                        traceback.print_exc()
                        await message.author.send(f"Invalid Command\n{error}")
                        return
            if 'su estado' in str(message.content).lower():
                if 'todos' not in str(message.content):
                    remove_text = 'su estado '
                    text = message.content.replace(remove_text, '')
                    text = bot.alternative_search(text)
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

                        if bot.usuarios["users"][i]["admin"] is True and bot.usuarios["users"][message.author.name]["superAdmin"] is True:
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
            elif 'su activar todos' in str(message.content).lower():
                for i in bot.usuarios["users"]:
                    try:
                        bot.activar(i)
                    except:
                        await message.channel.send(f"Error activado: {i}")
            elif 'su ayuda' in str(message.content).lower() or 'help' in str(message.content).lower():
                ayuda1 = "El banco cuenta con los siguientes comandos:\n- - GESTION:\n    su estado todos - Muestra el estado de cuenta de todos los usuarios\n    su estado USUARIO - Consulta el estado de cuenta del USUARIO\n    su cuota 0.00 - Asigna el acido a cobrar diariamente a todos los usuarios\n    su cobro interes - Aumenta la deuda en relacion con el interes de préstamos a todos los usuarios\n\n- - USUARIOS Y ADMINS:     \n    su activar @USUARIO (mención o nombre excato) - Activa la cuenta del USUARIO\n    su desactivar @USUARIO (mención o nombre excato) - Desactiva la cuenta del USUARIO\n    su admin @USUARIO (mención o nombre excato) - Activa la cuenta del USUARIO y lo hace admin\n    su noadmin @USUARIO (mención o nombre excato) - Quita el admin del USUARIO\n    su superadmin @USUARIO (mención o nombre excato) -  Activa la cuenta del USUARIO, lo hace admin y super-admin\n    su nosuperadmin @USUARIO (mención o nombre excato) -  Quita el super-admin del USUARIO"
                ayuda2 = '- - AVANZADO: (No tocar de preferencia)\n    su global - Consulta el estado general del bot. (Solo SU_A)\n    su log - Muestra todos los movimientos realizados. (SU_A)\n    su cobro cuotas - Fuerza el cobro a todas las cuentas con relacion al valor de "cuota" diaria\n    su cobro todo - Fuerza el cobro a todas las cuentas la cuota diaria y aumenta deudas en base a su interes\n    su comando CODIGO - [Codigo Python 3.8] Ejecuta cambios directos en el bot.\n        bot.usuarios["cuota"] = Valor (Valor de cuota diaria por guardar ácido)\n        bot.usuarios["debug"] = Valor (True o False) NO TOCAR\n        bot.usuarios["users"]["USUARIO"]["activado"] = Valor (True o False)\n        bot.usuarios["users"]["USUARIO"]["acid"] = Valor (Ácido en la cuenta)\n        bot.usuarios["users"]["USUARIO"]["admin"] = Valor (True o False)\n        bot.usuarios["users"]["USUARIO"]["superAdmin"] = Valor (True o False)\n        bot.usuarios["users"]["USUARIO"]["presNo"] = Valor (% de interés)\n        bot.usuarios["users"]["USUARIO"]["pres"] = Valor (Cantidad del Préstamo)\n        su c bot.save_usr(): Guarda todos los cambios\n        bot.cobro_cuota(): Cobra la cuota de membresía diaria a todos los usuarios\n        bot.cobro_interes(): Aumenta la deuda de acuerdo al interés de cada prestamo a todos los usuarios\n        Ejemplo: bot.usuarios["users"]["NSH~Alejandro"]["activado"] = False (Desactiva la cuenta)\n        Ejemplo 2:\n            bot.usuarios["users"]["NSH~Alejandro"]["presNo"] = 0.05\n            bot.usuarios["users"]["NSH~Alejandro"]["pres"] = 100000\n            (Pone un préstamo de 100000 con un 5% de aumento diario al usuario NSH~Alejandro)'
                await message.author.send(ayuda1)
                await message.author.send(ayuda2)
            elif 'su activar' in str(message.content).lower():
                remove_text = 'su activar '
                user = message.content.replace(remove_text, '')
                user = bot.alternative_search(user)
                try:
                    bot.activar(user)
                except:
                    await message.channel.send("Usuario no encontrado")
            elif 'su prestamo' in str(message.content).lower():
                pass
            elif 'su cobrar inter' in str(message.content).lower():
                bot.cobro_interes()
            elif 'su cobrar cuota' in str(message.content).lower():
                bot.cobro_cuota()
            elif 'su cobrar todo' in str(message.content).lower():
                bot.cobro_todo()

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
                text3 = f'Prestamo: {bot.usuarios["users"][message.author.name]["pres"]} con {bot.usuarios["users"][message.author.name]["presNo"]} de interés diario '

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
            elif (('bank state' in (str(message.content)).lower()) and ((str(message.guild) == GUILD) or (
                    (str(message.guild) == GUILD) or str(message.channel.type) == "private"))):
                administradores = ""
                for i in bot.usuarios['users']:
                    if (bot.usuarios['users'][f'{i}']['admin'] or bot.usuarios['users'][f'{i}']['superAdmin']) and str(
                            f'{i}') != "Legendary Bank":
                        administradores += f"  {i}\n"
                ayudasu = f"Banco: LGD Bank\n——————————\nFecha: {bot.usuarios['date']}\nCuota diaria: {float(bot.usuarios['cuota']) * 100}%\nUsarios: {len(bot.usuarios['users']) - 1}\n——————————\nAdministradores:\n{administradores}"
                await message.channel.send(ayudasu)
            else:
                try:
                    """Bot direct commands"""
                    if ('bank retirar' in (str(message.content)).lower()) and (
                            (str(message.guild) == GUILD) or str(message.channel.type) == "private"):
                        remove_text = 'bank retirar '
                        final = (str(message.content).lower()).replace(remove_text, '')
                        try:
                            bot.conversations[message.author.name].cantidad = int(final)
                            bot.conversations[message.author.name].gen_id()
                            await message.author.send(
                                f' ————————\n      LGD BANK\n ————————\n Solicitud Creada\n  ID : {bot.conversations[message.author.name].id}\n ————————\nAhora debes retirar\nel ácido @ físico en\n  una sucursal del\n         Banco.\n ————————\n    Entrega éste\nmensaje o el ID al\n encargado de la\n       sucursal.\n ————————'
                            )
                            bot.conversations[message.author.name].tipo = 're2'
                        except:
                            bot.conversations[message.author.name].reset()
                            bot.save_usr()
                            return

                    elif ('bank depositar' in (str(message.content)).lower()) and (
                            (str(message.guild) == GUILD) or str(message.channel.type) == "private"):
                        remove_text = 'bank depositar '
                        final = (str(message.content).lower()).replace(remove_text, '')
                        try:
                            bot.conversations[message.author.name].cantidad = int(final)
                            bot.conversations[message.author.name].gen_id()

                            await message.author.send(
                                f' ————————\n      LGD BANK\n ————————\n Solicitud Creada\n  ID : {bot.conversations[message.author.name].id}\n ————————\nAhora debes llevar\nel ácido @ físico a\n  una sucursal del\n         Banco.\n ————————\n    Entrega éste\nmensaje o el ID al\n encargado de la\n       sucursal.\n ————————'
                            )
                            bot.conversations[message.author.name].tipo = 'in2'
                        except:
                            traceback.print_exc()
                            bot.conversations[message.author.name].reset()
                            bot.save_usr()
                            return
                    elif ('bank transferir' in (str(message.content)).lower()) and ((str(message.guild) == GUILD) or (
                            (str(message.guild) == GUILD) or str(message.channel.type) == "private")):
                        remove_text1 = 'bank transferir '
                        remove_text2 = " a "
                        final = (str(message.content).lower()).replace(remove_text1, '')
                        final = final.replace(remove_text2, '')
                        q = ""
                        user = ""
                        for_q = True
                        for i in final:
                            if i in ("0123456789") and for_q is True:
                                q += str(i)
                            else:
                                for_q = False
                                user += str(i)
                        print(q, user)
                        try:
                            bot.conversations[message.author.name].cantidad = int(q)
                            bot.conversations[message.author.name].gen_id()
                            user = bot.alternative_search(user)

                            if bot.usuarios['users'][message.author.name]["acid"] - bot.conversations[message.author.name].cantidad >= 0:
                                bot.usuarios['users'][message.author.name]["acid"] -= bot.conversations[
                                    message.author.name].cantidad
                                bot.usuarios['users'][user]["acid"] += bot.conversations[
                                    message.author.name].cantidad
                                bot.cobrar_interes_transfer(user,
                                                            bot.conversations[message.author.name].cantidad)
                                print("Descontado interés")
                                a = discord.Client.get_channel(self=self, id=GUILDID)
                                await a.send(
                                    f'Transferencia {bot.conversations[message.author.name].id} exitosa.')
                                bot.save_usr()
                                bot.save_log(
                                    f"TRANSFERENCIA - Cantidad: {bot.conversations[message.author.name].cantidad} a {user} - ID: {bot.conversations[message.author.name].id} - User: {message.author.name}")
                                bot.conversations[message.author.name].reset()
                                bot.save_usr()

                        except:
                            traceback.print_exc()
                            bot.conversations[message.author.name].reset()
                            return
                except:
                    traceback.print_exc()
                    bot.conversations[message.author.name].reset()
                    return

        bot.save_usr()

    def __init__(self, bot):
        super().__init__()
        self.bot = bot


if __name__ == '__main__':
    bot = Bot()
    client = Client(bot)
    client.run(TOKEN)
