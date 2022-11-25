import timeit
from bs4 import BeautifulSoup as bs
from lxml import etree
import requests
import concurrent.futures
from urllib import parse
from Log import log

_URL2 = "https://pesquisa.marisa.com.br/busca?q="

class SamsClub():

    def start(self, names: list):
        start = timeit.default_timer()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for name in names:
                if(name != None):
                    futures.append(executor.submit(self.getByName, name=name))
        stop = timeit.default_timer()
        print("Time: ", stop -start)

    def getByName(self, name):
        try:
            links = self.searchByName(name)
            if len(links) > 0:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = []
                    for url in links:
                        if(url != None):
                            futures.append(executor.submit(self.getProduct, link=url))
        except Exception as e:
            log(f"{e}")

    def searchByName(self, name):
        links = []
        paginador = True
        iterador = 0
        while paginador:
            url = f"{_URL2}{parse.quote(name)}?page={iterador}"; 
            log(f"Request {url}")
            request = requests.get(url)
            htmlDoc = bs(request.text, "lxml")
            dom = etree.HTML(str(htmlDoc))
            products = dom.xpath("//div[@id='vitrine-container']//li//h4/a")
            if(products == None or len(products) == 0):
                log(f"Não foi possível encontrar produtos na página em {url}")
                break
            for product in products:
                links.append(str(product.attrib["href"]))

            error = dom.xpath("div[@class='sc-error-page-title']")
            if error is not None:
                log(f"Não foi possível encontrar produtos na página em {url}")
                break
            iterador += 45

        return links

    def getProduct(self, link):
        log(f"Estamos no getProduct {link}")