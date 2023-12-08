import pymongo
import os
from collections import defaultdict
import datetime

# MongoDB client and database
client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["test2"]

# Function to process VCF data
def process_vcf_data(vcf_file_path):
    data_dict = defaultdict(list)

    with open(vcf_file_path, "r") as vcf:
        for line in vcf:
            if line.startswith("#"):
                continue

            fields = line.strip().split("\t")
            chromosome, position, vcf_id, ref, alt, qual, filter_val, info, format_val, sample_data = fields

            data_dict['Chromosome'].append(chromosome)
            data_dict['Position'].append(position)
            data_dict['ID'].append(vcf_id)
            data_dict['REF'].append(ref)
            data_dict['ALT'].append(alt)
            data_dict['QUAL'].append(qual)
            data_dict['FILTER'].append(filter_val)

            info_fields = info.split(";")
            info_dict = {}
            for info_field in info_fields:
                key, value = info_field.split("=")
                info_dict[key] = value
            data_dict['INFO'].append(info_dict)

            format_fields = format_val.split(":")
            sample_fields = sample_data.split(":")
            format_dict = {}
            for field, value in zip(format_fields, sample_fields):
                format_dict[field] = value
            data_dict['FORMAT'].append(format_dict)

    return data_dict

# Function to insert data into MongoDB
def insert_data_into_mongodb(collection, data_dict):
    bulk_operations = []

    for i in range(len(data_dict['Chromosome'])):
        data_head = {
            'Chromosome': data_dict['Chromosome'][i],
            'Position': data_dict['Position'][i],
            'ID': data_dict['ID'][i],
            'REF': data_dict['REF'][i],
            'ALT': data_dict['ALT'][i],
            'QUAL': data_dict['QUAL'][i],
            'FILTER': data_dict['FILTER'][i],
            'INFO': data_dict['INFO'][i],
            'FORMAT': data_dict['FORMAT'][i],
            'Timestamp': datetime.datetime.now()
        }
        bulk_operations.append(pymongo.InsertOne(data_head))

    if bulk_operations:
        collection.bulk_write(bulk_operations)

# Directory containing VCF files
directory_path = "samples"

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
            data_dict = process_vcf_data(user_input)
            insert_data_into_mongodb(user_collection, data_dict)
            print("Data inserted successfully.")

        else:
            print("Invalid input or file format. Please provide a valid VCF file path.")

    elif user_choice == '2':
        # Allow the user to delete a VCF file
        print("Available VCF files:")
        for idx, vcf_file_name in enumerate(os.listdir(directory_path), start=1):
            if vcf_file_name.endswith(".vcf"):
                print(f"{idx}. {vcf_file_name}")
        vcf_to_delete_idx = input("Enter the number of the VCF file you want to delete: ")
        try:
            vcf_to_delete_idx = int(vcf_to_delete_idx)
            vcf_file_names = [f for f in os.listdir(directory_path) if f.endswith(".vcf")]
            if 1 <= vcf_to_delete_idx <= len(vcf_file_names):
                vcf_file_to_delete = vcf_file_names[vcf_to_delete_idx - 1]
                vcf_file_path_to_delete = os.path.join(directory_path, vcf_file_to_delete)
                os.remove(vcf_file_path_to_delete)
                print(f"Deleted {vcf_file_to_delete}")
            else:
                print("Invalid selection. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    elif user_choice == '3':
        # Quit the program
        break

    else:
        print("Invalid choice. Please select a valid option.")