from app.classes.entities import Cat

class Transactions:
    def __init__(self, collection):
        self.collection = collection

    def showOne(self, name):
        print(Cat(self.collection.find_one({"name": name})).result())

    def showAll(self):
        records = self.collection.find()
        if len(list(records.clone())) > 0:
            for item in records:
                print(Cat(item).result())
        else:
            print("No records are found!")
        
    def updateOne(self, name, data):
        self.collection.update_one({"name": name}, {"$set": data})
        self.showOne(name)

    def addFeature(self, name, feature):
        record = self.collection.find_one({"name": name})
        record['features'].append(feature)
        self.collection.update_one({"name": name}, {"$set": {"features": record['features']}})
        self.showOne(name)

    def deleteOne(self, name):
        self.collection.delete_one({"name": name})
        try:
            self.showOne(name)
        except TypeError:
            print(f"Record with name: {name} - deleted!")

    def deleteAll(self):
        self.collection.delete_many({})