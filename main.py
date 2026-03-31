from storage import load_user_data, save_user_data
from search import search_ingredients, search_colors, search_names, search_tags
from recipe import add_cocktail, delete_cocktail, list_drinks, update_cocktail
from favorite import add_favorite, show_favorites, remove_favorite

MENU = """
============================
🍸 Cocktail Recipe Manager 🍸
============================
1.  Search by Name
2.  Search by Ingredient
3.  Search by Color
4.  Search by Tag
5.  List all drinks
-----------------------------
6.  Add a cocktail
7.  Update a cocktail
8.  Delete a cocktail
-----------------------------
9.  Add to Favorites
10. Show Favorites
11. Remove from Favorites
-----------------------------
12. Quit
"""

def main():
    user_data = load_user_data()
    
    while True:
        print(MENU)
        choice = input("Enter option: ").strip()
        
        cocktails = user_data["recipes"]

        if choice == "1":
            name = input("Search by name: ")
            search_names(cocktails, name)
            
        elif choice == "2":
            ingredient = input("Search by ingredient: ")
            search_ingredients(cocktails, ingredient)
            
        elif choice == "3":
            colors = input("Search by colors: ")
            search_colors(cocktails, colors)
            
        elif choice == "4":
            tag = input("Search by tag: ")
            search_tags(cocktails, tag)
            
        elif choice == "5":
            list_drinks(cocktails)

        elif choice == "6":
            add_cocktail(user_data)
            
        elif choice == "7":
            update_cocktail(user_data)
            
        elif choice == "8":
            delete_cocktail(user_data)

        elif choice == "9":
            add_favorite(user_data)

        elif choice == "10":
            show_favorites(user_data)

        elif choice == "11":
            remove_favorite(user_data)

        elif choice == "12":
            print("Goodbye! 🍸")
            break
        
        else:
            print("Invalid option, please try again. \n")

if __name__ == "__main__":
    main()
