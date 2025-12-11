class FieldDTO:
    def __init__(self, index: int, price: int, is_unlocked: bool = False, fertilizer_name: str = None):
        self.index = index
        self.price = price
        self.is_unlocked = is_unlocked
        self.fertilizer_name = fertilizer_name