import React from 'react';
import { useLocation } from 'react-router-dom';
import { Typography, Container, Box } from '@mui/material';

const RecipeDetail = () => {
  const location = useLocation();
  const { recipe } = location.state || {};

  console.log('Recipe Detail:', recipe);

  if (!recipe) {
    return <Typography variant="h6" component="h2">레시피를 찾을 수 없습니다.</Typography>;
  }

  return (
    <Container style={{ textAlign: 'center', padding: '1rem', maxWidth: '100%', height: '100vh', overflow: 'auto' }}>
      <Box>
        <Typography variant="h4" component="h1" gutterBottom style={{ marginBottom: '1rem' }}>
          {recipe.name}
        </Typography>
        <Typography variant="h6" component="h2" style={{ marginTop: '1rem', marginBottom: '1rem' }}>
          만드는 방법
        </Typography>
        <ol style={{ textAlign: 'left', padding: '0 2rem' }}>
          {recipe.instructions.map((instruction, index) => (
            <li key={index} style={{ marginBottom: '1rem' }}>
              <Typography variant="body1" style={{ marginBottom: '1rem' }}>{instruction}</Typography>
            </li>
          ))}
        </ol>
      </Box>
    </Container>
  );
};

export default RecipeDetail;
