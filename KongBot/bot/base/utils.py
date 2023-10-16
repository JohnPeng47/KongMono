import json

class CustomDict(json.JSONEncoder):
    data: dict

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __contains__(self, key):
        return key in self.data

    def keys(self):
        return self.data.keys()
    
    def items(self):
        return self.data.items()
    
    def values(self):
        return self.data.values()
    
    ## correct this!!
    def default(self, obj):
        return obj.data