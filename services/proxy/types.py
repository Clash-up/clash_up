import datetime
import typing

from pydantic import Field, NonNegativeFloat, NonNegativeInt, PositiveInt

from shared.pyd_models import ClashBasePydModel
from shared.types import BattleModifier, Role, WarState

# --- current war types ---


class ClanMemberAttack(ClashBasePydModel):
    attacker_tag: str
    defender_tag: str
    stars: NonNegativeInt
    destruction_percentage: NonNegativeFloat
    order: PositiveInt
    duration: PositiveInt


class ClanMemberInWar(ClashBasePydModel):
    tag: str
    name: str
    townhall_level: NonNegativeInt
    map_position: PositiveInt
    attacks: list[ClanMemberAttack]  # max 2
    opponent_attacks: NonNegativeInt
    best_opponent_attack: ClanMemberAttack


class ClanInWar(ClashBasePydModel):
    tag: str
    name: str
    attacks: NonNegativeInt
    stars: NonNegativeInt
    destruction_percentage: NonNegativeFloat
    members: list[ClanMemberInWar]


class CurrentWar(ClashBasePydModel):
    state: WarState
    team_size: NonNegativeInt
    attacks_per_member: NonNegativeInt
    battle_modifier: BattleModifier
    preparation_start_time: datetime.datetime
    start_time: datetime.datetime
    end_time: datetime.datetime
    clan: ClanInWar
    opponent: ClanInWar


# --- clan info types ---


class League(ClashBasePydModel):
    id: PositiveInt
    name: str


class BuilderBaseLeague(ClashBasePydModel):
    id: PositiveInt
    name: str


class ClanMember(ClashBasePydModel):
    tag: str
    name: str
    role: Role
    townhall_level: NonNegativeInt = Field(alias="townHallLevel")
    exp_level: NonNegativeInt
    league: League
    trophies: NonNegativeInt
    builder_base_trophies: NonNegativeInt
    clan_rank: PositiveInt
    # previous_clan_rank: PositiveInt
    donations: NonNegativeInt
    donations_received: NonNegativeInt
    builder_base_league: BuilderBaseLeague


class ChatLanguage(ClashBasePydModel):
    id: PositiveInt
    name: str
    language_code: str


class ClanLocation(ClashBasePydModel):
    id: PositiveInt
    name: str
    is_country: bool
    country_code: str


class ClanDistrict(ClashBasePydModel):
    id: PositiveInt
    name: str
    level: PositiveInt = Field(alias="districtHallLevel")


class ClanCapital(ClashBasePydModel):
    level: PositiveInt = Field(alias="capitalHallLevel")
    districts: list[ClanDistrict]


class ClanInfo(ClashBasePydModel):
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


# --- player types ---


class Player(ClashBasePydModel):
    tag: str
    name: str
    townhall_level: NonNegativeInt = Field(alias="townHallLevel")
    exp_level: NonNegativeInt
    trophies: NonNegativeInt
    # best_trophies: NonNegativeInt
    war_stars: NonNegativeInt
    attack_wins: NonNegativeInt
    defense_wins: NonNegativeInt
    # builder_hall_level: NonNegativeInt
    # builder_base_trophies: NonNegativeInt
    # best_builder_base_trophies: NonNegativeInt
    role: Role
    # war_preference: str
    donations: NonNegativeInt
    donations_received: NonNegativeInt
    # clan_capital_contributions: NonNegativeInt
    # clan: typing.Optional[dict[str, typing.Any]]
    # league: League
    # builder_base_league: BuilderBaseLeague
    # achievements: list[dict[str, typing.Any]]
    # player_house: dict[str, typing.Any]
    # labels: list[dict[str, typing.Any]]
    # troops: list[dict[str, typing.Any]]
    # heroes: list[dict[str, typing.Any]]
    # hero_equipment: list[dict[str, typing.Any]]
    # spells: list[dict[str, typing.Any]]
