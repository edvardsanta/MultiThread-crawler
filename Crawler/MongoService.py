from bson import Decimal128
from pymongo import MongoClient

from ProdcutNormalizeModel import ProductToNormalize_Seller_PriceModel, ProductToNormalize_SellerModel, ProductToNormalizeModel


def startMongoClient(ConnectionString):
    mongoClient = MongoClient(ConnectionString)
    return mongoClient

def toMongoModel(model: ProductToNormalizeModel):
    Product_Dict ={
            "id_task": str(model.IdTask),
            "id_crawler":  model.IdCrawler,
            "crawler_date": model.CrawlerDate,
            "product_name": model.ProductName,
            "product_link": model.ProductLink,
            "product_brand": model.ProductBrand,
            "product_ean": model.ProductEAN,
            "product_ncm": model.ProductNCM,
            "product_model": model.ProductModel,
            "site_sku": model.Sku,
            "source": model.Source,
            "text_search": model.TextSearch,
            "attributes": model.Attributes,
            "sellers": list(map(toMongoSellers, model.Sellers))
            }
    Product_Dict = {k:v for (k,v) in Product_Dict.items() if v is not None}
    return Product_Dict

def toMongoSellers(seller: ProductToNormalize_SellerModel):
    Sellers_Dict = {
            "stock_quantity" : seller.StockQuantity,
            "seller_name": seller.SellerName,
            "seller_address": seller.SellerAddress,
            "prices" : list(map(toMongoSellers, seller.Prices))
            }
    Sellers_Dict = {k:v for (k,v) in Sellers_Dict.items() if v is not None}
    return Sellers_Dict


def toMongoPrices(price: ProductToNormalize_Seller_PriceModel):
    Prices_Dict ={
                "price": Decimal128(str(price.Price)),
                "price_from": price.PriceFrom,
                "price_payment_type": price.PricePaymentType,
                "price_currency": price.PriceCurrency,
                "cashback_value": price.CashbackValue,
                "cashback_is_percent": price.CashbackIsPercent,
                "discount_value": price.DiscountValue,
                "discount_is_percent": price.DiscountIsPercent
                }
            #Filtragem para verificação de valor None
    Prices_Dict = {k:v for (k,v) in Prices_Dict.items() if v is not None and v != 0}
    return Prices_Dict