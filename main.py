from fastapi import FastAPI
from dotenv import dotenv_values
from config.config import Config
from controller.Master_sdr import Master_sdr
config = dotenv_values(".env")
Cfx = Config(config)

sdr = Master_sdr(config)
app = FastAPI()

# documenting API
app = FastAPI(
    title="API NMS N5",
    description="API for handle data retriving for billing process",
    version="0.0.1",
    terms_of_service="",
    contact={
        "name": "NMS Team",
        "url": "https://t.me/+CJlgwrSO90UxOTE1",
        "email": "group.it.bb@psn.co.id",
    },
    license_info={
        "name": "psn",
        "url": "https://psn.co.id",
    },)
#


@app.post("/api/v1/list-sites/", tags=["Test"], status_code=200)
def get_list():
    return sdr.get_sites()
