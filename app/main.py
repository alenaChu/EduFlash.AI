from fastapi import FastAPI

app = FastAPI(title="EduFlash.AI")


@app.get("/")
async def root():
    return {"msg": "EduFlash.AI alive"}
