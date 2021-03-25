import cx_Oracle
import os
import collections
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

INVALIDPACKAGEOWNER = os.getenv('INVALIDPACKAGEOWNER')


def GetConnection(user, password, host, service, port):
    dsn_tns = cx_Oracle.makedsn(
        host, port, service_name=service)
    conn = cx_Oracle.connect(
        user=user, password=password, dsn=dsn_tns)
    return conn


def GetPackage(packageName, user, password, host, service, port) -> str:
    conn = GetConnection(user, password, host, service, port)

    with conn.cursor() as c:
        query = "select text from dba_source where type = 'PACKAGE BODY' and name = :packageName order by line"
        c.execute(query, packageName=packageName)

        packageAsString = ''.join(row[0] for row in c)

    return packageAsString


def GetTestPackage(package_name) -> str:
    return GetPackage(package_name, TESTUSER, TESTPASS, TESTHOST, TESTSERVICENAME, TESTPORT)


def GetProdPackage(package_name) -> str:
    return GetPackage(package_name, PRODUSER, PRODPASS, PRODHOST, PRODSERVICENAME, PRODPORT)


def GetInvalidPackages() -> list:
    conn = GetConnection(PRODUSER, PRODPASS, PRODHOST,
                         PRODSERVICENAME, PRODPORT)

    with conn.cursor() as cur:
        query = """select * from dba_objects where owner = :owner and status <> 'VALID'"""
        data = cur.execute(query, owner=INVALIDPACKAGEOWNER)
        cols = [c[0] for c in data.description]
        data.rowfactory = collections.namedtuple('INVALID_OBJECTS', cols)

        invalidList = [row.OBJECT_NAME for row in cur]

    return invalidList
