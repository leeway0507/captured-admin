"fastapi app"

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from platform_scrap.list.router import platform_list
from platform_scrap.page.router import platform_page
from shop_scrap.list.router import shop_list
from shop_scrap.page.router import shop_page
from table.router import table


app = FastAPI()

origins = [
    "http://localhost:3000",
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


app.include_router(table, prefix="/api/table", tags=["TABLE"])
app.include_router(platform_list, prefix="/api/platform/list", tags=["PLATFORM LIST"])
app.include_router(platform_page, prefix="/api/platform/page", tags=["PLATFORM PAGE"])
app.include_router(shop_list, prefix="/api/shop/list", tags=["SHOP LIST"])
app.include_router(shop_page, prefix="/api/shop/page", tags=["SHOP PAGE"])


# 422 error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """422 error handler"""
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
