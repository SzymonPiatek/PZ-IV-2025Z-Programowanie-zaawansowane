class Entity:
    _counters = {}

    def __init__(self, name: str, entity_type: str) -> None:
        self.name = name
        self.entity_type = entity_type.lower()

        count = Entity._counters.get(self.entity_type, 0) + 1
        Entity._counters[self.entity_type] = count
        self.id = count

    def key(self) -> str:
        return f"{self.entity_type}_{self.id}"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, name={self.name}, entity_type={self.entity_type})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Entity):
            return False
        return (
                self.id == other.id
                and self.entity_type == other.entity_type
                and self.name == other.name
        )

    def __repr__(self) -> str:
        return str(self)


class Cat(Entity):
    def __init__(self, name: str):
        super().__init__(name=name, entity_type="Cat")


class Dog(Entity):
    def __init__(self, name: str):
        super().__init__(name=name, entity_type="Dog")


class Human(Entity):
    def __init__(self, name: str):
        super().__init__(name=name, entity_type="Human")
