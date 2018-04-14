from pymongo import MongoClient
import random


class Mongoloide:
    def __init__(self):
        client = MongoClient('mongo', 27017)
        db = client.test_database
        self.db = client.test_database
        self.comparisons = db.comparisons
        self.rank_history = db.history
        self.users = db.users

    def add_comparison(self, name1, name2):
        compA = self.comparisons.find_one({"repo_name":name1})
        compB = self.comparisons.find_one({"repo_name":name2})

        if compA == None:
            compA = {"repo_name":name1,
                     "compared_to":[name2,]}
            comp = self.comparisons.insert_one(compA)
        else:
            new_values = compA["compared_to"] + [name2]
            compA = self.comparisons.update_one({"repo_name":name1}, {'$set': {'compared_to': new_values}})

        if compB == None:
            compB = {"repo_name":name2, "compared_to":[name1,]}
            comp = self.comparisons.insert_one(compB)
        else:
            new_values = compB["compared_to"] + [name1]
            compB = self.comparisons.update_one({"repo_name":name2}, {'$set': {'compared_to': new_values}})

    def get_related(self, name1, name2):
        try:
            compA = self.comparisons.find_one({"repo_name":name1})
            compB = self.comparisons.find_one({"repo_name":name2})
            related = [x for x in compA['compared_to'] if x != name2] + [x for x in compB['compared_to'] if x != name1]
            i = random.randint(0,len(related))
            return related[i]
        except ValueError:
            return []

    def get_user(self, name):
        return self.users.find_one({"user_name":name})

    def store_user(self, name, data):
        #Existig user
        user = self.users.find_one({"user_name":name})
        for key, value in data.items():
            user = self.users.update_one({"user_name":name}, {'$set': {key: value}}, upsert=True)
        return user

    def avg(self):
        avg =  set([ print(x) for x in self.users.aggregate(
            [
                {
                    "$group":
                    {
                        "_id": "null",
                        "avg_followers": { "$avg": "$followers" },
                        "avg_following": { "$avg": "$following" },
                        "avg_issuesOpen": { "$avg": "$issuesOpen" },
                        "avg_issuesClosed": { "$avg": "$issuesClosed" },
                        "avg_organizations": { "$avg": "$organizations" },
                        "avg_pinnedRepositories": { "$avg": "$pinnedRepositories" },
                        "avg_pullOpen": { "$avg": "$pullOpen" },
                        "avg_pullClosed": { "$avg": "$pullClosed" },
                        "avg_pullMerged": { "$avg": "$pullMerged" },
                        "avg_repositories": { "$avg": "$repositories" },
                        "avg_repositoriesContributedTo": { "$avg": "$repositoriesContributedTo" },
                        "avg_starredRepositories": { "$avg": "$starredRepositories" },
                        "avg_watching": { "$avg": "$watching" },
                        "avg_bio": { "$avg": "$bio" },
                        "avg_location": { "$avg": "$location" },
                        "avg_bio": { "$avg": { "$sum": {"$cond" : [ "$bio", 1, 0 ] }} },
                        "avg_location": { "$avg": { "$sum": {"$cond" : [ "$location", 1, 0 ] }} },
                        "avg_company": { "$avg": { "$sum": {"$cond" : [ "$company", 1, 0 ] }} },
                    }
                }
            ]
        ) ])
        return avg

