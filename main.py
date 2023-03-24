import json
from fastapi import Body, FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from src.schemas import User, CodePen
from src.service import S3Service, AuthService
from faunadb import query as q

app = FastAPI()

static = StaticFiles(directory="static", html=True)

@app.get("/api/auth")
async def auth_user(token:str):
    service = AuthService()
    user = await service.get_user(token)
    user = User(**user)
    try:
        return user.upsert()
    except Exception as e:
        user.create()
        return user.dict()

@app.post("/api/upload")
async def upload_code(sub: str, file: UploadFile = File(...)) -> PlainTextResponse:
    service = S3Service()
    key = f"{sub}/pencils/{file.filename}"
    url = service.upload_file(key, await file.read())
    return PlainTextResponse(url)

@app.post("/api/code")
async def upsert_code(sub:str,code:bytes=Body(...)):
    codepencil = CodePen(**{**json.loads(code), **{"sub": sub}})
    try:
        return codepencil.upsert()
    except Exception as e:
        codepencil.create()
        return codepencil.dict()

@app.get("/api/code")
def get_code_by_user(sub: str):
    query = q.paginate(q.match(q.index("codepen_by_sub"), sub))
    response = CodePen.q()(q.map_(lambda ref: q.get(ref), query))["data"]
    for r in response:
        yield r["data"]

@app.delete("/api/code")
async def delete_code_by_key(key: str):
    return CodePen.delete_by_key(key)

@app.get("/api/feed")
def get_code_feed(): 
    return CodePen.find_many()

app.mount("/", static, name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7777)