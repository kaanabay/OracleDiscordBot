import io
import os
from datetime import datetime

import discord
from discord.ext import commands
from dotenv import load_dotenv

import GeneralUtils
import OracleConn
import DifferHelper
import Logger

BOT = commands.Bot(command_prefix='!')


@BOT.event
async def on_ready():
    print(f'{BOT.user.name} has connected to Discord')


@BOT.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.MissingRequiredArgument):
        await ctx.send("A parameter is missing")


@BOT.command(name='gdiff', help='Verilen paketin prod ve test ortamları arasındaki farklarını bulur.')
async def GetPackageDiff(ctx, package_name: str):

    package_name = package_name.upper()

    testPackage = OracleConn.GetTestPackage(package_name).splitlines()
    prodPackage = OracleConn.GetProdPackage(package_name).splitlines()

    diff = DifferHelper.ComputeDiff(testPackage, prodPackage)

    if not prodPackage:
        await ctx.send('Hayallerde yaşıyor bazı paketler...')
    elif not diff:
        await ctx.send('No fark, no cry!')
    else:
        f = io.StringIO(diff)

        filename = f'{package_name}_DIFF_{GeneralUtils.GetDateStr(datetime.now())}.txt'
        Logger.Log(f'{filename} is generated.', str(ctx.message.author))

        await ctx.send(file=discord.File(f, filename=filename))


@BOT.command(name='gtest', help='Test ortamından paketi txt formatında getirir.')
async def GetTestPackage(ctx, package_name: str):
    package_name = package_name.upper()

    file = io.StringIO(OracleConn.GetTestPackage(package_name))
    filename = f'{package_name}_TEST_{GeneralUtils.GetDateStr(datetime.now())}.txt'
    Logger.Log(f'{filename} is generated.', str(ctx.message.author))

    await ctx.send(file=discord.File(file, filename=filename))


@BOT.command(name='gprod', help='Prod ortamından paketi txt formatında getirir.')
async def GetProdPackage(ctx, package_name: str):
    package_name = package_name.upper()

    file = io.StringIO(OracleConn.GetProdPackage(package_name))
    filename = f'{package_name}_PROD_{GeneralUtils.GetDateStr(datetime.now())}.txt'
    Logger.Log(f'{filename} is generated.', str(ctx.message.author))

    await ctx.send(file=discord.File(file, filename=filename))


@BOT.command(name='ginv', help='Prod ortamındaki invalid paketleri sorgular.')
async def GetInvalidPackages(ctx):
    invalidList = OracleConn.GetInvalidPackages()
    newLine = '\n'
    queryTime = GeneralUtils.GetDateStrPretty(datetime.now())
    if invalidList:
        msg = f'**Invalid Packages as of {queryTime}**```{newLine}{newLine.join(invalidList)}```'
    else:
        msg = 'Bütün paketlerin durumu iyi maşallah.'
    await ctx.send(msg)


load_dotenv()
BOT.run(os.getenv('DISCORD_TOKEN'))
