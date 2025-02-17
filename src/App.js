import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ImageUpload from './ImageUpload';
import RecipeList from './RecipeList';
import RecipeDetail from './RecipeDetail';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ImageUpload />} />
        <Route path="/recipes" element={<RecipeList />} />
        <Route path="/recipe/:name" element={<RecipeDetail />} />
      </Routes>
    </Router>
  );
}

export default App;
