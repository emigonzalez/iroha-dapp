import * as React from 'react';
import AssetForm from '../components/AssetForm';

export default function CreateAssets() {
  return (
    <div className="Page">
      <header className="Page-header center-x center-y flex-col">
        <AssetForm />
      </header>
    </div>
  );
}
