from pyspark.sql import SparkSession
from hdfs import InsecureClient

HDFS_URL = "http://localhost:9870"
HDFS_CSV_DIR = "/user/hdfs/example_csv/test_csvs" ## change back to csv_files
HDFS_PARQUET_DIR = "/user/hdfs/parquet_files"


def convert_csv_to_parquet():
    # Initialize SparkSession
    spark = (SparkSession.builder
        .appName("CSV to Parquet Conversion")
        .config("spark.hadoop.fs.defaultFS", "hdfs://localhost:9000")
        .config("spark.hadoop.ipc.client.max.response.size", "2147483648")
        .config("spark.driver.maxResultSize", "2g")
        .getOrCreate())

    # Initialize HDFS client
    hdfs_client = InsecureClient(HDFS_URL)

    # Ensure parquet directory exists
    try:
        if not hdfs_client.status(HDFS_PARQUET_DIR, strict=False):
            print(f"Creating directory {HDFS_PARQUET_DIR} on HDFS...")
            hdfs_client.makedirs(HDFS_PARQUET_DIR)
    except Exception as e:
        print(f"Error ensuring Parquet directory on HDFS: {e}")
        return

    try:
        # List all CSV files in the directory
        csv_files = hdfs_client.list(HDFS_CSV_DIR)
        csv_files = [f for f in csv_files if f.endswith('.csv')]

        if not csv_files:
            print("No CSV files found in the HDFS directory.")
            return

        print(f"Found {len(csv_files)} CSV files. Converting to Parquet...")

        for csv_file in csv_files:
            csv_path = f"{HDFS_CSV_DIR}/{csv_file}"
            parquet_path = f"{HDFS_PARQUET_DIR}/{csv_file.replace('.csv', '.parquet')}"

            print(f"Reading CSV file: {csv_path}")

            # Read CSV file into Spark DataFrame
            df = spark.read.option("header", "true").csv(csv_path)

            print(f"Writing Parquet file: {parquet_path}")

            # Write DataFrame to Parquet
            df.write.mode("overwrite").parquet(parquet_path)

            print(f"Successfully converted {csv_file} to Parquet.")

    except Exception as e:
        print(f"Error during CSV to Parquet conversion: {e}")

    finally:
        # Stop SparkSession
        spark.stop()


if __name__ == "__main__":
    convert_csv_to_parquet()
