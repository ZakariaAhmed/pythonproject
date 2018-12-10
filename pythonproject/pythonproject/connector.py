# Connecting towards google cloud api and map our tables
from google.cloud import bigquery
from ApiSettings import ApiSettings
# getting our confidential api info

settings = ApiSettings()
# Setup 
'''
client = bigquery.Client(project='totalkreditcrawler')
bucket_name = 'totalkreditbucket'
dataset_id = 'TotalKreditCrawler'
table_id = 'LoanCalculatorValues'
destination_uri = 'gs://{}/{}'.format(bucket_name, 'loancalculatorvalues.csv')
dataset_ref = client.dataset(dataset_id)
table_ref = dataset_ref.table(table_id)
table = client.get_table(table_ref)  
'''
'''
# Extract table to Google Cloud Storage
extract_job = client.extract_table(table_ref, destination_uri, location='EU') # API request
extract_job.result() # waits for the job to complete


# Load a JSON file from Cloud Storage
'''


class CrawlerEntity:
    def __init__(self, snippetName, snippetValue, snippetType, snippetResponseSelector):
        self.snippetName = snippetName
        self.snippetValue = snippetValue
        self.snippetType = snippetType
        self.snippetResponseSelector = snippetResponseSelector
        
class Website:
    def __init__(self, website, start_url):
        self.website = website
        self.start_url = start_url

def bqTable():
    client = bigquery.Client(project=settings.projectname)

