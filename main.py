from sensor.pipeline.training_pipeline import TrainingPipeline
from sensor.constant.application import APP_HOST, APP_PORT
from fastapi import FastAPI, File, UploadFile
from starlette.responses import RedirectResponse, StreamingResponse
from uvicorn import run as app_run
from fastapi.responses import Response
from sensor.exception import SensorException
from sensor.utils.main_utils import load_object
from sensor.ml.model.estimator import TargetValueMapping, ModelResolver
import pandas as pd
from io import BytesIO, StringIO
import sys, os
import warnings
warnings.filterwarnings('ignore')

app = FastAPI()

@app.get('/', tags=['authentication'])
async def index():
    return RedirectResponse(url = '/docs')

@app.get('/train')
async def trainRouteClient():
    try:
        training = TrainingPipeline()
        if training.is_pipeline_running:
            return Response('Training Pipeline is Already Running')
        training.run_pipeline()
        return Response('Training Successful !!')
    except Exception as e:
        raise Response(f'Error Occured {e}')

@app.post('/predict')
async def predict_route(data:UploadFile):
    try:
        content = await data.read()
        df = BytesIO(content)
        uploaded_df = pd.read_csv(df, index_col=0)
        uploaded_df.drop('class', axis=1, inplace=True)
        train_df = pd.read_csv()
        print(df.shape)
        resolve = ModelResolver()
        latest_model_path = resolve.get_latest_model_path()
        model = load_object(latest_model_path)
        pred_val = model.predict(uploaded_df)
        df['y_pred'] = pred_val
        df['y_pred'].replace(TargetValueMapping().reverse_mapping(), inplace=True)
        print(uploaded_df.shape)
        stream = StringIO()
        uploaded_df.to_csv(stream, index = False, index_label = False)
        response = StreamingResponse(content=iter([stream.getvalue()]), media_type='text/csv', 
                                    headers={"Content-Deposition":f"attachment;filename=data.csv"})
        return response
    except Exception as e:
        raise Response(f"Error Occured {e}")


if __name__ == '__main__':
    try:
        app_run(app=app, host=APP_HOST, port=APP_PORT)
    except Exception as e:
        raise SensorException(e, sys)