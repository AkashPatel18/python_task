from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import docker
import logging
import re
from pyngrok import ngrok, conf
import os
from models import DockerData
from utils import format_docker_url

app = FastAPI()
logging.basicConfig(level=logging.INFO)

client = docker.from_env()

config_path = os.path.join(os.getcwd(), "ngrok.yml")
conf.get_default().config_path = config_path

@app.post("/deploy")
async def deploy_container(data: DockerData):
    image = format_docker_url(data.image_url)
    
    try:
        container = client.containers.run(image, detach=True, ports={int(data.host_port): int(data.container_port)})
        ngrok_tunnels = {}

        tunnel_name = f"docker_{data.host_port}"
        ngrok_tunnels[tunnel_name] = ngrok.connect(data.host_port, "http")
        logging.info(f"ngrok tunnel started for port {data.host_port}: {ngrok_tunnels[tunnel_name].public_url}")

        return {"container_id": container.id, "ngrok_urls": [tunnel.public_url for tunnel in ngrok_tunnels.values()]}
    
    except Exception as e:
        logging.error(f"Error deploying container: {e}")
        raise HTTPException(status_code=500, detail=f"{e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
