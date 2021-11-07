import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from shutil import which
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SpringerSpider(scrapy.Spider):
    name = 'springer'
    allowed_domains = ['www.springer.com']

    def start_requests(self):
        for i in range(1,30):
            keyword="data"
            yield SeleniumRequest(url=f"https://link.springer.com/search/page/{i}?date-facet-mode=between&query=%5B{keyword}%5D&facet-start-year=2017&facet-content-type=%22Article%22&facet-language=%22En%22&facet-end-year=2022", callback=self.parse_result)
    def parse_result(self, response):
        browser = response.meta["driver"]
        try:
            Cookies_acc = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[@id='onetrust-accept-btn-handler']"))
            ).click()
        except TimeoutException:
            pass
        links_document=response.xpath("//h2/a/@href").getall()
        for u in links_document:
            yield SeleniumRequest(url=response.urljoin(u),callback=self.data_results)

        
        next_page = response.xpath("//a[@title='next']/@href").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield SeleniumRequest(url=next_page, callback=self.parse_result,script="window.scrollTo(0, document.body.scrollHeight);")

    
    def data_results(self,response):
        Title_Articl = response.xpath("//header/h1/text()").get()
        Published_Articl = response.xpath("//a/time/text()").get()
        author_names = response.xpath("//a[@data-test='author-name']/text()").getall()
        Volume_Articl = response.xpath("//b[@data-test='journal-volume']/text()").getall()
        Pages_Articl = response.xpath("(//p[@class='c-article-info-details']/span)[1]/text()").getall()
        Price_Articl = response.xpath("(//div[@class='buybox__buy']/p)[3]/text()").getall()
        Abstract_Articl = response.xpath("//div[@id='Abs1-content']/p/text()").get()
        Key_words = response.xpath("//li[@class='c-article-subject-list__subject']/span/text()").getall()
        DOI_Articl = response.xpath("//span[@class='c-bibliographic-information__value']/a/text()").get()
        Affiliation_Adresses = response.xpath("//ol[@class='c-article-author-affiliation__list']/li/p[@class='c-article-author-affiliation__address']/text()").getall()
        Affiliation_Authors = response.xpath("//ol[@class='c-article-author-affiliation__list']/li/p[@class='c-article-author-affiliation__authors-list']/text()").getall()
        data = {
            "Title_Articl":Title_Articl,
            "Published_Articl":Published_Articl,
            "author_names":author_names,
            "Volume_Articl":Volume_Articl,
            "Pages_Articl":Pages_Articl,
            "Price_Articl":Price_Articl,
            "Abstract_Articl":Abstract_Articl,
            "Key_words":Key_words,
            "DOI_Articl":DOI_Articl,
            "Affiliation_Adresses":Affiliation_Adresses,
            "Affiliation_Authors":Affiliation_Authors


        }
        yield data