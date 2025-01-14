from pyspark.sql import SparkSession

spark = (SparkSession.builder
    .appName("HDFS-Test")
    .config("spark.hadoop.fs.defaultFS", "hdfs://localhost:9000")
    .config("spark.hadoop.ipc.client.max.response.size", "2147483648")
    .config("spark.driver.maxResultSize", "2g")
    .getOrCreate())

# Path to HDFS file
hdfs_file_path = "hdfs://namenode:9000/user/hdfs/example_csv/test_csvs/customer_data.csv"

try:
    # Test reading CSV from HDFS
    print("Reading file from HDFS...")
    df = spark.read.csv(hdfs_file_path, header=True)
    print("DataFrame Schema:")
    df.printSchema()

    print("DataFrame Preview:")
    df.show()

except Exception as e:
    print(f"Error reading file from HDFS: {e}")

finally:
    spark.stop()

