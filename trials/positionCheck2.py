import pymongo

# Establish a connection to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Function to search for matching sample names by chromosome, position, and end values
def search_matching_samples(position, end):
    db = client["test4"]

    try:
        # Initialize a dictionary to store matching collections and their matching ObjectIDs
        matching_collections = {}

        # Iterate over all collections in the database
        for collection_name in db.list_collection_names():
            collection = db[collection_name]
            query = {
                "$or": [
                    {
                        "INFO.END": {"$gte": str(position), "$lte": str(end)}
                    },
                    {
                        "$and": [
                            {"INFO.END": {"$gte": str(position)},
                             "Position": {"$lte": str(end)}
                            }
                        ]
                    },
                    {
                        "$or": [
                            {"INFO.END": str(position)},
                            {"Position": str(end)}
                        ]
                    },
                    {
                        "$or": [
                            {"Position": {"$gte": str(position), "$lte": str(end)},
                             "INFO.END": {"$gte": str(position), "$lte": str(end)}
                            }
                        ]
                    },
                    {
                        "$and": [
                            {"Position": {"$lte": str(position), "$lte": str(end)},
                             "INFO.END": {"$gte": str(position), "$gte": str(end)}
                            }
                        ]
                    }
                ]
            }

            matching_documents = collection.find(query)

            matching_document_count = 0
            matching_document_ids = []

            for document in matching_documents:
                matching_document_count += 1
                matching_document_ids.append(document["_id"])  # Access the ObjectID field

            if matching_document_count > 0:
                matching_collections[collection_name] = {
                    "Document Count": matching_document_count,
                    "Matching Document ObjectIDs": matching_document_ids
                }

        if matching_collections:
            print("Matching Collections and Their Document Count:")
            for collection_name, data in matching_collections.items():
                print(f"Collection: {collection_name}, Document Count: {data['Document Count']}")
                if data['Matching Document ObjectIDs']:
                    print(f"Matching Document ObjectIDs: {', '.join(map(str, data['Matching Document ObjectIDs']))}")
                print()

    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Ask the user for input
position = input("Enter the position value: ")
end = input("Enter the end value: ")

# Call the search_matching_samples function
search_matching_samples(position, end)

# Close the MongoDB connection
client.close()