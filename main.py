import os

from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form
from mail import send_email
from log import log_action
from datetime import datetime


app = FastAPI(title="Система Повідомлень API")


@app.post("/send-email/")
async def send_email_endpoint(
    background_tasks: BackgroundTasks,
    email: str = Form(...),
    subject: str = Form(...),
    body: str = Form(...)
):
    background_tasks.add_task(send_email, email, subject, body)
    background_tasks.add_task(log_action, "send_email", {"email": email, "subject": subject})
    return {"message": "Запит на відправлення листа прийнято"}

@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    upload_dir = "uploaded"
    os.makedirs(upload_dir, exist_ok=True)

    file_location = os.path.join(upload_dir, file.filename)

    with open(file_location, "wb") as f:
        f.write(await file.read())

    return {
        "message": f"Файл {file.filename} завантажено",
        "filename": file.filename,
        "path": file_location
    }