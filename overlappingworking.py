import pymongo
import pandas as pd

# Define a function to get numbers in between two values
def get_numbers_in_between(start, end):
    numbers = []
    for num in range(start + 1, end):
        numbers.append(num)
    return numbers

# Connect to your MongoDB instance
client = pymongo.MongoClient("mongodb://localhost:27017")  # Replace with your MongoDB connection string

# List all the collections in the database
database = client["test7"]  # Replace with your database name
collections = database.list_collection_names()

# Get the user's input for A (start) and B (end)
A = int(input("Enter A (start number): "))
B = int(input("Enter B (end number): "))
C = str(input("Enter C (Chromosome number):"))
padding_percentage = 0.3

# Create a list to store matched data as dictionaries
matched_data = []
total_match = 0
matching_documents = []

# Initialize a set to store all field names
all_fields = set()

def extract_fields(extracted):
    for key, value in document.items():
        if isinstance(value, dict):
            # If it's a dictionary, add its keys as separate columns
            for sub_key, sub_value in value.items():
                column_name = f"{key}.{sub_key}"
                all_fields.add(column_name)
                extracted_data[column_name] = sub_value
        else:
            # Otherwise, add it as a regular column
            all_fields.add(key)
            extracted_data[key] = value
    matched_data.append(extracted_data)

def calculate_span_padding(start, end, padding_percentage):
    span = end - start
    padding = int(span * padding_percentage)
    return span, padding

# Iterate through the collections one by one
for collection_name in collections:
    collection = database[collection_name]

    # Iterate through the documents in the collection
    for document in collection.find():
        if "Position" in document:
            position = int(document["Position"])
        else:
            position = None

        if "INFO" in document and "END" in document["INFO"]:
            end = int(document["INFO"]["END"])
        else:
            end = None

        if "Chromosome" in document:
            chr = str(document["Chromosome"])
        else:
            chr = None

        span, padding = calculate_span_padding(A, B, padding_percentage)

        if (A - padding <= position <= B + padding or A - padding <= end <= B + padding) and C == chr:
            extracted_data = {
                "Collection": collection_name,
                "Document ID": str(document['_id']),
                "Position": position,
                "END": end
            }
            matching_documents.append(
                f"Collection: {collection_name}, Document ID: {document['_id']}, Position:{position}, END:{end}")
            print(
                f"Collection: {collection_name}, Document ID: {document['_id']}, Position:{position}, END:{end}")
            print('\n')
            extract_fields(extracted_data)
            if collection_name not in matching_documents:
                total_match += 1

# Close the MongoDB connection
client.close()

# Total number of matches
print(total_match)

# Create a DataFrame from the list of matched data
df = pd.DataFrame(matched_data)

# Specify the order of columns
column_order = sorted(all_fields)

# Reorder the DataFrame columns
df = df[column_order]

# Export the DataFrame to an Excel file
df.to_excel("matching_mongodb_data_with_overlapping.xlsx", index=False)