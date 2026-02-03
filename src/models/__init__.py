from .user import User
from .role import Role
from .item import Item
from .price import Price
from .stock import Stock
from .stock_line import StockLine
from .update import Update
from .shop import Shop
from .address import Address
from .zip_code import ZipCode
from .department import Department

User.model_rebuild()
Role.model_rebuild()
Role.model_rebuild()