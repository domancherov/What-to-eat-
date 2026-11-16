# 🍽️ What Should I Eat?

A Python CLI app that recommends meals based on ingredients you have at home and tracks your daily calorie intake.

## Features
- 🧺 Lists available ingredients with calorie info
- 🍳 Recommends recipes based on what you have at home
- ⏱️ Filters recipes by time available
- 👥 Supports multiple people
- 🔥 Logs meals and tracks daily calories
- 📊 Shows weekly calorie summary
- ⚠️ Exception handling for corrupted or empty data files

## How to Run
python main.py

what-should-i-eat/
├── main.py          # App class: main menu and user interaction
├── foods.py         # IngredientDatabase class: ingredient and calorie data
├── recommender.py   # Recipe, RecipeRepository, Recommender classes: recommendation logic
├── tracker.py       # MealTracker class: daily calorie logging and summary
├── exceptions.py    # Custom exception classes (WhatShouldIEatError, RecipeDataError, InvalidInputError)
└── data/
    ├── recipes.json # Recipe database (25 recipes)
    └── log.json     # Daily meal log
## Classes
- `App` (main.py): runs the menu loop and connects all the other classes
- `IngredientDatabase` (foods.py): stores ingredients and their calories
- `Recipe` (recommender.py): one recipe, knows if it fits the ingredients and time
- `RecipeRepository` (recommender.py): loads recipes from `data/recipes.json`
- `Recommender` (recommender.py): filters recipes and returns `Recommendation` results
- `MealTracker` (tracker.py): logs meals and prints daily / weekly summaries

## Tech Stack
- Python 3
- JSON (data storage)
- OOP
- Exception Handling
- File I/O

## What I Learned
- Modular Python project structure
- Object-oriented design (classes, encapsulation, separation of responsibilities)
- File I/O with JSON
- Exception handling
- Git & GitHub workflow
