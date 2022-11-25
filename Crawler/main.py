from Config import MongoConfig, CrawlerConfig
from MongoService import startMongoClient
from SumsClub import SamsClub
from Log import log

def main():
   if CrawlerConfig.enableDb:
        MongoConfig.set("ConnectionString", "")
        Mongo = startMongoClient(MongoConfig.config("ConnectionString"))
   crawler = SamsClub()
   log("Inciando crawler")
   crawler.start(CrawlerConfig.productToSearch) 

if __name__ == "__main__":
    main()



