from fastapi import FastAPI
from api.main import api
from fastapi.exceptions import RequestValidationError
import uvicorn

app = FastAPI()
app.mount("/api", api)


@app.get("/")
async def root():
    return "Hello world"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
