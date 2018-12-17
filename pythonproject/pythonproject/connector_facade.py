# Connecting towards google cloud api and map our tables
from google.cloud import bigquery

# getting our confidential api info

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


class Crawler_entity:
    def __init__(self, snippet_name, snippet_value, snippet_type, snippet_response_selector):
        self.snippet_name = snippet_name
        self.snippet_value = snippet_value
        self.snippet_type = snippet_type
        self.snippet_response_selector = snippet_response_selector
        
class Website_table(object):
    def __init__(self, website = None, start_url = None, last_crawled = None, last_crawled_month = None, total_sites_crawled = None, crawl_in_progress = None, allowed_domains = None):
        self.website = website
        self.start_url = start_url
        self.last_crawled = last_crawled
        self.last_crawled_month = last_crawled_month
        self.total_sites_crawled = total_sites_crawled
        self.crawl_in_progress = crawl_in_progress
        self.allowed_domains = allowed_domains

# next website to crawl, gets called on every crawl opening
def get_next_website(current_month_timestamp):
    client = bigquery.Client(project='pythonproject-225120')
    dataset_ref = client.dataset('CrawlingData')
    table_ref = dataset_ref.table('websiteList')
    table = client.get_table(table_ref)
    rows = client.list_rows(table)
    web_table = []
    query = (
            'SELECT * FROM CrawlingData.websiteList  WHERE (lastCrawled < \'' + current_month_timestamp + '\' AND crawlInProgress is NULL) OR (lastCrawled < \'' + current_month_timestamp + '\' AND crawlInProgress = "0" ) ORDER BY lastCrawled ASC LIMIT 1'
    )
    query_job = client.query(
        query,
        location='US')
    # self reminder change back to EU once, I update the tables on Google Cloud Big Query :)
    for row in query_job:
        print(row)
        if row['allowedDomains'] != 'None':
            w_list = Website_table(row['website'], row['start_url'], row['lastCrawled'], row['lastCrawledMonth'], row['totalSitesCrawled'], row['crawlInProgress'], row['allowedDomains'])
            web_table.append(w_list)
        else:
            print('throw error')
    return web_table

# the values we want to look for on each page we crawl, called on each page
def bq_table():
    client = bigquery.Client(project='pythonproject-225120')
    dataset_id = 'CrawlingData'
    table_id = 'crawlerEntities'
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    table = client.get_table(table_ref)
    rows = client.list_rows(table)
    crawler_entities = []
    for row in rows:
        ce = Crawler_entity(row['snippetName'], row['snippetValue'], row['snippetType'], row['snippetResponseSelector'])
        crawler_entities.append(ce)
    return crawler_entities


# Update our timestamp on website table, called everytime a crawl is finished.
def update_time_stamp(last_crawled_month, total_sites_crawled, current_website, current_time, crawl_in_progress):
    client = bigquery.Client(project='pythonproject-225120')
    dataset_id = 'CrawlingData'
    table_id = 'websiteList'
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    table = client.get_table(table_id)
    rows = client.list_rows(table)
    websiteList = []
    _zero = '0'
    query = (
            'UPDATE `CrawlingData.websiteList` SET `LastCrawled` = \'' + current_time + '\', `LastCrawledMonth` = \'' + last_crawled_month + '\', `TotalSitesCrawled` = \'' + total_sites_crawled + '\', `CrawlInProgress` = \'' + crawl_in_progress + '\' WHERE AllowedDomains = \'' + current_website + '\''
    )
    print('updated timestamp')
    query_job = client.query(
        query,
        location='US')
    return query_job.result()

# response data Gets called when we find a value we looking for

def response_data(website, snippet_name, loation_path, crawled_date):
    client = bigquery.Client(project='pythoccnproject-225120')
    dataset_id = 'ResponseData'
    table_id = 'ResponseDataTable'
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    table = client.get_table(table_ref)
    rows_to_insert = [
        (website, snippet_name, loation_path, crawled_date)
    ]
    errors = client.insert_rows(table, rows_to_insert)
    return errors