from storage import save_user_data
from display import show_recipe

def list_drinks(cocktails):
    if not cocktails:
        print("No cocktails in recipe.\n")
        return
    
    print("\nHow would you like to view cocktails?")
    print("1. Basis (as stored)")
    print("2. Alphabetical (A → Z)")
    choice = input("Enter choice (1 or 2):")
    
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
    
def add_cocktail(user_data):
    cocktails = user_data["recipes"]

    name = input("Name of cocktail: ")
    colors = input("Enter colors (comma separated): ").split(",")
    instructions = input("Instructions to make the cocktail: ")
    
    ingredients = []
    while True:
        item = input("Enter ingredient name (or 'done' when finished): ")
        if item.lower() == "done":
            break
        amount = input(f"Amount of {item}:")
        ingredients.append({"item": item, "amount": amount})
        
    tags = input("Enter tags (comma separated): ").split(",")
    
    new_cocktail = {
        "name": name,
        "ingredients": ingredients,
        "instructions": instructions,
        "colors": [c.strip() for c in colors],
        "tags": [t.strip() for t in tags],
    }
    
    cocktails.append(new_cocktail)
    save_user_data(user_data)
    print(f"\n{name} has been added successfully!\n")
    
def delete_cocktail(user_data):
    cocktails = user_data["recipes"]
    
    if not cocktails:
        print("No cocktails to delete.\n")
        return
    
    print("\n--- Delete a Cocktail ---")
    for i, drink in enumerate(cocktails, start=1):
        print(f"{i}. {drink['name']}")
    
    try:
        choice = int(input("Enter the number of the cocktail to delete: "))
        if 1 <= choice <= len(cocktails):
            confirm = input("Are you sure? (y/n): ")
            if confirm.lower() == "y":
                removed = cocktails.pop(choice - 1)
                save_user_data(user_data)
                print(f"\n'{removed['name']}' has been deleted.\n")
            else:
                print("Deletion cancelled.\n")
        else:
            print("Invalid number. Please try again.\n")
    except ValueError:
        print("Invalid input. Please enter a number.\n")
        
def update_cocktail(user_data):
    cocktails = user_data["recipes"]
    
    if not cocktails:
        print("No cocktails to update.\n")
        return
    
    print("\n--- Update a Cocktail ---")
    for i, drink in enumerate(cocktails, start=1):
        print(f"{i}. {drink['name']}")
    
    try:
        choice = int(input("\nEnter the number of the cocktail to edit: "))
        if not (1 <= choice <= len(cocktails)):
            print("Invalid number. Please try again.\n")
            return
        
        drink = cocktails[(choice - 1)]
        print(f"\nUpdateing '{drink['name']}")
        print("1. Name")
        print("2. Ingredients")
        print("3. Colors")
        print("4. Tags")
        print("5. Instructions")
        print("6. Cancel")
        
        options = input("Option number: ")
        
        if options == "1":
            drink["name"] = input("Enter new name: ")
            
        elif options == "2":
            print("Current ingredients:")
            for ing in drink["ingredients"]:
                print(f" - {ing['amount']} {ing['item']}")
            drink["ingredients"] = []
            print("Enter new ingredients (type 'done' when finished):")
            while True:
                item = input(f"New item:")
                if item.lower() == "done":
                    break
                amount = input(f"Amount of {item}:")
                drink["ingredients"].append({"item": item, "amount": amount})
        
        elif options == "3":
            print(f"Current colors: {', '.join(drink.get('colors', []))}")
            new_colors = input("Enter new colors (comma separated): ")
            drink["colors"] = [c.strip() for c in new_colors.split(",")]
            
        elif options == "4":
            print(f"Current tags: {', '.join(drink.get('tags', []))}")
            new_tags = input("Enter new tags (comma separated): ")
            drink["tags"] = [t.strip() for t in new_tags.split(",")]
            
        elif options == "5":
            print(f"Current instructions: {drink['instructions']}")
            drink["tags"] = input("Enter new instructions: ")
            
        elif options == "6":
            print("Update cancelled.\n")
            return
            
        else:
            print("Invalid option. Update cancelled.\n")
            return
        
        save_user_data(user_data)
        print(f"\n'{drink['name']}' has been updated successfully!\n")
        
    except ValueError:
        print("Invalid input. Please enter a number.\n")
        