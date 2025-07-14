import os
import threading
import queue

from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form
from mail import send_email
from log import log_action
from datetime import datetime


app = FastAPI(title="Система Повідомлень API")

task_queue = queue.Queue()

def background_worker():
    while True:
        func, args, kwargs = task_queue.get()
        try:
            func(*args, **kwargs)
        except Exception as e:
            log_action("task_error", {"error": str(e)})
        finally:
            task_queue.task_done()

worker_thread = threading.Thread(target=background_worker, daemon=True)
worker_thread.start()

def add_task_to_queue(func, *args, **kwargs):
    task_queue.put((func, args, kwargs))

@app.post("/send-email/")
async def send_email_endpoint(
    email: str = Form(...),
    subject: str = Form(...),
    body: str = Form(...)
):
    add_task_to_queue(send_email, email, subject, body)
    add_task_to_queue(log_action, "send_email", {"email": email, "subject": subject})
    return {"message": "Запит на відправлення листа прийнято"}

@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
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