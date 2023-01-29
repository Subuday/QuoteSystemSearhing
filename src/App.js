import logo from './logo.svg';
import React, {Component} from 'react';
import './App.css';
import axios from 'axios';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import 'bootstrap/dist/css/bootstrap.min.css';

class App extends Component {
    state = {
        selectedFile: null,
        chapter: null,
        getContext: false,
    }

    fileChangedHandler = event => {
        this.setState({ selectedFile: event.target.files[0] })
    }

    getContextHandler = event => {
        this.setState({ getContext: true})
    }

    uploadHandler = () => {
      var that = this;
      const formData = new FormData()
      formData.append(
        'file',
        this.state.selectedFile,
        this.state.selectedFile.name
      )
      axios.post('http://127.0.0.1:5000/quote', formData)
        .then(function (response) {
            that.setState({ chapter: response["data"]["chapters"][0]})
            console.log(response["data"]["chapters"][0]);
          })
    }

  render() {
    return (
    <div className="App">
      <header className="App-header">
        <input className="input" type="file" onChange={this.fileChangedHandler}/>
        <Button className="input" onClick={this.uploadHandler}>Find quote!</Button>
        {this.state.chapter != null &&
            <Card>
              <Card.Title>{this.state.chapter["source"]["book"] + " " + this.state.chapter["source"]["chapter"]}</Card.Title>
              <Card.Body dangerouslySetInnerHTML={{__html: this.state.chapter["highlight"]["text"].join("...")}}></Card.Body>
            </Card>
        }
        <Button className="input" onClick={this.getContextHandler}>Get quote in context</Button>
        {this.state.chapter != null && this.state.getContext &&
            <Card>
              <Card.Title>{"Full chapter " + this.state.chapter["source"]["book"] + " " + this.state.chapter["source"]["chapter"]}</Card.Title>
              <Card.Body>{this.state.chapter["source"]["text"]}</Card.Body>
            </Card>
        }
      </header>
    </div>
    );
  }
}

export default App;
