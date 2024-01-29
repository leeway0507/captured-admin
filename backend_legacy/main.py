"fastapi app"

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from router.production import production_router, size_batch_router, s3_storage_router
from router.dev.platform import platform_router, kream_db_router
from router.dev.shop import shop_router, shop_db_router, table_router

app = FastAPI()

origins = [
    "http://localhost:4000",
    "http://127.0.0.1:4000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    table_router, prefix="/api/dev/shop/table", tags=["SHOP_TABLE_ROUTER"]
)
app.include_router(
    size_batch_router, prefix="/api/production/size_batch", tags=["SIZE_BATCH"]
)
app.include_router(platform_router, prefix="/api/dev/kream", tags=["PLATFORM"])
app.include_router(s3_storage_router, prefix="/api/production/s3", tags=["S3_STORAGE"])
app.include_router(production_router, prefix="/api/production", tags=["production"])
app.include_router(shop_db_router, prefix="/api/dev/shop/db", tags=["dev/shop/db"])
app.include_router(shop_router, prefix="/api/dev/shop", tags=["dev/shop/scrap/list"])
app.include_router(kream_db_router, prefix="/api/dev/kream/db", tags=["dev/kream/db"])


# 422 error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """422 error handler"""
    print(exc.errors())
    print(request.headers)
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )


from uvicorn.config import LOGGING_CONFIG
import uvicorn

if __name__ == "__main__":
    LOGGING_CONFIG["formatters"]["access"][
        "fmt"
    ] = '%(levelprefix)s %(asctime)s - %(client_addr)s - "%(request_line)s" %(status_code)s'
    uvicorn.run("main:app", port=8005, reload=True, host="0.0.0.0")