class GraphManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GraphManager, cls).__new__(cls)
        return cls._instance
    
g1 = GraphManager()
g2 = GraphManager()
print(g1)
print(g2)