# Use the base Hadoop Namenode image
FROM bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8

# Switch to root user to install Python and add necessary packages
USER root

# Update the repositories to use a newer Debian version (buster)
RUN sed -i 's|stretch|buster|' /etc/apt/sources.list

# Install dirmngr, gnupg, and curl
RUN apt-get update && apt-get install -y dirmngr gnupg curl

# Fetch and add GPG keys non-interactively (check if files already exist)
RUN if [ ! -f /usr/share/keyrings/debian-archive-keyring.gpg ]; then \
      curl -fsSL https://ftp-master.debian.org/keys/archive-key-10.asc | gpg --batch --dearmor -o /usr/share/keyrings/debian-archive-keyring.gpg; \
    fi && \
    if [ ! -f /usr/share/keyrings/debian-security-keyring.gpg ]; then \
      curl -fsSL https://ftp-master.debian.org/keys/archive-key-11-security.asc | gpg --batch --dearmor -o /usr/share/keyrings/debian-security-keyring.gpg; \
    fi

# Install Python 3 and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Upgrade pip to the latest version
RUN pip3 install --upgrade pip

# Install required Python libraries
RUN pip3 install \
    requests \
    hdfs \
    beautifulsoup4 \
    pyspark \
    fastapi \
    uvicorn \
    pyarrow \
    pandas
