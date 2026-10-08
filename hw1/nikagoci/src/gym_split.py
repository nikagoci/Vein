"""GymSplit - command-line gym workout split generator.

This implementation follows the GymSplit specification:
- Goal: muscle gain, fat loss, or general fitness
- Experience: beginner or intermediate
- Training days: 3, 4, or 5
- Equipment: full gym or limited equipment
- Invalid input is rejected and requested again
- Every training day contains at least 4 exercises
- Limited-equipment plans avoid gym machines, cables, and barbells
"""

GOALS = {
    "1": "Muscle Gain",
    "2": "Fat Loss",
    "3": "General Fitness",
}

EXPERIENCE_LEVELS = {
    "1": "Beginner",
    "2": "Intermediate",
}

EQUIPMENT_OPTIONS = {
    "1": "Full Gym",
    "2": "Limited Equipment",
}

# Each exercise has a name, equipment type, and rep range.
# "limited" means it can be performed with dumbbells, bands, or bodyweight.
EXERCISES = {
    "push": [
        ("Bench Press", "gym", "3 x 6-10"),
        ("Incline Dumbbell Press", "limited", "3 x 8-12"),
        ("Dumbbell Shoulder Press", "limited", "3 x 8-12"),
        ("Cable Triceps Pushdown", "gym", "2 x 10-15"),
        ("Dumbbell Lateral Raise", "limited", "2 x 12-15"),
        ("Push-Ups", "limited", "3 x 10-15"),
    ],
    "pull": [
        ("Lat Pulldown", "gym", "3 x 8-12"),
        ("Cable Row", "gym", "3 x 8-12"),
        ("One-Arm Dumbbell Row", "limited", "3 x 8-12"),
        ("Dumbbell Curl", "limited", "2 x 10-15"),
        ("Pull-Ups", "limited", "3 x 6-12"),
        ("Band Row", "limited", "3 x 10-15"),
    ],
    "legs": [
        ("Leg Press", "gym", "3 x 8-12"),
        ("Barbell Squat", "gym", "3 x 6-10"),
        ("Goblet Squat", "limited", "3 x 8-12"),
        ("Dumbbell Romanian Deadlift", "limited", "3 x 8-12"),
        ("Dumbbell Lunges", "limited", "3 x 10-12"),
        ("Bodyweight Squat", "limited", "3 x 12-15"),
        ("Leg Extension", "gym", "2 x 10-15"),
        ("Standing Calf Raise", "limited", "3 x 12-20"),
    ],
}

# Templates determine the split for 3, 4, and 5 training days.
SPLITS = {
    3: ["Full Body A", "Full Body B", "Full Body C"],
    4: ["Upper Body", "Lower Body", "Upper Body B", "Lower Body B"],
    5: ["Push", "Pull", "Legs", "Upper Body", "Lower Body"],
}


def get_choice(prompt, options):
    """Ask until the user enters one of the allowed numeric choices."""
    while True:
        print(prompt)
        for key, value in options.items():
            print(f"{key}. {value}")

        choice = input("Choose an option: ").strip()

        if choice in options:
            return choice

        print("Invalid input. Please choose one of the listed options.\n")


def get_training_days():
    """Ask until the user selects 3, 4, or 5 training days."""
    while True:
        value = input("How many days per week do you want to train (3, 4, or 5)? ").strip()

        if value in {"3", "4", "5"}:
            return int(value)

        print("Invalid input. Please enter 3, 4, or 5.\n")


def available_exercises(category, equipment, experience):
    """Return exercises compatible with the selected equipment."""
    exercises = EXERCISES[category]

    if equipment == "Limited Equipment":
        exercises = [exercise for exercise in exercises if exercise[1] == "limited"]

    # Beginners receive a simpler selection.
    if experience == "Beginner":
        exercises = exercises[:4]

    return exercises


def choose_exercises(categories, equipment, experience):
    """Build at least four exercises for a workout."""
    selected = []

    for category in categories:
        candidates = available_exercises(category, equipment, experience)

        for exercise in candidates:
            if exercise not in selected:
                selected.append(exercise)

            if len(selected) >= 4:
                return selected

    return selected


def categories_for_day(day_name):
    """Map a workout name to exercise categories."""
    if day_name == "Upper Body":
        return ["push", "pull"]
    if day_name == "Upper Body B":
        return ["pull", "push"]
    if day_name == "Lower Body":
        return ["legs"]
    if day_name == "Lower Body B":
        return ["legs"]
    if day_name == "Push":
        return ["push"]
    if day_name == "Pull":
        return ["pull"]
    if day_name == "Legs":
        return ["legs"]
    if day_name == "Full Body A":
        return ["push", "legs", "pull"]
    if day_name == "Full Body B":
        return ["pull", "legs", "push"]
    if day_name == "Full Body C":
        return ["legs", "push", "pull"]

    return ["push", "pull", "legs"]


def generate_plan(days, equipment, experience):
    """Generate a workout plan matching the requested number of days."""
    plan = []

    for day_number, day_name in enumerate(SPLITS[days], start=1):
        categories = categories_for_day(day_name)
        exercises = choose_exercises(categories, equipment, experience)

        plan.append(
            {
                "day": day_number,
                "name": day_name,
                "exercises": exercises,
            }
        )

    return plan


def print_plan(goal, experience, days, equipment, plan):
    """Display the generated workout plan."""
    print("\n" + "=" * 45)
    print("GYMSPLIT WORKOUT PLAN")
    print("=" * 45)
    print(f"Goal: {goal}")
    print(f"Experience: {experience}")
    print(f"Training days: {days}")
    print(f"Equipment: {equipment}")

    for workout in plan:
        print(f"\nDAY {workout['day']} — {workout['name']}")
        print("-" * 35)

        for number, (name, _, reps) in enumerate(workout["exercises"], start=1):
            print(f"{number}. {name} — {reps}")

    print("\nPlan generated successfully.")


def main():
    print("=" * 45)
    print("Welcome to GymSplit!")
    print("Generate a simple weekly gym workout split.")
    print("=" * 45 + "\n")

    goal_choice = get_choice("What is your goal?", GOALS)
    experience_choice = get_choice(
        "\nWhat is your experience level?",
        EXPERIENCE_LEVELS,
    )
    days = get_training_days()
    equipment_choice = get_choice(
        "\nWhat equipment do you have?",
        EQUIPMENT_OPTIONS,
    )

    goal = GOALS[goal_choice]
    experience = EXPERIENCE_LEVELS[experience_choice]
    equipment = EQUIPMENT_OPTIONS[equipment_choice]

    plan = generate_plan(days, equipment, experience)

    print_plan(goal, experience, days, equipment, plan)


if __name__ == "__main__":
    main()
