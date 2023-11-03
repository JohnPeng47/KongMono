from pymongo import MongoClient
from bson.objectid import ObjectId
from typing import Dict, List
from config import settings

class DBConnection:
    # def __init__(self, host=settings.DB_HOST, port=27017, username=None, password=None):
    def __init__(self, host='18.191.159.163', port=27017, username=None, password=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = None
        self.db = None
        self.connected = False

        DATABASE = "kongbot"
        self.connect(DATABASE)

    def connect(self, database):
        try:
            self.client = MongoClient(self.host, self.port)
            self.db = self.client[database]

            if self.username and self.password:
                self.db.authenticate(self.username, self.password)

            self.connected = True
            print(f"Connected to database '{database}'")
        except Exception as e:
            print(f"Failed to connect to database: {e}")

    def disconnect(self):
        try:
            self.client.close()
            print("Disconnected from database")
        except Exception as e:
            print(f"Failed to disconnect from database: {e}")

    def get_collection(self, collection):
        if self.connected:
            return self.db[collection]
        else:
            print("Not connected to any database")

    # db methods for inserting/updating LLM generated output
    def clear_cache(self):
        return db_conn.get_collection("cache").delete_many({})

    def clear_key_cache(self, key: str):
        return db_conn.get_collection("cache").delete_many(
            {
                "key": {
                    "$regex": f".*{key}.*"
                }
            }
        )

    def get_generated(self, key: str):
        try:
            return db_conn.get_collection("cache").find_one({
                "key": key
            })["node"]
        except TypeError as e:
            print("Unable to find cached key: ", key)
            return None

    def insert_generated(self, key: str, data: dict):
        return db_conn.get_collection("cache").update_one(
            {
                "key": key
            }, {
                "$set": {
                    "node": data,
                }
            }, upsert=True)

    # DB methods for storing graphs
    def get_all_graphs(self) -> List[Dict]:
        # Find all the graphs
        graphs = db_conn.get_collection("graphs").find()

        # Extract their insertion timestamps
        results = []
        for graph in graphs:
            insertion_timestamp = ObjectId(graph['_id']).generation_time
            results.append((graph, insertion_timestamp))

        results.sort(key=lambda x: x[1])
        return results

    def find_graph(self, id) -> Dict:
        graph = db_conn.get_collection("graphs").find_one(
            {
                "id": id
            }
        )

        if graph:
            del graph["_id"]
            return graph

    def insert_graph(self, graph: dict, run_id: str = None):
        if run_id:
            graph["run_id"] = run_id

        return db_conn.get_collection("graphs").update_one(
            {
                "id": graph["id"]
            }, {
                "$set": graph
            },
            upsert=True)

    # does it make sense to store this on graph in separate collection?
    # thinking is, we may not want to load the full graph in mem if we just
    # want to grab the metadata
    def insert_graph_metadata(self, graph_id: str, metadata: Dict):
        return db_conn.get_collection("graph_metadata").update_one(
            {
                "id": graph_id,
            }, {
                "$set": {
                    "metadata": metadata,
                }
            },
            upsert=True)

    def get_graph_metadata_all(self, pagination=10):
        return db_conn.get_collection("graph_metadata").find({}).sort("timestamp", -1).limit(pagination)

    def get_graph_metadata(self, graph_id):
        return db_conn.get_collection("graph_metadata").find_one(
            {
                "id" : graph_id
            }
        )

    def load_most_recent_graph(self) -> Dict:
        # Get all graphs
        all_graphs = self.get_all_graphs()

        # If there are no graphs in the collection, return None or appropriate message
        if not all_graphs:
            return None

        # Sort the graphs based on the insertion timestamp in descending order
        sorted_graphs = sorted(all_graphs, key=lambda x: x[1], reverse=True)

        # Get the most recent graph
        most_recent_graph = sorted_graphs[0][0]

        # Convert the most recent graph to JSON and return
        return most_recent_graph

    # for storing evals
    def store_prompt_n_output(self,
                              base_llm_query: str,
                              prompt: str,
                              output: str,
                              error_status: bool = False) -> Dict:
        """
        base_llm_query is the class name of the BaseLLMQuery
        """
        HISTORICAL_PROMPT_LEN = 5
        self.db.get_collection("LLM_queries").update_one(
            {
                "query_name": base_llm_query
            }, {
                # only keep last n prompts
                "$push": {
                    "historical_prompts": {
                        "$each": [{
                            "prompt": prompt,
                            "output": output,
                            "error_status": error_status
                        }],
                        "$slice": - HISTORICAL_PROMPT_LEN  # Keep the last 5 prompts only
                    }
                }
            }, upsert=True)

    def get_prompt_n_output(self, base_llm_query: str) -> Dict:
        return self.db.get_collection("LLM_queries").find_one({
            "query_name": base_llm_query
        })


db_conn = DBConnection()
