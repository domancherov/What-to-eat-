from foods import IngredientDatabase
from recommender import Recommender
from tracker import MealTracker
from exceptions import InvalidInputError, RecipeDataError


class App:
    """Command line interface that ties the whole project together."""

    def __init__(self):
        self.ingredients_db = IngredientDatabase()
        self.recommender = Recommender()
        self.tracker = MealTracker()

    def run(self):
        self._print_header()

        while True:
            self._print_menu()
            choice = input("\nChoice: ").strip()

            if choice == "1":
                self._handle_recommendation()
            elif choice == "2":
                self.tracker.show_today()
            elif choice == "3":
                self.tracker.show_weekly()
            elif choice == "4":
                print("Enjoy your meal! 🍴")
                break
            else:
                print("❌ Invalid choice. Please enter 1-4.")

    # ---------- display helpers ----------

    @staticmethod
    def _print_header():
        print("=" * 40)
        print("     🍽️  WHAT SHOULD I EAT? 🍽️")
        print("=" * 40)

    @staticmethod
    def _print_menu():
        print("\n1. Get Meal Recommendation")
        print("2. Today's Calories")
        print("3. Weekly Summary")
        print("4. Exit")

    def _print_ingredients(self):
        print("\n🧺 Available ingredients:")
        for i, (name, kcal) in enumerate(self.ingredients_db.items(), 1):
            print(f"  {i}. {name} ({kcal} kcal)")

    # ---------- menu actions ----------

    def _handle_recommendation(self):
        self._print_ingredients()

        try:
            raw = input("\nIngredients you have (comma separated): ").strip()
            if not raw:
                raise InvalidInputError("Please enter at least one ingredient.")

            ingredients = [i.strip().lower() for i in raw.split(",") if i.strip()]
            if not ingredients:
                raise InvalidInputError("Please enter valid ingredient names.")

            try:
                max_time = int(input("How many minutes do you have? "))
                people = int(input("How many people? "))
            except ValueError as e:
                raise InvalidInputError("Time and number of people must be valid numbers.") from e

            if max_time <= 0 or people <= 0:
                raise InvalidInputError("Time and number of people must be greater than zero.")

            results = self.recommender.recommend(ingredients, max_time, people)

        except (InvalidInputError, RecipeDataError) as e:
            print(f"\n❌ {e}")
            return

        if not results:
            print("\n❌ No matching recipes found.")
            return

        print(f"\n✅ {len(results)} recipe(s) found:\n")
        for i, r in enumerate(results, 1):
            print(f"  {i}. {r.name} — {r.time} min — {r.calories} kcal ({people} people)")

        self._ask_to_log(results)

    def _ask_to_log(self, results):
        log_choice = input("\nWant to log a meal? (enter number / no): ").strip()
        if log_choice.isdigit():
            idx = int(log_choice) - 1
            if 0 <= idx < len(results):
                selected = results[idx]
                self.tracker.log_meal(selected.name, selected.calories)
            else:
                print("❌ Invalid selection.")
        elif log_choice.lower() not in ("no", "n", ""):
            print("❌ Invalid input. Meal not logged.")


def main():
    App().run()


if __name__ == "__main__":
    main()