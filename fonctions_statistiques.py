from datetime import datetime as dt
import sqlite3
import os
import time
import Fonction_Modules as fm
import RPi.GPIO as GPIO
from grove.grove_button import GroveButton
from grove.adc import ADC

if not os.path.isfile("bdd.db"):
    with sqlite3.connect("bdd.db", check_same_thread=False) as conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE CREATURE(nom,sante, nourri, desaltere, ennui, etat, derniereConnexion);")
        cur.execute("CREATE TABLE CAPTEURS(boutonNourrir,boutonBoire,potentiometre);")
        cur.execute("INSERT INTO CREATURE(nom,sante, nourri, desaltere, ennui, etat,  derniereConnexion) VALUES('Bmo', 100, 20, 20, 10, 'vivant', '" + str(dt.today().strftime("%Y-%m-%d %H:%M:%S")) + "' );")
        cur.execute("INSERT INTO CAPTEURS(boutonNourrir,boutonBoire,potentiometre) VALUES(False,False,50);") #50 charge neutre temporaire

#----Variables----
database = sqlite3.connect("bdd.db", check_same_thread=False)
dicStatuts: dict= {"sante":"est malade", "nourri":"a faim",
                         "ennui":"s'ennuie" , "desaltere":"a soif"}
dicPaliers: dict = {"sante": 50, "nourri": 50, "desaltere": 50, "ennui": 50}
date: str = "2024-12-02 16:37:56"
date2: str = "2024-12-01 23:37:56"
affecteNormal: list = [30,  4,    2]
affecteFort: list =   [45,  11,   5]
pinPoten = 0
def afficher_db(db: str, table: str) -> dict:
    """return la data de la table sql sous forme de dictionnaire."""
    try:
        con = database
        con.row_factory = sqlite3.Row
        
        # Exécution de la requête
        cursor = con.execute(f"SELECT * FROM [{table}]")
        rows = cursor.fetchall()
        
        # Conversion des résultats en JSON
        json_data = []
        for row in rows:
            result = {k: row[k] for k in row.keys()}
            json_data.append(result)
        return json_data[0] #on n'a qu'un seul utilisateur pour le moment donc je prends juste la première valeur
    
    #Gérer tout types d'erreurs dans la lecture
    except sqlite3.Error as e:
        print(f"Erreur de db: {e}")
        return {"erreur": str(e)}
    
    except Exception as e:
        print(f"Erreur innatendue: {e}")
        return {"erreur": "erreur"}

def miseAjourDonnéeBDD(table:str,attribut:str,donnee:str | int )-> None:
    """met à jour les attributs de la base de données"""
    conn = database
    cur = conn.cursor()
    time.sleep(1)
    cur.execute("UPDATE " + table + " SET " + attribut + " = '" + str(donnee) + "';")  # 50 charge neutre temporaire
    cur.execute("SELECT * from CREATURE;")
    t = cur.fetchall()[0][1]
    return(t)

def gestionDonnees()-> None:
    # crée une database si elle n'existe pas déjà avec les tables
    conn = database
    cur = conn.cursor()
    
    #sinon modifie les données normalement
    
    cur.execute("SELECT etat from CREATURE;")
    s = cur.fetchall()[0][0]

    if s == "mort":#(ça veut dire que le Tamagotchi est mort et aucune action n'a été réalisée depuis)
        return  
        
    elif s == "reanime": #(ça veut dire que le bouton de reset a été pressé sur le site, qui a modifié la db)
        cur.execute("update CREATURE set sante = 100, nourri = 50, desaltere = 50, ennui = 50, etat = 'vivant' from (select * from CREATURE);")   
    else:
        # sinon modifie les données normalement
        derniereConnexion()
    


def tempsPasse(derniereConnexion:str="")-> list:
    if derniereConnexion == "":
        conn = database
        cur = conn.cursor()
        cur.execute("SELECT derniereConnexion from CREATURE;")
        derniereConnexion = cur.fetchall()[0][0] #permet de récup les résultats des lignes exécutées
            
    derniereCo_dt = dt.strptime(derniereConnexion, "%Y-%m-%d %H:%M:%S")
    ajd = dt.now()
    diff = ajd-derniereCo_dt
    ecart_jrs = diff.days
    ecart_h = diff.seconds//3600
    ecart_min = (diff.seconds%3600 )// 60
    return [ecart_jrs,ecart_h,ecart_min]


def stat_A_Zero(stat:int):
    #renvoie la stat à zéro si elle est inférieure à 0
    if stat < 0:
        return 0
    else:
        return stat

def besoinQuiSEcoule(nomStatSpe:str,tempsPasse1:list,manque_grosManque:list):

    j, h, m = tempsPasse1[0], tempsPasse1[1], tempsPasse1[2]
    conn = database
    cur = conn.cursor()
    cur.execute("SELECT "+nomStatSpe+" from CREATURE;")
    statSpe = float(cur.fetchall()[0][0])
    #statSpe = cur.fetchall()[0][0]
    cur.execute("SELECT sante from CREATURE;")
        
    stats = float(cur.fetchall()[0][0])
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
    
    print(statSpe,stats)
    miseAjourDonnéeBDD("CREATURE",nomStatSpe, stat_A_Zero(statSpe))
    miseAjourDonnéeBDD("CREATURE", "sante", stat_A_Zero(stats))
    

def faim(derniereConnexion,manque:list[int,int,int])-> None:
    #applique un effet de faim au tamagotchi, faisant baisser sa satiété
    print("faim")
    besoinQuiSEcoule("nourri",tempsPasse(derniereConnexion),manque)


def nourrir(t)-> None:
    """Augmente la statistique nourri dans la bdd"""
    sasiete = float(afficher_db("bdd.db","CREATURE")["nourri"])
    miseAjourDonnéeBDD("CREATURE","nourri", sasiete + 10)
    fm.sortie_buzz(5, 1, 0.5, 500, 1) #petit bruit pour confirmer l'action
bouton_nourrir = fm.GroveButton(16)
bouton_nourrir.on_press = nourrir


def soif(derniereConnexion, manque:list):
    print("soif")
    besoinQuiSEcoule("desaltere",tempsPasse(derniereConnexion),manque)


def ennui(derniereConnexion, manque:list):
    print("ennui")
    besoinQuiSEcoule("ennui",tempsPasse(derniereConnexion),manque)


def derniereConnexion() -> None:
    #save la dernière connexion toutes les 1 minutes
    global dicStatuts
    t = tempsPasse()
    conn = database
    cur = conn.cursor()
    cur.execute("SELECT derniereConnexion from CREATURE;")
    derniereCo_save = cur.fetchall()[0][0]
    if t is int:
        miseAjourDonnéeBDD("CREATURE", "derniereConnexion", str(dt.now().strftime("%Y-%m-%d %H:%M:%S")))
    if t[2] > 1 or t[1] > 0 or t[0] > 0:
        miseAjourDonnéeBDD("CREATURE", "derniereConnexion", str(dt.now().strftime("%Y-%m-%d %H:%M:%S")))
        affectation = statutAffecte(dicStatuts)
        #mise à jour de toutes les autres stats
        faim(derniereCo_save,affectation["nourri"])
        soif(derniereCo_save,affectation["desaltere"])
        ennui(derniereCo_save,affectation["ennui"])
#derniereConnexion()


def mourir() -> None:
    conn = database
    cur = conn.cursor()
    cur.execute("SELECT sante from CREATURE;")
    sante = float(cur.fetchall()[0][0])
    if sante <= 0:
        miseAjourDonnéeBDD("CREATURE", "etat", "mort")


def statutAffiche(dicPaliers:dict,dicStatuts:dict) -> list[str]:

    global pinPoten
    #récupère toutes les stats actuelles de la BDD
    conn = database
    cur = conn.cursor()
    cur.execute("SELECT sante, nourri, desaltere, ennui from CREATURE;")
    sante, nourri, desaltere, ennui = cur.fetchall()[0]
    d = {"sante": float(sante), "nourri": float(nourri), "desaltere": float(desaltere), "ennui": float(ennui)}
    statTemp = fm.temperature(pinPoten)
    statuts = []
    statuts.append(statTemp)
    for i in d:
        if d[i] < dicPaliers[i]:
            statuts.append(dicStatuts[i])

    # si le Tamagotchi a tous les statuts, il est triste
    if len(statuts) == len(dicStatuts):
        statuts.append("est triste")

    #à l'inverse, s'il n'en a aucun, il est heureuxx !
    elif len(statuts) == 0:
        statuts.append("est heureux")
    return statuts

#print(statutAffiche({"santé": 50, "nourri": 50, "désaltéré": 50, "ennui": 5}))

def statutAffecte(dicStatuts:dict) -> dict:
                    #jour heure minute
    global affecteNormal
    global affecteFort
    dictAffectStats = {"sante": None, "nourri": None, "desaltere": None, "ennui": None}
    #au cas où on change le nom associé à la clé
    malade = dicStatuts["sante"]

    statutsCreature = statutAffiche(dicPaliers,dicStatuts)
    for statut in dicStatuts:
        if dicStatuts[statut] in statutsCreature:
            #s'il est malade, toutes ses stats se vident plus vite
            if statut == malade:
                for s in dicStatuts:
                    dictAffectStats[s] = affecteFort
                return dictAffectStats
            else:
                dictAffectStats[statut] = affecteFort
        else:
            dictAffectStats[statut] = affecteNormal

    return dictAffectStats


#statutAffecte(dicStatuts) #mets les affectations liées au statut dan la base de données..


"""
with database as conn:
    cur = conn.cursor()
    cur.execute("update CREATURE set sante = 100, nourri = 50, desaltere = 50, ennui = 50 from (select * from CREATURE);")
    cur.execute("SELECT sante, nourri, desaltere, ennui from CREATURE;")
    print(cur.fetchall()[0])
listePaliers = [50, 50, 50, 50]
#statutAffiche(listePaliers)
"""

gestionDonnees()
