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

def user_rank(user):

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
        user(login: "%s"){
            %s
        }
    }''' % (user, queryBody)

    r = requests.post(url=url, json=query(q), headers=headers)
    json_data = json.loads(r.text)

    return json_data['data']



def repository_rank(user, repo):

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
              history(first:0){
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
      repository(owner: "%s", name: "%s") {
        %s
      }
    }''' % (user, repo, queryBody)

    r = requests.post(url=url, json=query(q), headers=headers)
    json_data = json.loads(r.text)

    return json_data['data']

if __name__ == '__main__':
	print(repository_rank("faviouz", "cantina"))
	print(user_rank("faviouz"))
