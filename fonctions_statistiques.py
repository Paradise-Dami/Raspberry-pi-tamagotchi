from datetime import datetime as dt
import sqlite3
import os
import time

def afficher_db(db: str, table: str) -> dict:
    """return la data de la table sql sous forme de dictionnaire."""
    try:
        con = sqlite3.connect(db)
        con.row_factory = sqlite3.Row
        
        # Exécution de la requête
        cursor = con.execute(f"SELECT * FROM [{table}]")
        rows = cursor.fetchall()
        
        # Conversion des résultats en JSON
        json_data = []
        for row in rows:
            result = {k: row[k] for k in row.keys()}
            json_data.append(result)
        con.close()
        return result
    
    except sqlite3.Error as e:
        print(f"Erreur de db: {e}")
        return {"erreur": str(e)}
    
    except Exception as e:
        print(f"Erreur innatendue: {e}")
        return {"erreur": "erreur"}

def miseAjourDonnéeBDD(table:str,attribut:str,donnee:str | int | list | dict)-> None:
    """met à jour les attributs de la base de données"""
    with sqlite3.connect("bdd.db") as conn:
            cur = conn.cursor()
            time.sleep(1)
            cur.execute("UPDATE " + table + " SET " + attribut + " = '" + str(donnee) + "';")  # 50 charge neutre temporaire


def gestionDonnees()-> None:
    # crée une database si elle n'existe pas déjà avec les tables
    if not os.path.isfile("bdd.db"):
        with sqlite3.connect("bdd.db") as conn:
            cur = conn.cursor()
            cur.execute("CREATE TABLE CREATURE(nom,sante, nourri, desaltere, ennui, statut,derniereConnexion);")
            cur.execute("CREATE TABLE CAPTEURS(boutonNourrir,boutonBoire,potentiometre);")
            cur.execute("INSERT INTO CREATURE(nom,sante, nourri, desaltere, ennui, statut, derniereConnexion) VALUES('Beemo', 100, 20, 20, 10, 'Heureux', '" + str(dt.today().strftime("%Y-%m-%d %H:%M:%S")) + "' );")
            cur.execute("INSERT INTO CAPTEURS(boutonNourrir,boutonBoire,potentiometre) VALUES(False,False,50);") #50 charge neutre temporaire

    #sinon modifie les données normalement
    else:
        print("aaaaaaa")
        derniereConnexion()




def tempsPasse(derniereConnexion:str="")-> list:
    
    if derniereConnexion == "":
        with sqlite3.connect("bdd.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT dernièreConnexion from CREATURE;")
            derniereConnexion = cur.fetchall()[0][0] #permet de récup les résultats des lignes exécutées
            
    #print(derniereConnexion)
    derniereCo_dt = dt.strptime(derniereConnexion, "%Y-%m-%d %H:%M:%S")
    ajd = dt.now()
    #print(ajd)
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

    j, h, m = tempsPasse1[0], tempsPasse1[1], tempsPasse1[2]
    with sqlite3.connect("bdd.db") as conn:
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
        

#besoinQuiSEcoule("nourri",tempsPasse(date),[20,5,1]) #test sans le code lié au sql

def faim(derniereConnexion,manque:list[int,int,int])-> None:
    print("faim")
    besoinQuiSEcoule("nourri",tempsPasse(derniereConnexion),manque)

def soif(derniereConnexion, manque:list):
    print("soif")
    besoinQuiSEcoule("désaltéré",tempsPasse(derniereConnexion),manque)

def ennui(derniereConnexion, manque:list):
    print("ennui")
    besoinQuiSEcoule("ennui",tempsPasse(derniereConnexion),manque)
'''
faim("")
ennui("")
soif("")
'''
def derniereConnexion():
    #save la dernière connexion toutes les 5 minutes
    t = tempsPasse()
    with sqlite3.connect("bdd.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT dernièreConnexion from CREATURE;")
        derniereCo_save = cur.fetchall()[0][0]
        if t is int:
            miseAjourDonnéeBDD("CREATURE", "dernièreConnexion", str(dt.now().strftime("%Y-%m-%d %H:%M:%S")))
        if t[2] > 5 or t[1] > 0 or t[0] > 0:
            miseAjourDonnéeBDD("CREATURE", "dernièreConnexion", str(dt.now().strftime("%Y-%m-%d %H:%M:%S")))
            #mise à jour de toutes les autres stats
            faim(derniereCo_save,0)
            soif(derniereCo_save,)
            ennui(derniereCo_save,)
#derniereConnexion()
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

dicStatuts = {"sante":"est malade", "nourri":"a faim",
                         "ennui":"s'ennuie" , "désaltéré":"a soif"}

def statutAffiche(dicPaliers:dict,dicStatuts:dict) -> list[str]:

    #récupère toutes les stats actuelles de la BDD
    with sqlite3.connect("bdd.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT sante, nourri, désaltéré, ennui from CREATURE;")
        sante, nourri, desaltere, ennui = cur.fetchall()[0]
        d = {"santé": sante, "nourri": nourri, "désaltéré": desaltere, "ennui": ennui}

        #print(sante, nourri, desaltere, ennui)

        #liste_statuts_autres = {"froid": temp, "chaud":temp2}
        statuts = []
        for i in d:
            if d[i] < dicPaliers[i]:
                statuts.append(dicStatuts[i])

        # si le Tamagotchi a tous les statuts, il est triste
        if len(statuts) == len(dicStatuts):
            statuts.append("est triste")

        #à l'inverse, s'il n'en a aucun, il est heureuxx !
        elif len(statuts) == 0:
            statuts.append("est heureux")
        print(statuts)
        miseAjourDonnéeBDD("CREATURE", "statut", statuts)
        return statuts

#print(statutAffiche({"santé": 50, "nourri": 50, "désaltéré": 50, "ennui": 50}))

def statutAffecte(dicStatuts:dict) -> dict:
                    #jour heure minute
    affecteNormal = [30,  2,    2]
    affecteFort =   [45,  11,   5]
    dictAffectStats = {"santé": None, "nourri": None, "désaltéré": None, "ennui": None}
    #au cas où on change le nom associé à la clé
    malade = dicStatuts["santé"]
    with sqlite3.connect("bdd.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT statut from CREATURE;")
        statutsCreature = cur.fetchall()[0]
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
with sqlite3.connect("bdd.db") as conn:
    cur = conn.cursor()
    cur.execute("update CREATURE set sante = 100, nourri = 50, désaltéré = 50, ennui = 50 from (select * from CREATURE);")
    cur.execute("SELECT sante, nourri, désaltéré, ennui from CREATURE;")
    print(cur.fetchall()[0])
listePaliers = [50, 50, 50, 50]
#statutAffiche(listePaliers)
"""

#gestionDonnees()