import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Typography, Container, Box } from '@mui/material';
import axios from 'axios';
import getRecipesFromIngredients from './openai';

const ImageUpload = () => {
  const navigate = useNavigate();
  const [image, setImage] = useState(null);
  const [detectionResult, setDetectionResult] = useState(null);

  const handleImageUpload = async (file) => {
    if (file) {
      setImage(URL.createObjectURL(file));

      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await axios.post('http://localhost:5000/detect', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });

        const detections = response.data.detections;
        setDetectionResult(detections);
        
        const ingredients = detections.map(d => d.ingredient);
        const recipesText = await getRecipesFromIngredients(ingredients);
        const parsedRecipes = parseRecipes(recipesText);
        navigate('/recipes', { state: { recipes: parsedRecipes, ingredients } });

      } catch (error) {
        console.error('Error uploading image:', error);
      }
    }
  };

  const parseRecipes = (text) => {
    return text.split('\n\n').map((recipeText, index) => {
      const nameMatch = recipeText.match(/레시피 이름: (.+)/);
      const ingredientsMatch = recipeText.match(/재료: (.+)/);
      const instructionsMatch = recipeText.match(/조리법: (.+)/);

      const name = nameMatch ? nameMatch[1] : `레시피 ${index + 1}`;
      const ingredients = ingredientsMatch ? ingredientsMatch[1].split(', ') : [];
      const instructions = instructionsMatch ? instructionsMatch[1].split(/(?:\d+\.\s)/).filter(Boolean).map(step => step.trim()) : [];

      return {
        name,
        ingredients,
        instructions,
      };
    });
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    handleImageUpload(file);
  };

  return (
    <Container style={{ textAlign: 'center', padding: '1rem', maxWidth: '100%', height: '100vh', overflow: 'hidden' }}>
      <Box>
        <Typography variant="h4" component="h1" gutterBottom style={{ marginBottom: '1rem' }}>
          레시피 추천
        </Typography>
        <Typography variant="body1" gutterBottom style={{ marginBottom: '0.5rem', color: 'red' }}>
          * 사진을 업로드하면 AI가 레시피 리스트를 제공합니다.
        </Typography>
        <Box
          border={1}
          borderRadius="borderRadius"
          borderColor="grey.400"
          display="flex"
          flexDirection="column"
          alignItems="center"
          justifyContent="center"
          padding="1rem"
          marginTop="1rem"
          style={{ borderStyle: 'dotted', height: '200px', maxWidth: '400px', margin: '0 auto', cursor: 'pointer' }}
          component="label"
        >
          {image ? (
            <img src={image} alt="Uploaded" style={{ maxWidth: '100%', maxHeight: '100%' }} />
          ) : (
            <Box
              display="flex"
              flexDirection="column"
              alignItems="center"
              justifyContent="center"
              style={{ height: '100%', textAlign: 'center' }}
            >
              <Typography variant="h6" component="h2" gutterBottom>
                사진 업로드
              </Typography>
              <Typography variant="body2" gutterBottom>
                (촬영/갤러리 이미지)
              </Typography>
            </Box>
          )}
          <input
            type="file"
            hidden
            onChange={handleFileChange}
          />
        </Box>
      </Box>
    </Container>
  );
};

export default ImageUpload;
