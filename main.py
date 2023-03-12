# References
# https://docs.scrapy.org/en/latest/_modules/scrapy/signalmanager.html?highlight=dispatcher#
# https://stackoverflow.com/questions/12394184/scrapy-call-a-function-when-a-spider-quits
# https://stackoverflow.com/questions/53747127/scrapy-crawler-process-setting
# https://towardsdatascience.com/how-to-run-scrapy-from-a-script-ff07fd6b792b
# https://stackoverflow.com/questions/34528524/scrapy-closespider-pagecount-setting-dont-work-as-should

import json
import scrapy
from scrapy.crawler import CrawlerProcess
import plot_graph
from scrapy import signals
from pydispatch import dispatcher

class Query(scrapy.Spider):
    name = "spidey"

    custom_settings = {
        'DOWNLOAD_TIMEOUT': 200,
        'CLOSESPIDER_PAGECOUNT': 300,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'DOWNLOAD_DELAY': 1
    }

    def __init__(self):

        super()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

        self.url_main = "https://firststop.sos.nd.gov/api/Records/businesssearch"

        self.url_business = "https://firststop.sos.nd.gov/api/FilingDetail/business/{}/false"

        self.data = {
            "SEARCH_VALUE": "X",
            "STARTS_WITH_YN": "true",
            "ACTIVE_ONLY_YN": "true"
        }

        self.headers_main = {
            "Content-Type": "application/json"
        }

        self.headers_business = {
            "accept": "*/*",
            "Content-Type": "application/json",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fr;q=0.8,hi;q=0.7",
            "authorization": "undefined",
            "referer": "https://firststop.sos.nd.gov/search/business",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
        }

        self.do_additional_check_on_business_name = True

        self.results = {}

    def start_requests(self):

        yield scrapy.http.JsonRequest(
            url=self.url_main,
            data=self.data,
            callback=self.parse_main_response,
        )

    def check_if_name_starts_with_X(self, business_name):

        first_letter = business_name.strip()[0].upper()
        return first_letter == "X"

    def parse_main_response(self, response):

        businessesData = json.loads(response.text)['rows']

        for business_id, business_data in businessesData.items():

            business_name = business_data["TITLE"][0]

            if not self.check_if_name_starts_with_X(business_name):
                continue

            business_data["TITLE"] = business_name
            self.results[business_id] = business_data

            yield scrapy.http.Request(
                url=self.url_business.format(business_id),
                headers=self.headers_business,
                method='GET',
                callback=self.parse_each_business_response,
                cb_kwargs={'business_id': business_id}
                )

    def parse_each_business_response(self, response, business_id):

        drawer_data = json.loads(response.text)['DRAWER_DETAIL_LIST']
        business_data = self.results[business_id]

        for section in drawer_data:
            business_data[section['LABEL']] = section['VALUE']

    
    def spider_closed(self, spider):

        with open('businesses_data.json', 'w') as destf:
            json.dump(self.results, destf)


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(Query)
    process.start()

    plot_graph.plot_businesses()