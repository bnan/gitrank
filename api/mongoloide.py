from pymongo import MongoClient
import random


class Mongoloide:
    def __init__(self):
        client = MongoClient('mongo', 27017)
        db = client.test_database
        self.db = client.test_database
        self.comparisons = db.comparisons
        self.users = db.users
        self.repos = db.repos

    def add_comparison(self, name1, name2):
        compA = self.comparisons.find_one({"repo_name":name1})
        compB = self.comparisons.find_one({"repo_name":name2})

        if compA == None:
            compA = {"repo_name":name1,
                     "compared_to":[name2,],
                     "history":[]}
            comp = self.comparisons.insert_one(compA)
        else:
            new_values = compA["compared_to"] + [name2]
            compA = self.comparisons.update_one({"repo_name":name1}, {'$set': {'compared_to': new_values}})

        if compB == None:
            compB = {"repo_name":name2, "compared_to":[name1,], "history":[]}
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
        except Exception:
            return []

    def set_score(self, name, score):
        comp = self.comparisons.find_one({"repo_name":name })
        new_scores = comp["history"]+[score]
        comp = self.comparisons.update_one({"repo_name":name }, {'$set': {'history': new_scores}})

    def get_history(self, name):
        comp = self.comparisons.find_one({"repo_name":name })
        return comp["history"]

    def get_user(self, name):
        return self.users.find_one({"user_name":name})

    def store_user(self, name, data):
        user = self.users.find_one({"user_name":name})
        for key, value in data.items():
            user = self.users.update_one({"user_name":name}, {'$set': {key: value}}, upsert=True)
        return user

    def users_average(self):
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
                    }
                }
            ]
        ) ])
        return avg


    def get_repo(self, name):
        return self.repos.find_one({"repo_name":name})

    def store_repo(self, name, data):
        repo = self.repos.find_one({"repo_name":name})
        for key, value in data.items():
            repo = self.repos.update_one({"repo_name":name}, {'$set': {key: value}}, upsert=True)
        return repo

    def repos_average(self):
        avg =  set([ print(x) for x in self.repos.aggregate(
            [
                {
                    "$group":
                    {
                        "_id": "null",
                        "avg_stargazers":   { "$avg": "$stargazers" },
                        "avg_watchers":     { "$avg": "$watchers" },
                        "avg_forkCount":    { "$avg": "$forkCount" },
                        "avg_branches":     { "$avg": "$branches" },
                        "avg_tags":         { "$avg": "$tags" },
                        "avg_totalCommits": { "$avg": "$totalCommits" },

                        "avg_deployments":  { "$avg": "$deployments" },
                        "avg_releases":     { "$avg": "$releases" },
                        "avg_issuesOpen":   { "$avg": "$issuesOpen" },
                        "avg_issuesClosed": { "$avg": "$issuesClosed" },
                        "avg_pullOpen":     { "$avg": "$pullOpen" },

                        "avg_pullClosed":   { "$avg": "$pullClosed" },
                        "avg_pullMerged":   { "$avg": "$pullMerged" },
                        "avg_mileOpen":     { "$avg": "$mileOpen" },
                        "avg_mileClosed":   { "$avg": "$mileClosed" },
                        "avg_languages":    { "$avg": "$languages" },

                    }
                }
            ]
        ) ])
        return avg

