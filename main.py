import uvicorn
from fastapi import FastAPI, HTTPException
from hdfs import InsecureClient
from pyarrow import parquet as pq
from io import BytesIO

from starlette.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# HDFS configuration
HDFS_URL = "http://localhost:9870"
HDFS_USER = "hdfs"
client = InsecureClient(HDFS_URL, user=HDFS_USER)

# Function to read Parquet file from HDFS
def read_parquet_from_hdfs(hdfs_path):
    try:
        with client.read(hdfs_path) as reader:
            # Load Parquet file into a Pandas DataFrame
            table = pq.read_table(BytesIO(reader.read()))
            return table.to_pandas()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# API endpoint to list available Parquet files
@app.get("/files")
def list_parquet_files():
    try:
        files = client.list("/", status=False)  # Replace "/" with your HDFS directory
        parquet_files = [f for f in files if f.endswith(".parquet")]
        return {"files": parquet_files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# API endpoint to read a specific Parquet file
@app.get("/data/{file_name}")
def get_parquet_data(file_name: str):
    try:
        hdfs_path = f"/{file_name}"  # Replace "/" with your HDFS directory
        df = read_parquet_from_hdfs(hdfs_path)
        return df.to_dict(orient="records")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    config = uvicorn.Config(host="127.0.0.1",
                            port=8000,
                            log_level="info",
                            app="main:app")
    server = uvicorn.Server(config)
    server.run()