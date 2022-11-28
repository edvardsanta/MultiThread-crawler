from Config import MongoConfig, CrawlerConfig
from MongoService import startMongoClient
from Marisa import Marisa
from Log import log

def main():
   if CrawlerConfig.enableDb:
        MongoConfig.set("ConnectionString", "")
        Mongo = startMongoClient(MongoConfig.config("ConnectionString"))
   crawler = Marisa()
   log("Inciando crawler")
   crawler.start(CrawlerConfig.productToSearch) 

if __name__ == "__main__":
    main()



