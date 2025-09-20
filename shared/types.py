from enum import StrEnum

from pydantic import BaseModel, ConfigDict, alias_generators


# Nie spotkałem się z niektórymi stanami, ale są w swaggerze coc'a
class WarState(StrEnum):
    CLAN_NOT_FOUND = "clan_not_found"
    ACCESS_DENIED = "access_denied"
    NOT_IN_WAR = "not_in_war"
    IN_MATCHMAKING = "in_matchmaking"
    ENTER_WAR = "enter_war"
    MATCHED = "matched"
    PREPARATION = "preparation"
    WAR = "war"
    IN_WAR = "in_war"
    ENDED = "ended"


class Role(StrEnum):
    NOT_MEMBER = "not_member"  # probably not used
    MEMBER = "member"
    LEADER = "leader"
    ELDER = "admin"
    COLEADER = "coLeader"


class BattleModifier(StrEnum):
    NONE = "none"
    HARD_MODE = "hard_mode"


class ClashBaseModel(BaseModel):
    model_config = ConfigDict(alias_generator=alias_generators.to_camel, populate_by_name=True)
