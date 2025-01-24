from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import perf_calc
app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root(request: Request):
    respo = templates.TemplateResponse(
        "index.html", 
        {"request": request,
          "message": "Hello, FastAPI!",
            "test": "Test test test",
            "random_number": perf_calc.get_random_number()}
        )
        

    return respo

@app.get("home")
def home_page(request: Request):




    return