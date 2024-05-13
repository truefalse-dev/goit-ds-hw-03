class Cat:
    def __init__(self, row):
        self.row = row

    def result(self):
        return f"name: {self.row['name']}, age: {self.row['age']}, features: [{', '.join(self.row['features'])}]"