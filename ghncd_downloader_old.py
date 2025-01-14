import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from hdfs import InsecureClient

BASE_URL = "https://www.ncei.noaa.gov/data/global-historical-climatology-network-daily/access/"
DOWNLOAD_TIMEOUT = 5
MAX_WORKERS = 20

# HDFS configuration
HDFS_URL = "http://localhost:9870"  # Change this to your HDFS URI
HDFS_DIR = "/user/hdfs/csv_files"  # Directory in HDFS where you want to store the files

# Initialize HDFS client
hdfs_client = InsecureClient(HDFS_URL)


def download_and_upload_to_hdfs(file_url, hdfs_file_path, current_index, total_files):
    try:
        print(f"Processing file {current_index}/{total_files}: {file_url}")

        # Download the file content from the URL
        response = requests.get(file_url, stream=True, timeout=DOWNLOAD_TIMEOUT)

        if response.status_code == 200:
            # Stream the content directly to HDFS
            with hdfs_client.write(hdfs_file_path, overwrite=True) as writer:
                for chunk in response.iter_content(chunk_size=1024):
                    writer.write(chunk)
            return f"Uploaded {hdfs_file_path} successfully to HDFS. ({current_index}/{total_files})"
        else:
            return f"Error downloading {file_url}: Status code {response.status_code} ({current_index}/{total_files})"

    except requests.exceptions.Timeout:
        return f"Download timeout for {file_url} ({current_index}/{total_files})"
    except Exception as e:
        return f"Error downloading or uploading {file_url}: {str(e)} ({current_index}/{total_files})"


def download_and_upload_csv_files():
    print("Retrieving content from website...")
    response = requests.get(BASE_URL)

    if response.status_code != 200:
        print(f"Error retrieving website: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a', href=True)

    # Filter for CSV links
    csv_links = [link['href'] for link in links if link['href'].endswith('.csv')]
    total_files = len(csv_links)

    if not csv_links:
        print("No CSV files found on the website.")
        return

    print(f"{total_files} CSV files found. Starting download and upload to HDFS...")

    # Download and upload each CSV file concurrently
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_file = {
            executor.submit(
                download_and_upload_to_hdfs,
                BASE_URL + csv_link,
                f"{HDFS_DIR}/{csv_link}",
                current_index=i + 1,  # Current file number
                total_files=total_files
            ): csv_link
            for i, csv_link in enumerate(csv_links)
        }

        for future in as_completed(future_to_file):
            csv_link = future_to_file[future]
            try:
                result = future.result()
                print(result)
            except Exception as e:
                print(f"Error with {csv_link}: {e}")

    print("Download and upload completed.")


if __name__ == "__main__":
    download_and_upload_csv_files()
