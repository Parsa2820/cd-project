class Symbol:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.address = -1

    def __str__(self):
        return f'{self.id}.\t{self.name}'
