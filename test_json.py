import json
from storage import load_user_data, save_user_data

user_data = load_user_data()

cocktails = user_data["recipes"]
favorites = user_data["favorites"]

save_user_data(user_data)

def search_names(search_item):
    search_item = search_item.strip().lower()
    matches = [drink for drink in cocktails if search_item in drink["name"].lower()]

    if matches:
        print(f"\nCocktails matching '{search_item}':")
        for drink in matches:
            show_recipe(drink)
    else:
        print(f"\nNo cocktails found with '{search_item}'.\n")


def search_ingredients(search_item):
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


def search_colors(search_item):
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


def search_tags(search_item):
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


def show_recipe(drink):
    print(f"\n---{drink['name']}---")
    print(f"Colors: {', '.join(drink['colors'])}")
    print("Ingredients: ")
    for ing in drink['ingredients']:
        print(f"- {ing['amount']} {ing['item']}")
    print(f"Instructions: {drink['instructions']}")
    print(f"Tags: {', '.join(drink['tags'])}")
    print()

def add_cocktail():
    name = input("Name of the cocktail: ")
    colors = input("Enter colors (separate by comma): ").split(",")
    instructions = input("Instructions to make the cocktail: ")

    ingredients = []

    while True:
        item = input("Enter ingredient name (or 'done' when finish): ")
        if item.lower() == "done":
            break
        amount = input(f"Amount for {item}: ")
        ingredients.append({"item": item, "amount": amount})

    tags = input("Enter tags (separate by comma): ").split(",")

    new_cocktail = {
        "name": name,
        "ingredients": ingredients,
        "instructions": instructions,
        "colors": [color.strip() for color in colors],
        "tags": [tag.strip() for tag in tags]
    }

    cocktails.append(new_cocktail)

    with open("recipes.json", "w") as f:
        json.dump(cocktails, f, indent=4)

    print(f"\n{name} has been added successfully! \n")

def delete_cocktail():
    if not cocktails:
        print("No cocktail in recipe.\n")
        return

    for i, drink in enumerate(cocktails, start=1):
        print(f"{i}: {drink['name']}")

    try:
        choice = int(input("\nEnter the number of the cocktail to delete: "))
        if 1 <= choice <= len(cocktails):
            confirm = input("Are you sure? (y/n): ")
            if confirm.lower() == "y":
                removed = cocktails.pop(choice - 1)
                with open("recipes.json", "w") as f:
                    json.dump(cocktails, f, indent=4)
                print(f"'{removed['name']}' has been deleted.\n")
            else:
                print("Not removed.\n")
        else:
            print("Invalid number. Please try again.\n")
    except ValueError:
        print("Invalid input. Please enter a number.\n")
        
def show_favorites():
    if not favorites:
        print("No favorites added yet.\n")
        return

    print("\n--- Favorite Cocktails ---")
    for i, drink in enumerate(favorites, start=1):
        print(f"{i}. {drink['name']}")
    print()
    
def remove_favorite():
    if not favorites:
        print("No favorites to remove.\n")
        return

    for i, drink in enumerate(favorites, start=1):
        print(f"{i}: {drink['name']}")

    try:
        choice = int(input("\nEnter the number of the favorite cocktail to remove: "))
        if 1 <= choice <= len(favorites):
            removed = favorites.pop(choice - 1)
            save_favorites()
            print(f"'{removed['name']}' has been removed from favorites.\n")
        else:
            print("Invalid number. Please try again.\n")
    except ValueError:
        print("Invalid input. Please enter a number.\n")

def update_cocktail():
    if not cocktails:
        print("No cocktails in recipe.\n")
        return

    # Show cocktails list
    for i, drink in enumerate(cocktails, start=1):
        print(f"{i}: {drink['name']}")

    try:
        choice = int(input("\nEnter the number of the cocktail to edit: "))
        if 1 <= choice <= len(cocktails):
            drink = cocktails[choice - 1]

            print(f"\nUpdating {drink['name']}")
            print("1. Name")
            print("2. Ingredients")
            print("3. Colors")
            print("4. Tags")
            print("5. Instructions")
            print("6. Cancel")

            option = input("Option number: ")
            if option == "1":  # Name
                drink['name'] = input("Enter new name: ")
            elif option == "2":  # Ingredients
                print("Current Ingredients: ")
                for ing in drink['ingredients']:
                    print(f"- {ing['amount']} {ing['item']}")
                drink['ingredients'] = []
                print("Enter new ingredients (type 'done' when finished):")
                while True:
                    item = input("New item: ")
                    if item.lower() == "done":
                        break
                    amount = input(f"Amount for {item}: ")
                    drink['ingredients'].append({"item": item, "amount": amount})
            elif option == "3":  # Colors
                print(f"Current colors: {', '.join(drink.get('colors', []))}")
                new_colors = input("Enter new colors (comma separated): ")
                drink['colors'] = [color.strip() for color in new_colors.split(",")]
            elif option == "4":  # Tags
                print(f"Current tags: {', '.join(drink['tags'])}")
                new_tags = input("Enter new tags (comma separated): ")
                drink['tags'] = [tag.strip() for tag in new_tags.split(",")]
            elif option == "5":  # Instructions
                print(f"Current instructions: {drink['instructions']}")
                drink['instructions'] = input("Enter new instructions: ")
            elif option == "6":  # Cancel
                print("Update cancelled.")
                return
            else:
                print("Invalid option.")
                return
            # Save changes back to JSON
            with open("recipes.json", "w") as f:
                json.dump(cocktails, f, indent=4)

            print(f"\n{drink['name']} has been updated successfully!\n")
        else:
            print("Invalid number. Please try again.\n")
    except ValueError:
        print("Invalid input. Please enter a number.\n")

def save_favorites():
    with open("favorites.json", "w") as f:
        json.dump(favorites, f, indent=4)

def add_favorite():
    name = input("Enter the name of the cocktail to add to favorites: ")
    for drink in cocktails:
        if drink['name'].lower() == name.lower():
            if drink not in favorites:
                favorites.append(drink)
                save_favorites()
                print(f"{name} has been added to favorites.\n")
            else:
                print(f"{name} is already in favorites.\n")
            return
    print(f"{name} not found in recipes.\n")

def list_of_drink():
    if not cocktails:
        print("No cocktails in recipe.\n")
        return

    print("\nHow would you like to view cocktails?")
    print("1. Basic (as stored)")
    print("2. Alphabetical (A → Z)")
    choice = input("Enter choice (1 or 2): ")

    if choice == "1":
        drinks_to_show = cocktails
    elif choice == "2":
        drinks_to_show = sorted(cocktails, key=lambda d: d["name"].lower())
    else:
        print("Invalid choice. Showing basic order.\n")
        drinks_to_show = cocktails

    print("\n--- All Cocktails ---")
    for i, drink in enumerate(drinks_to_show, start=1):
        print(f"{i}. {drink['name']}")
    print()

while True:
    menu = "Search: \n1. Name \n2. Ingredient \n3. Colors \n4. Tag \n5. Add \n6. Delete \n7. List the drinks \n8. Add to Favorites \n9. Show Favorites \n10. Remove from Favorites \n11. Quit \n"
    print(menu)
    choice = input("Enter your search option: ")

    if choice == "1":
        name = input("Search with the cocktail's name: ")
        search_names(name)
    elif choice == "2":
        ingredient = input("Cocktail with ingredient you like: ")
        search_ingredients(ingredient)
    elif choice == "3":
        colors = input("Cocktail with the colors you like: ")
        search_colors(colors)
    elif choice == "4":
        tag = input("Cocktail with the tag you like: ")
        search_tags(tag)
    elif choice == "5":
        add_cocktail()
    elif choice == "6":
        delete_cocktail()
    elif choice == "7":
        list_of_drink()
    elif choice == "8":
        add_favorite()
    elif choice == "9":
        show_favorites()
    elif choice == "10":
        remove_favorite()
    elif choice == "11":
        print("Goodbye! 🍸")
        break
    else:
        print("Invalid option, please try again. \n")