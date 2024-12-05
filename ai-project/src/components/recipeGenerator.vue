<template>
  <div class="container">
    <div class="header">
      <h1>AutoChef</h1>
      <img src="../assets/logo.png" alt="Logo" class="logo" />
    </div>

    <div class="sample-text">
      <p>Welcome to AutoChef! Enter some ingredients below and let me suggest some recipes for you! Please separate ingredients with commas and spaces between them (ex. "steak, cheese, penne noodles, tomato sauce").</p>
    </div>

    <div class="input-section">
      <div class="input-container">
        <input type="text" v-model="ingredients" placeholder="Enter ingredients here..." />
        <button id="submit-btn" @click="generateRecipes">Submit</button>
      </div>

      <!-- Dietary Preferences Checkboxes in a Row -->
      <div class="checkboxes">
        <div class="checkbox-item" v-for="(option, index) in options" :key="index">
          <input type="checkbox" v-model="option.checked" :id="'option' + index">
          <label :for="'option' + index">{{ option.label }}</label>
        </div>
      </div>
    </div>

    <!-- Recipe Output Box -->
    <div class="output-box" v-if="recipes.length > 0">
      <h2>Recipe Suggestions:</h2>
      <div class="recipe-box" v-for="(recipe, index) in recipes" :key="index">
        <p>{{ recipe }}</p>
      </div>
      <div class="suggestion-container">
        <input type="text" v-model="suggestion" placeholder="Add a suggestion to modify the recipe..." />
        <button class = "modify-recipe-btn" @click="modifyRecipe">Modify Recipe</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'AutoChef',
  data() {
    return {
      ingredients: '',
      options: [
        { label: 'Vegetarian', checked: false },
        { label: 'High Protein', checked: false },
        { label: 'Low Protein', checked: false },
        { label: 'High Carb', checked: false },
        { label: 'Low Carb', checked: false }
      ],
      recipes: [],
      suggestion: '',
    };
  },
  methods: {
    async generateRecipes() {
      const dietaryPreferences = this.options.filter(option => option.checked).map(option => option.label).join(', ');

      try {
        const response = await axios.post('http://localhost:5000/generate_recipe', {
          ingredients: this.ingredients,
          preferences: dietaryPreferences
        });
        this.recipes = response.data.recipe ? [response.data.recipe] : ['No recipes found.'];
      } catch (error) {
        console.error(error);
        this.recipes = ['Error generating recipes.'];
      }
    },
    async modifyRecipe() {
  if (this.suggestion.trim() && this.recipes.length > 0) {
    // Pass the first recipe (or any desired recipe) along with the suggestion for modification
    const recipeToModify = this.recipes[0];  // Assuming you are modifying the first recipe

    try {
      const response = await axios.post('http://localhost:5000/modify_recipe', {
        recipe: recipeToModify,
        suggestion: this.suggestion
      });

      // Update the recipe with the modified result
      this.recipes = response.data.modifiedRecipe ? [response.data.modifiedRecipe] : ['No modified recipe found.'];
      this.suggestion = '';  // Clear the suggestion box after submission
    } catch (error) {
      console.error(error);
    }
  }
}
  }
};
</script>

<style>
html, body {
  height: 100%;
  margin: 0;
  padding: 0;
  font-family: 'Roboto', sans-serif;
}

body {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  height: 100vh;
  margin: 0;
  background-color: #fff7e1;
  overflow-x: hidden;
}

.container {
  width: 85vw;
  max-width: 1200px;
  background-color: #fff;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  padding: 40px;
  justify-content: flex-start;
  box-sizing: border-box;
}

.header {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 30px;
  margin-bottom: 40px;
  background: linear-gradient(45deg, #FFB800, #FF6F00);
  border-radius: 50px;
  padding: 20px 40px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  transform: scale(1.05);
}

.header h1 {
  font-family: 'Poppins', sans-serif;
  font-size: 3.5em;
  font-weight: 700;
  color: #fff;
  text-shadow: 4px 4px 12px rgba(0, 0, 0, 0.2);
  margin: 0;
  letter-spacing: 2px;
}

.logo {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  object-fit: cover;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease-in-out;
}

.logo:hover {
  transform: rotate(360deg);
}

.sample-text {
  font-family: 'Roboto', sans-serif;
  font-size: 1.25em;
  color: #333;
  margin-bottom: 40px;
  text-align: center;
  line-height: 1.6;
  letter-spacing: 0.5px;
}

.input-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 40px;
}

.input-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
}

input[type="text"] {
  width: 70%;
  padding: 12px 16px;
  font-size: 1.1em;
  font-weight: 500;
  border-radius: 30px;
  border: 2px solid #ddd;
  transition: border-color 0.3s, box-shadow 0.3s ease-in-out;
}

input[type="text"]:focus {
  border-color: #FFB800;
  box-shadow: 0 0 8px rgba(255, 184, 0, 0.6);
  outline: none;
}

#submit-btn {
  padding: 12px 25px;
  background-color: #FF6F00;
  color: white;
  font-size: 1.1em;
  font-weight: 600;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s ease-in-out;
}

#submit-btn:hover {
  background-color: #E65100;
  transform: scale(1.05);
}

button.modify-recipe-btn {
  padding: 12px 25px;
  background-color: #FF6F00;
  color: white;
  font-size: 1.1em;
  font-weight: 600;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s ease-in-out;
}

button.modify-recipe-btn:hover {
  background-color: #E65100;
  transform: scale(1.05);
}

.checkbox-item {
  display: flex;
  align-items: center;
  font-size: 1.1em;
  color: #333;
  margin-bottom: 12px;
}

.checkbox-item input {
  margin-right: 12px;
  accent-color: #FF6F00;
  width: 20px;
  height: 20px;
  transition: transform 0.2s ease-in-out;
}

.checkbox-item input:hover {
  transform: scale(1.2);
}

.checkbox-item input:checked {
  background-color: #FFB800;
  border-color: #FF6F00;
}

/* Flexbox for checkboxes in a row */
.checkboxes {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
  margin-top: 20px;
}

/* Scrollable output box */
.output-box {
  margin-top: 40px;
  padding: 20px;
  background-color: #FFFAE1;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-height: 300px;
  overflow-y: auto;
}

.output-box h2 {
  font-size: 1.5em;
  font-weight: 600;
  color: #FF6F00;
}

.recipe-box p {
  font-size: 1.1em;
  color: #333;
  margin: 10px 0;
}

.recipe-box {
  white-space: pre-wrap; /* Preserve spaces and line breaks */
  word-wrap: break-word; /* Wrap long words */
  max-height: 400px; /* Limit box height */
  overflow-y: auto; /* Add scroll if needed */
  padding: 15px;
  background-color: #f9f9f9; /* Light gray for readability */
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  line-height: 1.6; /* Space between lines */
}

.recipe-box > div {
  margin-bottom: 10px; /* Spacing between each line */
}
</style>
