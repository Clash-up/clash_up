import datetime
import typing

from pydantic import Field, NonNegativeFloat, NonNegativeInt, PositiveInt

from shared.types import BattleModifier, ClashBaseModel, Role, WarState


class ClanMemberInWar(ClashBaseModel):
    tag: str
    name: str
    townhall_level: NonNegativeInt
    map_position: PositiveInt
    opponent_attacks: NonNegativeInt


class ClanInWar(ClashBaseModel):
    tag: str
    name: str
    attacks: NonNegativeInt
    stars: NonNegativeInt
    destruction_percentage: NonNegativeFloat
    members: list[ClanMemberInWar]


class CurrentWar(ClashBaseModel):
    state: WarState
    team_size: NonNegativeInt
    attacks_per_member: NonNegativeInt
    battle_modifier: BattleModifier
    preparation_start_time: datetime.datetime
    start_time: datetime.datetime
    end_time: datetime.datetime
    clan: ClanInWar
    opponent: ClanInWar


class League(ClashBaseModel):
    id: PositiveInt
    name: str


class BuilderBaseLeague(ClashBaseModel):
    id: PositiveInt
    name: str


class ClanMember(ClashBaseModel):
    tag: str
    name: str
    role: Role
    townhall_level: NonNegativeInt = Field(alias="townHallLevel")
    exp_level: NonNegativeInt
    league: League
    trophies: NonNegativeInt
    builder_base_trophies: NonNegativeInt
    clan_rank: PositiveInt
    previous_clan_rank: PositiveInt
    donations: NonNegativeInt
    donations_received: NonNegativeInt
    builder_base_league: BuilderBaseLeague


class ChatLanguage(ClashBaseModel):
    id: PositiveInt
    name: str
    language_code: str


class ClanLocation(ClashBaseModel):
    id: PositiveInt
    name: str
    is_country: bool
    country_code: str


class ClanDistrict(ClashBaseModel):
    id: PositiveInt
    name: str
    level: PositiveInt = Field(alias="districtHallLevel")


class ClanCapital(ClashBaseModel):
    level: PositiveInt = Field(alias="capitalHallLevel")
    districts: list[ClanDistrict]


class ClanInfo(ClashBaseModel):
    tag: str
    name: str
    description: str
    location: ClanLocation
    is_family_friendly: bool
    level: PositiveInt = Field(alias="clanLevel")
    clan_points: NonNegativeInt
    clan_builder_base_points: NonNegativeInt
    clan_capital_points: NonNegativeInt
    capital_league: dict[str, typing.Any]
    required_trophies: NonNegativeInt
    war_win_streak: NonNegativeInt
    war_wins: NonNegativeInt
    war_ties: NonNegativeInt
    war_losses: NonNegativeInt
    is_war_log_public: bool
    war_league: dict[str, typing.Any]
    members: NonNegativeInt
    member_list: list[ClanMember]
    required_builder_base_trophies: NonNegativeInt
    required_townhall_level: NonNegativeInt
    clan_capital: ClanCapital
    chat_language: ChatLanguage
