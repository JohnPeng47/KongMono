from utils.db import db_conn

def cache_result(func):
    def wrapper(self, *args, **kwargs):
        if self.cache_policy == "CACHE":
            res = db_conn.get_generated(self.key())
            if res:
                return res
        result = func(self, *args, **kwargs)
        if self.cache_policy == "CACHE" and result:
            db_conn.insert_generated(self.key(), result)
        return result
    return wrapper
