from fastapi import FastAPI

app = FastAPI(root_path="/ingest")

@app.get("/health")
def root():
    return {"message": "services receiver works"}
