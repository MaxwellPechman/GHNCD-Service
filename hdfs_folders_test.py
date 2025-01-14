from hdfs import InsecureClient

# HDFS connection settings
HDFS_URL = "http://localhost:9870"  # Adjust if necessary
HDFS_DIR = "/user/hdfs/csv_files"  # Directory to check

def check_hdfs_directory_exists(hdfs_client, directory_path: str) -> bool:
    try:
        status = hdfs_client.status(directory_path, strict=False)

        if status:
            print(f"Directory exists: {directory_path}")
            return True
        else:
            print(f"Directory does not exist: {directory_path}")
            return False

    except Exception as e:
        print(f"Error checking directory {directory_path}: {e}")
        return False


client = InsecureClient(HDFS_URL)
check_hdfs_directory_exists(client, HDFS_DIR)