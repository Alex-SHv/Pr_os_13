from DTO.field_dto import FieldDTO
from DTO.fertilizer_dto import FertilizerDTO

class Mapper:
    @staticmethod
    def get_field_dto_list(num_fields: int, base_price: int):
        return [FieldDTO(index=i, price=base_price, is_unlocked=False) for i in range(num_fields)]

    @staticmethod
    def fertilizer_data_to_dto(name: str, data: dict):
        return FertilizerDTO(name=name, multiplier=data.get("multiplier", 1), price=data.get("price", 0))