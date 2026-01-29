from fastapi.middleware.cors import CORSMiddleware
from fastapi import  FastAPI

from routers import db_query
from routers import users, items, ext_secret, ext_chat
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)



def start_test():
    print("测试启动")


def shutdown_test():
    print("测试关闭")


app = FastAPI(
    docs_url=None,
    redoc_url=None,
    title="api接口基础模板",
    description="这是一个基于FastAPI的JWT认证示例接口",
    version="1.0.1",
    summary="这是一个基于FastAPI的JWT认证示例接口",
    openapi_url="/openapi.json",
    openapi_tags=[
        {
            "name": "用户接口",
            "description": "用户相关操作1",
            "externalDocs": {
                "description": "在线调试",
                "url": "http://127.0.0.1:8000/docs#/items",
            },
        },
        {
            "name": "items",
            "description": "项目相关操作",
            "externalDocs": {
                "description": "更多信息",
                "url": "https://example.com/items",
            },
        },
    ],
    
    servers=[
        {"url": "http://127.0.0.1:8001", "description": "本地开发环境"},
        {"url": "http://192.168.1.68:8000", "description": "生产环境"}
    ],
    dependencies=[],
    on_startup=[start_test],
    on_shutdown=[shutdown_test],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=str("./app/static")), name="static")
# 注册路由
app.include_router(users.router)
app.include_router(items.router)
app.include_router(ext_secret.router)
app.include_router(ext_chat.router)
app.include_router(db_query.router)

# sqladmin


# 使用本地资源相关接口
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
