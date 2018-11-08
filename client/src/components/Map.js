import React, { Component } from 'react';
import Button from './Button'
import map_html from './one_trip.html';
import axios from 'axios'

class Map extends Component {
    handleClick = async () => {
        console.log('thanks for clicking! ')
        const { data } = await axios.get('/api')
        console.log('data', data)
    }

    render() {
        return (
            <div>
                <h2>This is supposed to be a map</h2>
                <div dangerouslySetInnerHTML={{__html: map_html}}/>
                <Button text='Get a random trip' onClick={this.handleClick} />
            </div>
        )
    }
 }

export default Map;