# Schémas pour l'API : modèles de données pour validation et sérialisation
from .client_schema.client_schemas import ClientCreate, ClientUpdate, ClientResponse
from .commune_schema.commune_schemas import CommuneCreate, CommuneUpdate, CommuneResponse
from .commande_schema.commande_schemas import CommandeCreate, CommandeUpdate, CommandeResponse

from .user_schema import *
from .item_schema import ItemCreate, ItemRead, ItemUpdate, ItemDelete
from .department_schema import *