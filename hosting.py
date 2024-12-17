from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
import fonctions_statistiques as fx


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
    nourri=float(fx.afficher_db("bdd.db","CREATURE")["nourri"])
    fx.miseAjourDonnéeBDD("CREATURE","sante",nourri+10)
    return None


@app.post("/boire")
async def boire() -> None:
    desaltere=float(fx.afficher_db("bdd.db","CREATURE")["desaltere"])
    fx.miseAjourDonnéeBDD("CREATURE","desaltere",desaltere+10)
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
async def nourrir():
    stim=int(fx.afficher_db("bdd.db","CREATURE")["ennui"])
    fx.miseAjourDonnéeBDD("CREATURE","sante",stim+1)
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
    data = fx.statutAffiche(fx.dicPaliers,fx.dicStatuts)
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

