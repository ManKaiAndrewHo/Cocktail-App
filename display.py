def show_recipe(drink):
    print(f"\n---{drink['name']}---")
    print(f"Colors: {', '.join(drink['colors'])}")
    print("Ingredients: ")
    for ing in drink['ingredients']:
        print(f"- {ing['amount']} {ing['item']}")
    print(f"Instructions: {drink['instructions']}")
    print(f"Tags: {', '.join(drink['tags'])}")
    print()