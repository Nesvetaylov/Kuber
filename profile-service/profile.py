from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"service": "Profile Service", "status": "active"}

@app.get("/health/live")
def liveness():
    return {"status": "alive"}

@app.get("/health/ready")
def readiness():
    return {"status": "ready"}