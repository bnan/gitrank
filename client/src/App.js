import React, { Component } from 'react'
import './App.css'

class App extends Component {
    constructor(props) {
        super(props)
        this.state = {
            users: [],
            repositories: [],
            url1: '',
            url2: '',
        }
    }

    handleObject1(e) {
        this.setState({ url1: e.target.value })
    }

    handleObject2(e) {
        this.setState({ url2: e.target.value })
    }

    isRepository(url) {
        return (new RegExp("^https://github.com/.+/.+$").test(url))
    }

    handleCompare(e) {
        e.preventDefault()

        if (this.isRepository(this.state.url1) !== this.isRepository(this.state.url2)) {
            this.setState({
                users: [],
                repositories: []
            })
        } else if (this.isRepository(this.state.url1)) {
            this.setState({
                users: [],
                repositories: [
                    { name: 'tensorflow/tensorflow', description: 'Machine learning framework' },
                    { name: 'pytorch/pytorch', description: 'Another machine learning framework' }
                ]
            })
        } else {
            this.setState({
                users: [
                    { "name": "faviouz", "avatar": "https://avatars2.githubusercontent.com/u/180382?s=460&v=4", "bio": "Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque ante sollicitudin." },
                    { "name": "ludeed", "avatar": "https://avatars0.githubusercontent.com/u/9322214?s=400&v=4", "bio": "Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque ante sollicitudin." }
                ],
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
                                <input onChange={(e) => this.handleObject1(e)} type="text" className="form-control" id="url1" placeholder="https://github.com/tensorflow/tensorflow"/>
                                {' vs '}
                                <input onChange={(e) => this.handleObject2(e)} type="text" className="form-control" id="url2" placeholder="https://github.com/pytorch/pytorch"/>
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
                                        <img width="64" height="64" className="mr-3" src={user.avatar} alt={user.bio}/>

                                        <div className="media-body">
                                            <h5 className="mt-0">{user.name}</h5>
                                            <p>{user.bio}</p>

                                            <ul>
                                                <li>hey</li>
                                                <li>hey</li>
                                                <li>hey</li>
                                                <li>hey</li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>

                <div className="row">
                    {this.state.repositories.map((repo, index) => (
                        <div key={index} className="col-sm-6">
                            <div className="card">
                                <div className="card-body">
                                    <div className="media">
                                        <div className="media-body">
                                            <h5 className="mt-0">{repo.name}</h5>
                                            <p>{repo.description}</p>

                                            <ul>
                                                <li>hey</li>
                                                <li>hey</li>
                                                <li>hey</li>
                                                <li>hey</li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        )
    }
}

export default App
