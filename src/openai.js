import axios from 'axios';

const API_KEY = process.env.REACT_APP_OPENAI_API_KEY;

const getRecipesFromIngredients = async (ingredients) => {
  const prompt = `기본 전제: 앞으로 대답해줄 내용은 최대한 자세히(준비해야 할 재료 양과 같은 내용도 서술) 서술해줘. 
  다음 재료가 있습니다: ${ingredients.join(', ')}. 이 재료를 사용한 3가지 다른 레시피를 제안해줘. 각 레시피는 다음 형식을 따르세요:
1. 레시피 이름
2. 재료: 재료 목록
3. 조리법: 조리 방법 목록
각 레시피는 다음과 같이 구분합니다.

레시피 예시:
레시피 이름: 당근 수프
재료: 당근, 물, 소금
조리법: 1. 당근을 썰고 물에 넣어 몇 분 끓입니다. 2. 소금을 몇g 넣어 간을 맞춥니다. 

이 형식을 따르되, 최대한 자세하게 서술해서 3가지 레시피를 제안해 주세요.`;

  const maxRetries = 5;
  const retryDelay = 2000;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const response = await axios.post(
        'https://api.openai.com/v1/chat/completions',
        {
          model: 'gpt-3.5-turbo',
          messages: [{ role: 'user', content: prompt }],
          max_tokens: 2000,
          temperature: 0.7,
        },
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${API_KEY}`,
          },
        }
      );
      console.log('OpenAI API Response:', response.data.choices[0].message.content);
      return response.data.choices[0].message.content;
    } catch (error) {
      if (error.response && error.response.status === 429 && attempt < maxRetries - 1) {
        console.warn(`Rate limit exceeded. Retrying in ${retryDelay}ms...`);
        await sleep(retryDelay);
      } else {
        console.error('Error fetching recipes from OpenAI:', error);
        break;
      }
    }
  }
  return '';
};

const sleep = (milliseconds) => {
  return new Promise(resolve => setTimeout(resolve, milliseconds));
};

export default getRecipesFromIngredients;
