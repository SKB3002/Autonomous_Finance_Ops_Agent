class ShortTermMemory:
    def __init__(self, run_id):
        self.run_id = run_id
        self.store = {}

    def add(self, key, value):
        self.store[key] = value

    def get(self, key):
        return self.store.get(key)

    def dump(self):
        return self.store

