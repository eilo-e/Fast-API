from fastapi import FastAPI, status, HTTPException, Query, Path, Form, Body, File, UploadFile
from fastapi.responses import JSONResponse
import random
from typing import List

app = FastAPI()

names_list = [
    {"id": 1, "name": "ali"},
    {"id": 2, "name": "ailin"},
    {"id": 3, "name": "omid"},
    {"id": 4, "name": "mohammad ali"},
    {"id": 5, "name": "amir ali"},
]


@app.get("/")
def root():
    return {"message": "hello world!"}


@app.get("/names/{name_id}")
def retrieve_names_detail(name_id: int = Path(title="Object id"), description="the id of name"):
    for name in names_list:
        if name["id"] == name_id:
            return name
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="we could not find an item with that id",
    )


@app.post("/names", status_code=status.HTTP_201_CREATED)
def create_name(name: str = Body(embed=True)):
    name_obj = {"id": random.randint(6, 100), "name": name}
    names_list.append(name_obj)
    return name_obj


@app.put("/names/{name_id}")
def update_name_detail(name_id: int = Path(), name: str = Form()):
    for item in names_list:
        if item["id"] == name_id:
            item["name"] = name
            return f"the object with id: {name_id} were updated to {name}"
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="could not find that id"
    )


@app.delete("/names/{name_id}")
def delete_name(name_id: int):
    for item in names_list:
        if item["id"] == name_id:
            names_list.remove(item)
            return JSONResponse(
                content={"detail": "object removed succesfully"},
                status_code=status.HTTP_202_ACCEPTED,
            )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="could not find that id"
    )


@app.get("/names")
def retrieve_names_list(
    q: str | None = Query(
        description="it will search by title provided",
        alias="search",
        default=None,
        max_length=50,
    ),
):
    if q:
        return [item for item in names_list if item["name"] == q]
    return names_list


@app.post("/upload_file/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read() #async reading
    print(file.__dict__)
    return{"filename":file.filename, "content_type":file.content_type, "file_size":len(content)}


@app.post("/upload_multiple/")
async def upload_multiple(files: List[UploadFile]):
    return [
        {"filename": file.filename, "content_type": file.content_type}
        for file in files
    ]