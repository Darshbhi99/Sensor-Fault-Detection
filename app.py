# from fastapi import FastAPI, UploadFile
from sensor.entity.config_entity import S3Config


# app = FastAPI()

# @app.get('/')
# async def root():
#     return {"message": "Hello World"}

# @app.post('/uploadfile')
# async def uploadfile(file: UploadFile):
#     return {"message": "Uploaded file: " + file.filename}
# import pandas as pd
# from sensor.ml.model.estimator import ModelResolver
# from sensor.utils.main_utils import load_object
# df = pd.read_csv(r"artifact\02_24_2023_13_56_20\data_validation\validated\test.csv", index_col=0)
# df = df.drop('class', axis=1)
# print(df.shape)
# resolve = ModelResolver()
# latest_model_path = resolve.get_latest_model_path()
# model = load_object(latest_model_path)
# pred_val = model.predict(df)
# print(pred_val)
ans = S3Config()
print(ans.__dict__)