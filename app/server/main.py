import numpy as np
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI, File, UploadFile
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from predict import YOLOInference
import nest_asyncio
from pyngrok import ngrok
from typing import List
import argparse

global app

YOLO_CHECKPOINT = ''

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
]

app = FastAPI(middleware=middleware)

@app.get("/")
def read_root():
    return {"If you see this, it means everything's alright."}

@app.post('/predict/')
async def predict(
    files: List[UploadFile] = File(...)
):
    for file in files:
      try:
          contents = file.file.read()
          with open(file.filename, 'wb') as f:
              f.write(contents)
      except Exception:
          return {"message": "There was an error uploading the file(s)"}
      finally:
          file.file.close()

    model = YOLOInference(
        YOLO_CHECKPOINT,
        [x.filename for x in files],
        save_images=False,
        save_path='./'
    )
    res = model.run()
    return {"file": res}


ngrok.set_auth_token("2THhoVviVOXuBq97RU9WW095Vtx_6pDFzgtkzRocdaTdBeVG7")
ngrok_tunnel = ngrok.connect(
    addr=8000,
    domain="moving-legally-boar.ngrok-free.app")
print('Public URL:', ngrok_tunnel.public_url)
nest_asyncio.apply()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("-m", "--model_ckpt", default="torchFlow-ckpt.pt")
  args = parser.parse_args()
  YOLO_CHECKPOINT = args.model_ckpt

  uvicorn.run(app, port=8000)
