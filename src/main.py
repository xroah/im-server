from fastapi import FastAPI
from api.main import create_api
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return "Hello world"

if __name__ == "__main__":
    app.mount("/api", create_api(True))
    uvicorn.run(app, host="0.0.0.0", port=8888)
else:
    app.mount("/api", create_api())
