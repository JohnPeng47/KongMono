class Prompt:
    def __init__(self, template: str):
        self.template = template
    
    def sub(self, **kwargs):
        for k, v in kwargs.items():
            self.template = self.template.replace("{" + k + "}", v)
        return self.template