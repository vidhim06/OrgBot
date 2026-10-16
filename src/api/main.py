from fastapi import FastAPI

app = FastAPI(title="OrgBot API")


@app.get("/")
def home():
    return {"message": "Welcome to OrgBot!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}