class Inventory:
    def __init__(self):
        self.items = {}

    def add(self, item, amount=1):
        self.items[item] = self.items.get(item, 0) + amount

    def remove(self, item):
        if item in self.items:
            self.items[item] -= 1
            if self.items[item] <= 0:
                del self.items[item]

    def has(self, item):
        return item in self.items