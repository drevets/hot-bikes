import React, { Component } from 'react';

class Button extends Component {

    render() {
        return (
            <button type='submit' onClick={this.props.onClick}>{this.props.text}</button>
        )
    }

}

export default Button;