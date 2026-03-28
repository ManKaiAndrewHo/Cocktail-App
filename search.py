from display import show_recipe

def search_names(cocktails, search_item):
    search_item = search_item.strip().lower()
    matches = [drink for drink in cocktails if search_item in drink["name"].lower()]

    if matches:
        print(f"\nCocktails matching '{search_item}':")
        for drink in matches:
            show_recipe(drink)
    else:
        print(f"\nNo cocktails found with '{search_item}'.\n")


def search_ingredients(cocktails, search_item):
    search_item = search_item.strip().lower()
    matches = []

    for drink in cocktails:
        for ingredient in drink["ingredients"]:
            if search_item in ingredient["item"].lower():
                matches.append(drink)
                break  # No need to check other ingredients in this drink

    if matches:
        print(f"\nCocktails containing ingredient '{search_item}':")
        for drink in matches:
            show_recipe(drink)
    else:
        print(f"\nNo cocktails found containing '{search_item}'.\n")


def search_colors(cocktails, search_item):
    search_item = search_item.strip().lower()
    matches = []

    for drink in cocktails:
        for color in drink.get("colors", []):
            if search_item in color.lower():
                matches.append(drink)
                break

    if matches:
        print(f"\nCocktails with color '{search_item}':")
        for drink in matches:
            show_recipe(drink)
    else:
        print(f"\nNo cocktails found with color '{search_item}'.\n")


def search_tags(cocktails, search_item):
    search_item = search_item.strip().lower()
    matches = []

    for drink in cocktails:
        for tag in drink.get("tags", []):
            if search_item in tag.lower():
                matches.append(drink)
                break

    if matches:
        print(f"\nCocktails with tag '{search_item}':")
        for drink in matches:
            show_recipe(drink)
    else:
        print(f"\nNo cocktails found with tag '{search_item}'.\n")
