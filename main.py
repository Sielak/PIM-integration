from datetime import date
import json
from fastapi import FastAPI, Request, Response, status
from fastapi.logger import logger
from fastapi.params import File
from starlette.routing import request_response
import models
from lib.PIM import PIM
from lib.jeeves import Jeeves
import os
from sentry_asgi import SentryMiddleware
import sentry_sdk
import socket
from pydantic import ValidationError


# Main config
if socket.gethostname() == 'bma-app-101':
    environment = 'Prod'
else:
    environment = 'Test'
sentry_sdk.init(dsn="https://ee3b6075e1c648b79646e5e6c8e3119e@o229295.ingest.sentry.io/5761061", environment=environment)

app = FastAPI()

# Endpoints
@app.post("/AddToPim", status_code=200)
def AddToPim(model: models.ProductID, response: Response, debug: bool = False):
    # Send data to PIM
    try:
        jeevs = Jeeves()
        productNr = model.Product
        query = jeevs.get_info_about_product(productNr)
        #print(query)
        result = PIM(query, 'JeevesInboundExtension', debug).send_request()
        return result
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'info': str(e)}

@app.post("/GetProductFromPim")
def GetProductFromPim(model: models.ImportEntities, response: Response, debug: bool = False):
    jeeves_data = models.WriteData()
    jeeves_data.ProcesType = "PIMto1J"
    try:
        model = models.ImportEntities.parse_obj(model)  # Check data from pim  
        model = json.dumps(model.dict())
        model = str(model).translate(str.maketrans({"'": r"''"}))
        jeeves_data.Text7 = model
        Jeeves().insert2dp_data(jeeves_data)  # write json to dp_data
    except ValidationError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        jeeves_data.Text7 = str(model)
        jeeves_data.ExecuteProcedure = 'N'
        jeeves_data.Text2 = "JSON ERROR"
        jeeves_data.Message = e
        Jeeves().insert2dp_data(jeeves_data)  # write json to dp_data
        return {'info': str(e)}
    
    if debug is True:
        return {'model': model}
    else:
        return {'info': "OK"}


# Sentry config
app = SentryMiddleware(app)
# Uvicorn config
if __name__ == "__main__":
    import uvicorn
    dir_path = os.path.dirname(os.path.realpath(__file__))
    if dir_path == "/home/ubuntu/dev/pim_integration":
        port = 8103
    else:
        port = 8100
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    log_config["formatters"]["access"]["fmt"] = '%(asctime)s [%(name)s] %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True, debug=True, log_config=log_config)