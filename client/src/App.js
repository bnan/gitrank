import React, { Component } from 'react'
import './App.css'

const API_URL = 'http://localhost:1337/api/v1'

class App extends Component {
    constructor(props) {
        super(props)
        this.state = {
            users: [],
            repos: [],
            suggestions: [],
            repo1: null,
            repo2: null,
            user1: null,
            user2: null,
            error: null
        }
    }

    handleRepo1(e) {
        this.setState({ repo1: e.target.value })
    }

    handleRepo2(e) {
        this.setState({ repo2: e.target.value })
    }

    handleUser1(e) {
        this.setState({ user1: e.target.value })
    }

    handleUser2(e) {
        this.setState({ user2: e.target.value })
    }

    isBestUserAtMetric(user, f) {
        let best = true

        for (let u of this.state.users) {
            if (f(u) > f(user)) {
                best = false
            }
        }

        return best
    }

    isBestRepoAtMetric(repo, f) {
        let best = true

        for (let r of this.state.repos) {
            if (f(r) > f(repo)) {
                best = false
            }
        }

        return best
    }

    async getRepositories(name1, name2) {
        try {
            name1 = name1.replace('/', '.')
            name2 = name2.replace('/', '.')
            let response = await fetch(API_URL + '/repository/' + name1 + '/' + name2)
            let json = await response.json()
            this.setState({ error: json['error'], loading: false })
            return json['results']
        } catch (error) {
            console.error(error)
        }
    }

    async getUsers(user1, user2) {
        try {
            let response = await fetch(API_URL + '/user/' + user1 + '/' + user2)
            let json = await response.json()
            this.setState({ error: json['error'], loading: false })
            return json['results']['users']
        } catch (error) {
            console.error(error)
        }
    }

    async handleRepoCompare(e) {
        e.preventDefault()
        if (!this.state.repo1 || !this.state.repo2) {
            this.setState({ users: [], repos: [], suggestions: [], averages: [], error: true, loading: false })
        } else {
            this.setState({ users: [], repos: [], suggestions: [], averages: [], error: false, loading: true })
            let results = await this.getRepositories(this.state.repo1, this.state.repo2)
            this.setState({ users: [], repos: results['repositories'], suggestions: results['suggestions'], averages: results['averages'] })
        }
    }

    async handleUserCompare(e) {
        e.preventDefault()
        if (!this.state.user1 || !this.state.user2) {
            this.setState({ users: [], repos: [], suggestions: [], averages: [], error: true, loading: false })
        } else {
            this.setState({ users: [], repos: [], suggestions: [], averages: [], error: false, loading: true})
            let users = await this.getUsers(this.state.user1, this.state.user2)
            this.setState({ users: users, repos: [], suggestions: [], averages: [] })
        }
    }

    render() {
        return (
            <div className="container">
                <div className="card mt-4 mb-4">
                    <div className="card-body">
                        <h1>GitRank</h1>

                        <p>Compare two GitHub repositories and choose the best library.</p>
                        <form className="form-inline text-center mb-4">
                            <div className="form-group">
                                <input onChange={(e) => this.handleRepo1(e)} type="text" className="form-control mr-2" placeholder="tensorflow/tensorflow" />
                                {' vs '}
                                <input onChange={(e) => this.handleRepo2(e)} type="text" className="form-control ml-2 mr-3" placeholder="pytorch/pytorch" />
                            </div>
                            <button onClick={(e) => this.handleRepoCompare(e)} className="btn btn-primary">Compare</button>
                        </form>

                        {this.state.suggestions && this.state.suggestions.length !== 0 && (
                            <div className="alert alert-primary" role="alert">
                                Other people have considered
                                <ul>
                                    {this.state.suggestions.map((suggestion, index) => <li><a key={index} href={"https://github.com/"+suggestion.replace('.', '/')}>{suggestion.replace('.', '/')}</a></li>)}
                                </ul>
                            </div>
                        )}

                        <p>Compare two GitHub users and see who's best.</p>
                        <form className="form-inline text-center">
                            <div className="form-group">
                                <input onChange={(e) => this.handleUser1(e)} type="text" className="form-control mr-2" placeholder="faviouz" />
                                {' vs '}
                                <input onChange={(e) => this.handleUser2(e)} type="text" className="form-control ml-2 mr-3" placeholder="torvalds" />
                            </div>
                            <button onClick={(e) => this.handleUserCompare(e)} className="btn btn-primary">Fight</button>
                        </form>
                    </div>
                </div>

                {this.state.error && (
                    <div className="alert alert-danger" role="alert">
                        Oops, something went wrong!
                    </div>
                )}

                {this.state.loading && (
                    <div className="alert alert-primary" role="alert">
                        Loading...
                    </div>
                )}

                {this.state.users.length > 0 && (
                <div className="row">
                    <div className="col-sm-12">
                        <table style={{background:'white'}} className="table table-bordered">
                            <thead className="thead-light">
                                <tr>
                                    <th scope="col">Metric</th>
                                    {this.state.users.map((user, index) => (
                                        <th scope="col" key={index}><img alt={user.name} width={24} height={24} src={user.avatarUrl}/> {user.name}</th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <th scope="row">Bio</th>
                                    {this.state.users.map((user, index) => (
                                        <td key={index}>{user.bio}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Created At</th>
                                    {this.state.users.map((user, index) => (
                                        <td key={index}>{user.createdAt}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Location</th>
                                    {this.state.users.map((user, index) => (
                                        <td key={index}>{user.location}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Company</th>
                                    {this.state.users.map((user, index) => (
                                        <td key={index}>{user.company}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Followers</th>
                                    {this.state.users.map((user, index) => (
                                        <td className={this.isBestUserAtMetric(user, (user) => user.followers) ? "table-success" : "table-danger"} key={index}>{user.followers}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Following</th>
                                    {this.state.users.map((user, index) => (
                                        <td className={this.isBestUserAtMetric(user, (user) => user.following) ? "table-success" : "table-danger"} key={index}>{user.following}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Repositories</th>
                                    {this.state.users.map((user, index) => (
                                        <td className={this.isBestUserAtMetric(user, (user) => user.repositories) ? "table-success" : "table-danger"} key={index}>{user.repositories}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Repositories Contributed To</th>
                                    {this.state.users.map((user, index) => (
                                        <td className={this.isBestUserAtMetric(user, (user) => user.repositoriesContributedTo) ? "table-success" : "table-danger"} key={index}>{user.repositoriesContributedTo}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Issues Open</th>
                                    {this.state.users.map((user, index) => (
                                        <td className={this.isBestUserAtMetric(user, (user) => user.issuesOpen) ? "table-success" : "table-danger"} key={index}>{user.issuesOpen}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Issues Closed</th>
                                    {this.state.users.map((user, index) => (
                                        <td className={this.isBestUserAtMetric(user, (user) => user.issuesClosed) ? "table-success" : "table-danger"} key={index}>{user.issuesClosed}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Pull Requests Open</th>
                                    {this.state.users.map((user, index) => (
                                        <td className={this.isBestUserAtMetric(user, (user) => user.pullOpen) ? "table-success" : "table-danger"} key={index}>{user.pullOpen}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Pull Requests Merged</th>
                                    {this.state.users.map((user, index) => (
                                        <td className={this.isBestUserAtMetric(user, (user) => user.pullMerged) ? "table-success" : "table-danger"} key={index}>{user.pullMerged}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Pull Requests Closed</th>
                                    {this.state.users.map((user, index) => (
                                        <td className={this.isBestUserAtMetric(user, (user) => user.pullClosed) ? "table-success" : "table-danger"} key={index}>{user.pullClosed}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Starred Repositories</th>
                                    {this.state.users.map((user, index) => (
                                        <td className={this.isBestUserAtMetric(user, (user) => user.starredRepositories) ? "table-success" : "table-danger"} key={index}>{user.starredRepositories}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Organizations</th>
                                    {this.state.users.map((user, index) => (
                                        <td className={this.isBestUserAtMetric(user, (user) => user.organizations) ? "table-success" : "table-danger"} key={index}>{user.organizations}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Pinned Repositories</th>
                                    {this.state.users.map((user, index) => (
                                        <td className={this.isBestUserAtMetric(user, (user) => user.pinnedRepositories) ? "table-success" : "table-danger"} key={index}>{user.pinnedRepositories}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Watching</th>
                                    {this.state.users.map((user, index) => (
                                        <td className={this.isBestUserAtMetric(user, (user) => user.watching) ? "table-success" : "table-danger"} key={index}>{user.watching}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">GitRank</th>
                                    {this.state.users.map((user, index) => (
                                        <td className={this.isBestUserAtMetric(user, (user) => user.score) ? "bg-success" : "bg-danger"} key={index}>{user.score}</td>
                                    ))}
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                )}

                {this.state.repos.length > 0 && (
                <div className="row">
                    <div className="col-sm-12">
                        <table style={{background:'white'}} className="table table-bordered">
                            <thead className="thead-light">
                                <tr>
                                    <th scope="col">Metric</th>
                                    {this.state.repos.map((repo, index) => (
                                        <th scope="col" key={index}>{repo.name}</th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <th scope="row">Description</th>
                                    {this.state.repos.map((repo, index) => (
                                        <td key={index}>{repo.description}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Languages</th>
                                    {this.state.repos.map((repo, index) => (
                                        <td key={index}>{repo.languages.join(', ')}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">License</th>
                                    {this.state.repos.map((repo, index) => (
                                        <td key={index}>{repo.license}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Created</th>
                                    {this.state.repos.map((repo, index) => (
                                        <td key={index}>{repo.createdAt}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Last Updated</th>
                                    {this.state.repos.map((repo, index) => (
                                        <td className={this.isBestRepoAtMetric(repo, (repo) => repo.pushedAt) ? "table-success" : "table-danger"} key={index}>{repo.pushedAt}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Stars <br/><small className="font-weight-normal">Average: {this.state.averages['avg_stargazers']}</small></th>
                                    {this.state.repos.map((repo, index) => (
                                        <td className={this.isBestRepoAtMetric(repo, (repo) => repo.stargazers) ? "table-success" : "table-danger"} key={index}>{repo.stargazers}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Watchers <br/><small className="font-weight-normal">Average: {this.state.averages['avg_watchers']}</small></th>
                                    {this.state.repos.map((repo, index) => (
                                        <td className={this.isBestRepoAtMetric(repo, (repo) => repo.watchers) ? "table-success" : "table-danger"} key={index}>{repo.watchers}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Forks <br/><small className="font-weight-normal">Average: {this.state.averages['avg_forkCount']}</small></th>
                                    {this.state.repos.map((repo, index) => (
                                        <td className={this.isBestRepoAtMetric(repo, (repo) => repo.forkCount) ? "table-success" : "table-danger"} key={index}>{repo.forkCount}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Commits <br/><small className="font-weight-normal">Average: {this.state.averages['avg_totalCommits']}</small></th>
                                    {this.state.repos.map((repo, index) => (
                                        <td className={this.isBestRepoAtMetric(repo, (repo) => repo.totalCommits) ? "table-success" : "table-danger"} key={index}>{repo.totalCommits}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Deployments <br/><small className="font-weight-normal">Average: {this.state.averages['avg_deployments']}</small></th>
                                    {this.state.repos.map((repo, index) => (
                                        <td className={this.isBestRepoAtMetric(repo, (repo) => repo.deployments) ? "table-success" : "table-danger"} key={index}>{repo.deployments}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Releases <br/><small className="font-weight-normal">Average: {this.state.averages['avg_releases']}</small></th>
                                    {this.state.repos.map((repo, index) => (
                                        <td className={this.isBestRepoAtMetric(repo, (repo) => repo.releases) ? "table-success" : "table-danger"} key={index}>{repo.releases}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Issues <br/><small className="font-weight-normal">Average: {this.state.averages['avg_issuesOpen'] + this.state.averages['avg_issuesClosed']}</small></th>
                                    {this.state.repos.map((repo, index) => (
                                        <td className={this.isBestRepoAtMetric(repo, (repo) => repo.issuesClosed+repo.issuesOpen) ? "table-success" : "table-danger"} key={index}>{repo.issuesOpen + repo.issuesClosed}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Pull Requests <br/><small className="font-weight-normal">Average: {this.state.averages['avg_pullOpen'] + this.state.averages['avg_pullClosed'] + this.state.averages['avg_pullMerged']}</small></th>
                                    {this.state.repos.map((repo, index) => (
                                        <td className={this.isBestRepoAtMetric(repo, (repo) => repo.pullOpen+repo.pullClosed+repo.pullMerged) ? "table-success" : "table-danger"} key={index}>{repo.pullOpen + repo.pullMerged + repo.pullClosed}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Milestones <br/><small className="font-weight-normal">Average: {this.state.averages['avg_mileOpen'] + this.state.averages['avg_mileClosed']}</small></th>
                                    {this.state.repos.map((repo, index) => (
                                        <td className={this.isBestRepoAtMetric(repo, (repo) => repo.mileOpen+repo.mileClosed) ? "table-success" : "table-danger"} key={index}>{repo.mileOpen+repo.mileClosed}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Branches <br/><small className="font-weight-normal">Average: {this.state.averages['avg_branches']}</small></th>
                                    {this.state.repos.map((repo, index) => (
                                        <td className={this.isBestRepoAtMetric(repo, (repo) => repo.branches) ? "table-success" : "table-danger"} key={index}>{repo.branches}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Tags <br/><small className="font-weight-normal">Average: {this.state.averages['avg_tags']}</small></th>
                                    {this.state.repos.map((repo, index) => (
                                        <td className={this.isBestRepoAtMetric(repo, (repo) => repo.tags) ? "table-success" : "table-danger"} key={index}>{repo.tags}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">GitRank<br/><small className="font-weight-normal">Average: {this.state.averages['avg_score']}</small></th>
                                    {this.state.repos.map((repo, index) => (
                                        <td className={this.isBestRepoAtMetric(repo, (repo) => repo.score) ? "bg-success" : "bg-danger"} key={index}>{repo.score.toFixed(3)}</td>
                                    ))}
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                )}
            </div>
        )
    }
}

export default App
