from decimal import Decimal
from builtins import str
import re
from typing_extensions import Self
class StringExtension(str):
    def init(self) -> None:
        super().init()

    @staticmethod
    def remove_no_decimal_chars(s: str) -> str:
        r"""
        Remove caracteres que NÂO são números(decimais)
        """
        s = re.sub("[^0-9.,]", "" , s)
        return s

    @staticmethod
    def remove_spaces(s: str) -> str:
        r"""
        Remove espaços
        """
        s = re.sub("\s+", "", s)
        return s

    @classmethod
    def strip_one_space(cls, s: str):
        r"""
        Remove apenas o espaço do começo ou do fim da string
        """
        if s.startswith(" "):
            s = s[1:]
        if s.endswith(" "):
            s = s[:-1]
        return s
    @classmethod
    def convert_to_currency(cls, param: str) -> Decimal:
        """
        Converte para moeda \n
        Remove caracteres que NÂO são números(decimais) -> Substituí caracteres ->
        Converte String para Decimal
        """
        param = cls.remove_no_decimal_chars(param)
        if (param == None or param == ""):
            return 0

        if "," in param:
            param = param.replace(".", "")
            param = param.replace(",", ".")
        decimal = Decimal(param)

        return decimal
