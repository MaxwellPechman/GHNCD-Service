from hdfs import InsecureClient

HDFS_URL = "http://localhost:9870"
HDFS_DIR = "/user/hdfs/example_csv"

# Local file paths for the CSV files
LOCAL_FILES = [
    "test_csvs/weather_data.csv",
    "test_csvs/sale_data.csv",
    "test_csvs/customer_data.csv"
]

def upload_files_to_hdfs():
    # Initialize HDFS client
    hdfs_client = InsecureClient(HDFS_URL)

    # Ensure the target directory exists on HDFS
    try:
        if not hdfs_client.status(HDFS_DIR, strict=False):
            print(f"Creating directory {HDFS_DIR} on HDFS...")
            hdfs_client.makedirs(HDFS_DIR)
    except Exception as e:
        print(f"Error creating HDFS directory: {e}")
        return

    # Upload each file to HDFS
    for local_file in LOCAL_FILES:
        try:
            hdfs_path = f"{HDFS_DIR}/{local_file}"
            print(f"Uploading {local_file} to HDFS at {hdfs_path}...")
            with open(local_file, "rb") as file_data:
                hdfs_client.write(hdfs_path, file_data, overwrite=True)
            print(f"Successfully uploaded {local_file} to {hdfs_path}")
        except Exception as e:
            print(f"Error uploading {local_file}: {e}")

if __name__ == "__main__":
    upload_files_to_hdfs()
