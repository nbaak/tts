class element ():
    def __init__(self, value):
        self.value = value
        self.attributes = {}
       
    def add_attribute(self, key, value):
        self.attributes[key] = value


class KeyValueStore ():
    def __init__(self):
        self.store = {}
        
    def add_key(self, key, value):
        if key not in self.store:
            self.store[key] = element(value)
    
    def add_attribute(self, key, att, value):
        self.store[key].add_attribute(att, value)

    def get_attribute(self, key, att):
        try:
            return self.store[key].attributes[att]
        except:
            return "attribute_not_found"
        
    def get_value(self, key):
        try:
            return self.store[key].value
        except:
            return "key_not_found"
    