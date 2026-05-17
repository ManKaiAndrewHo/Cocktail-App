def show_recipe(drink):
    print(f"\n---{drink['name']}---")
    colors = drink.get("colors") or drink.get("color", [])
    print(f"Colors: {', '.join(colors)}")
    print("Ingredients: ")
    for ing in drink['ingredients']:
        print(f"- {ing['amount']} {ing['item']}")
    print(f"Instructions: {drink['instructions']}")
    print(f"Tags: {', '.join(drink['tags'])}")
    print()