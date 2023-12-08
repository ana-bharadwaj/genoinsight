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
E = str(input("Enter D (Is it deletion or duplication):"))

# Create a list to store matched data as dictionaries
matched_data = []
total_match = 0
matching_documents = []

# Create two lists to separate matching ALT values equal to E and not equal to E
matched_data_alt_e = []
matched_data_alt_not_e = []

# Initialize a set to store all field names
all_fields = set()

D = (B - A) * 0.15
Lower = A - D
Upper = B + D

def extract_fields(extracted_data, document):
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

        if "ALT" in document:
            alt = document["ALT"]
        else:
            alt = None

        if Lower <= position < Upper and Lower < end <= Upper and C == chr:
            extracted_data = {
                "Collection": collection_name,
                "Document ID": str(document['_id']),
                "Position": position,
                "END": end,
                "ALT": alt
            }

            if alt == E:
                matched_data_alt_e.append(extracted_data)
            else:
                matched_data_alt_not_e.append(extracted_data)

            if collection_name not in matching_documents:
                total_match += 1

# Print matching documents with ALT equal to E first
for matched_doc in matched_data_alt_e:
    print(f"Collection: {matched_doc['Collection']}, Document ID: {matched_doc['Document ID']}, Position: {matched_doc['Position']}, END: {matched_doc['END']}, ALT: {matched_doc['ALT']}")

# Print matching documents with ALT not equal to E
for matched_doc in matched_data_alt_not_e:
    print(f"Collection: {matched_doc['Collection']}, Document ID: {matched_doc['Document ID']}, Position: {matched_doc['Position']}, END: {matched_doc['END']}, ALT: {matched_doc['ALT']}")

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
df.to_excel("matching_mongodb_data5.xlsx", index=False)