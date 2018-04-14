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

    isBestAtMetric(repo, prop) {
        let best = true

        for (let r of this.state.repos) {
            if (r[prop] > repo[prop]) {
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
            return json['results']
        } catch (error) {
            console.error(error)
        }
    }

    async handleRepoCompare(e) {
        e.preventDefault()
        if (!this.state.repo1 || !this.state.repo2) {
            this.setState({ users: [], repos: [], error: true, loading: false })
        } else {
            this.setState({ users: [], repos: [], error: false, loading: true })
            let repos = await this.getRepositories(this.state.repo1, this.state.repo2)
            console.log(repos)
            this.setState({ users: [], repos: repos })
        }
    }

    async handleUserCompare(e) {
        e.preventDefault()
        if (!this.state.user1 || !this.state.user2) {
            this.setState({ users: [], repos: [], error: true, loading: false })
        } else {
            this.setState({ users: [], repos: [], error: false, loading: true })
            let users = await this.getUsers(this.state.user1, this.state.user2)
            this.setState({ users: users, repos: [] })
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

                <div className="row">
                    {this.state.users.map((user, index) => (
                        <div key={index} className="col-sm-6">
                            <div className="card">
                                <div className="card-body">
                                    <div className="media">
                                        <img width="64" height="64" className="mr-3" src={user.avatarUrl} alt={user.bio}/>
                                        <div className="media-body">
                                            <h5 className="mt-0">{user.name}</h5>
                                            <p>{user.bio}</p>

                                            <ul>
                                                <li>{user.followers} followers</li>
                                                <li>{user.following} following</li>
                                                <li>{user.issuesOpen} open issues out of {user.issuesClosed + user.issuesOpen}</li>
                                                <li>{user.watching} watching</li>
                                                <li>registered since {user.createdAt}</li>
                                                <li>Score {user.score}</li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>

                {this.state.repos.length > 0 && (
                <div className="row">
                    <div className="col-sm-12">
                        <table style={{background:'white'}} className="table table-bordered table-responsive">
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
                                    <th scope="row">Created At</th>
                                    {this.state.repos.map((repo, index) => (
                                        <td key={index}>{repo.createdAt}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Last Updated At</th>
                                    {this.state.repos.map((repo, index) => (
                                        <td className={this.isBestAtMetric(repo, 'pushedAt') ? "table-success" : "table-danger"} key={index}>{repo.pushedAt}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Stars</th>
                                    {this.state.repos.map((repo, index) => (
                                        <td className={this.isBestAtMetric(repo, 'stargazers') ? "table-success" : "table-danger"} key={index}>{repo.stargazers}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Watchers</th>
                                    {this.state.repos.map((repo, index) => (
                                        <td className={this.isBestAtMetric(repo, 'watchers') ? "table-success" : "table-danger"} key={index}>{repo.watchers}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Forks</th>
                                    {this.state.repos.map((repo, index) => (
                                        <td className={this.isBestAtMetric(repo, 'forkCount') ? "table-success" : "table-danger"} key={index}>{repo.forkCount}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Commits</th>
                                    {this.state.repos.map((repo, index) => (
                                        <td className={this.isBestAtMetric(repo, 'totalCommits') ? "table-success" : "table-danger"} key={index}>{repo.totalCommits}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Deployments</th>
                                    {this.state.repos.map((repo, index) => (
                                        <td className={this.isBestAtMetric(repo, 'deployments') ? "table-success" : "table-danger"} key={index}>{repo.deployments}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Releases</th>
                                    {this.state.repos.map((repo, index) => (
                                        <td className={this.isBestAtMetric(repo, 'releases') ? "table-success" : "table-danger"} key={index}>{repo.releases}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Issues</th>
                                    {this.state.repos.map((repo, index) => (
                                        <td className={this.isBestAtMetric(repo, 'issuesOpen') ? "table-success" : "table-danger"} key={index}>{repo.issuesOpen} open, {repo.issuesClosed} closed</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Pull Requests</th>
                                    {this.state.repos.map((repo, index) => (
                                        <td className={this.isBestAtMetric(repo, 'pullOpen') ? "table-success" : "table-danger"} key={index}>{repo.pullOpen} open, {repo.pullMerged} merged, {repo.pullClosed} closed</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Milestones</th>
                                    {this.state.repos.map((repo, index) => (
                                        <td className={this.isBestAtMetric(repo, 'mileClosed') ? "table-success" : "table-danger"} key={index}>{repo.mileOpen} open, {repo.mileClosed} closed</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Branches</th>
                                    {this.state.repos.map((repo, index) => (
                                        <td className={this.isBestAtMetric(repo, 'branches') ? "table-success" : "table-danger"} key={index}>{repo.branches}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">Tags</th>
                                    {this.state.repos.map((repo, index) => (
                                        <td className={this.isBestAtMetric(repo, 'tags') ? "table-success" : "table-danger"} key={index}>{repo.tags}</td>
                                    ))}
                                </tr>
                                <tr>
                                    <th scope="row">GitRank</th>
                                    {this.state.repos.map((repo, index) => (
                                        <td className={this.isBestAtMetric(repo, 'score') ? "bg-success" : "bg-danger"} key={index}>{repo.score}</td>
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
