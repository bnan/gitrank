from pymongo import MongoClient
import random
from github import parse_user_rank, user_rank

class Mongoloide:

    def __init__(self):
        client = MongoClient('mongo', 27017)
        db = client.test_database
        self.comparisons = db.comparisons
        self.rank_history = db.history
        self.users = db.users

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

    def get_user(self, name):
        return self.user.find_one({"user_name":name})

    def store_user(self, name, data):
        #Existig user
        user = self.user.find_one({"user_name":name})
        user = self.user.update_one({"user_name":name}, {'$set': {key: value}}, upsert=True)
        return user 
        
    def avg(self):
        avg =  self.user.aggregate(
            [
                {
                    "$group":
                    {
                        "avgFollowers": { "$avg": "followers" },
                        "avgfollowing": { "$avg": "following" },
                    }
                }
            ]
        )
        print(avg)

if __name__ == "__main__":
    user = parse_user_rank(user_rank("ludeed", "faviouz"))
    mon = MongoClient()
    mon.store_user(user)
    mon.avg()

