from fastapi.exceptions import HTTPException

class GraphAuthorizationError(Exception):
    def __init__(self, graph_id: str, email: str):
        message = f"{email} tried to access graph: {graph_id}"
        super().__init__(message = message)
    
class GraphNotFound(HTTPException):
    def __init__(self, status_code=404, detail="No graph metadata found"):
        super().__init__(status_code=status_code, detail=detail)