import uuid
import sys
from typing import Optional, List
from dataclasses import dataclass
from faker import Faker 


@dataclass
class Node:
    """Node class for the linked list."""
    data: dict
    #next could be either a Node object or None. Optional annotation 
    next: Optional['Node'] = None


class LinkedList:
            
    """Linked list implementation for storing objects."""

    def __init__(self):
        self.head = None
        self.size = 0
    
    def append(self, data: dict) -> None:
        """Add a new node with data to the end of the linked list."""
        new_node = Node(data)
        self.size += 1
        
        if not self.head:
            self.head = new_node
            return
        
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
    
    def search_by_name(self, name: str) -> List[dict]:
        """Search for objects by name."""
        results = []
        search_term = name.lower()
        current = self.head
        
        while current:
            # Use exact matching (constant time for fixed-length comparison)
            if search_term == current.data["name"].lower():
                results.append(current.data)
            current = current.next
        
        return results
    
    def to_list(self) -> List[dict]:
        """Convert linked list to a regular list for sorting."""
        result = []
        current = self.head
        
        while current:
            result.append(current.data)
            current = current.next
        
        return result
    
    def from_list(self, data_list: List[dict]) -> None:
        """Rebuild linked list from a sorted list."""
        self.head = None
        self.size = 0
        
        for data in data_list:
            self.append(data)
    
    def sort_by_date(self, ascending: bool = True) -> List[dict]:
        """Sort the linked list by date and return the sorted list."""
        data_list = self.to_list()
        
        # Sort the list by date
        data_list.sort(key=lambda x: x["date"], reverse=not ascending)
        
        # Rebuild the linked list with the sorted data
        self.from_list(data_list)
        
        return data_list

#
def generate_random_objects(count: int = 15) -> LinkedList:
    """Generate random objects with realistic data using Faker."""
    linked_list = LinkedList()
    fake = Faker()
    
    for x in range(count):
        # Generate a random date within the last year
        random_date = fake.date_time_between(start_date='-3y', end_date='now')
        
        # Create the object with realistic fake data
        obj = {
            #Function from Faker library to generate realistic data
            "id": str(uuid.uuid4()),
            "name": fake.name(),
            "date": random_date
        }
        
        #Append the object to the linked list
        linked_list.append(obj)
    
    return linked_list


def format_date(dt):
    """Format datetime for display."""
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def display_objects(objects):
    """Display objects formatted"""
    if not objects:
        print("No objects found.")
        return
    
    # Format and display the objects
    print(f"{'ID':<36} | {'Name':<23} | {'Date'}")
    print("-" * 90)
    
    for obj in objects:
        print(f"{obj['id']:<36} | {obj['name']:<23} | {format_date(obj['date'])}")


def print_menu():
    """Print the main menu."""
    print("\n==== Object Tracker ====")
    print("1. Search objects by name")
    print("2. Sort objects by date")
    print("3. Exit")
    print("===========================")


def main():
    """Main function to run the CLI program."""
    # Initialize linked list with random objects
    linked_list = generate_random_objects(15)
    print(f"Generated {linked_list.size} random objects.")
    
    # Display all objects for a start
    print("\nAll objects:")
    display_objects(linked_list.to_list())
    
    # Main menu loop
    while True:
        print_menu()
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            # Search objects by name
            name = input("Enter name to search for: ")
            results = linked_list.search_by_name(name)
            print(f"\nSearch results for '{name}':")
            display_objects(results)
        
        elif choice == '2':
            # Sort objects by date
            print("\nSort order:")
            print("1. Ascending (oldest to newest)")
            print("2. Descending (newest to oldest)")
            sort_choice = input("Enter sort order (1 or 2): ")
            
            ascending = True
            if sort_choice == '2':
                ascending = False
            
            if ascending == True:
                direction = "ascending"
            else:
                direction = "descending"

            print(f"\nSorting objects by date in {direction} order:")
            sorted_list = linked_list.sort_by_date(ascending)
            display_objects(sorted_list)
        
        elif choice == '3':
            # Exit the program
            print("Exiting the program.")
            sys.exit(0)
        
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")
        sys.exit(0)