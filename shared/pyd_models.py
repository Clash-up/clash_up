import uuid

from pydantic import BaseModel, ConfigDict, NonNegativeInt, alias_generators, computed_field

from shared.types import Role


class ClashBasePydModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=alias_generators.to_camel, populate_by_name=True, from_attributes=True
    )


class WarEntryRead(ClashBasePydModel):
    stars: NonNegativeInt | None
    destruction_percentage: NonNegativeInt | None
    duration: NonNegativeInt | None


class PlayerRead(ClashBasePydModel):
    id: uuid.UUID
    name: str
    tag: str
    trophies: NonNegativeInt
    donations: NonNegativeInt
    donations_received: NonNegativeInt
    role: Role
    town_hall_level: NonNegativeInt
    cw_attacks_grouped: list[list[WarEntryRead]]

    @computed_field(return_type=NonNegativeInt)
    @property
    def total_cw_attacks(self) -> NonNegativeInt:
        return sum(len(group) for group in self.cw_attacks_grouped)

    @computed_field(return_type=NonNegativeInt)
    @property
    def max_cw_attacks(self) -> NonNegativeInt:
        return 2 * len(self.cw_attacks_grouped)
