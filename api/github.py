import requests
import json
import math
import time
import dateutil.parser


url = 'https://api.github.com/graphql'
api_token = 'a68f7ffae3ee31dd86209dcc5e56be49e9cd974a'
headers = {'Authorization': f'token {api_token}'}


def query(q):
    payload = { "query": q }
    r = requests.post(url=url, json=payload, headers=headers)
    data = json.loads(r.text)['data']
    return data


def author_rank(username):
    return rank_followers(followers) + rank_following(following)


def rank_followers(followers):
    return 0


def rank_following(following):
    return 0


def get_users(user1, user2):
    queryBody = '''
        followers {
          totalCount
        }
        following {
          totalCount
        } issuesOpen:issues(states:OPEN) { totalCount
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
        repositories(privacy: PUBLIC, affiliations: OWNER) {
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
        bio
        location
        company
        createdAt
        avatarUrl
        login'''

    q = '''
    {
        user1:user(login: "%s"){
            %s
        },
        user2:user(login: "%s"){
            %s
        }
    }''' % (user1, queryBody, user2, queryBody)

    return parse_users(query(q))


def get_repositories(user1, repo1, user2, repo2):
    queryBody = '''
        createdAt
        stargazers {
          totalCount
        }
        watchers {
          totalCount
        }
        forkCount
        branches:refs(refPrefix: "refs/heads/") {
          totalCount
        }
        tags:refs(refPrefix: "refs/tags/") {
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
        deployments {
          totalCount
        }
        releases {
          totalCount
        }
        issuesOpen: issues(states: OPEN) {
          totalCount
        }
        issuesClosed: issues(states: CLOSED) {
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
        licenseInfo {
  	  name
  	}
        description
        hasWikiEnabled
        isArchived
        isFork
        nameWithOwner'''

    q = '''
    {
      repo1:repository(owner: "%s", name: "%s") {
        %s
      },
      repo2:repository(owner: "%s", name: "%s") {
        %s
      }
    }''' % (user1, repo1, queryBody, user2, repo2, queryBody)

    return parse_repositories(query(q))


# Function that parse the data from the users request to be easier to digest
def parse_users(data):
    parsed_data = [
        {
            "name": data['user1']['login'],
            "followers"  : data['user1']['followers']['totalCount'],
            "following"  : data['user1']['following']['totalCount'],
            "issuesOpen" : data['user1']['issuesOpen']['totalCount'],
            "issuesClosed" : data['user1']['issuesClosed']['totalCount'],
            "organizations" : data['user1']['organizations']['totalCount'],
            "pinnedRepositories" : data['user1']['pinnedRepositories']['totalCount'],
            "pullOpen" : data['user1']['pullOpen']['totalCount'],
            "pullClosed" : data['user1']['pullClosed']['totalCount'],
            "pullMerged" : data['user1']['pullMerged']['totalCount'],
            "repositories" : data['user1']['repositories']['totalCount'],
            "repositoriesContributedTo" : data['user1']['repositoriesContributedTo']['totalCount'],
            "starredRepositories" : data['user1']['starredRepositories']['totalCount'],
            "watching" : data['user1']['watching']['totalCount'],
            "bio" : data['user1']['bio'],
            "location" : data['user1']['location'],
            "company"  : data['user1']['company'],
            "createdAt": data['user1']['createdAt'],
            "avatarUrl": data['user1']['avatarUrl'],
            "score": None
        },
        {
            "name": data['user2']['login'],
            "followers"  : data['user2']['followers']['totalCount'],
            "following"  : data['user2']['following']['totalCount'],
            "issuesOpen" : data['user2']['issuesOpen']['totalCount'],
            "issuesClosed" : data['user2']['issuesClosed']['totalCount'],
            "organizations" : data['user2']['organizations']['totalCount'],
            "pinnedRepositories" : data['user2']['pinnedRepositories']['totalCount'],
            "pullOpen" : data['user2']['pullOpen']['totalCount'],
            "pullClosed" : data['user2']['pullClosed']['totalCount'],
            "pullMerged" : data['user2']['pullMerged']['totalCount'],
            "repositories" : data['user2']['repositories']['totalCount'],
            "repositoriesContributedTo" : data['user2']['repositoriesContributedTo']['totalCount'],
            "starredRepositories" : data['user2']['starredRepositories']['totalCount'],
            "watching" : data['user2']['watching']['totalCount'],
            "bio" : data['user2']['bio'],
            "location" : data['user2']['location'],
            "company"  : data['user2']['company'],
            "createdAt": data['user2']['createdAt'],
            "avatarUrl": data['user2']['avatarUrl'],
            "score": None
        }
    ]

    return parsed_data

# Function that parse the data from the repositories request to be easier to digest
def parse_repositories(data):
    languages1 = [t['node']['name'] for t in data['repo1']['languages']['edges']]
    languages2 = [t['node']['name'] for t in data['repo2']['languages']['edges']]
    license1 = data['repo1']['licenseInfo']['name'] if data['repo1']['licenseInfo'] else 'N/A'
    license2 = data['repo2']['licenseInfo']['name'] if data['repo2']['licenseInfo'] else 'N/A'

    parsed_data = [
        {
            "name": data['repo1']['nameWithOwner'],
            "createdAt" : data['repo1']['createdAt'],
            "stargazers": data['repo1']['stargazers']['totalCount'],
            "watchers" : data['repo1']['watchers']['totalCount'],
            "forkCount": data['repo1']['forkCount'],
            "branches" : data['repo1']['branches']['totalCount'] if
                        data['repo1']['branches']['totalCount'] else 1,
            "tags" : data['repo1']['tags']['totalCount'],
            "totalCommits" : data['repo1']['master']['commit']['history']['totalCount'],
            "pushedAt" : data['repo1']['pushedAt'],
            "deployments":  data['repo1']['deployments']['totalCount'],
            "releases" :  data['repo1']['releases']['totalCount'],
            "issuesOpen":  data['repo1']['issuesOpen']['totalCount'],
            "issuesClosed": data['repo1']['issuesClosed']['totalCount'],
            "pullOpen":  data['repo1']['pullOpen']['totalCount'],
            "pullClosed": data['repo1']['pullClosed']['totalCount'],
            "pullMerged": data['repo1']['pullMerged']['totalCount'],
            "mileOpen": data['repo1']['mileOpen']['totalCount'],
            "mileClosed": data['repo1']['mileClosed']['totalCount'],
            "languages" : languages1,
            "license" : license1,
            "description" : data['repo1']['description'],
            "hasWikiEnabled" : data['repo1']['hasWikiEnabled'],
            "isArchived" : data['repo1']['isArchived'],
            "isFork" : data['repo1']['isFork'],
            "score": None
        },
        {
            "name": data['repo2']['nameWithOwner'],
            "createdAt" : data['repo2']['createdAt'],
            "stargazers": data['repo2']['stargazers']['totalCount'],
            "watchers" : data['repo2']['watchers']['totalCount'],
            "forkCount": data['repo2']['forkCount'],
            "branches" : data['repo2']['branches']['totalCount'] if
                        data['repo2']['branches']['totalCount'] else 1,
            "tags" : data['repo2']['tags']['totalCount'],
            "totalCommits" : data['repo2']['master']['commit']['history']['totalCount'],
            "pushedAt" : data['repo2']['pushedAt'],
            "deployments":  data['repo2']['deployments']['totalCount'],
            "releases" :  data['repo2']['releases']['totalCount'],
            "issuesOpen":  data['repo2']['issuesOpen']['totalCount'],
            "issuesClosed": data['repo2']['issuesClosed']['totalCount'],
            "pullOpen":  data['repo2']['pullOpen']['totalCount'],
            "pullClosed": data['repo2']['pullClosed']['totalCount'],
            "pullMerged": data['repo2']['pullMerged']['totalCount'],
            "mileOpen": data['repo2']['mileOpen']['totalCount'],
            "mileClosed": data['repo2']['mileClosed']['totalCount'],
            "languages" : languages2,
            "license" : license2,
            "description" : data['repo2']['description'],
            "hasWikiEnabled" : data['repo2']['hasWikiEnabled'],
            "isArchived" : data['repo2']['isArchived'],
            "isFork" : data['repo2']['isFork'],
            "score": None
        }
    ]

    return parsed_data

# Calculate User rank
def calc_user_rank(data,avg_user):
    # name                           | x
    # followers                      | +
    # following                      | -
    # issuesOpen                     | +
    # issuesClosed                   | +
    # organizations                  | +
    # pinnedRepositories             | ++
    # pullOpen                       | ++
    # pullClosed                     | ++
    # pullMerged                     | +++
    # repositories                   | ++++
    # repositoriesContributedTo      | ++++
    # starredRepositories            | -
    # watching                       | -
    # bio                            | --
    # location                       | --
    # company                        |
    # createdAt                      |
    # avatarUrl                      | x
    # score                          | x

    # List of weights each component has on the rank
    weights = [4/65, 2/65, 4/65, 4/65, 4/65, 5/65, 5/65, 5/65, 6/65, 7/65, 7/65, 2/65, 2/65, 1/65,
            1/65, 3/65, 3/65]
    score = 0
    idx = -1

    for field in data:
        # Skip unwanted params
        if field == "name":
            continue
        if field == "avatarUrl":
            break;

        param = None
        # Parsing some of the params so that they can be used in the calc of the score
        if field == "bio" or field == "company":
            param = data[field] != ""
        elif field == "location":
            param = data[field] != None
        else:
            param = data[field]


        idx = idx + 1 # increment to get the next weights array offset

        # Depending on the type of variable the multiple params aftect the score in different ways
        if type(param) == int:
            if param == 0:
                continue

            avg_val = avg_user["avg_"+field] * 1.125

            par = param/avg_val

            if par > 1:
                par = 1

            score = score + (weights[idx] * par)

        elif type(param) == bool:
            score = score + (weights[idx] if param else 0)
        else: # Date - str
            val = int(time.time())
            try:
                val = int(time.mktime(dateutil.parser.parse(param).timetuple()))
            except:
                pass

            now = int(time.time())

            t_diff = now - val

            avg_val = avg_user["avg_"+field]
            t_diff_avg = (now - avg_val)

            par = t_diff / t_diff_avg

            if par > 1:
                par = 1

            score = score + (weights[idx] * (par))

    return score


# Calculate Repository rank
def calc_repository_rank(data, avg_repo):
    # name                          | x
    # createdAt                     |
    # stargazers                    | ++
    # watchers                      | ++
    # forkCount                     | ++
    # branches                      | +
    # tags                          | +
    # totalCommits                  | +++
    # pushedAt                      | ++
    # deployments                   | ++
    # releases                      | ++
    # issuesOpen                    | +
    # issuesClosed                  | +
    # pullOpen                      | ++
    # pullClosed                    | ++
    # pullMerged                    | +++
    # mileOpen                      |
    # mileClosed                    |
    # languages (number)            | x
    # license                       |
    # description                   | -
    # hasWikiEnabled                | -
    # isArchived                    | ---
    # isFork                        | --
    # score                         | x

    # List of weights each component has on the rank
    weights = [ 4/107, 6/107, 6/107, 6/107, 5/107, 5/107, 7/107, 6/107, 6/107, 6/107, 5/107, 5/107, 6/107, 6/107, 7/107, 4/107, 4/107, 4/107, 3/107, 3/107, 1/107, 2/107]
    score = 0
    idx = -1

    for field in data:
        # Skip unwanted params
        if field == "name" or field == "languages":
            continue
        if field == "score":
            break;

        param = None
        # Parsing some of the params so that they can be used in the calc of the score
        if field == "description" or field == "license":
            param = data[field] != None
        else:
            param = data[field]


        idx = idx + 1 # increment to get the next weights array offset

        # Depending on the type of variable the multiple params aftect the score in different ways
        if type(param) == int:
            if param == 0:
                continue

            avg_val = avg_repo["avg_"+field] * 1.125

            par = param/avg_val

            if par > 1:
                par = 1

            score = score + (weights[idx] * par)

        elif type(param) == bool:
            score = score + (weights[idx] if param else 0)
        else: # Date - str
            val = int(time.time())
            try:
                val = int(time.mktime(dateutil.parser.parse(param).timetuple()))
            except:
                pass

            now = int(time.time())

            t_diff = (now - val)  # Get time diff in days

            avg_val = avg_repo["avg_"+field]
            t_diff_avg = (now - avg_val)

            par = 0
            if field == "createdAt":
                par = t_diff / t_diff_avg

            else:
                par = t_diff_avg / t_diff

            if par > 1:
                par = 1

            score = score + (weights[idx] * (par))

    return score


if __name__ == '__main__':
    print(get_repositories("bnan", "markovitter", "joaobranquinho", "wake_me_up"))
    print()
    print(get_users("faviouz", "dedukun"))
