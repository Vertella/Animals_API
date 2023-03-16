import requests
import json
import sys

# Defines the base URL for the API
base_url = "http://localhost:8000"

response = requests.get("https://localhost:8000/animals")
response.request
data = response.json()

# Defines a function to get all animals from the API
def get_all_animals():
    response = requests.get(f"{base_url}/animals")
    if response.status_code == 200:
        animals = response.json()
        print(f"Total animals: {len(animals)}")
        for animal in animals:
            print(f"{animal['id']}. {animal['common_name']} ({animal['scientific_name']}) - {animal['population']} - {animal['conservation_status']} - {animal['native_region']}")
    else:
        print("Error retrieving animals")

# Define a function to get an animal by ID from the API
def get_animal_by_id():
    animal_id = input("Enter the animal ID: ")
    response = requests.get(f"{base_url}/animals/{animal_id}")
    if response.status_code == 200:
        animal = response.json()
        print(f"{animal['id']}. {animal['common_name']} ({animal['scientific_name']}) - {animal['population']} - {animal['conservation_status']} - {animal['native_region']}")
    elif response.status_code == 404:
        print("Animal not found")
    else:
        print("Error retrieving animal")

# Defines a function to add a new animal to the API
def add_animal():
    common_name = input("Enter the common name: ")
    scientific_name = input("Enter the scientific name: ")
    population = int(input("Enter the population: "))
    conservation_status = input("Enter the conservation status (Least_Concern/Near_Threatened/Endangered/Critically_Endangered/Extinct): ")
    native_region = input("Enter the native region: ")
    data = {"common_name": common_name, "scientific_name": scientific_name, "population": population, "conservation_status": conservation_status, "native_region": native_region}
    headers = {"Content-type": "application/json"}
    response = requests.post(f"{base_url}/animals", data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        animal = response.json()
        print(f"{animal['id']}. {animal['common_name']} ({animal['scientific_name']}) - {animal['population']} - {animal['conservation_status']} - {animal['native_region']}")
    else:
        print("Error adding animal")

# Defines a function to update an existing animal in the API
def update_animal(animal_id: int):
    response = requests.get(f"{base_url}/animals/{animal_id}")
    if response.status_code != 200:
        print("Animal not found.")
        return

    animal = response.json()

    while True:
        print(f"What would you like to update for {animal['common_name']} ({animal['scientific_name']})?")
        print("1. Common name")
        print("2. Scientific name")
        print("3. Population")
        print("4. Conservation status")
        print("5. Native region")
        print("6. All details")
        print("7. Cancel")

        choice = input("Enter your choice (1-7): ")

        update_data = {}
        if choice == "1":
            common_name = input("Enter the new common name: ")
            update_data = {"common_name": common_name}
        elif choice == "2":
            scientific_name = input("Enter the new scientific name: ")
            update_data = {"scientific_name": scientific_name}
        elif choice == "3":
            population = int(input("Enter the new population: "))
            update_data = {"population": population}
        elif choice == "4":
            conservation_status = input("Enter the new conservation status: ")
            update_data = {"conservation_status": conservation_status}
        elif choice == "5":
            native_region = input("Enter the new native region: ")
            update_data = {"native_region": native_region}
        elif choice == "6":
            common_name = input(f"Enter the new common name ({animal['common_name']}): ")
            scientific_name = input(f"Enter the new scientific name ({animal['scientific_name']}): ")
            population = int(input(f"Enter the new population ({animal['population']}): "))
            conservation_status = input(f"Enter the new conservation status ({animal['conservation_status']}): ")
            native_region = input(f"Enter the new native region ({animal['native_region']}): ")
            update_data = {
                "common_name": common_name,
                "scientific_name": scientific_name,
                "population": population,
                "conservation_status": conservation_status,
                "native_region": native_region
            }
        elif choice == "7":
            return
        else:
            print("Invalid choice. Please try again.")
            continue

        response = requests.patch(f"{base_url}/animals/{animal_id}", json=update_data)
        if response.status_code == 200:
            animal = response.json()
            print(f"Animal updated: {animal['common_name']} ({animal['scientific_name']}) - {animal['population']} - {animal['conservation_status']} - {animal['native_region']}")
            return
        else:
            print("Error updating animal. Please try again.")


# Defines a function to delete an animal from the API
def delete_animal(animal_id):
    # send delete request to the API
    response = requests.delete(f"{base_url}/animals/{animal_id}")
    if response.status_code == 204:
        print(f"Animal with ID {animal_id} has been deleted.")
    else:
        print(f"Error deleting animal with ID {animal_id}: {response.status_code} - {response.json()['message']}")


# Defines a function to search for an animal
def search_animal(base_url):
    search_term = input("Enter the name of the animal you want to find")
    response = requests.get(f"{base_url}/animals/search", params={"q": search_term})
    if response.status_code == 200:
        results = response.json()
        if len(results) > 0:
            print(f"Search results for '{search_term}':")
            for result in results:
                print(f"{result['id']}. {result['common_name']} ({result['scientific_name']}) - {result['population']} - {result['conservation_status']} - {result['native_region']}")
        else:
            print(f"No results found for '{search_term}'.")
    else:
        print("An error occurred while searching for animals.")

# Defines a function to get all conservation statuses
def get_conservation_status(base_url):
    response = requests.get(f"{base_url}/conservation-status")
    if response.status_code == 200:
        conservation_statuses = set(animal['conservation_status'] for animal in response.json())
        print(f"Total conservation statuses: {len(conservation_statuses)}")
        for status in conservation_statuses:
            print(f"{status}")
    else:
        print("Error retrieving conservation statuses")

# Function to quit program
def exit_program():
    print("Exiting program...")
    sys.exit()


# Function that display the starting menu
def show_menu():    
    print("Welcome to the Animals Conservation API Client!")
    print("Please select an option:")
    print("1. View all animals")
    print("2. Get animal by ID")
    print("3. Add a new animal")
    print("4. Update an existing animal")
    print("5. Delete an animal")
    print("6. Search animals by name")
    print("7. Get all conservation statuses")
    print("8. Quit")
    user_choice = input("Enter your choice (1-8): ")
    if user_choice == "1":
        get_all_animals(base_url)
    elif user_choice == "2":
        get_animal_by_id(base_url)
    elif user_choice == "3":
        add_animal()
    elif user_choice == "4":
        update_animal()
    elif user_choice == "5":
        delete_animal()   
    elif user_choice == "6":
        search_animal()
    elif user_choice == "7":
        get_conservation_status()
    elif user_choice == "8":
        exit_program()     
    else:
        print("Invalid choice. Please try again.")

# Calling the show menu function
show_menu()