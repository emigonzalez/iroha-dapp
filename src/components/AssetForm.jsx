import React, { useState } from 'react';

const AssetForm = () => {
    const [assetName, setAssetName] = useState("");
    const [domain, setDomain] = useState("");
    const [precision, setPrecision] = useState(0);
    const [isLoading, setIsLoading] = useState(false);

    const createAsset = async (event) => {
        setIsLoading(true);
        event.preventDefault();

        await fetch('https://jsonplaceholder.typicode.com/posts', {
            method: 'POST',
            body: JSON.stringify({
              title: assetName,
              body: domain,
              userId: precision,
            }),
            headers: {
              'Content-type': 'application/json; charset=UTF-8',
            },
          })
            .then((response) => response.json())
            .then((json) => alert(`Activo Creado Correctamente: ${JSON.stringify(json)}`))
            .then(() => setIsLoading(false));
    }

    return (
        <form onSubmit={(event) => {createAsset(event); event.preventDefault();}}>
            <div className="mb-3">
                <label htmlFor="assetName" className="form-label">Nombre de Activo</label>
                <span className="text-danger"> * </span>
                <input 
                    required type="text" className="form-control" id="assetName" 
                    value={assetName} onChange={(event) => setAssetName(event.target.value)}
                />
            </div>
            <div className="mb-3">
                <label htmlFor="domainId" className="form-label">Dominio</label>
                <span className="text-danger"> * </span>
                <input 
                    required type="text" className="form-control" id="domainId"
                    value={domain} onChange={(event) => setDomain(event.target.value)}
                />
            </div>
            <div className="mb-3">
                <label htmlFor="precision" className="form-label">Precision</label>
                <span className="text-danger"> * </span>
                <input 
                    required type="number" className="form-control" id="precision" min="0" max="100" 
                    value={precision} onChange={(event) => setPrecision(event.target.value)}
                />
            </div>
            <button type="submit" className="btn btn-primary" disabled={isLoading}>Crear Activo</button>
        </form>
    )
}

export default AssetForm;
