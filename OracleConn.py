import cx_Oracle
import os
from dotenv import load_dotenv

load_dotenv()

TESTUSER = os.getenv('TESTUSER')
TESTPASS = os.getenv('TESTPASS')
TESTHOST = os.getenv('TESTHOST')
TESTSERVICENAME = os.getenv('TESTSERVICENAME')
TESTPORT = os.getenv('TESTPORT')

PRODUSER = os.getenv('PRODUSER')
PRODPASS = os.getenv('PRODPASS')
PRODHOST = os.getenv('PRODHOST')
PRODSERVICENAME = os.getenv('PRODSERVICENAME')
PRODPORT = os.getenv('PRODPORT')


def GetPackage(packageName, user, password, host, service, port) -> str:
    dsn_tns = cx_Oracle.makedsn(
        host, port, service_name=service)
    conn = cx_Oracle.connect(
        user=user, password=password, dsn=dsn_tns)

    c = conn.cursor()
    c.execute(
        f"select text from dba_source where type = 'PACKAGE BODY' and name = '{packageName}' order by line")

    packageAsString = ''.join(row[0] for row in c)
    conn.close()

    return packageAsString


def GetTestPackage(package_name) -> str:
    return GetPackage(package_name, TESTUSER, TESTPASS, TESTHOST, TESTSERVICENAME, TESTPORT)


def GetProdPackage(package_name) -> str:
    return GetPackage(package_name, PRODUSER, PRODPASS, PRODHOST, PRODSERVICENAME, PRODPORT)
