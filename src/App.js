// App.js
import { Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import Home from './pages/Home';
import ListAssets from './pages/ListAssets';
import CreateAsset from './pages/CreateAssets';

const App = () => {
 return (
    <>
      <Navigation />
       <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/assets" element={<ListAssets />} />
          <Route path="/assets/create" element={<CreateAsset />} />
       </Routes>
    </>
 );
};

export default App;
