from storage import save_user_data

def show_favorites(user_data):
    favorites = user_data["favorites"]
    
    if not favorites:
        print("No favorites yet.\n")
        return
    
    print("\n--- Your Favorite Cocktails ---")
    for i, drink in enumerate(favorites, start=1):
        print(f"{i}. {drink['name']}")
    print()
    
def add_favorite(user_data):
    cocktails = user_data["recipes"]
    favorites = user_data["favorites"]
    
    name = input("Enter the name of the cocktail to add to favorites: ").strip()
    
    for drink in cocktails:
        if drink["name"].lower() == name.lower():
            if any(f["name"].lower() == drink["name"].lower() for f in favorites):
                print(f"{drink['name']} is already in your favorites.\n")
            else:
                favorites.append(drink)
                save_user_data(user_data)
                print(f"{drink['name']} has been added to your favorites!\n")
            return
        
    print(f"'{name}' not found in cocktail recipes.\n")
    
def remove_favorite(user_data):
    favorites = user_data["favorites"]
    
    if not favorites:
        print("No favorites to remove.\n")
        return
    
    print("\n--- Remove a Favorite Cocktail ---")
    for i, drink in enumerate(favorites, start=1):
        print(f"{i}. {drink['name']}")
    
    try:
        choice = int(input("Enter the number of the cocktail to remove from favorites: "))
        if 1 <= choice <= len(favorites):
            removed = favorites.pop(choice - 1)
            save_user_data(user_data)
            print(f"{removed['name']} has been removed from your favorites.\n")
        else:
            print("Invalid number. Please try again.\n")
    except ValueError:
        print("Invalid input. Please enter a number.\n")
    