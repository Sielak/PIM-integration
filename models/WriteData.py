from pydantic import BaseModel


class WriteData(BaseModel):
    ProcesType: str = None
    Text2: str = "JSON OK"
    Text7: str = None
    ExecuteProcedure: str = 'Y'
    Message: str = ''