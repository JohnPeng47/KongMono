
class GraphAuthorizationError(Exception):
    def __init__(self, graph_id: str, email: str):
        message = f"{email} tried to access graph: {graph_id}"
        super().__init__(message = message)