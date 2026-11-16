import json
import os
from datetime import date


class MealTracker:
    """Logs meals to a JSON file and shows daily / weekly calorie summaries."""

    def __init__(self, log_file="data/log.json"):
        self.log_file = log_file

    # ---------- file handling ----------

    def _load(self):
        if not os.path.exists(self.log_file):
            return {}
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return {}
                data = json.loads(content)
                if not isinstance(data, dict):
                    print("⚠️  Log file format was invalid. Starting fresh.")
                    return {}
                return data
        except json.JSONDecodeError:
            print("⚠️  Log file was corrupted. Starting fresh.")
            return {}
        except OSError as e:
            print(f"⚠️  Could not read log file: {e}")
            return {}

    def _save(self, log):
        try:
            directory = os.path.dirname(self.log_file)
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump(log, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Could not save log: {e}")

    # ---------- public API ----------

    def log_meal(self, meal_name, calories):
        log = self._load()
        today = str(date.today())

        if today not in log:
            log[today] = {"meals": [], "total_calories": 0}

        log[today]["meals"].append({"meal": meal_name, "calories": calories})
        log[today]["total_calories"] += calories
        self._save(log)
        print(f"✅ {meal_name} logged. Today's total: {log[today]['total_calories']} kcal")

    def show_today(self):
        try:
            log = self._load()
            today = str(date.today())

            if today not in log or not log[today].get("meals"):
                print("Nothing logged today.")
                return

            print(f"\n📅 {today} - Daily Summary")
            print("-" * 30)
            for entry in log[today]["meals"]:
                print(f"  🍽️  {entry['meal']} — {entry['calories']} kcal")
            print(f"  🔥 Total: {log[today]['total_calories']} kcal")

        except Exception as e:
            print(f"❌ Could not load today's summary: {e}")

    def show_weekly(self):
        try:
            log = self._load()
            print("\n📊 Weekly Calorie Summary")
            print("-" * 30)
            if not log:
                print("No records yet.")
                return
            for day, data in sorted(log.items()):
                print(f"  {day}: {data.get('total_calories', 0)} kcal")

        except Exception as e:
            print(f"❌ Could not load weekly summary: {e}")