from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from dotenv import dotenv_values
from config.config import Config
from controller.Master_sdr import Master_sdr
from models.Client import IsStatusUpdate, IsPostMiniPC
from models.Scheduler import IsScheduler
from fastapi_pagination import Page, add_pagination, paginate
config = dotenv_values(".env")
Cfx = Config(config)

sdr = Master_sdr(config)
app = FastAPI()

# documenting API
app = FastAPI(
    title="API NMS N3 & N5",
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


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/n5/add-mini-pc", tags=["SDR Module"], status_code=200)
async def add_mini_pc(post: IsPostMiniPC):
    sdr.add_mini_pc(post)
    return post


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

@app.delete("/api/v1/terminal-delete/{id}", tags=["SDR Terminal Reference"], status_code=200)
# def update_single_sites(id: int, post: IsStatusUpdate):
def update_single_sites(id: int):
    sdr.del_mini_pc(id)
    return f"Sukses delete: {id}"


@app.put("/api/v1/update-mini-pc/{id}", tags=["SDR Terminal Reference"], status_code=200)
# def update_single_sites(id: int, post: IsStatusUpdate):
def update_mini_pc(id: int, post: IsStatusUpdate):
    sdr.update_mini_pc(id, post)
    return post


@app.post("/api/v1/download-test/{uname}&{ip_tr}&{ip_server}&{port}&{time_processing}", tags=["Do Test SDR"], status_code=200)
def dothis(uname: str, ip_tr: str, ip_server: str, port: str, time_processing: str):
    return sdr.download(uname, ip_tr, ip_server, port, time_processing)


@app.post("/api/v1/upload-test/{uname}&{ip_tr}&{ip_server}&{port}&{time_processing}", tags=["Do Test SDR"], status_code=200)
def dothis(uname: str, ip_tr: str, ip_server: str, port: str, time_processing: str):
    return sdr.upload(uname, ip_tr, ip_server, port, time_processing)

@app.get("/api/v1/get-all-scheduler", tags=["Scheduler SDR"], status_code=200)
def get_scheduler():
    return sdr.get_scheduler_paginate()

@app.get("/api/v1/get-scheduler-kratos", tags=["Scheduler SDR"], status_code=200)
def get_scheduler_concat():
    return sdr.get_scheduler_kratos()

@app.get("/api/v1/get-scheduler/{id}", tags=["Scheduler SDR"], status_code=200)
def get_scheduler(id: int):
    return sdr.get_scheduler(id)


@app.post("/api/v1/post-scheduler/", tags=["Scheduler SDR"], status_code=200)
def post_scheduler(post: IsScheduler):
    sdr.post_scheduler(post)
    return (post)


@app.put("/api/v1/update-scheduler/{id}", tags=["Scheduler SDR"], status_code=200)
def update_scheduler(id: str, post: IsScheduler):
    sdr.update_scheduler(id, post)
    return (post)


@app.delete("/api/v1/delete-scheduler/{id}", tags=["Scheduler SDR"], status_code=200)
def delete_scheduler(id: str):
    sdr.delete_scheduler(id)
    return "Sukses Deleted"


@app.get("/api/n5/max-download/{device_id}", tags=["SDR Module"], status_code=200)
async def get_val_max_download_today(device_id: str):
    return sdr.get_val_max_download_today(device_id)


@app.get("/api/n5/max-upload/{device_id}", tags=["SDR Module"], status_code=200)
async def get_val_max_upload_today(device_id: str):
    return sdr.get_val_max_upload_today(device_id)
