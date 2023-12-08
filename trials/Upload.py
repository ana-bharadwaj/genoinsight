import pymongo
import os

client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["test6"]

# Function to process and insert data into the database
def process_and_insert_vcf(vcf_file_path, collection):
    formats = []
    with open(vcf_file_path, "r") as vcf:
        for line in vcf:
            # Skip header lines
            if line.startswith("#"):
                continue

            fields = line.strip().split("\t")
            chromosome, position, vcf_id, ref, alt, qual, filter_val, info, format_val, sample_data = fields

            # Create a dictionary for the main fields
            dataHead = {
                'Chromosome': chromosome,
                'Position': position,
                'ID': vcf_id,
                'REF': ref,
                'ALT': alt,
                'QUAL': qual,
                'FILTER': filter_val,
            }


            # Split the data into individual fields based on semicolon (;)
            info_fields = info.split(";")

            info_dict = {}
            for field in info_fields:
                if "=" in field:
                    key, value = field.split("=")
                    info_dict[key] = value
                else:
                    info_dict[field] = None

            dataHead['INFO'] = info_dict
            
            format_fields = formats[i].split(":")
            format_data = {field: value for field, value in zip(format_fields, sample_data.split(":"))}
            dataHead['FORMAT'] = format_data


            # Insert dataHead into the MongoDB collection
            collection.insert_one(dataHead)

def parse_through(folder_path):
    for file in os.listdir(folder_path):
        if file.endswith(".vcf"):
            # Specify the full path to the VCF file
            vcf_file_path = os.path.join(folder_path, file)

            # Create a collection with the same name as the VCF file (remove the ".vcf" extension)
            collection_name = os.path.splitext(file)[0]
            collection = database[collection_name]

            # Process and insert data from the VCF file into the database
            process_and_insert_vcf(vcf_file_path, collection)

# Rest of your code
# ...

while True:
    print("\nMain Menu:")
    print("1. Add VCF File")
    print("2. Delete VCF File")
    print("3. Quit")
    user_choice = input("Enter your choice (1/2/3): ")

    if user_choice == '1':
        # Allow the user to add a VCF file
        user_input = input("Enter the path of the VCF file you want to add: ")
        if os.path.isfile(user_input) and user_input.endswith(".vcf"):
            # Create a collection with a user-specified name
            user_collection_name = input("Enter a name for the collection: ")
            user_collection = database[user_collection_name]
            # Process and insert data from the user-provided VCF file into the database
            process_and_insert_vcf(user_input, user_collection)
        else:
            parse_through(user_input)

    # Rest of your menu options (delete and quit) here...
    elif user_choice == '2':
        # Handle the delete option
        while True:
            print("\nDelete Documents Menu:")
            print("1. Delete by Chromosome")
            print("2. Show collections")
            print("3. Back to main menu")
            delete_choice = input("Enter your choice (1/2/3): ")

            if delete_choice == '1':
                collection_name_to_delete = input("Enter the collection name (sample) you want to delete: ")
            # Check if the collection (sample) exists
                if collection_name_to_delete in database.list_collection_names():
                    collection_to_delete = database[collection_name_to_delete]
                # Delete all documents in the specified collection
                    delete_result = collection_to_delete.delete_many({})
                    print(f"Deleted {delete_result.deleted_count} documents in Collection: {collection_name_to_delete}")
            elif delete_choice == '2':
                collection_names = database.list_collection_names()
                #Print the collection names
                for collection_name in collection_names:
                    print(collection_name)
            else:
                break
 
    elif user_choice == '3':
        # Quit the program
        break
    else:
        print("Invalid choice. Please select a valid option.")
      