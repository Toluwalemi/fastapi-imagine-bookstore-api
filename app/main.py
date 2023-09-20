from fastapi import FastAPI

app = FastAPI(title="BookStore API")


@app.get("/")
def read_root():
    return {"Hello": "World"}
