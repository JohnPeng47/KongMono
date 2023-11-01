from pydantic import BaseModel, constr
from typing import Dict, Union

NodeId = constr(regex=r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89aAbB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$")

class GeneratorArg(BaseModel):
    node_id: NodeId
    data: Dict
class GeneratorResult(BaseModel):
    node_id: NodeId
    data: Union[Dict, str]
