from hdfs import InsecureClient
import requests

# HDFS connection details
HDFS_URL = "http://localhost:9870"  # Adjust this URL if needed
HDFS_DIR = "/user/hdfs/test_directory"  # Directory to upload the file

# Create a test file content
test_file_name = "test_file.txt"
test_file_content = "Hello, this is a test file for HDFS!"


def check_hdfs_connection(hdfs_url: str):
    """Check if HDFS URL is accessible by making a simple GET request to the Namenode."""
    try:
        print(f"Checking connection to HDFS at {hdfs_url}...")
        response = requests.get(hdfs_url)
        if response.status_code == 200:
            print("HDFS connection successful!")
        else:
            print(f"Error connecting to HDFS. Status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"Error while connecting to HDFS: {e}")
        return False
    return True


def upload_to_hdfs(hdfs_client: InsecureClient, hdfs_path: str, content: bytes):
    """Uploads a file to HDFS."""
    try:
        # Ensure the directory exists
        hdfs_client.makedirs(HDFS_DIR)
        print(f"Directory {HDFS_DIR} ensured on HDFS.")

        # Upload the file to HDFS
        with hdfs_client.write(hdfs_path, overwrite=True) as writer:
            writer.write(content)
        print(f"Successfully uploaded {test_file_name} to HDFS at {hdfs_path}")
    except Exception as e:
        print(f"Error while uploading to HDFS: {e}")
        raise  # Re-raise the exception to catch it in the calling function


def test_upload():
    """Test the file upload to HDFS."""
    # Check if the HDFS connection is working
    if not check_hdfs_connection(HDFS_URL):
        print("Cannot connect to HDFS. Exiting...")
        return

    # Create a test file content
    print("Uploading a test file to HDFS...")
    hdfs_client = InsecureClient(HDFS_URL)

    try:
        upload_to_hdfs(hdfs_client, f"{HDFS_DIR}/{test_file_name}", test_file_content.encode())

        # Verify the file exists
        print("Verifying the file on HDFS...")
        file_status = hdfs_client.status(f"{HDFS_DIR}/{test_file_name}")
        if file_status:
            print(f"File {test_file_name} successfully uploaded to HDFS at {HDFS_DIR}")
        else:
            print(f"Failed to find the file {test_file_name} on HDFS.")
    except Exception as e:
        print(f"Error during test upload: {e}")


if __name__ == "__main__":
    test_upload()
