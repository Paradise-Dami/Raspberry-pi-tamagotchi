from datetime import datetime as dt

from database_code import *


def tempsPasse(derniereConnexion:str="")-> list:
    
    if derniereConnexion == "":
        with sqlite3.connect("bdd.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT dernièreConnexion from CREATURE;")
            derniereConnexion = cur.fetchall()[0][0] #permet de récup les résultats des lignes exécutées
            
    #print(derniereConnexion)
    derniereCo_dt = dt.strptime(derniereConnexion, "%Y-%m-%d %H:%M:%S")
    ajd = dt.now()
    print(ajd)
    diff = ajd-derniereCo_dt
    ecart_jrs = diff.days
    ecart_h = diff.seconds//3600
    #print(ecart_h, 0)
    ecart_min = (diff.seconds%3600 )// 60
    return [ecart_jrs,ecart_h,ecart_min]

date = "2024-12-02 16:37:56"
date2 = "2024-12-01 23:37:56"

#print(tempsPasse())
#print(tempsPasse(date))
def stat_A_Zero(stat:int):
    #renvoie la stat à zéro si elle est inférieure à 0
    if stat < 0:
        return 0
    else:
        return stat

def besoinQuiSEcoule(nomStatSpe:str,tempsPasse1:list,manque_grosManque:list):
    #n'inclut pas la précision des heures si il y'a au moins un jour d'écoulé
    j, h, m = tempsPasse1[0], tempsPasse1[1], tempsPasse1[2]
    print(f"jours :{j} heures :{h} minutes: {m}")
    with sqlite3.connect("bdd.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT "+nomStatSpe+" from CREATURE;")
        statSpe = float(cur.fetchall()[0][0])
        #statSpe = cur.fetchall()[0][0]
        cur.execute("SELECT sante from CREATURE;")
        
        stats = eval(cur.fetchall()[0][0])
        print(statSpe, stats)
        manqueTempsReel = manque_grosManque[2]
        manque = manque_grosManque[1]
        grosManque = manque_grosManque[0]

        while j > 0 or h > 0 or m > 0:
            
            if statSpe <= 0:
                if j >= 0:
                    stats -= grosManque/2
                    j -= 1
                elif h > 0:
                    stats -= manque/2
                    h -= 1
                else:
                    stats -= manqueTempsReel/ 2
                    m -= 1
            else:
                if j > 0:
                    statSpe -= grosManque
                    j -= 1
                elif h > 0:
                    statSpe -= manque
                    h -= 1
                else:
                    statSpe -= manqueTempsReel/ 2
                    m -= 1
        

        miseAjourDonnéeBDD("CREATURE",nomStatSpe, stat_A_Zero(statSpe))
        miseAjourDonnéeBDD("CREATURE", "sante", stat_A_Zero(stats))
        

#besoinQuiSEcoule("nourri",tempsPasse(date),[20,5,1]) #test sans le code lié au sql

def faim(derniereConnexion):
    besoinQuiSEcoule("nourri",tempsPasse(derniereConnexion),[20,5,1])

def soif(derniereConnexion):
    besoinQuiSEcoule("désaltéré",tempsPasse(derniereConnexion),[20,5,1])

def ennui(derniereConnexion):
    besoinQuiSEcoule("ennui",tempsPasse(derniereConnexion),[20,5,1])
"""
faim("")
ennui("") #à vérifier : en mettant à jour la db
soif("")
"""
def derniereConnexion():
    #save la dernière connexion toutes les 5 minutes
    t = tempsPasse()
    with sqlite3.connect("bdd.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT dernièreConnexion from CREATURE;")
        derniereCo_save = float(cur.fetchall()[0][0])
    if t is int:
        miseAjourDonnéeBDD("CREATURE", "dernièreConnexion", str(dt.now().strftime("%Y-%m-%d %H:%M:%S")))
    if t[2] > 5 or t[1] > 0 or t[0] > 0:
        miseAjourDonnéeBDD("CREATURE", "dernièreConnexion", str(dt.now().strftime("%Y-%m-%d %H:%M:%S")))
    #mise à jour de toutes les autres stats
        faim(derniereCo_save)
        soif(derniereCo_save)
        ennui(derniereCo_save)
print(derniereConnexion())
"""

print(tempsPasse(date))
print(tempsPasse(date2))
"""
def mourir():
    with sqlite3.connect("bdd.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT sante from CREATURE;")
        sante = eval(cur.fetchall()[0][0])
    if sante <= 0:
        return True
    else:
        return False

