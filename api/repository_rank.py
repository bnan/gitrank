import requests
import json


url = 'https://api.github.com/graphql'
api_token = 'a68f7ffae3ee31dd86209dcc5e56be49e9cd974a'
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

    queryBody = '''
        createdAt
        stargazers {
          totalCount
        }
        watchers {
          totalCount
        }
        forkCount
        refs(refPrefix: "refs/") {
          totalCount
        }
        master: ref(qualifiedName: "master") {
          commit: target {
            ... on Commit {
              history{
                totalCount
              }
            }
          }
        }
        pushedAt
        diskUsage
        deployments {
          totalCount
        }
        releases {
          totalCount
        }
        issueOpen: issues(states: OPEN) {
          totalCount
        }
        issueClosed: issues(states: CLOSED) {
          totalCount
        }
        pullOpen: pullRequests(states: OPEN) {
          totalCount
        }
        pullClosed: pullRequests(states: CLOSED) {
          totalCount
        }
        pullMerged: pullRequests(states: MERGED) {
          totalCount
        }
        mileOpen: milestones(states: OPEN) {
          totalCount
        }
        mileClosed: milestones(states: CLOSED) {
          totalCount
        }
        languages(first: 5, orderBy: {field: SIZE, direction: DESC}) {
          edges {
            node {
              name
            }
          }
        }
        isArchived
        isFork
        isMirror
        isLocked
        '''

    q = '''
    {
      repo1: repository(owner: "makeorbreak-io", name: "peimi") {
        %s
      },
      repo2: repository(owner: "bnan", name: "markovitter") {
        %s
      }
    }''' % (queryBody,queryBody)

    r = requests.post(url=url, json=query(q), headers=headers)
    print(r.text)

