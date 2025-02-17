import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Button, Typography, Container, Box } from '@mui/material';
import getRecipesFromIngredients from './openai'; // 기본 내보내기 임포트

const RecipeList = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { recipes, detectedIngredients } = location.state || { recipes: [], detectedIngredients: [] };

  console.log('Recipe List:', recipes);
  console.log('Detected Ingredients:', detectedIngredients);

  const refreshRecipes = async () => {
    try {
      const ingredients = detectedIngredients.length > 0 ? detectedIngredients : ['돼지고기', '당근', '감자', '파', '양파'];
      const recipesText = await getRecipesFromIngredients(ingredients);
      const parsedRecipes = parseRecipes(recipesText);
      console.log('Parsed Recipes:', parsedRecipes);
      navigate('/recipes', { state: { recipes: parsedRecipes, detectedIngredients: ingredients } });
    } catch (error) {
      console.error('Error refreshing recipes:', error);
    }
  };

  const parseRecipes = (text) => {
    console.log('Raw Recipes Text:', text);

    const recipesArray = text.split('레시피 이름:').slice(1);
    const parsedRecipes = recipesArray.map((recipeText, index) => {
      try {
        const nameMatch = recipeText.match(/(.+?)\n/);
        const name = nameMatch ? nameMatch[1].trim() : `레시피 ${index + 1}`;
        const ingredientsMatch = recipeText.match(/재료:([\s\S]+?)조리법:/);
        const ingredients = ingredientsMatch ? ingredientsMatch[1].trim().split('\n').map(item => item.replace('-', '').trim()) : [];
        const instructionsMatch = recipeText.match(/조리법:([\s\S]+)/);
        const instructions = instructionsMatch ? instructions[1].trim().split('\n').map(step => step.trim()) : [];

        console.log('Name:', name);
        console.log('Ingredients:', ingredients);
        console.log('Instructions:', instructions);

        return {
          name,
          ingredients,
          instructions,
        };
      } catch (error) {
        console.error('Error parsing recipe:', recipeText, error);
        return {
          name: `레시피 ${index + 1}`,
          ingredients: [],
          instructions: [],
        };
      }
    });

    return parsedRecipes;
  };

  const handleRecipeClick = (recipe) => {
    console.log('Clicked Recipe:', recipe);
    navigate(`/recipe/${recipe.name}`, { state: { recipe } });
  };

  return (
    <Container style={{ textAlign: 'center', padding: '1rem', maxWidth: '100%', height: '100vh', overflow: 'auto' }}>
      <Box>
        <Typography variant="h4" component="h1" gutterBottom style={{ marginBottom: '1rem' }}>
          추천 레시피
        </Typography>
        {recipes.map((recipe, index) => (
          <Box
            key={index}
            border={1}
            borderRadius="16px"
            borderColor="grey.400"
            padding="1rem"
            marginBottom="1rem"
            display="flex"
            flexDirection="column"
            alignItems="center"
            justifyContent="center"
            style={{ backgroundColor: '#f9f9f9', cursor: 'pointer' }}
            onClick={() => handleRecipeClick(recipe)}
          >
            <Typography variant="h6" component="h2" gutterBottom>
              {recipe.name}
            </Typography>
            <Typography variant="body1" style={{ marginTop: '0.5rem' }}>
              재료:
            </Typography>
            <ul>
              {recipe.ingredients.map((ingredient, index) => (
                <li key={index}>{ingredient}</li>
              ))}
            </ul>
          </Box>
        ))}
        <Button variant="contained" onClick={refreshRecipes} style={{ marginTop: '1rem' }}>
          다른 레시피 추천
        </Button>
      </Box>
    </Container>
  );
};

export default RecipeList;