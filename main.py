import json

def load_recipes():
    with open("recipes.json", "r") as f:
        recipes = json.load(f)  # list of dicts
    return recipes

#def search(input):


def main():
    recipes = load_recipes()
    print("Cocktail Recipes:")
    for recipe in recipes:
        print(f"- {recipe['name']}")


if __name__ == "__main__":
    main()
