import time as t
import sqlite3
from operator import truediv


def faim(date_ajd, derniereConnexion,cursor):
    faim = cursor.execute("SELECT faim from CREATURE;")
    soif = cursor.execute("SELECT soif from CREATURE;")
    if faim == 0:
        return 0
    if date_ajd == derniereConnexion:
        return faim-20
    else:
        temps = date_ajd - derniereConnexion
        if temps > 3 : # jours and soif == 100:
            if soif == 0:
                faim = faim - temps * 10
                return 0 if faim == 0 else faim
            else:
                faim = faim - temps * 15
                return 0 if faim == 0 else faim

def mourir(cursor):
    sante = cursor.execute("SELECT sante from CREATURE;")
    if sante == 0:
        return True
    else:
        return False

def soif(date_ajd, derniereConnexion,cursor):
    if date_ajd == derniereConnexion:
        return cursor.execute("SELECT sante from CREATURE;")-15
    else:
        temps = date_ajd - derniereConnexion
        if temps > 3 : # and faim == 100:
            return cursor.execute("SELECT sante from CREATURE;") - 30