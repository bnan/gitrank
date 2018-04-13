import requests
import json


url = 'https://api.github.com/graphql'
api_token = 'a68f7ffae3ee31dd86209dcc5e56be49e9cd974a'
headers = {'Authorization': f'token {api_token}'}

def query(q):
    return { "query": f"{q}" }

def author_rank(username):
    return rank_followers(followers) + rank_following(following)

def rank_followers(followers):
    return 0

def rank_following(following):
    return 0

if __name__ == '__main__':
    q = '''
    query{
        user(login: "faviouz"){
            followers{
                totalCount
            }
            following {
                totalCount
            }
            issues{
              totalCount
            }
            organizations{
              totalCount
            }
            pinnedRepositories{
              totalCount
            }
            pullRequests{
              totalCount
            }
            repositories(privacy: PUBLIC){
              totalCount
            }
            repositoriesContributedTo(privacy: PUBLIC){
              totalCount
            }
            starredRepositories{
              totalCount
            }
            watching(privacy: PUBLIC){
              totalCount
            }
            location
            company
            createdAt
            avatarUrl
          }
    }'''

    r = requests.post(url=url, json=query(q), headers=headers)
    print(r.text)

