import json
from dataclasses import dataclass
from exceptions import RecipeDataError


class Recipe:
    """A single recipe from the recipe database."""

    def __init__(self, name, required, time, calories_per_person):
        self.name = name
        self.required = required
        self.time = time
        self.calories_per_person = calories_per_person

    @classmethod
    def from_dict(cls, data):
        try:
            return cls(
                name=data["name"],
                required=data["required"],
                time=data["time"],
                calories_per_person=data["calories_per_person"],
            )
        except (KeyError, TypeError) as e:
            raise RecipeDataError(f"Invalid recipe format in data: missing or bad field {e}") from e

    def has_ingredients(self, available):
        return all(item in available for item in self.required)

    def fits_time(self, max_time):
        return self.time <= max_time

    def total_calories(self, people):
        return self.calories_per_person * people


@dataclass
class Recommendation:
    """A recipe suggestion calculated for a given number of people."""

    name: str
    time: int
    calories: int
    people: int


class RecipeRepository:
    """Loads recipes from a JSON file."""

    def __init__(self, path="data/recipes.json"):
        self.path = path

    def load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    raise RecipeDataError(f"Recipe file is empty: {self.path}")
                data = json.loads(content)
        except FileNotFoundError as e:
            raise RecipeDataError(f"Recipe file not found: {self.path}") from e
        except json.JSONDecodeError as e:
            raise RecipeDataError(f"Recipe file is corrupted: {e}") from e
        except OSError as e:
            raise RecipeDataError(f"Could not read recipe file: {e}") from e

        if not isinstance(data, list):
            raise RecipeDataError("Recipe file must contain a list of recipes.")

        return [Recipe.from_dict(item) for item in data]


class Recommender:
    """Recommends recipes based on ingredients, time and number of people."""

    def __init__(self, repository=None):
        self.repository = repository or RecipeRepository()

    def recommend(self, ingredients, max_time, people):
        results = []

        for recipe in self.repository.load():
            if recipe.has_ingredients(ingredients) and recipe.fits_time(max_time):
                results.append(
                    Recommendation(
                        name=recipe.name,
                        time=recipe.time,
                        calories=recipe.total_calories(people),
                        people=people,
                    )
                )

        return results