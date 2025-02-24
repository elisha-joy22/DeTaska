from fastapi import FastAPI

app = FastAPI()

@app.route("/")
def read_route():
    return {"messsage":"Welcome to DeTaska API 🚀"}