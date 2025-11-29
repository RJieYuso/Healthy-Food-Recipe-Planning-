# Personalized Nutritional Meal Planning System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📖 About The Project

In today's fast-paced society, many people struggle to plan healthy meals, often leading to food waste and a reliance on expensive food delivery services. Existing recipe applications are typically too general and fail to connect a user's available ingredients with their personal health goals. This project, the **Personalized Nutritional Meal Planning System**, aims to solve this problem by creating a smart web application. The system will provide tailored recipe recommendations based on a user's dietary restrictions, health objectives (like weight loss or muscle gain), and the ingredients they already have in their kitchen, empowering users to make healthier, more economical, and sustainable food choices.

---

## 🚀 Modules Under Development
1. User Ingredient & Nutrition Module

  - Create User Profile API
  - Implement health condition validation
  - Setup Cosmos DB (Microsoft Azure) Users collection

  - Develop nutrition planning logic
  - Implement food expiry tracking
  - Create notification system for expiry

2. Ingredients Condition Visualization Module

  - Research AI models for food prediction
  - Setup Azure Machine Learning workspace
  - Create ingredient condition prediction API

  - Train initial AI model
  - Develop visualization data endpoints
  - Implement condition scoring system

3. Application UI Module

  - Setup React Native project
  - Create basic navigation structure
  - Develop user input forms

  - Implement recipe display components
  - Create ingredient management UI
  - Develop settings and profile screens

4. Recipe Recommendation AI Module

  - Setup recommendation algorithm
  - Create recipe database structure
  - Develop rating system API

  - Implement collaborative filtering
  - Train recommendation model
  - Create recommendation endpoints

---

## 👥 Our Team

A big thanks to our dedicated team (Group 26) for their contributions to this project.

*   **HO RONG JIE** - Module 4
*   **FATIN NURQASDINA BINTI RASHID** - Module 3
*   **MUHAMMAD AKMAL BAIHAQI BIN KHAIRUL ANAM MAK** - Module 2
*   **DHESEETHRA A/P BALAKRISHNAN** - Module 1

# API Documentation

This document describes the available API endpoints.

## 1. **User Profile API**

### Endpoint: `/api/users/{id}`
- **Method**: `POST`
- **Request**:
  - `userId`: (string) User's ID.
  - `healthConditions`: (array) List of health conditions (e.g., diabetes, hypertension, allergies).
  - `dietaryRestrictions`: (array) List of dietary restrictions (e.g., vegetarian, vegan, gluten-free).
  - `age`: (number) User's age.
  - `weight`: (number) User's weight.
  - `height`: (number) User's height.

- **Response**:
  - `userId`: (string) User's ID.
  - `healthScore`: (number) A score indicating the user's health (1-100).
  - `nutritionPlan`: 
    - `dailyCalories`: (number) Recommended daily calories intake.
    - `macronutrients`: 
      - `protein`: (string) Protein intake (e.g., "150g").
      - `carbs`: (string) Carbs intake (e.g., "250g").
      - `fats`: (string) Fats intake (e.g., "70g").
    - `recommendedFoods`: (array) List of recommended food items.

---

## 2. **Ingredient Prediction API**

### Endpoint: `/api/predict-condition`
- **Method**: `POST`
- **Request**:
  - `ingredientType`: (string) Type of ingredient (e.g., vegetable, fruit, dairy, meat, grain).
  - `purchaseDate`: (string, ISO date format) Date of purchase.
  - `expiryDate`: (string, optional, ISO date format) Expiry date.
  - `storageCondition`: (string) Storage condition (e.g., fridge, freezer, pantry).

- **Response**:
  - `condition`: (string) Condition of the ingredient (Good, Warning, Critical).
  - `daysUntilExpiry`: (number) Number of days until the ingredient expires.
  - `confidence`: (number) Confidence level of the prediction (0-1).
  - `recommendation`: (string) Suggested action (e.g., "Use within 3 days").

---

## 3. **Recipe Recommendation API**

### Endpoint: `/api/recommend-recipes`
- **Method**: `POST`
- **Request**:
  - `availableIngredients`: (array) List of ingredients you currently have.
  - `userPreferences`: 
    - `cuisine`: (array) List of preferred cuisines (e.g., Italian, Mexican).
    - `cookingTime`: (number) Maximum cooking time in minutes.
    - `difficulty`: (string) Difficulty level (e.g., easy, medium, hard).
  - `healthConstraints`: (array) List of health constraints (e.g., vegetarian, gluten-free).

- **Response**:
  - `recommendations`: (array) List of recommended recipes.
    - `recipeId`: (string) Unique ID of the recipe.
    - `title`: (string) Recipe title.
    - `matchScore`: (number) Match score (0-100).
    - `ingredientsUsed`: (array) List of ingredients used in the recipe.
    - `missingIngredients`: (array) List of missing ingredients.
    - `cookingTime`: (number) Cooking time in minutes.
    - `nutritionScore`: (number) Nutrition score for the recipe.

---

### Summary

- **User Profile API**: Used to create a personalized nutrition plan based on the user's health conditions and dietary needs.
- **Ingredient Prediction API**: Provides information about the condition of an ingredient based on storage and purchase details.
- **Recipe Recommendation API**: Suggests recipes based on available ingredients, preferences, and health constraints.
