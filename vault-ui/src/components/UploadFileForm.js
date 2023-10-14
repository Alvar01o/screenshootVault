import React from 'react';

function UploadFileForm(props) {
    return (
        <section className="upload-file-form">
            {props.children}    
        </section>
    );
}

export default UploadFileForm;