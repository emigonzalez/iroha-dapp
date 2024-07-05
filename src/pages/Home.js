import * as React from 'react';
import logo from '../images/logo.svg';
import './Page.css';
import Button from '@mui/material/Button';

function Home() {
  return (
    <div className="Page">
      <header className="Page-header center-y center-x">
        <img src={logo} className="Page-logo" alt="logo" />
        <p className="pt-5">Iroha Example DApp</p>
        <Button variant="contained">Hello world</Button>
      </header>
    </div>
  );
}

export default Home;
