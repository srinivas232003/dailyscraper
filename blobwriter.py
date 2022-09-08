from azure.storage.blob import AppendBlobService,BlobPermissions
from azure.storage.blob.baseblobservice import BaseBlobService
from datetime import datetime,timedelta
storage_account_key="your_azure_account_key"
storage_account_name="account_name"
connection_string='''connection_string'''
container_name="container_name"
blob_name="your_blob_name"
def append_data_to_blob(data):
  if data==[]:
    return None
  data='\n'.join([','.join(i) for i in data])
  service = AppendBlobService(account_name=storage_account_name, account_key=storage_account_key)
  try:
    service.append_blob_from_text(container_name=container_name, blob_name="ddmmyyy_verge.csv", text = data)
  except:
    service.create_blob(container_name=container_name, blob_name="ddmmyyy_verge.csv")
    service.append_blob_from_text(container_name=container_name, blob_name="ddmmyyy_verge.csv", text = data)
    print('Data Appended to Blob Successfully.')
def generate_link():
  url=f"https://{storage_account_name}.blob.core.windows.net/{container_name}/{blob_name}"
  service1=BaseBlobService(account_name=storage_account_name,account_key=storage_account_key)
  token=service1.generate_blob_shared_access_signature(container_name,blob_name,permission=BlobPermissions.READ,expiry=datetime.utcnow()+timedelta(minutes=5))
  url_sas=f"{url}?{token}"
  return url_sas