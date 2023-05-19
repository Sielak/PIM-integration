from pydantic import BaseModel, Field
from typing import Optional, List

class MetaData(BaseModel):
    Key: str

class EntityField(BaseModel):
    FieldTypeId: str
    Value: str
    Language: Optional[str]
    CVLMetaData: Optional[MetaData]

class Entity(BaseModel):
    Id: str
    Fields: List[EntityField]

class ImportEntities(BaseModel):
    ImportEntities: List[Entity]
    