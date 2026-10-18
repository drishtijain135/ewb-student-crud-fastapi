from fastapi import FastAPI

app = FastAPI(title="EWB Student Database API")


@app.get("/")
def home():
    return {"message": "Student Database API is running"}