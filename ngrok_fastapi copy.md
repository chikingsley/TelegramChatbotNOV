# Using ngrok with FastAPI

You can leverage the [ngrok-python](https://github.com/ngrok/ngrok-python) library to embed the ngrok agent in to FastAPI Applications.

warning

ngrok-python and FastAPI libraries used in this example are sensitive to versions. Use of Virtual Environments is highly recommended

```
# requirements.txtngrok==1.3.0uvicorn==0.29.0fastapi==0.111.0loguru==0.7.2
```

```
pip install -r requirements.txt
```

```
# main.pyfrom contextlib import asynccontextmanagerfrom os import getenvimport ngrokimport uvicornfrom fastapi import FastAPIfrom loguru import loggerNGROK_AUTH_TOKEN = getenv("NGROK_AUTH_TOKEN", "")NGROK_EDGE = getenv("NGROK_EDGE", "edge:edghts_")APPLICATION_PORT = 5000# ngrok free tier only allows one agent. So we tear down the tunnel on application termination@asynccontextmanagerasync def lifespan(app: FastAPI):    logger.info("Setting up Ngrok Tunnel")    ngrok.set_auth_token(NGROK_AUTH_TOKEN)    ngrok.forward(        addr=APPLICATION_PORT,        labels=NGROK_EDGE,        proto="labeled",    )    yield    logger.info("Tearing Down Ngrok Tunnel")    ngrok.disconnect()app = FastAPI(lifespan=lifespan)@app.get("/")async def root():    return {"message": "Hello World"}if __name__ == "__main__":    uvicorn.run("main:app", host="127.0.0.1", port=APPLICATION_PORT, reload=True)
```