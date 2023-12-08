import pymongo
import os

client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["test3"]

# Initialize empty arrays to store fields
chromosomes = []
positions = []
ids = []
refs = []
alts = []
quals = []
filters = []
infos = []
formats = []
samples = []
data_dict = {}
dataHead = {}
# (You can keep these arrays as they are)
'''
# Your VCF file path
directory_path = "samples"
print('hi')

# Initialize an empty list to store VCF file names
vcf_file_names = []

# Use os.listdir() to get a list of all files in the directory
for file in os.listdir(directory_path):
    if file.endswith(".vcf"):
        # Append the VCF file name to the list
        vcf_file_names.append(file)
'''

# Function to process and insert data into the database
def process_and_insert_vcf(vcf_file_path, collection):
    with open(vcf_file_path, "r") as vcf:
        for line in vcf:
            # Skip header lines
            if line.startswith("#"):
                continue

            fields = line.strip().split("\t")
            chromosome, position, vcf_id, ref, alt, qual, filter_val, info, format_val, sample_data = fields

            # Append fields to their respective arrays
            chromosomes.append(chromosome)
            positions.append(position)
            ids.append(vcf_id)
            refs.append(ref)
            alts.append(alt)
            quals.append(qual)
            filters.append(filter_val)
            infos.append(info)
            formats.append(format_val)
            samples.append(sample_data)

        # Print or manipulate the arrays as needed
        for i in range(len(chromosomes)):
            dataHead = {
                'Chromosome': chromosomes[i],
                'Position': positions[i],
                'ID': ids[i],
                'REF': refs[i],
                'ALT': alts[i],
                'QUAL': quals[i],
                'FILTER': filters[i]
            }

            # Split the data into individual fields based on semicolon (;)
            data_fields = infos[i].split(";")

            # Loop through the data fields and add them to the dictionary
            for field in data_fields:
                key, value = field.split("=")
                data_dict[key] = value

            # Add INFO and FORMAT dictionaries to dataHead
            dataHead['INFO'] = data_dict

            format_fields = formats[i].split(":")
            format_data = {field: value for field, value in zip(format_fields, sample_data.split(":"))}
            dataHead['FORMAT'] = format_data

            # Insert dataHead into the MongoDB collection
            collection.insert_one(dataHead)

# (You can keep this function as it is)

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

folder_path_sample = "samples"
parse_through(folder_path_sample)

# Function to delete a VCF file
'''
def delete_vcf_file(vcf_file_name):
    vcf_file_path = os.path.join(directory_path, vcf_file_name)
    os.remove(vcf_file_path)
    print(f"Deleted {vcf_file_name}")
'''
# Main menu loop
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

    elif user_choice == '2':
    
            print("\nDelete Documents Menu:")
            print("1. Delete by Chromosome")
            print("2. Show collections")
            delete_choice = input("Enter your choice (1/2/3): ")

            if delete_choice == '1':
                chromosome_to_delete = input("Enter the chromosome you want to delete: ")
                delete_result = database.collection.delete_many({'Chromosome': chromosome_to_delete})
                print(f"Deleted {delete_result.deleted_count} documents with Chromosome: {chromosome_to_delete}")

            elif delete_choice == '2':
                for collections_name in database.list_collections_names():
                    print(collections_name)

            else:
                print("Invalid choice. Please select a valid option.")
    elif user_choice == '3':
        # Quit the program
        break

    else:
        print("Invalid choice. Please select a valid option.")