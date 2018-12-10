from ApiSettings import ApiSettings
from google.cloud import bigquery

apk = ApiSettings()

class WebsiteList(object):
    def __init__(self, website = None, start_url = None, lastCrawled = None, lastCrawledMonth = None, totalSitesCrawled = None, crawlInProgress = None, allowedDomains = None):
        self.website = website
        self.start_url = start_url
        self.lastCrawled = lastCrawled
        self.lastCrawledMonth = lastCrawledMonth
        self.totalSitesCrawled = totalSitesCrawled
        self.crawlInProgress = crawlInProgress
        self.allowedDomains = allowedDomains

    # next Website to crawl
    @classmethod
    def getNextWebsite(self, currentMonthTimeStamp):
        client = bigquery.Client(project=apk.projectname)
        dataset_ref = client.dataset(apk.websitelistDataSet)
        table_ref = dataset_ref.table(apk.websitelistTableId)
        table = client.get_table(table_ref)
        rows = client.list_rows(table)
        webTable = []
        query = (
                'SELECT * FROM TotalKreditCrawler.websites_2 WHERE (LastCrawled < \'' + currentMonthTimeStamp + '\' AND CrawlInProgress is NULL) OR (LastCrawled < \'' + currentMonthTimeStamp + '\' AND CrawlInProgress = "0" ) ORDER BY LastCrawled ASC LIMIT 1'
        )
        query_job = client.query(
            query,
            location='US')
        # self reminder change back to EU once, I update the tables on Google Cloud Big Query :)
        for row in query_job:
            print(row)
            if row['AllowedDomains'] != 'None':
                wlList = WebsiteList(row['website'], row['start_url'], row['lastCrawled'], row['lastCrawledMonth'], row['totalSitesCrawled'], row['crawlInProgress'], row['allowedDomains'])
                webTable.append(wlList)
            else:
                print('throw error')
        return webTable