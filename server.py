from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from Backend import perf_calc as perf_calc
from Backend import rotation_calc as rotation_calc
from Backend import refusal as refusal

app = FastAPI()

templates = Jinja2Templates(directory="Frontend")

@app.get("/")
def read_root(request: Request):
    respo = templates.TemplateResponse(
        "index.html", 
        {"request": request,
          "title": "TOLD TEST",
            "uncorrected_max_eff_TO_dist_text": "Uncorrected maximum effort takeoff distance: ",
            "uncorrected_max_eff_TO_dist": perf_calc.try_get_uncorrected_max_eff_field_length(perf_calc.aircraft_grossweight, perf_calc.takeoff_factor, perf_calc.data),
            "gross_weight_text": perf_calc.aircraft_grossweight,
            "takeoff_factor_text": perf_calc.takeoff_factor,
            "rotation_speed_calculated": rotation_calc.get_rotation_speed(perf_calc.aircraft_grossweight, perf_calc.takeoff_factor, rotation_calc.data),
            "runway_avail": perf_calc.rwy_available,
            "uncorrected_refusal_test": refusal.get_refusal_p1(perf_calc.takeoff_factor, perf_calc.rwy_available, refusal.data),
            "uncorrected_refusal_test_p2": refusal.get_refusal_p2(refusal.get_refusal_p1(perf_calc.takeoff_factor, perf_calc.rwy_available, refusal.data), perf_calc.aircraft_grossweight, refusal.data1)

            }
    )
        
    
    return respo


# endpoint to recieve value for gross weight
@app.get("/get_gwt") # mailbox (what we are listening on), get is request type -> serving get 
def handle_gwt(query):
    query = float(query)
    perf_calc.aircraft_grossweight = query
    print(query)
    return RedirectResponse("/")

@app.get("/get_takeoff_factor")
def handle_to_factor(get_to_factor: float):
    perf_calc.takeoff_factor = get_to_factor
    return RedirectResponse("/")

@app.get("/get_rwy_available")
def handle_rwy_available(get_rwy_available: float):
    perf_calc.rwy_available = get_rwy_available
    return RedirectResponse("/")
