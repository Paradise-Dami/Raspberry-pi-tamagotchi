from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import subprocess
import time

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

"""@app.post("/run_script")
async def run_script(background_tasks: BackgroundTasks, request: Request):
    background_tasks.add_task(run_python_script, request)
    return templates.TemplateResponse("result.html", {"request": request})

def run_python_script(request):
    try:
        output = subprocess.run(["python", "/path/to/your/script.py"], capture_output=True, text=True, check=True)
        print(f"Script output:\n{output.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Script execution failed:\n{e.stderr}")"""

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

