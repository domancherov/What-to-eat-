class IngredientDatabase:
    """Holds ingredients and their calorie values."""

    DEFAULT_CALORIES = {
        "egg": 70,
        "tomato": 20,
        "cheese": 80,
        "bread": 75,
        "potato": 90,
        "onion": 15,
        "olive oil": 45,
        "pasta": 130,
        "chicken": 165,
        "lentil": 120,
        "rice": 130,
        "cucumber": 10,
        "parsley": 5,
        "flour": 100,
        "milk": 60,
    }

    def __init__(self, calories=None):
        self._calories = dict(calories or self.DEFAULT_CALORIES)

    def names(self):
        return list(self._calories.keys())

    def get_calories(self, name):
        return self._calories.get(name)

    def items(self):
        return self._calories.items()
