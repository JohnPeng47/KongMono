# Currently 3 main error classes
class GraphRuntimeError(Exception):
    """
    Recoverable errors, can usually just handle via retry
    """
class GraphInitializationError(Exception):
    """
    Errors when initializing the graph. Reinit graph
    """
class GraphCriticalError(Exception):
    """
    Unknown errors, dont know how to handle
    """

class GeneratorException(GraphRuntimeError):
    """
    Errors when generating something with LLM, recoverable
    """

class ConfigInitError(GraphInitializationError):
    """
    Wrong graph config option
    """