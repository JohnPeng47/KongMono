from .service import GraphManager
from functools import wraps
from fastapi import Response

def lock_graph(graph_manager: GraphManager):
    def actual_decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            graph_id = kwargs.get("graph_id", None)
            graph_manager.acquire_lock(graph_id)

            try:
                result = f(*args, **kwargs)
            except Exception as e:
                raise e
            finally:
                graph_manager.release_lock(graph_id)
                
            return result
        return decorated_function
    return actual_decorator
    