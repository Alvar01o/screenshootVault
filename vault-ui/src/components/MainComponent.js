import React from 'react';
import './MainComponent.css';

function MainComponent(props) {
    return (
        <main id="main-content">
            {props.children}    
        </main>
    );
}

export default MainComponent;