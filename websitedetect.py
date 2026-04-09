import requests
from bs4 import BeautifulSoup
from azure.storage.blob import BlobServiceClient
import difflib

URL = "http://YOUR-IP:8000/testpage.html"
CONNECTION_STRING = "PASTE_YOUR_CONNECTION_STRING"
CONTAINER = "monitor"
FILE_NAME = "latest.txt"

blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)

def get_content(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup.get_text()

def get_old():
    try:
        blob_client = blob_service_client.get_blob_client(container=CONTAINER, blob=FILE_NAME)
        return blob_client.download_blob().readall().decode()
    except:
        return ""

def save(content):
    blob_client = blob_service_client.get_blob_client(container=CONTAINER, blob=FILE_NAME)
    blob_client.upload_blob(content, overwrite=True)

def detect(old, new):
    return list(difflib.unified_diff(old.splitlines(), new.splitlines()))

def main():
    new = get_content(URL)
    old = get_old()

    if old:
        diff = detect(old, new)
        if diff:
            print("Change detected")
        else:
            print("No change")
    else:
        print("First run")

    save(new)

if __name__ == "__main__":
    main()
