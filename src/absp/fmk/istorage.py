"""istorage module."""

class IStorage:

    def __init__(self, _mapper:dict):
        self.mapper_ = _mapper

    async def get(self, _interface:object, *args) -> object:
        return await self.mapper_[_interface](*args)
