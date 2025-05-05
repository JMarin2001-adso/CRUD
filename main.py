
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI,status
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from routes.routes import routes,routes_d


app=FastAPI()
app.title ="proyecto IPS"
app.version= "0.0.1"
app.description= "API descripcion"

load_dotenv()

app.include_router(routes)
app.include_router(routes_d)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials= True,
    allow_methods=["GET","POST","PUT","DELETE","PATCH"],
    allow_headers=["*"],
)

@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="Default API",
    tags=["APP"],
)


def message():
    """ inicio del API

    Returns:
         Message
    """
    return HTMLResponse("<h1>ejercio de creacion crud</h1>")

if __name__=="__name__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)










