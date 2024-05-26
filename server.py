from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
import sqlite3
import httpx
import logging
from config.db import init_db
from template import load_form

app = FastAPI()
logging.basicConfig(level=logging.INFO)

init_db()

@app.get("/", response_class=HTMLResponse)
async def read_form():
    return load_form()

@app.post("/submit")
async def handle_form(image_url: str = Form(...), host_port: str = Form(...), container_port: str = Form(...)):
    try:
        conn = sqlite3.connect('docker_data.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO docker_data (image_url, host_port, container_port) VALUES (?, ?, ?)
        ''', (image_url, host_port, container_port))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post("http://localhost:8001/deploy", json={"image_url": image_url, "host_port": host_port, "container_port": container_port})

        except Exception as e:
            logging.error(f"Error sending data to client: {e}")
            raise HTTPException(status_code=500, detail=e)
        
    return response.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
