from src.models.base import AddressBase
from src.schemas.commune_schema.commune_schemas import CommuneResponse
from src.schemas.zip_code_schema.zip_code_response import ZipCodeResponse


class AddressResponse(AddressBase):
    id: int
    commune: CommuneResponse
    zip_code: ZipCodeResponse