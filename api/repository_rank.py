import requests
import json


url = 'https://api.github.com/graphql'
api_token = 'abf45d6aab2ff86839f056e5a53efa787515ae28'
headers = {'Authorization': f'token {api_token}'}

def query(q):
    return { "query": f"{q}" }

def repository_rank(name):
    return rank_followers(followers) + rank_following(following)

def rank_followers(followers):
    return 0

def rank_following(following):
    return 0

if __name__ == '__main__':
    q = '''
    {
        user(login: "faviouz") {
            followers(last: 20) {
              edges {
                node {
                  login
                  createdAt
                }
              }
            }
        }
    }'''

    r = requests.post(url=url, json=query(q), headers=headers)
    print(r.text)

