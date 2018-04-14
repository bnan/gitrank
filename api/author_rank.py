import requests
import json


url = 'https://api.github.com/graphql'
api_token = 'a68f7ffae3ee31dd86209dcc5e56be49e9cd974a'
headers = {'Authorization': f'token {api_token}'}

def query(q):
    return { "query": q }

def author_rank(username):
    return rank_followers(followers) + rank_following(following)

def rank_followers(followers):
    return 0

def rank_following(following):
    return 0

if __name__ == '__main__':

    queryBody = '''
        followers {
          totalCount
        }
        following {
          totalCount
        }
        issuesOpen:issues(states:OPEN) {
          totalCount
        }
        issuesClosed:issues(states:CLOSED) {
          totalCount
        }
        organizations {
          totalCount
        }
        pinnedRepositories(privacy:PUBLIC) {
          totalCount
        }
        pullOpen:pullRequests(states:OPEN) {
          totalCount
        }
        pullClosed:pullRequests(states:CLOSED) {
          totalCount
        }
        pullMerged:pullRequests(states:MERGED) {
          totalCount
        }
        repositories(privacy: PUBLIC) {
          totalCount
        }
        repositoriesContributedTo(privacy: PUBLIC) {
          totalCount
        }
        starredRepositories {
          totalCount
        }
        watching(privacy: PUBLIC) {
          totalCount
        }
        location
        company
        createdAt
        avatarUrl
        '''

    q = '''
    {
        user1:user(login: "dedukun"){
            %s
        },
        user2:user(login: "faviouz"){
            %s
        }
    }''' % (queryBody,queryBody)

    r = requests.post(url=url, json=query(q), headers=headers)
    print(r.text)

