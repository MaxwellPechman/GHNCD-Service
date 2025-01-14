#!/bin/bash
set -e

# Format the Namenode if it's the first time
if [ ! -d "/hadoop/dfs/name/current" ]; then
  echo "Formatting HDFS Namenode..."
  hdfs namenode -format -force
fi

# Start the Namenode
echo "Starting HDFS Namenode..."
exec hdfs namenode