import React from 'react';
import './MainComponent.css';

function MainComponent(props:any) {
    return (
        <main id="main-content">
            {props.children}    
        </main>
    );
}

export default MainComponent;