from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
import fonctions_statistiques as fx
import sqlite3

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Affiche la page html 'home.html' quand on accède a http://127.0.0.1:8000'
    """
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/mort", response_class=HTMLResponse)
async def mort(request: Request):
    """
    Affiche la page html 'dead_page.html' quand on accède a http://127.0.0.1:8000/mort'
    """
    fx.mourir()
    return templates.TemplateResponse("dead_page.html", {"request": request})

@app.post("/nourrir")
async def nourrir() -> None:
    nourri =float(fx.afficher_db("bdd.db","CREATURE")["nourri"])
    nourri += 10
    nourriCheck = fx.statMinMax(nourri)
    fx.miseAjourDonnéeBDD("CREATURE","nourri",nourriCheck)
    return None


@app.post("/boire")
async def boire() -> None:
    desaltere=float(fx.afficher_db("bdd.db","CREATURE")["desaltere"])
    desaltere += 10
    desaltereCheck = fx.statMinMax(desaltere)
    fx.miseAjourDonnéeBDD("CREATURE","desaltere",desaltereCheck)
    return None

@app.post("/reset")
async def run_script(background_tasks: BackgroundTasks, request: Request):
    background_tasks.add_task(reset)
    return None

@app.post("/maj")
async def run_script(background_tasks: BackgroundTasks, request: Request):
    fx.gestionDonnees()
    return None

@app.post("/gratouille")
async def stim():
    stim=float(fx.afficher_db("bdd.db","CREATURE")["ennui"])
    stim += 5
    stimCheck = fx.statMinMax(stim)
    fx.miseAjourDonnéeBDD("CREATURE","ennui",stimCheck)
    return None

@app.get("/get_stats_tamagotchi")
async def get_stats_tamagotchi():
    """
    Récupère toutes les stats du tamagotchi et ensuite les envoient
    au fichier script.js
    """
    data = fx.afficher_db("bdd.db","CREATURE")
    return JSONResponse(content=data)

@app.get("/get_statut")
async def get_statut():
    """
    Récupère l'humeur du tamagotchi et ensuite les envoient
    au fichier script.js
    """
    data = fx.statutAffiche(fx.DIC_PALIERS,fx.DIC_STATUTS)
    return JSONResponse(content=data)


@app.get("/get_temp")
async def get_temp():
    """
    Récupère l'humeur du tamagotchi et ensuite les envoient
    au fichier script.js
    """
    conn = fx.DATABASE
    cur = conn.cursor()
    cur.execute("SELECT temp from CAPTEURS;")
    temp = float(cur.fetchall()[0][0])
    return JSONResponse(content=data)

def reset():
    """
    Réanime le tamagotchi en remettant a la normale ses stats
    """
    print(fx.miseAjourDonnéeBDD("CREATURE", "etat", "reanime"))
    fx.gestionDonnees()
    print("resettttt")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)























"""from flask import Flask, jsonify, request

app = Flask(__name__)

nourrir: int=0

# Define a Python function
def nourrir(nombre:int) -> int:
    nourrir: int += nombre
    return nourrir

# Create an endpoint that calls the Python function
@app.route('/nombre', methods=['GET'])
def add_numbers():
    # Get query parameters
    x = int(request.args.get('x'))
    y = int(request.args.get('y'))

    # Call the Python function
    result = my_python_function(x, y)
    
    # Return the result as JSON
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
"""

