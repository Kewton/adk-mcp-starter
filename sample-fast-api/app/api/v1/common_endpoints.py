from fastapi import APIRouter
router = APIRouter()


@router.get("/",
            summary="Hello World",
            description="Hello Worldです。疎通確認に使用してください。")
def home_hello_world():
    return {"message": "Hello World"}

