from pydantic import BaseModel, constr
from typing import Dict

NodeId = constr(regex=r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89aAbB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$")

class MTLLMArg:
    id: NodeId
    arg: Dict
    