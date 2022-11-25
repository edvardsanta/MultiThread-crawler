class MongoConfig():

    __conf = {
    "ConnectionString": "",

    "ProductsToNormalizeCollection": 
    {
      "DataBaseName": "test_normalizer",
      "CollectionName": "products_to_normalize"
    },
    "LogCollection": 
    {
      "DataBaseName": "log",
      "CollectionName": "crawler_app_log"
    },
    "CrawlerStatusLogCollection": 
    {
      "DataBaseName": "test_normalizer",
      "CollectionName": "log_crawler_status"
    }
            }

    setters = ["ConnectionString", "password"]

    @staticmethod
    def config(name):
      return MongoConfig.conf[name]

    @staticmethod
    def set(name, value):
      if name in MongoConfig.setters:
        MongoConfig.conf[name] = value
      else:
        raise NameError("Name not accepted in set() method")
        

class CrawlerConfig():

    enableDb: bool=False
    productToSearch = ["vestido", "sapato", "camisa"]

    
        
