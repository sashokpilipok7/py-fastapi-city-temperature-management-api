from fastapi import FastAPI

app = FastAPI()

# app.include_router(city.router)
@app.get("/")
def read_root():
    return {"Hello": "World"}