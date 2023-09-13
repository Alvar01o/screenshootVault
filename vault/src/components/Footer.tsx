import React, { Component } from "react";
import PropTypes from "prop-types";

class Footer extends Component {
    constructor(props: any) {
        super(props);
    }

    static propTypes = {};

    render() {
        return (<footer><p>&copy; 2023 Your Company Name. All Rights Reserved.</p></footer>)
    }
}

Footer.propTypes = {};

export default Footer;

