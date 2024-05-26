from pydantic import BaseModel

class DockerData(BaseModel):
    image_url: str
    host_port: str
    container_port: str