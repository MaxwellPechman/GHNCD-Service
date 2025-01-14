import requests
from bs4 import BeautifulSoup
from hdfs import InsecureClient
from concurrent.futures import ThreadPoolExecutor

GHNCD_URL = "https://www.ncei.noaa.gov/data/global-historical-climatology-network-daily/access/"
HDFS_URL = "http://localhost:9870"
HDFS_DIR = "/user/hdfs/csv_files"


def request_content_from_url(url: str):
    response = requests.get(url)

    if response.status_code != 200:
        return None

    return response.content


def extract_tag_content(html_code: bytes, tag: str):
    content = []

    soup = BeautifulSoup(html_code, 'html.parser')
    tags = soup.find_all(tag)

    for tag in tags:
        content.append(tag['href'])

    return content


def upload_content_to_hdfs(hdfs_client: InsecureClient, hdfs_path: str, content: bytes):
    try:
        if not hdfs_client.status(HDFS_DIR, strict=False):
            print(f"Creating directory {HDFS_DIR} on HDFS...")
            hdfs_client.makedirs(HDFS_DIR)

        print(f"Uploading to HDFS: {hdfs_path}")
        with hdfs_client.write(hdfs_path, overwrite=True) as writer:
            writer.write(content)

        print(f"Successfully uploaded file to HDFS: {hdfs_path}")

    except Exception as e:
        print(f"Error while uploading to HDFS: {e}")


def download_and_upload_file(hdfs_client: InsecureClient, file_url: str):
    file_name = file_url.split("/")[-1]
    hdfs_file_path = f"{HDFS_DIR}/{file_name}"

    print(f"Downloading file: {file_url}")
    file_response = requests.get(file_url, stream=True)

    if file_response.status_code == 200:
        try:
            upload_content_to_hdfs(hdfs_client, hdfs_file_path, file_response.content)
        except Exception as e:
            print(f"Error while uploading {file_name} to HDFS: {e}")
    else:
        print(f"Failed to download file: {file_url}")


def update_files():
    hdfs_client = InsecureClient(HDFS_URL)

    print("Requesting content from:", GHNCD_URL)
    content = request_content_from_url(GHNCD_URL)

    if content is None:
        print("Error while requesting content from:", GHNCD_URL)
        return

    files = extract_tag_content(content, 'a')
    csv_files = [f for f in files if f.endswith('.csv')]

    print(f"Found {len(csv_files)} CSV files.")

    # Create a thread pool and process files concurrently
    with ThreadPoolExecutor(max_workers=20) as executor:  # Adjust max_workers as needed
        file_urls = [GHNCD_URL + file for file in csv_files]
        executor.map(lambda url: download_and_upload_file(hdfs_client, url), file_urls)


if __name__ == "__main__":
    update_files()
