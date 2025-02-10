from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from Backend import perf_calc, rotation_calc, refusal, handle_route
from database import database_handler as db_handler

app = FastAPI()
templates = Jinja2Templates(directory="Frontend")

class Origin(BaseModel):
    airport_name: str

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/get_data")
async def handle_data(
    gwt: str,
    get_to_factor: str,
    get_rwy_available: str,
    get_rwy_slope: str,
    enter_db_country: str
):
    try:
        gwt = float(gwt)
        response_data = {
            "uncorrected_max_eff_TO_dist": perf_calc.try_get_uncorrected_max_eff_field_length(gwt, get_to_factor, perf_calc.data),
            "gross_weight_text": round(gwt * 1000),
            "takeoff_factor_text": get_to_factor,
            "rotation_speed_calculated": rotation_calc.get_rotation_speed(gwt, get_to_factor, rotation_calc.data),
            "runway_avail": get_rwy_available,
            "uncorrected_refusal_test_p2": refusal.get_refusal_p2(
                refusal.get_refusal_p1(get_to_factor, get_rwy_available), gwt),
            "partially_corrected_refusal_p3": refusal.get_refusal_p3(
                refusal.get_refusal_p2(
                    refusal.get_refusal_p1(get_to_factor, get_rwy_available), gwt),
                get_rwy_slope),
            "runway_slope": get_rwy_slope,
            "sids": db_handler.get_sids(handle_route.origin_airfield)
        }
        return JSONResponse(content=response_data)
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

@app.post("/set_origin")
async def set_origin(origin: Origin):
    handle_route.origin_airfield = origin.airport_name
    handle_route.route = origin.airport_name
    return JSONResponse(content={"status": "success"})

@app.get("/fetch_airports")
async def fetch_airports():
    return JSONResponse(content={
        "small_airports": db_handler.get_small_airfields(),
        "medium_airports": db_handler.get_medium_airfields(),
        "large_airports": db_handler.get_large_airfields()
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)