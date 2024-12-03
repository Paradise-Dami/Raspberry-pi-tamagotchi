import time as t
import sqlite3
from datetime import datetime as dt

from database_code import *
def tempsPasse(cursor):
    derniereCo = cursor.execute("SELECT dernièreConnexion from CREATURE;")
    derniereCo_dt = dt.strptime(derniereCo, "%Y-%m-%d %H:%M:%S")
    ajd = dt.now()
    ecart_jrs = (ajd-derniereCo_dt).days
    ecart_h = ((ajd - derniereCo_dt).seconds)/60**2
    return ecart_jrs if ecart_jrs > 0 else float(ecart_h)

date = "2024-12-02 23:37:56"
date2 = "2024-12-01 23:37:56"

def stat_A_Zero(stat:int):
    #renvoie la stat à zéro si elle est inférieure à 0
    if stat < 0:
        return 0
    else:
        return stat

def besoinQuiSEcoule(nomStatSpe:str,tempsPasse1:int|float,cursor,manque_grosManque:list):
    #n'inclut pas la précision des heures si il y'a au moins un jour d'écoulé
    j, h = 0, 0
    if type(tempsPasse1) is int:
        j = tempsPasse1
    else:
        h = int(tempsPasse1)
    #statSpe = cursor.execute("SELECT "+nomStatSpe+" from CREATURE;")
    #stats = cursor.execute("SELECT sante from CREATURE;")
    statSpe = 100
    stats = 100
    manque = manque_grosManque[0]
    grosManque = manque_grosManque[1]

    while j > 0 and h > 0:

        if statSpe <= 0:
            if j >= 0:
                stats -= grosManque/2
                j -= 1
            else:
                stats -= manque/2
                h -= 1
        else:
            if j >= 0:
                statSpe -= grosManque
                j -= 1
            else:
                statSpe -= manque
                h -= 1

    #miseAjourDonnéeBDD("CREATURE",nomStatSpe, stat_A_Zero(statSpe),cursor)
    #miseAjourDonnéeBDD("CREATURE", "sante", stat_A_Zero(stats),cursor)

besoinQuiSEcoule("e",tempsPasse(date),temp(),[1,20])
def faim(derniereConnexion,cursor):
    besoinQuiSEcoule(derniereConnexion,cursor,[1,20])

def derniereConnexion(cursor):
    #save la dernière connexion toutes les 5 minutes
    t = tempsPasse(cursor)
    if t is int:
        miseAjourDonnéeBDD("CREATURE", "dernièreConnexion", str(dt.now()), cursor)
    elif t > 5:
        miseAjourDonnéeBDD("CREATURE", "dernièreConnexion", str(dt.now()), cursor)

print(derniereConnexion())


print(tempsPasse(date))
print(tempsPasse(date2))

def mourir(cursor):
    sante = cursor.execute("SELECT sante from CREATURE;")
    if sante == 0:
        return True
    else:
        return False

