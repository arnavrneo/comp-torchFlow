import numpy as np
import onnxruntime
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI, File, UploadFile
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from predict import ONNXInference
import nest_asyncio
from pyngrok import ngrok
from typing import List
import argparse

global app

ONNX_CHECKPOINT = ''

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
    return {"Hello": "World"}

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
    
    model = ONNXInference(
        ONNX_CHECKPOINT, 
        [x.filename for x in files],
        save_image=False, 
        save_path='./'
    )
    res = model.run()
    return {"file": res}



ngrok_tunnel = ngrok.connect(8000)
ngrok.set_auth_token("2THhoVviVOXuBq97RU9WW095Vtx_6pDFzgtkzRocdaTdBeVG7")
print('Public URL:', ngrok_tunnel.public_url)
nest_asyncio.apply()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("-m", "--model_ckpt")
  args = parser.parse_args()
  ONNX_CHECKPOINT = args.model_ckpt
  
  uvicorn.run(app, port=8000)
