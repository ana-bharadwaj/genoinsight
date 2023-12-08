import pymongo
from tabulate import tabulate

# Establish a connection to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Function to search for matching samples by position and end values
def search_matching_samples(position, end):
    db = client["test4"]

    try:
        # Initialize a list to store matching document details
        matching_documents = []

        # Iterate over all collections in the database
        for collection_name in db.list_collection_names():
            collection = db[collection_name]
            query = {
                "INFO.END": str(end),
                "Position": position
            }

            cursor = collection.find(query)

            for document in cursor:
                matching_documents.append(document)

        if matching_documents:
            # Display matching documents as a table
            headers = []
            rows = []

            # Extract headers from the first document
            for key, value in matching_documents[0].items():
                headers.append(key)

            # Additional headers for INFO and FORMAT fields
            info_headers = []
            format_headers = []

            for document in matching_documents:
                info = document.get("INFO", {})
                format = document.get("FORMAT", {})
                info_headers = list(info.keys())
                format_headers = list(format.keys())
                break

            headers.remove("INFO")
            headers.remove("FORMAT")
            headers.extend(["INFO." + header for header in info_headers])
            headers.extend(["FORMAT." + header for header in format_headers])

            for document in matching_documents:
                row = []
                for header in headers:
                    if header.startswith("INFO."):
                        row.append(document["INFO"].get(header[5:], ''))
                    elif header.startswith("FORMAT."):
                        row.append(document["FORMAT"].get(header[7:], ''))
                    else:
                        row.append(str(document.get(header, '')))

                rows.append(row)

            table = tabulate(rows, headers, tablefmt="grid")
            # Print the table with grid lines
            print(table)
        else:
            print("No matching documents found.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Ask the user for input
position = input("Enter the position value: ")
end = input("Enter the end value: ")

# Call the search_matching_samples function
search_matching_samples(position, end)

# Close the MongoDB connection
client.close()