import React, { useState } from 'react';

import './Page.css';
import Card from '../components/Card';
import Button from '@mui/material/Button';

export default function ListAssets() {
  const [assets, setAssets] = useState([]);

  const getAssets = async () => {
    await fetch('https://jsonplaceholder.typicode.com/posts')
    .then((response) => response.json())
    .then((json) => setAssets(json))
    .then((json) => console.log(json));
  }

  const SearchInput = () => {
    return (
      <div className="input-group">
        <div className="form-outline" data-mdb-input-init>
          <input type="search" id="form1" className="form-control" placeholder='Buscar activos' />
        </div>
        <Button variant="contained" onClick={() => getAssets()}>Buscar</Button>
      </div>
    )
  }

  return (
    <div className="Page">
      <header className="Page-header center-x">
        <div className="container text-center">
          <div className="row mb-5">
            <div className="col" />
            <div className="col">
              <SearchInput/>
            </div>
            <div className="col" />
          </div>
          <hr/>
          <div className="row">
              {assets.map((asset, index) => (
                <div key={index} className="col-3 p-2">
                  <Card title={asset.title} description={asset.body} />
                </div>
              ))}
          </div>
        </div>
      </header>
    </div>
  );
}
