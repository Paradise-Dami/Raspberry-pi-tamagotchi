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
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/nourrir")
async def nourrir():
    sante=fx.afficher_db("bdd.db","CREATURE")["sante"]
    if sante <= 20:
        fx.miseAjourDonnéeBDD("CREATURE","sante",sante+1)
    return None


@app.post("/boire")
async def run_script(background_tasks: BackgroundTasks, request: Request):
    background_tasks.add_task(boire)
    return None


@app.post("/affamer")
async def nourrir():
    sante=int(fx.afficher_db("bdd.db","CREATURE")["sante"])
    fx.miseAjourDonnéeBDD("CREATURE","sante",sante-1)
    return None

@app.get("/get_stats_tamagotchi")
async def get_stats_tamagotchi():
    data = fx.afficher_db("bdd.db","CREATURE")
    return JSONResponse(content=data)


def boire():
    print("j'ai pas d'onomathopées pour la soif a part AHHHHHH")


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

