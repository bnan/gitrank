from pymongo import MongoClient
import random

class Mongoloide:

    def __init__(self):
        client = MongoClient('mongo', 27017)
        db = client.test_database
        self.comparisons = db.comparisons
        self.rank_history = db.history

    def add_comparison(self, name1, name2):
        compA = self.comparisons.find_one({"repo_name":name1})
        compB = self.comparisons.find_one({"repo_name":name2})

        if( compA == None ):
            compA = {"repo_name":name1,
                     "compared_to":[name2,]}
            comp = self.comparisons.insert_one(compA)
        else:
            new_values = compA["compared_to"] + [name2]
            compA = self.comparisons.update_one({"repo_name":name1}, {'$set': {'compared_to': new_values}})

        if( compB == None ):
            compB = {"repo_name":name2,
                     "compared_to":[name1,]}
            comp = self.comparisons.insert_one(compB)
        else:
            new_values = compB["compared_to"] + [name1]
            compB = self.comparisons.update_one({"repo_name":name2}, {'$set': {'compared_to': new_values}})

    def get_related(self, name ):
        comp = self.comparisons.find_one({"repo_name":name})
        i = random.randint(1,len(comp['compared_to'])-1)
        return comp['compared_to'][i]

