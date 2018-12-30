import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {
  state = {
    ready: false,
    error: null
  };

  componentDidMount() {
    setInterval(() => {
      fetch("http://127.0.0.1:8002/ready")
        .then(res => res.json())
        .then(
          (result) => {
            console.log(result);
            this.setState({
              ready: result
            });
          },
          // Note: it's important to handle errors here
          // instead of a catch() block so that we don't swallow
          // exceptions from actual bugs in components.
          (error) => {
            this.setState({
              error
            });
          }
        )
    }, 5000);
  }
  render() {
    let ready = this.state.ready;
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            Edit <code>src/App.js</code> and save to reload.
          </p>
          <p>{'ready? '+ready}</p>
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
        </header>
      </div>
    );
  }
}

export default App;
