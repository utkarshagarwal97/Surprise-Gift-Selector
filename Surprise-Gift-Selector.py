import random
import csv
import os
from tabulate import tabulate
import matplotlib.pyplot as plt

# File paths
ITEMS_FILE = "items.csv"
SKIPPED_FILE = "skipped_items.csv"
MARKED_FILE = "marked_off_items.csv"

# Function to read a list from a CSV file
def read_csv(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            reader = csv.reader(file)
            return [row for row in reader]
    return []

# Function to write a list to a CSV file
def write_csv(file_name, data):
    with open(file_name, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

# Function to load all data from CSV files
def load_data():
    return read_csv(ITEMS_FILE), read_csv(SKIPPED_FILE), read_csv(MARKED_FILE)

# Function to save all data to CSV files
def save_data(items, skipped_items, marked_off_items):
    write_csv(ITEMS_FILE, items)
    write_csv(SKIPPED_FILE, skipped_items)
    write_csv(MARKED_FILE, marked_off_items)

# Function to display a bar chart of purchased items and their costs
def show_spending_graph(marked_off_items):
    if not marked_off_items:
        print("No purchased items to display.")
        return

    item_names = [item[0] for item in marked_off_items]
    prices = [float(item[2]) if len(item) > 2 and item[2].replace('.', '', 1).isdigit() else 0 for item in marked_off_items]

    plt.bar(item_names, prices)
    plt.title("Spending on Purchased Items")
    plt.xlabel("Item")
    plt.ylabel("Price")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

def main():
    # Load data from CSV files
    items, skipped_items, marked_off_items = load_data()

    print("🎁 Welcome to the Enhanced Surprise Gift Selector! 🎁")
    
    while True:
        # Main menu
        print("\nMain Menu:")
        print("1. Add items to your gift list")
        print("2. Add an already purchased item")
        print("3. Show all available items yet to buy")
        print("4. Surprise me with a random gift")
        print("5. View already purchased items and spending graph")
        print("6. View skipped items")
        print("7. Search or filter items")
        print("8. Edit an item")
        print("9. Exit the program")
        
        choice = input("What would you like to do? (1-9): ").strip()
        
        if choice == "1":
            # Add items
            while True:
                item = input("Enter the name of the gift to add (or type 'no' to stop): ").strip().title()
                if item.lower() == "no":
                    break
                if any(item == existing_item[0] for existing_item in items):
                    print(f"⚠️ '{item}' is already in your list. Try adding something else.")
                    continue
                priority = input(f"Set a priority for '{item}' (0-10, 10 being highest): ").strip()
                if priority.isdigit() and 0 <= int(priority) <= 10:
                    priority = int(priority)
                    items.append([item, priority])
                    print(f"🎁 '{item}' with priority {priority} has been added to your list.")
                else:
                    print("⚠️ Invalid priority. Please enter a number between 0 and 10.")
            save_data(items, skipped_items, marked_off_items)
        
        elif choice == "2":
            # Add an already purchased item
            while True:
                item = input("Enter the name of the purchased item (or type 'no' to stop): ").strip().title()
                if item.lower() == "no":
                    break
                if any(item == existing_item[0] for existing_item in marked_off_items):
                    print(f"⚠️ '{item}' is already marked as purchased.")
                    continue
                priority = input(f"Set a priority for '{item}' (0-10, 10 being highest): ").strip()
                if not (priority.isdigit() and 0 <= int(priority) <= 10):
                    print("⚠️ Invalid priority. Please enter a number between 0 and 10.")
                    continue
                price = input(f"Enter the price for '{item}': ").strip()
                if not price.replace('.', '', 1).isdigit():
                    print("⚠️ Invalid price. Please enter a valid number.")
                    continue
                marked_off_items.append([item, int(priority), price])
                print(f"🛒 '{item}' added to purchased items with priority {priority} and price {price}.")
            save_data(items, skipped_items, marked_off_items)

        elif choice == "3":
            # Show available items
            available_items = [item for item in items if item[0] not in [skipped[0] for skipped in skipped_items] + [marked[0] for marked in marked_off_items]]
            if available_items:
                available_items.sort(key=lambda x: int(x[1]), reverse=True)  # Sort by priority
                print("\nAvailable Items (Sorted by Priority):")
                print(tabulate(available_items, headers=["Gift Name", "Priority"], tablefmt="pretty"))
            else:
                print("⚠️ No items are currently available to buy.")

        elif choice == "4":
            # Surprise me
            available_items = [item for item in items if item[0] not in [marked[0] for marked in marked_off_items]]
            
            if skipped_items:
                print("\n⏩ You have skipped items in your list:")
                print(tabulate(skipped_items, headers=["Gift Name", "Priority"], tablefmt="pretty"))
                include_skipped = input("Would you like to include skipped items in the selection? (yes/no): ").strip().lower()
                if include_skipped == "yes":
                    available_items.extend(skipped_items)
                    skipped_items.clear()
            
            if not available_items:
                print("⚠️ No more items available for selection. Add more or check purchased items.")
                continue
            
            random_item = random.choice(available_items)
            print(f"🎉 Surprise Gift: {random_item[0]} (Priority: {random_item[1]}) 🎉")
            
            while True:
                print("\nOptions:")
                print("1. Skip this gift for now")
                print("2. Mark this gift as purchased")
                print("3. Return to the main menu")
                
                action = input("What would you like to do? (1-3): ")
                
                if action == "1":
                    skipped_items.append(random_item)
                    print(f"'{random_item[0]}' has been skipped for now.")
                    break
                elif action == "2":
                    price = input(f"Enter the price for '{random_item[0]}': ").strip()
                    marked_off_items.append(random_item + [price])
                    print(f"'{random_item[0]}' has been marked as purchased at a price of {price}.")
                    break
                elif action == "3":
                    print("Returning to the main menu.")
                    break
                else:
                    print("Invalid choice. Please choose a valid option.")
            
            save_data(items, skipped_items, marked_off_items)

        elif choice == "5":
            # View purchased items and spending graph
            if marked_off_items:
                print("\n🛒 Purchased Gifts:")
                print(tabulate(marked_off_items, headers=["Gift Name", "Priority", "Price"], tablefmt="pretty"))
                show_spending_graph(marked_off_items)
            else:
                print("No gifts have been marked as purchased yet.")

        elif choice == "6":
            # View skipped items
            if skipped_items:
                print("\n⏩ Skipped Items:")
                print(tabulate(skipped_items, headers=["Gift Name", "Priority"], tablefmt="pretty"))
            else:
                print("No items have been skipped yet.")

        elif choice == "7":
            # Search or filter items
            query = input("Enter the item name or priority to search: ").strip()
            results = [item for item in items if query.lower() in item[0].lower() or (query.isdigit() and int(query) == int(item[1]))]
            if results:
                print("\nSearch Results:")
                print(tabulate(results, headers=["Gift Name", "Priority"], tablefmt="pretty"))
            else:
                print("No matching items found.")

        elif choice == "8":
            # Edit an item
            print("\nEdit an Item:")
            print(tabulate(items, headers=["Index", "Gift Name", "Priority"], showindex=True, tablefmt="pretty"))
            index = input("Enter the index of the item to edit: ").strip()
            if index.isdigit() and 0 <= int(index) < len(items):
                index = int(index)
                print(f"Editing '{items[index][0]}' (Priority: {items[index][1]})")
                new_name = input("Enter new name (or press Enter to keep current): ").strip().title()
                new_priority = input("Enter new priority (0-10, or press Enter to keep current): ").strip()
                if new_name:
                    items[index][0] = new_name
                if new_priority.isdigit() and 0 <= int(new_priority) <= 10:
                    items[index][1] = int(new_priority)
                print(f"Item updated to: {items[index][0]} (Priority: {items[index][1]})")
                save_data(items, skipped_items, marked_off_items)
            else:
                print("Invalid index.")

        elif choice == "9":
            # Exit the program
            print("👋 Goodbye! See you next time! 🎁")
            break
        
        else:
            print("Invalid choice. Please select a valid option from the menu.")

if __name__ == "__main__":
    main()
