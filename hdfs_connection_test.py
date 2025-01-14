from hdfs import InsecureClient
from requests.exceptions import ConnectionError

# HDFS configuration
HDFS_URL = "http://localhost:9870"
HDFS_USER = "hdfs"

def test_hdfs_connection():
    try:
        # Create an HDFS client
        client = InsecureClient(HDFS_URL)

        # Try to list the root directory
        print("Connecting to HDFS...")
        directories = client.list("/")
        print(f"Successfully connected to HDFS at {HDFS_URL}.")
        print("Root directory contents:")
        for directory in directories:
            print(f" - {directory}")

    except ConnectionError as e:
        print(f"Failed to connect to HDFS at {HDFS_URL}. Ensure the NameNode is reachable and running.")
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


test_hdfs_connection()
