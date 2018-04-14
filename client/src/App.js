import React, { Component } from 'react'
import './App.css'

const API_URL = 'http://localhost:1337/api/v1'

class App extends Component {
    constructor(props) {
        super(props)
        this.state = {
            users: [],
            repositories: [],
            url1: 'tensorflow/tensorflow',
            url2: 'pytorch/pytorch',
        }
    }

    handleObject1(e) {
        this.setState({ url1: e.target.value })
    }

    handleObject2(e) {
        this.setState({ url2: e.target.value })
    }

    isRepository(url) {
        return (new RegExp("^.+/.+$").test(url))
    }

    async getRepositories(name1, name2) {
        try {
            name1 = name1.replace('/', '.')
            name2 = name2.replace('/', '.')
            let response = await fetch(API_URL + '/repository/' + name1 + '/' + name2)
            let json = await response.json()
            console.log(json)
            return json['results']
        } catch (error) {
            console.error(error)
        }
    }

    async getUsers(user1, user2) {
        try {
            let response = await fetch(API_URL + '/user/' + user1 + '/' + user2)
            let json = await response.json()
            console.log(json)
            return json['results']
        } catch (error) {
            console.error(error)
        }
    }

    async handleCompare(e) {
        e.preventDefault()

        if (this.state.url1 === this.state.url2 && this.isRepository(this.state.url1) !== this.isRepository(this.state.url2)) {
            this.setState({
                users: [],
                repositories: []
            })
        } else if (this.isRepository(this.state.url1)) {
            let repositories = await this.getRepositories(this.state.url1, this.state.url2)
            this.setState({
                users: [],
                repositories: repositories
            })
        } else {
            let users = await this.getUsers(this.state.url1, this.state.url2)
            this.setState({
                users: users,
                repositories: []
            })
        }
    }

    render() {
        return (
            <div className="container">
                <div className="card mt-4 mb-4 text-center">
                    <div className="card-body">
                        <h1>gitrank</h1>
                        <p>Compare two GitHub users or repositories.</p>
                        <form className="form-inline text-center">
                            <div className="form-group">
                                <input onChange={(e) => this.handleObject1(e)} type="text" className="form-control" id="url1" />
                                {' vs '}
                                <input onChange={(e) => this.handleObject2(e)} type="text" className="form-control" id="url2" />
                            </div>
                            <button onClick={(e) => this.handleCompare(e)} className="btn btn-primary btn-lg" id="compare">Compare</button>
                        </form>
                    </div>
                </div>

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
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>

                <div className="row">
                    <div className="col-sm-12">
                        <div className="card">
                            <div className="card-body">
                                <table className="table table-striped table-hover">
                                    <thead>
                                        <tr>
                                            <th scope="col">Metric</th>
                                            {this.state.repositories.map((repo, index) => (
                                                <th scope="col" key={index}>{repo.name}</th>
                                            ))}
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <th scope="row">Last Updated</th>
                                            {this.state.repositories.map((repo, index) => (
                                                <td key={index}>{repo.pushedAt}</td>
                                            ))}
                                        </tr>
                                        <tr>
                                            <th scope="row">Languages</th>
                                            {this.state.repositories.map((repo, index) => (
                                                <td key={index}>{repo.languages.join(', ')}</td>
                                            ))}
                                        </tr>
                                        <tr>
                                            <th scope="row">Commits</th>
                                            {this.state.repositories.map((repo, index) => (
                                                <td key={index}>{repo.totalCommits}</td>
                                            ))}
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

export default App
