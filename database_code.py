import sqlite3
import os
import time
from datetime import datetime as dt
"""
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return "bite"

print(find("test.db", "Users\prude\PycharmProjects\tamagotchi\test.db"))
"""
#ferme la connexion à la database automatiquement en sortant de la boucle


#création de la database avec ses tables

def miseAjourDonnéeBDD(table:str,attribut:str,donnee:str | int,cursor):
    """met à jour les attributs de la base de données"""
    time.sleep(1)
    cursor.execute("UPDATE " + table + " SET " + attribut + " = '" + str(donnee) + "';")  # 50 charge neutre temporaire


try:
    # crée une database si elle n'existe pas déjà avec les tables
    if not os.path.isfile("bdd.db"):
        with sqlite3.connect("bdd.db") as conn:
            cur = conn.cursor()
            cur.execute("CREATE TABLE CREATURE(nom,sante, nourri, désaltéré, ennui, statut,dernièreConnexion);")
            cur.execute("CREATE TABLE CAPTEURS(boutonNourrir,boutonBoire,potentiomètre);")
            cur.execute("INSERT INTO CREATURE(nom,sante, faim, soif, ennui, statut) VALUES('Beemo', 100, 20, 20, 10, 'Heureux', '" + str(dt.today()) + "' );")
            cur.execute("INSERT INTO CAPTEURS(boutonFaim,boutonSoif,potentiomètre) VALUES(False,False,50);") #50 charge neutre temporaire

    #sinon s'y connecte
    else:
        with sqlite3.connect("database.db") as conn:
            cur = conn.cursor()
            #miseAjourDonnéeBDD("CREATURE","nourri",5,cur)

            pass

except sqlite3.OperationalError as e:
    print("Failed to open database:", e)

def temp():
    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()
        return cur






