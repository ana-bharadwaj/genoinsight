import pymongo
import pandas as pd

#Define a function to get numbers in between two values
def get_numbers_in_between(start, end):
    numbers = []
    for num in range(start + 1, end):
        numbers.append(num)
    return numbers

#Connect to your MongoDB instance
client = pymongo.MongoClient("mongodb://localhost:27017")  # Replace with your MongoDB connection string

#List all the collections in the database
database = client["test4"]  # Replace with your database name
collections = database.list_collection_names()

#Get the user's input for A (start) and B (end)
A = int(input("Enter A (start number): "))
B = int(input("Enter B (end number): "))

#Create a list to store matching document IDs
matching_documents = []

#Iterate through the collections one by one
for collection_name in collections:
    collection = database[collection_name]

    # Iterate through the documents in the collection
    for document in collection.find():
        position = 0
        end = 0  # Reset position and end for each document

        if "Position" in document:
            position = int(document["Position"])

        # Check if the document has an "INFO" field
        if "INFO" in document:
            # Check if "END" is present in the "INFO" field
            if "END" in document["INFO"]:
                end = int(document["INFO"]["END"])

        if A <= position and B >= end:
            matching_documents.append(f"Collection: {collection_name}, Document ID: {document['_id']}, Position: {position}, END: {end}")

#Create a list to store the data for the Excel file
data = []

#Append the matched documents to the data
for match in matching_documents:
    data.append([match, "", "", "", ""])

#Close the MongoDB connection
client.close()

#Create a DataFrame from the data
df = pd.DataFrame(data, columns=["", "Collection", "Document ID", "Position", "END"])

#Export the DataFrame to an Excel file
df.to_excel("matching_mongodb_data3.xlsx", index=False)