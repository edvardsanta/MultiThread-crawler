import asyncio
import logging
import threading
from time import sleep
import timeit
import aiohttp
import requests
from multiprocessing import Pool
from lxml import etree
from bs4 import BeautifulSoup
import concurrent.futures
_URL = "https://www.dafiti.com.br/catalog/?q={@name}"

def Search() -> list:
    links : list= []
    page: int = 1

    url = _URL.replace("{@name}", "vestido")
    request = requests.get(url)
    sleep(1)
    if(request.status_code == 200):
        htmlDoc = BeautifulSoup(request.text, "lxml")
        dom = etree.HTML(str(htmlDoc))
        products = dom.xpath("//div[@class='product-box']/div/a")
        if(products == None or len(products) == 0):
            return None
        for product in products:
            links.append(str(product.attrib["href"]))
    return links

async def GetProductAsync(link: str):
     async with aiohttp.ClientSession() as request:
        async with request.get(link) as resp:
            response = await resp.text()
            logging.info(f"OK em {link}")

def GetProduct(link : str):
    logging.info(f"Estamos aqui {link}")
    r = requests.get(link)
    if(r.status_code == 200):
        logging.info(f"ok em {link}")

async def GatherTasks():
    logging.info("Main started")
    logging.info("Criando mulitplas tasks")
    await asyncio.gather(*[GetProductAsync(url) for url in links]) # awaits completion of all tasks
    logging.info("Main Ended")

links = Search()

if __name__ == '__main__':    
    #Log
    logger_format = '%(asctime)s: %(threadName)s: %(message)s'
    logging.basicConfig(format=logger_format, level=logging.INFO, datefmt="%H:%M:%S")


    logging.info("thread pool executor")
    start = timeit.default_timer()    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for url in links:
            if(url != None):
                futures.append(executor.submit(GetProduct, link=url))
    stop = timeit.default_timer()
    print("Time: ", stop -start)

    logging.info("Thread Creation")
    threads = [threading.Thread(target=GetProduct, args=(url,)) for url in links]
    start = timeit.default_timer()
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join() 
    stop = timeit.default_timer()
    print("Time: ", stop -start)


    logging.info("Multiprocessing log")
    with Pool(len(links)) as p:
        start = timeit.default_timer()
        print(f"Quantidade de produtos encontrados {len(links)}")
        threadsParallel = p.map(GetProduct, links)
        stop = timeit.default_timer()
        print("Time: ", stop -start)

    logging.info("Single Thread Async") 
    start = timeit.default_timer()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(GatherTasks())
    stop = timeit.default_timer()
    print("Time: ", stop -start)

