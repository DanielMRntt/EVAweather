class ConditionEntity:
    def __init__(self, id: int, name: str, description: str):
        self.id = id
        self.name = name
        self.description = description

    @staticmethod
    def from_dict(data: dict) -> 'ConditionEntity':
        return ConditionEntity(
            id=data.get('id'),
            name=data.get('name'),
            description=data.get('description')
        )

    def __repr__(self):
        return f"ConditionEntity(id={self.id}, name='{self.name}', description='{self.description}')"
