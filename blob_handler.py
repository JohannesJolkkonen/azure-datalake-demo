import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

try:
    connect_str = os.getenv('AZURE_STORAGE_CONN_STRING')
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    print('Azure Blob Storage v' + __version__ + " - Python handler")
except Exception as e:
    print('Exception: ', e)

def create_container(blob_service_client):
    container_name = "enterprise-" + str(uuid.uuid4())
    container_client = blob_service_client.create_container(container_name)
    return container_client

def upload_blob(upload_file_path, blob_service_client, container_name):
    local_file_name = upload_file_path.split('/')[-1]
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
    print('\nUploading to Azure Storage as blob:\n\t' + local_file_name)
    with open(upload_file_path, "rb") as data:
        blob_client.upload_blob(data)
    return blob_client

def list_container_blobs(container):
    # List the blobs in the container
    container_client = blob_service_client.get_container_client(container)
    blob_list = container_client.list_blobs()
    print("\nListing blobs...")
    for blob in blob_list:
        print('\t' + blob.name)

upload_dir = 'C:/Users/johan/Documents/Code/mock-data-generator/data'
my_container = "enterprise-af7524b7-7bbe-4d1d-a19a-27ddaaa46338"
for file in os.listdir(upload_dir):
    upload_blob(upload_dir + '/' + file, blob_service_client, my_container)

list_container_blobs(my_container)
