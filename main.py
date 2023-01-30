from fastapi import FastAPI
from dotenv import dotenv_values
from config.config import Config
from controller.Master_sdr import Master_sdr
from models.Client import IsStatusUpdate
config = dotenv_values(".env")
Cfx = Config(config)

sdr = Master_sdr(config)
app = FastAPI()

# documenting API
app = FastAPI(
    title="API NMS N5",
    description="API for handle SDR Client",
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


@app.get("/api/v1/list-sites/", tags=["SDR Terminal Reference"], status_code=200)
def get_list():
    return sdr.get_sites()


@app.get("/api/v1/status-on/", tags=["SDR Terminal Reference"], status_code=200)
def get_list_on():
    return sdr.get_sites_status_on()


@app.get("/api/v1/status-off/", tags=["SDR Terminal Reference"], status_code=200)
def get_list_off():
    return sdr.get_sites_status_off()


@app.get("/api/v1/terminal-detil/{id}", tags=["SDR Terminal Reference"], status_code=200)
def get_single_sites(id: int):
    return sdr.get_single_sites(id)


@app.get("/api/v1/terminal-update-status/{id}/{post}", tags=["SDR Terminal Reference"], status_code=200)
# def update_single_sites(id: int, post: IsStatusUpdate):
def update_single_sites(id: int, post: str):
    sdr.update_single_sites(id, post)
    return post
