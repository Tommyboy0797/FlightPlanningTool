from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from Backend import perf_calc as perf_calc

app = FastAPI()

templates = Jinja2Templates(directory="Frontend")

@app.get("/")
def read_root(request: Request):
    respo = templates.TemplateResponse(
        "index.html", 
        {"request": request,
          "title": "TOLD TEST",
            "uncorrected_max_eff_TO_dist_text": "Uncorrected maximum effort takeoff distance: ",
            "uncorrected_max_eff_TO_dist": perf_calc.try_get_uncorrected_max_eff_field_length(perf_calc.aircraft_grossweight, perf_calc.takeoff_factor, perf_calc.data)}
    )
        
    
    return respo


# endpoint to recieve value
@app.get("/get_data") # mailbox (what we are listening on), get is request type -> serving get 
def handle_value(query):
    query = float(query)
    perf_calc.aircraft_grossweight = query
    print(query)
    return RedirectResponse("/")




