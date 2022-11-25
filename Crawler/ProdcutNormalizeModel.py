import datetime
from decimal import Decimal
import uuid

#region [ ProductToNormalize_Seller_Price ]
class ProductToNormalize_Seller_PriceModel:
    Price  : Decimal=None
    PriceFrom : Decimal=None
    PricePaymentType : str=None
    PriceCurrency : str=None
    CashbackValue : Decimal=None
    CashbackIsPercent : bool=None
    DiscountValue : Decimal=None
    DiscountIsPercent : bool=None
    Installments = []
#endregion

class ProductToNormalize_SellerModel:
    StockQuantity : Decimal=None
    SellerName : str=None
    SellerAddress : str=None
    Prices: list=None
    Shippings :list=None

    #region Add
    def AddPrice(self, model: ProductToNormalize_Seller_PriceModel) -> ProductToNormalize_Seller_PriceModel:
        """Adiciona o objeto à lista (Prices)"""
        if (self.Prices is None):
            self.Prices = []

        self.Prices.append(model)
        self.VerifyPricesIntegrid()
        return model
    #endregion

    #region Generate
    @classmethod
    def GeneratePrice(cls, autoInsertInList = False) -> ProductToNormalize_Seller_PriceModel:
        """Gera um novo objeto Price"""
        price = ()
        if(autoInsertInList):
            cls.AddPrice(model=price)

        return price
#endregion

class ProductToNormalizeModel:
    IdTask : uuid=None
    IdCrawler : int=None
    ProductName : str=None
    ProductLink : str=None
    ProductBrand :str=None
    ProductEAN :str=None
    ProductNCM : str=None
    ProductModel : str=None
    Sku : str=None
    CrawlerDate : datetime=None
    Source : str=None
    TextSearch : str=None
    Sellers: list=None 
    Attributes: list=None
    
    #region Add
    @classmethod
    def AddSeller(cls, model: ProductToNormalize_SellerModel) -> ProductToNormalize_SellerModel:
        r"""Adiciona o objeto à lista (Sellers)"""
        if (cls.Sellers == None):
            cls.Sellers = []
        cls.Sellers.append(model)

        return model
    #endregion

    #region Generate
    @classmethod
    def GenerateSeller(cls, autoInsertInList = False) -> ProductToNormalize_SellerModel:
        r"""Gera um objeto-modelo do Seller"""
        seller = ProductToNormalize_SellerModel()
        if(autoInsertInList):
            cls.AddSeller(seller)
        return seller
    #endregion
    



