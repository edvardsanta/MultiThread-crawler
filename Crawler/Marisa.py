from threading import Lock
import timeit
from bs4 import BeautifulSoup as bs
from lxml import etree
import requests
import concurrent.futures
from urllib import parse
from Log import log
from ProdcutNormalizeModel import *
from StringExtensions import *

_URL1 = "https://marisa.com.br/"
_URL2 = "https://pesquisa.marisa.com.br/busca?q="
searchInParallel = 5
productInParallel = 1

lock = Lock()

class Marisa():

    def start(self, names: list):
        start = timeit.default_timer()
        with concurrent.futures.ThreadPoolExecutor(max_workers=searchInParallel) as executor:
            futures = []
            for name in names:
                if(name != None):
                    futures.append(executor.submit(self.getByName, name=name))
        stop = timeit.default_timer()
        print("Time: ", stop -start)

    def getByName(self, name):
        try:
            links = self.searchByName(name)
            self.getByLink(links)
        except Exception as e:
            log(f"{e}")

    def getByLink(self, links):
        with concurrent.futures.ThreadPoolExecutor(max_workers=productInParallel) as executor:
            futures = []
            for url in links:
                if(url != None):
                    futures.append(executor.submit(self.getProduct, link=f"https:{url}"))
        
            

    def searchByName(self, name):
        links = []
        paginador = True
        iterador = 1
        while paginador:
            lock.acquire()
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
            if iterador == 2:
                lock.release()
                break
            iterador += 1
            

        return links

    def getProduct(self, link):
        request = requests.get(link)
        htmlDoc = bs(request.text, "lxml")
        dom = etree.HTML(str(htmlDoc))
        productNormalize = ProductToNormalizeModel()
        productName = dom.xpath("//h1[@itemprop='name']")[0].text
        productNormalize.ProductName = productName
        sku = dom.xpath("//input[@class='productId']")[0].text
        productNormalize.Sku = sku
        productNormalize.ProductLink = link
        productSeller = productNormalize.GenerateSeller()
        seller = dom.xpath("//span[@class='product-brand-name']")[0].text
        productSeller.SellerName = "Marisa" if seller == None or len(seller) == 0  else seller
        productSeller.SellerLink = _URL1
        productPrice = productSeller.GeneratePrice()
        priceFrom = dom.xpath("//small[contains(@class, 'product--price-from')]")[0].text
        price = dom.xpath("//input[@class = 'productPrice']")[0].text
        productPrice.PriceFrom = priceFrom
        productPrice.Price = price


        



            
        