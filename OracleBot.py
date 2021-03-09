import io
import os

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

        filename = f'{package_name}_DIFF_{GeneralUtils.GetDateStr()}.txt'
        Logger.Log(f'{filename} is generated.', str(ctx.message.author))

        await ctx.send(file=discord.File(f, filename=filename))


@BOT.command(name='gtest', help='Test ortamından paketi txt formatında getirir.')
async def GetTestPackage(ctx, package_name: str):
    package_name = package_name.upper()

    file = io.StringIO(OracleConn.GetTestPackage(package_name))
    filename = f'{package_name}_TEST_{GeneralUtils.GetDateStr()}.txt'
    Logger.Log(f'{filename} is generated.', str(ctx.message.author))

    await ctx.send(file=discord.File(file, filename=filename))


@BOT.command(name='gprod', help='Prod ortamından paketi txt formatında getirir.')
async def GetProdPackage(ctx, package_name: str):
    package_name = package_name.upper()

    file = io.StringIO(OracleConn.GetProdPackage(package_name))
    filename = f'{package_name}_PROD_{GeneralUtils.GetDateStr()}.txt'
    LLogger.Log(f'{filename} is generated.', str(ctx.message.author))

    await ctx.send(file=discord.File(file, filename=filename))

load_dotenv()
BOT.run(os.getenv('DISCORD_TOKEN'))
