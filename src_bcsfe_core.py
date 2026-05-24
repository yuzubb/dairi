# === COMBINED FILE ===
# フォルダ: src_bcsfe_core
# 元ファイル(8件): __init__.py, country_code.py, crypto.py, game_version.py, locale_handler.py, log.py, max_value_helper.py, theme_handler.py

# ============================================================
# FILE: __init__.py
# ============================================================
from __future__ import annotations
from typing import Any

from requests.exceptions import ConnectionError
from requests import Response
from json.decoder import JSONDecodeError
from bcsfe.cli import color, dialog_creator

from bcsfe.core import (
    country_code,
    crypto,
    game,
    game_version,
    io,
    locale_handler,
    log,
    server,
    theme_handler,
    max_value_helper,
)
from bcsfe.core.country_code import CountryCode, CountryCodeType
from bcsfe.core.crypto import Hash, HashAlgorithm, Hmac, NyankoSignature, Random
from bcsfe.core.game.battle.battle_items import BattleItems
from bcsfe.core.game.battle.cleared_slots import ClearedSlots
from bcsfe.core.game.battle.slots import LineUps
from bcsfe.core.game.battle.enemy import (
    Enemy,
    EnemyNames,
    EnemyDescriptions,
    EnemyDictionary,
)
from bcsfe.core.game.catbase.beacon_base import BeaconEventListScene
from bcsfe.core.game.catbase.cat import (
    Cat,
    Cats,
    UnitBuy,
    TalentData,
    NyankoPictureBook,
    StorageItem,
)
from bcsfe.core.game.catbase.gambling import GamblingEvent
from bcsfe.core.game.catbase.gatya import (
    Gatya,
    GatyaInfos,
    GatyaDataSet,
    GatyaDataOptionSet,
    GatyaDataOption,
)
from bcsfe.core.game.catbase.gatya_item import (
    GatyaItemBuy,
    GatyaItemNames,
    GatyaItemCategory,
    GatyaItemBuyItem,
)
from bcsfe.core.game.catbase.item_pack import (
    ItemPack,
    Purchases,
    PurchaseSet,
    PurchasedPack,
)
from bcsfe.core.game.catbase.login_bonuses import LoginBonus
from bcsfe.core.game.catbase.matatabi import Matatabi
from bcsfe.core.game.catbase.drop_chara import CharaDrop
from bcsfe.core.game.catbase.medals import Medals, MedalNames
from bcsfe.core.game.catbase.mission import (
    Missions,
    MissionNames,
    MissionConditions,
)
from bcsfe.core.game.catbase.my_sale import MySale
from bcsfe.core.game.catbase.nyanko_club import NyankoClub
from bcsfe.core.game.catbase.officer_pass import OfficerPass
from bcsfe.core.game.catbase.powerup import PowerUpHelper
from bcsfe.core.game.catbase.scheme_items import SchemeItems
from bcsfe.core.game.catbase.special_skill import (
    SpecialSkills,
    SpecialSkill,
    AbilityData,
    AbilityDataItem,
)

from bcsfe.core.game.catbase.stamp import StampData
from bcsfe.core.game.catbase.talent_orbs import (
    TalentOrb,
    TalentOrbs,
    OrbInfo,
    OrbInfoList,
    RawOrbInfo,
    SaveOrb,
    SaveOrbs,
)
from bcsfe.core.game.catbase.unlock_popups import (
    UnlockPopups,
    UnlockPopupData,
    UnlockPopupLine,
)
from bcsfe.core.game.catbase.upgrade import Upgrade
from bcsfe.core.game.catbase.user_rank_rewards import (
    UserRankRewards,
    RankGifts,
    RankGiftDescriptions,
)
from bcsfe.core.game.catbase.playtime import PlayTime
from bcsfe.core.game.gamoto.base_materials import BaseMaterials
from bcsfe.core.game.gamoto.cat_shrine import CatShrine, CatShrineLevels
from bcsfe.core.game.gamoto.gamatoto import (
    Gamatoto,
    GamatotoLevels,
    GamatotoMembersName,
)
from bcsfe.core.game.gamoto.ototo import Ototo
from bcsfe.core.game.localizable import Localizable
from bcsfe.core.game.map.aku import AkuChapters
from bcsfe.core.game.map.challenge import ChallengeChapters
from bcsfe.core.game.map.chapters import Chapters
from bcsfe.core.game.map.dojo import Dojo
from bcsfe.core.game.map.enigma import Enigma
from bcsfe.core.game.map.event import EventChapters
from bcsfe.core.game.map.ex_stage import ExChapters
from bcsfe.core.game.map.gauntlets import GauntletChapters
from bcsfe.core.game.map.item_reward_stage import ItemRewardChapters
from bcsfe.core.game.map.legend_quest import LegendQuestChapters
from bcsfe.core.game.map.map_reset import MapResets
from bcsfe.core.game.map.outbreaks import Outbreaks
from bcsfe.core.game.map.story import StoryChapters, TreasureText, StageNames
from bcsfe.core.game.map.timed_score import TimedScoreChapters
from bcsfe.core.game.map.tower import TowerChapters
from bcsfe.core.game.map.uncanny import UncannyChapters
from bcsfe.core.game.map.zero_legends import ZeroLegendsChapters
from bcsfe.core.game.map.map_names import MapNames
from bcsfe.core.game.map.map_option import MapOption
from bcsfe.core.game_version import GameVersion
from bcsfe.core.io.adb_handler import AdbHandler, AdbNotInstalled
from bcsfe.core.io.waydroid import WayDroidHandler
from bcsfe.core.io.bc_csv import CSV, Delimeter, Row
from bcsfe.core.io.command import Command, CommandResult
from bcsfe.core.io.config import Config, ConfigKey
from bcsfe.core.io.data import Data
from bcsfe.core.io.json_file import JsonFile
from bcsfe.core.io.path import Path
from bcsfe.core.io.save import SaveError, SaveFile, CantDetectSaveCCError
from bcsfe.core.io.thread_helper import thread_run_many, Thread
from bcsfe.core.io.yaml import YamlFile
from bcsfe.core.io.git_handler import GitHandler, Repo
from bcsfe.core.io.root_handler import RootHandler
from bcsfe.core.locale_handler import (
    LocalManager,
    ExternalLocaleManager,
    ExternalLocale,
)
from bcsfe.core.log import Logger
from bcsfe.core.server.event_data import (
    ServerItemData,
    ServerItemDataItem,
    ServerGatyaData,
    ServerGatyaDataSet,
    ServerGatyaDataItem,
)
from bcsfe.core.server.client_info import ClientInfo
from bcsfe.core.server.game_data_getter import GameDataGetter
from bcsfe.core.server.headers import AccountHeaders
from bcsfe.core.server.managed_item import (
    BackupMetaData,
    ManagedItem,
    ManagedItemType,
)
from bcsfe.core.server.request import RequestHandler, MultiPartFile, MultipartForm
from bcsfe.core.server.server_handler import ServerHandler
from bcsfe.core.server.updater import Updater
from bcsfe.core.theme_handler import (
    ThemeHandler,
    ExternalTheme,
    ExternalThemeManager,
)
from bcsfe.core.max_value_helper import MaxValueHelper, MaxValueType


class CoreData:
    def init_data(self):
        self.config = Config(config_path, print_config_err)
        self.logger = Logger(log_path)
        self.local_manager = LocalManager()
        self.theme_manager = ThemeHandler()
        self.max_value_manager = MaxValueHelper()
        self.game_data_getter: GameDataGetter | None = None
        self.gatya_item_names: GatyaItemNames | None = None
        self.gatya_item_buy: GatyaItemBuy | None = None
        self.chara_drop: CharaDrop | None = None
        self.gamatoto_levels: GamatotoLevels | None = None
        self.gamatoto_members_name: GamatotoMembersName | None = None
        self.localizable: Localizable | None = None
        self.abilty_data: AbilityData | None = None
        self.enemy_names: EnemyNames | None = None
        self.rank_gift_descriptions: RankGiftDescriptions | None = None
        self.rank_gifts: RankGifts | None = None
        self.treasure_text: TreasureText | None = None
        self.cat_shrine_levels: CatShrineLevels | None = None
        self.medal_names: MedalNames | None = None
        self.mission_names: MissionNames | None = None
        self.mission_conditions: MissionConditions | None = None

    def get_game_data_getter(
        self,
        save: SaveFile | None = None,
        cc: CountryCode | None = None,
        gv: GameVersion | None = None,
    ) -> GameDataGetter:
        if self.game_data_getter is None:
            if cc is None and save is not None:
                cc = save.cc
            if cc is None:
                raise ValueError("cc must be provided if save is not provided")
            if gv is None and save is not None:
                gv = save.game_version
            if gv is None:
                raise ValueError("gv must be provided if save is not provided")
            self.game_data_getter = GameDataGetter(cc, gv)
        return self.game_data_getter

    def get_gatya_item_names(self, save: SaveFile) -> GatyaItemNames:
        if self.gatya_item_names is None:
            self.gatya_item_names = GatyaItemNames(save)
        return self.gatya_item_names

    def get_gatya_item_buy(self, save: SaveFile) -> GatyaItemBuy:
        if self.gatya_item_buy is None:
            self.gatya_item_buy = GatyaItemBuy(save)
        return self.gatya_item_buy

    def get_chara_drop(self, save: SaveFile) -> CharaDrop:
        if self.chara_drop is None:
            self.chara_drop = CharaDrop(save)
        return self.chara_drop

    def get_gamatoto_levels(self, save: SaveFile) -> GamatotoLevels:
        if self.gamatoto_levels is None:
            self.gamatoto_levels = GamatotoLevels(save)
        return self.gamatoto_levels

    def get_gamatoto_members_name(self, save: SaveFile) -> GamatotoMembersName:
        if self.gamatoto_members_name is None:
            self.gamatoto_members_name = GamatotoMembersName(save)
        return self.gamatoto_members_name

    def get_localizable(self, save: SaveFile) -> Localizable:
        if self.localizable is None:
            self.localizable = Localizable(save)
        return self.localizable

    def get_ability_data(self, save: SaveFile) -> AbilityData:
        if self.abilty_data is None:
            self.abilty_data = AbilityData(save)
        return self.abilty_data

    def get_enemy_names(self, save: SaveFile) -> EnemyNames:
        if self.enemy_names is None:
            self.enemy_names = EnemyNames(save)
        return self.enemy_names

    def get_rank_gift_descriptions(self, save: SaveFile) -> RankGiftDescriptions:
        if self.rank_gift_descriptions is None:
            self.rank_gift_descriptions = RankGiftDescriptions(save)
        return self.rank_gift_descriptions

    def get_rank_gifts(self, save: SaveFile) -> RankGifts:
        if self.rank_gifts is None:
            self.rank_gifts = RankGifts(save)
        return self.rank_gifts

    def get_treasure_text(self, save: SaveFile) -> TreasureText:
        if self.treasure_text is None:
            self.treasure_text = TreasureText(save)
        return self.treasure_text

    def get_cat_shrine_levels(self, save: SaveFile) -> CatShrineLevels:
        if self.cat_shrine_levels is None:
            self.cat_shrine_levels = CatShrineLevels(save)
        return self.cat_shrine_levels

    def get_medal_names(self, save: SaveFile) -> MedalNames:
        if self.medal_names is None:
            self.medal_names = MedalNames(save)
        return self.medal_names

    def get_mission_names(self, save: SaveFile) -> MissionNames:
        if self.mission_names is None:
            self.mission_names = MissionNames(save)
        return self.mission_names

    def get_mission_conditions(self, save: SaveFile) -> MissionConditions:
        if self.mission_conditions is None:
            self.mission_conditions = MissionConditions(save)
        return self.mission_conditions

    def get_lang(self, save: SaveFile) -> str:
        return self.get_localizable(save).get_lang() or "en"


config_path = None
print_config_err = True
log_path = None


def set_config_path(path: Path):
    global config_path
    config_path = path


def set_log_path(path: Path):
    global log_path
    log_path = path


def update_external_content(_: Any = None):
    """Updates external content."""

    color.ColoredText.localize("updating_external_content")
    print()
    ExternalThemeManager.update_all_external_themes()
    ExternalLocaleManager.update_all_external_locales()
    core_data.init_data()

    clear_game_data = dialog_creator.YesNoInput().get_input_once("clear_game_data_q")
    if clear_game_data is None:
        return

    if clear_game_data:
        GameDataGetter.delete_old_versions(0)
        color.ColoredText.localize("cleared_game_data")


def print_no_internet():
    color.ColoredText.localize("no_internet")


core_data = CoreData()


def localize(key: str, escape: bool = True, **kwargs: Any) -> str:
    return core_data.local_manager.get_key(key, escape=escape, **kwargs)


__all__ = [
    "server",
    "io",
    "locale_handler",
    "country_code",
    "log",
    "game_version",
    "crypto",
    "game",
    "theme_handler",
    "max_value_helper",
    "AdbHandler",
    "AdbNotInstalled",
    "CountryCode",
    "Path",
    "Data",
    "CSV",
    "ServerHandler",
    "GameVersion",
    "SaveFile",
    "JsonFile",
    "ManagedItem",
    "ManagedItemType",
    "BackupMetaData",
    "Cat",
    "Upgrade",
    "PowerUpHelper",
    "TalentOrb",
    "TalentOrbs",
    "OrbInfo",
    "OrbInfoList",
    "RawOrbInfo",
    "SaveOrb",
    "SaveOrbs",
    "ConfigKey",
    "SpecialSkill",
    "WayDroidHandler",
    "EnemyDescriptions",
    "EnemyDictionary",
    "GatyaItemCategory",
    "ServerItemData",
    "GatyaItemBuyItem",
    "ServerItemDataItem",
    "ServerGatyaData",
    "ServerGatyaDataSet",
    "ServerGatyaDataItem",
    "GatyaDataOptionSet",
    "GatyaDataOption",
    "MaxValueType",
    "GamblingEvent",
    "UnitBuy",
    "NyankoPictureBook",
    "StorageItem",
    "OfficerPass",
    "LocalManager",
    "MapOption",
    "CantDetectSaveCCError",
    "UnlockPopupData",
    "UnlockPopupLine",
]


# ============================================================
# FILE: country_code.py
# ============================================================
from __future__ import annotations
import enum
from bcsfe.cli import dialog_creator
from bcsfe import core


class CountryCodeType(enum.Enum):
    EN = "en"
    JP = "jp"
    KR = "kr"
    TW = "tw"


class CountryCode:
    def __init__(self, cc: str | CountryCodeType):
        self.value = cc.value if isinstance(cc, CountryCodeType) else cc
        self.value = self.value.lower()

    def get_code(self) -> str:
        return self.value

    def get_client_info_code(self) -> str:
        code = self.get_code()
        if code == "jp":
            return "ja"
        return code

    def get_patching_code(self) -> str:
        code = self.get_code()
        if code == "jp":
            return ""
        return code

    @staticmethod
    def from_patching_code(code: str) -> CountryCode:
        if code == "":
            return CountryCode(CountryCodeType.JP)
        return CountryCode(code)

    @staticmethod
    def from_code(code: str) -> CountryCode:
        return CountryCode(code)

    @staticmethod
    def get_all() -> list["CountryCode"]:
        return [CountryCode(cc) for cc in CountryCodeType]

    @staticmethod
    def get_all_str() -> list[str]:
        ccts = CountryCode.get_all()
        return [cc.get_code() for cc in ccts]

    def __str__(self) -> str:
        return self.get_code()

    def __repr__(self) -> str:
        return self.get_code()

    def copy(self) -> CountryCode:
        return self

    @staticmethod
    def select() -> CountryCode | None:
        index = dialog_creator.ChoiceInput.from_reduced(
            CountryCode.get_all_str(),
            dialog="country_code_select",
            single_choice=True,
        ).single_choice()
        if index is None:
            return None
        return CountryCode.get_all()[index - 1]

    @staticmethod
    def select_from_ccs(ccs: list[CountryCode]) -> CountryCode | None:
        index = dialog_creator.ChoiceInput.from_reduced(
            [cc.get_code() for cc in ccs],
            dialog="country_code_select",
            single_choice=True,
        ).single_choice()
        if index is None:
            return None
        return ccs[index - 1]

    def __eq__(self, o: object) -> bool:
        if isinstance(o, CountryCode):
            return self.get_code() == o.get_code()
        elif isinstance(o, str):
            return self.get_code() == o
        elif isinstance(o, CountryCodeType):
            return self.get_code() == o.value
        return False

    def get_cc_lang(self) -> core.CountryCode:
        if core.core_data.config.get_bool(core.ConfigKey.FORCE_LANG_GAME_DATA):
            locale = core.core_data.config.get_str(core.ConfigKey.LOCALE)
            return core.CountryCode.from_code(locale)
        return self

    @staticmethod
    def get_langs() -> list[str]:
        return ["de", "it", "es", "fr", "th"]

    def is_lang(self) -> bool:
        return self.get_code() in CountryCode.get_langs()


# ============================================================
# FILE: crypto.py
# ============================================================
from __future__ import annotations
import enum
import hashlib
import hmac
import random
from bcsfe import core


class HashAlgorithm(enum.Enum):
    """An enum representing a hash algorithm."""

    MD5 = enum.auto()
    SHA1 = enum.auto()
    SHA256 = enum.auto()


class Hash:
    """A class to hash data."""

    def __init__(self, algorithm: HashAlgorithm):
        """Initializes a new instance of the Hash class.

        Args:
            algorithm (HashAlgorithm): The hash algorithm to use.
        """
        self.algorithm = algorithm

    def get_hash(
        self,
        data: core.Data,
        length: int | None = None,
    ) -> core.Data:
        """Gets the hash of the given data.

        Args:
            data (core.Data): The data to hash.
            length (int | None, optional): The length of the hash. Defaults to None.

        Raises:
            ValueError: Invalid hash algorithm.

        Returns:
            core.Data: The hash of the data.
        """
        if self.algorithm == HashAlgorithm.MD5:
            hash = hashlib.md5()
        elif self.algorithm == HashAlgorithm.SHA1:
            hash = hashlib.sha1()
        elif self.algorithm == HashAlgorithm.SHA256:
            hash = hashlib.sha256()
        else:
            raise ValueError("Invalid hash algorithm")
        hash.update(data.get_bytes())
        if length is None:
            return core.Data(hash.digest())
        return core.Data(hash.digest()[:length])


class Random:
    """A class to get random data"""

    @staticmethod
    def get_bytes(length: int) -> bytes:
        """Gets random bytes.

        Args:
            length (int): The length of the bytes.

        Returns:
            bytes: The random bytes.
        """
        return bytes(random.getrandbits(8) for _ in range(length))

    @staticmethod
    def get_alpha_string(length: int) -> str:
        """Gets a random string of the given length.

        Args:
            length (int): The length of the string.

        Returns:
            str: The random string.
        """
        characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return "".join(random.choice(characters) for _ in range(length))

    @staticmethod
    def get_hex_string(length: int) -> str:
        """Gets a random hex string of the given length.

        Args:
            length (int): The length of the string.

        Returns:
            str: The random string.
        """
        characters = "0123456789abcdef"
        return "".join(random.choice(characters) for _ in range(length))

    @staticmethod
    def get_digits_string(length: int) -> str:
        """Gets a random digits string of the given length.

        Args:
            length (int): The length of the string.

        Returns:
            str: The random string.
        """
        characters = "0123456789"
        return "".join(random.choice(characters) for _ in range(length))


class Hmac:
    def __init__(self, algorithm: HashAlgorithm):
        self.algorithm = algorithm

    def get_hmac(self, key: core.Data, data: core.Data) -> core.Data:
        if self.algorithm == HashAlgorithm.MD5:
            alg = hashlib.md5
        elif self.algorithm == HashAlgorithm.SHA1:
            alg = hashlib.sha1
        elif self.algorithm == HashAlgorithm.SHA256:
            alg = hashlib.sha256
        else:
            raise ValueError("Invalid hash algorithm")
        hmac_data = hmac.new(
            key.get_bytes(), data.get_bytes(), digestmod=alg
        ).digest()
        return core.Data(hmac_data)


class NyankoSignature:
    def __init__(self, inquiry_code: str, data: str):
        self.inquiry_code = inquiry_code
        self.data = data

    def generate_signature(self) -> str:
        """Generates a signature from the inquiry code and data.

        Returns:
            str: The signature.
        """
        random_data = Random.get_hex_string(64)
        key = self.inquiry_code + random_data
        hmac_ = Hmac(HashAlgorithm.SHA256)
        signature = hmac_.get_hmac(core.Data(key), core.Data(self.data))

        return random_data + signature.to_hex()

    def generate_signature_v1(self) -> str:
        """Generates a signature from the inquiry code and data.

        Returns:
            str: The signature.
        """

        data = self.data + self.data  # repeat data for some reason
        random_data = Random.get_hex_string(40)
        key = self.inquiry_code + random_data
        hmac_ = Hmac(HashAlgorithm.SHA1)
        signature = hmac_.get_hmac(core.Data(key), core.Data(data))

        return random_data + signature.to_hex()


# ============================================================
# FILE: game_version.py
# ============================================================
from __future__ import annotations
from typing import Any
from bcsfe import core


class GameVersion:
    """A class to represent a game version."""

    def __init__(self, game_version: int):
        """Initializes a new instance of the GameVersion class.

        Args:
            game_version (int): Game version as an integer. e.g 120102 for 12.1.2
        """
        self.game_version = game_version

    def to_string(self) -> str:
        """Converts the game version to a string.

        Returns:
            str: Game version as a string. e.g 12.1.2
        """
        split_gv = str(self.game_version).zfill(6)
        split_gv = [
            str(int(split_gv[i : i + 2])) for i in range(0, len(split_gv), 2)
        ]
        return ".".join(split_gv)

    def get_parts_zfill(self) -> list[str]:
        """Gets the parts of the game version as a list of strings with leading zeros.

        Returns:
            list[str]: Game version parts as strings with leading zeros. e.g ["12", "01", "02"]
        """
        return [part.zfill(2) for part in self.to_string().split(".")]

    def get_parts(self) -> list[int]:
        """Gets the parts of the game version as a list of integers.

        Returns:
            list[int]: Game version parts as integers. e.g [12, 1, 2]
        """
        return [int(part) for part in self.get_parts_zfill()]

    def format(self) -> str:
        """Formats the game version as a string with leading zeros.

        Returns:
            str: Game version as a string with leading zeros. e.g 12.01.02
        """
        parts = self.get_parts_zfill()
        string = ""
        for part in parts:
            string += f"{part}."
        return f"{string[:-1]}"

    def __str__(self) -> str:
        """Converts the game version to a string.

        Returns:
            str: Game version as a string. e.g 12.1.2
        """
        return self.to_string()

    def __repr__(self) -> str:
        """Converts the game version object to a string.

        Returns:
            str: Game version object as a string. e.g game_version(120102) 12.1.2
        """
        return f"game_version({self.game_version}) {self.to_string()}"

    @staticmethod
    def read(data: core.Data) -> GameVersion:
        """Reads a 4 byte int from a Data object.

        Args:
            data (core.Data): Data object to read from.

        Returns:
            GameVersion: Game version read from the Data object.
        """
        return GameVersion(data.read_int())

    def write(self, data: core.Data):
        """Writes the 4 byte game version to a Data object.

        Args:
            data (core.Data): Data object to write to.
        """
        data.write_int(self.game_version)

    def serialize(self) -> dict[str, Any]:
        """Serializes the game version to a dictionary.

        Returns:
            dict[str, Any]: Serialized game version.
        """
        return {"game_version": self.game_version}

    @staticmethod
    def deserialize(game_version: dict[str, Any]) -> GameVersion:
        """Deserializes a game version from a dictionary.

        Args:
            game_version (dict[str, Any]): Serialized game version.

        Returns:
            GameVersion: Deserialized game version.
        """
        return GameVersion(game_version["game_version"])

    @staticmethod
    def from_string(game_version: str) -> GameVersion:
        """Converts a string to a GameVersion object.

        Args:
            game_version (str): Game version as a string. e.g 12.1.2

        Returns:
            GameVersion: Game version as a GameVersion object.
        """
        split_gv = game_version.split(".")
        if len(split_gv) == 2:
            split_gv.append("0")
        final = ""
        for split in split_gv:
            final += split.zfill(2)
        return GameVersion(int(final))

    def __eq__(self, other: Any) -> bool:
        """Checks if the game version is equal to another object.

        Args:
            other (Any): Object to compare to.

        Returns:
            bool: True if the game version is equal to the other object, False otherwise.
        """
        if isinstance(other, GameVersion):
            return self.game_version == other.game_version
        elif isinstance(other, int):
            return self.game_version == other
        elif isinstance(other, str):
            return (
                self.game_version == GameVersion.from_string(other).game_version
            )
        else:
            return False

    def __ne__(self, other: Any) -> bool:
        """Checks if the game version is not equal to another object.

        Args:
            other (Any): Object to compare to.

        Returns:
            bool: True if the game version is not equal to the other object, False otherwise.
        """
        return not self.__eq__(other)

    def __lt__(self, other: Any) -> bool:
        """Checks if the game version is less than another object.

        Args:
            other (Any): Object to compare to.

        Returns:
            bool: True if the game version is less than the other object, False otherwise.
        """
        if isinstance(other, GameVersion):
            return self.game_version < other.game_version
        elif isinstance(other, int):
            return self.game_version < other
        elif isinstance(other, str):
            return (
                self.game_version < GameVersion.from_string(other).game_version
            )
        else:
            return False

    def __le__(self, other: Any) -> bool:
        """Checks if the game version is less than or equal to another object.

        Args:
            other (Any): Object to compare to.

        Returns:
            bool: True if the game version is less than or equal to the other object, False otherwise.
        """
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other: Any) -> bool:
        """Checks if the game version is greater than another object.

        Args:
            other (Any): Object to compare to.

        Returns:
            bool: True if the game version is greater than the other object, False otherwise.
        """
        return not self.__le__(other)

    def __ge__(self, other: Any) -> bool:
        """Checks if the game version is greater than or equal to another object.

        Args:
            other (Any): Object to compare to.

        Returns:
            bool: True if the game version is greater than or equal to the other object, False otherwise.
        """
        return not self.__lt__(other)

    def __add__(self, other: Any) -> GameVersion:
        """Adds the game version to another object.

        Args:
            other (Any): Object to add to.

        Returns:
            GameVersion: Game version added to the other object.
        """
        if isinstance(other, GameVersion):
            return GameVersion(self.game_version + other.game_version)
        elif isinstance(other, int):
            return GameVersion(self.game_version + other)
        elif isinstance(other, str):
            return GameVersion(
                self.game_version + GameVersion.from_string(other).game_version
            )
        else:
            return NotImplemented

    def __sub__(self, other: Any) -> GameVersion:
        """Subtracts the game version from another object.

        Args:
            other (Any): Object to subtract from.

        Returns:
            GameVersion: Game version subtracted from the other object.
        """
        return self.__add__(-other)


# ============================================================
# FILE: locale_handler.py
# ============================================================
from __future__ import annotations
import dataclasses
import tempfile
from typing import Any
from bcsfe import core
from bcsfe.cli import color


class PropertySet:
    """Represents a set of properties in a property file."""

    def __init__(self, locale: str, property: str):
        """Initializes a new instance of the PropertySet class.

        Args:
            locale (str): Language code of the locale.
            property (str): Name of the property file.
        """
        self.locale = locale
        self.property = property
        self.path = LocalManager.get_locale_folder(locale).add(property + ".properties")
        self.properties: dict[str, tuple[str, str]] = {}
        self.parse()

    def parse(self):
        """Parses the property file.

        Raises:
            KeyError: If a key is already defined in the property file.
        """
        lines = self.path.read().to_str().splitlines()
        i = 0
        in_multi_line = False
        multi_line_text = ""
        multi_line_key = ""

        while i < len(lines):
            line = lines[i]
            finish_multiline = False
            if (in_multi_line and not line.startswith(">")) or (
                in_multi_line and i == len(lines) - 1
            ):
                in_multi_line = False
                finish_multiline = True
                if multi_line_key in self.properties:
                    raise KeyError(
                        f"Key {multi_line_key} already exists in property file"
                    )
                if line.startswith(">"):
                    multi_line_text += line[1:]
                else:
                    multi_line_text = multi_line_text[:-1]  # remove extra newline
                self.properties[multi_line_key] = (multi_line_text, self.property)
                multi_line_text = ""
                multi_line_key = ""
            if line.startswith("#") or not line:
                i += 1
                continue
            if line.startswith(">") and in_multi_line:
                multi_line_text += line[1:] + "\n"

            parts = line.split("=")
            if line.strip().endswith("="):
                in_multi_line = True
                multi_line_key = parts[0]

            if not in_multi_line and not finish_multiline:
                key = parts[0]
                value = "=".join(parts[1:])
                if key in self.properties:
                    raise KeyError(f"Key {key} already exists in property file")
                self.properties[key] = (value, self.property)

            i += 1

    def get_key(self, key: str) -> str:
        """Gets a key from the property file.

        Args:
            key (str): Key to get.

        Returns:
            str: Value of the key.
        """
        return (
            self.properties.get(key, key)[0].replace("\\n", "\n").replace("\\t", "\t")
        )

    @staticmethod
    def from_config(property: str) -> PropertySet:
        """Gets a PropertySet from the language code in the config.

        Args:
            property (str): Name of the property file.

        Returns:
            PropertySet: PropertySet for the property file.
        """
        return PropertySet(
            core.core_data.config.get_str(core.ConfigKey.LOCALE), property
        )


class LocalManager:
    """Manages properties for a locale"""

    def __init__(self, locale: str | None = None):
        """Initializes a new instance of the LocalManager class.

        Args:
            locale (str): Language code of the locale.
        """
        if locale is None:
            lc = core.core_data.config.get_str(core.ConfigKey.LOCALE)
        else:
            lc = locale

        self.locale = lc
        self.path = LocalManager.get_locale_folder(lc)
        self.properties: dict[str, PropertySet] = {}
        self.all_properties: dict[str, tuple[str, str]] = {}
        self.en_properties: dict[str, tuple[str, str]] = {}
        self.en_properties_path = LocalManager.get_locale_folder("en")
        self.authors: list[str] = ["fieryhenry"]
        self.name: str = "English"
        self.parse()
        if self.locale == "en":
            self.en_properties = self.all_properties

        if core.core_data.config.get_bool(core.ConfigKey.SHOW_MISSING_LOCALE_KEYS):
            key = self.get_key("missing_locale_keys")
            print(key)
            print()
            missing = self.get_missing_keys()
            for key in missing:
                print(f"{key[2]}\n{key[0]}={key[1]}\n")
            if not missing:
                print(self.get_key("none"))

            print()

            key = self.get_key("extra_locale_keys")
            print(key)
            print()
            extra = self.get_extra_keys()
            for key in extra:
                print(f"{key[2]}\n{key[0]}={key[1]}\n")
            if not extra:
                print(self.get_key("none"))

            print()

    def get_missing_keys(self) -> list[tuple[str, str, str]]:
        missing = set(self.en_properties.keys()) - set(self.all_properties.keys())

        return [
            (
                key,
                self.en_properties[key][0],
                self.en_properties[key][1] + ".properties",
            )
            for key in missing
        ]

    def get_extra_keys(self) -> list[tuple[str, str, str]]:
        extra = set(self.all_properties.keys()) - set(self.en_properties.keys())

        return [
            (
                key,
                self.all_properties[key][0],
                self.all_properties[key][1] + ".properties",
            )
            for key in extra
        ]

    def parse(self):
        """Parses all property files in the locale folder recursively."""
        for file in self.path.glob("**/*.properties", recursive=True):
            file_name = file.strip_path_from(self.path).path
            property_set = PropertySet(self.locale, file_name[:-11])
            self.all_properties.update(property_set.properties)
            self.properties[file_name[:-11]] = property_set

        metadata_path = self.path.add("metadata.json")

        if metadata_path.exists():
            data = core.JsonFile.from_path(metadata_path)
            self.authors = data.get("authors") or ["fieryhenry"]
            self.name = data.get("name") or "English"

        if self.locale != "en":
            for file in self.en_properties_path.glob("**/*.properties", recursive=True):
                file_name = file.strip_path_from(self.en_properties_path).path
                property_set = PropertySet("en", file_name[:-11])
                self.en_properties.update(property_set.properties)

    def get_key(self, key: str, escape: bool = True, **kwargs: Any) -> str:
        """Gets a key from the property file.

        Args:
            key (str): Key to get.

        Returns:
            str: Value of the key.
        """
        try:
            text = self.get_key_recursive(key, kwargs, escape)
        except RecursionError:
            text = key

        for kwarg_key, kwarg_value in kwargs.items():
            value = str(kwarg_value)
            if escape:
                value = LocalManager.escape_string(value)
            text = text.replace("{" + kwarg_key + "}", value)

        if "$(" in text:
            text = self.parse_condition(text, kwargs)

        return text

    def parse_condition(self, text: str, kwargs: dict[str, Any]) -> str:
        counter = 0
        final_text = ""
        in_expression = False
        expression_text = ""
        count_down = 0
        while counter < len(text):
            char = text[counter]
            if counter == len(text) - 1:
                final_text += char
                break
            next_char = text[counter + 1]
            if char == "\\":
                final_text += next_char
                counter += 2
                continue
            if char == "$" and next_char == "(":
                count_down = 0
                in_expression = True
            elif char == "/" and next_char == "$":
                count_down = 2
                in_expression = False
                if len(expression_text) < 3:
                    counter += 1
                    continue
                new_expression_text = expression_text[2:-1]
                expression_text = ""
                parts = new_expression_text.split(":")
                if len(parts) < 2:
                    counter += 1
                    continue
                keyword = parts[0].strip()
                expression = parts[1].strip()
                conditions = expression.split("$,")
                string = ""
                for i, condition in enumerate(conditions):
                    condition = condition.strip()
                    if not condition:
                        continue
                    if i == len(conditions) - 1:
                        string = condition
                        break
                    condition_parts = condition.split("($")
                    if len(condition_parts) < 2:
                        continue
                    logic = condition_parts[0].strip()
                    word = condition_parts[1].strip()
                    if not word:
                        continue
                    word = word[:-1]
                    value = kwargs.get(keyword)
                    if value is None:
                        continue
                    equality = None
                    if logic.startswith("=="):
                        equality = "=="
                    elif logic.startswith("!="):
                        equality = "!="
                    elif logic.startswith(">="):
                        equality = ">="
                    elif logic.startswith("<="):
                        equality = "<="
                    elif logic.startswith(">"):
                        equality = ">"
                    elif logic.startswith("<"):
                        equality = "<"
                    if equality is None:
                        continue
                    logic_parts = logic.split(equality)
                    if len(logic_parts) < 2:
                        continue
                    logic_value = logic_parts[1].strip()

                    if isinstance(value, int):
                        if not logic_value.isdigit():
                            continue
                        logic_value = int(logic_value)

                    if equality == "==":
                        if logic_value == value:
                            string = word
                            break
                    elif equality == "!=":
                        if logic_value != value:
                            string = word
                            break

                    if isinstance(logic_value, int) and not string:
                        if equality == ">":
                            if logic_value > value:
                                string = word
                                break
                        elif equality == ">=":
                            if logic_value >= value:
                                string = word
                                break
                        elif equality == "<":
                            if logic_value < value:
                                string = word
                                break
                        elif equality == "<=":
                            if logic_value <= value:
                                string = word
                                break

                final_text += string

            if in_expression:
                expression_text += char
            else:
                if count_down <= 0:
                    final_text += char
                else:
                    count_down -= 1

            counter += 1

        return final_text

    @staticmethod
    def get_special_chars() -> list[str]:
        return ["<", ">", "/"]

    @staticmethod
    def escape_string(string: str) -> str:
        for char in LocalManager.get_special_chars():
            string = string.replace(char, "\\" + char)
        return string

    def get_key_recursive(
        self,
        key: str,
        kwargs: dict[str, Any],
        escape: bool = True,
    ) -> str:
        value = self.all_properties.get(key)
        if value is None:
            value = self.en_properties.get(key, (key, key))
        value = value[0].replace("\\n", "\n").replace("\\t", "\t")
        # replace {{key}} with the value of the key
        if "{{" not in value:
            return value
        char_index = 0
        while char_index < len(value):
            if value[char_index] == "{" and value[char_index + 1] == "{":
                key_name = ""
                char_index += 2
                while value[char_index] != "}":
                    key_name += value[char_index]
                    char_index += 1

                if key_name != key:
                    value = value.replace(
                        "{{" + key_name + "}}",
                        self.get_key(key_name, escape, **kwargs),
                    )
            char_index += 1

        return value

    @staticmethod
    def get_all_aliases(value: str) -> list[str]:
        """Gets all aliases from a string. Aliases are separated by |.

        Args:
            value (str): String to get aliases from.

        Returns:
            list[str]: List of aliases.
        """
        if "|" not in value:
            return [value]
        i = 0
        aliases: list[str] = []
        while i < len(value):
            char = value[i]
            prev_char = value[i - 1] if i > 0 else ""
            if char == "|" and prev_char != "\\":
                aliases.append(value[:i])
                value = value[i + 1 :]
                i = 0
            i += 1

        aliases.append(value)
        return aliases

    @staticmethod
    def from_config() -> LocalManager:
        """Gets a LocalManager from the language code in the config.

        Returns:
            LocalManager: LocalManager for the locale.
        """
        return LocalManager(core.core_data.config.get_str(core.ConfigKey.LOCALE))

    def check_duplicates(self):
        """Checks for duplicate keys in all property files.

        Raises:
            KeyError: If a key is already defined in the property file.
        """
        keys: set[str] = set()
        for property in self.properties.values():
            for key in property.properties.keys():
                if key in keys:
                    raise KeyError(f"Duplicate key {key}")
                keys.add(key)

    @staticmethod
    def get_all_locales() -> list[str]:
        """Gets all locales in the locales folder.

        Returns:
            list[str]: List of locales.
        """
        locales: list[str] = []
        for folder in LocalManager.get_locales_folder().get_dirs():
            locales.append(folder.basename())
        for folder in LocalManager.get_external_locales_folder().get_dirs():
            locales.append(folder.basename())
        return locales

    @staticmethod
    def get_locales_folder() -> core.Path:
        """Gets the locales folder.

        Returns:
            core.Path: Path to the locales folder.
        """
        return core.Path("locales", True)

    @staticmethod
    def get_external_locales_folder() -> core.Path:
        """Gets the external locales folder.

        Returns:
            core.Path: Path to the external locales folder.
        """
        return core.Path.get_documents_folder().add("external_locales")

    @staticmethod
    def get_locale_folder(locale: str) -> core.Path:
        """Gets the folder for a locale.

        Args:
            locale (str): Language code of the locale.

        Returns:
            core.Path: Path to the locale folder.
        """
        if locale.startswith("ext-"):
            return LocalManager.get_external_locales_folder().add(locale)
        return LocalManager.get_locales_folder().add(locale)

    @staticmethod
    def remove_locale(locale: str):
        """Removes a locale.

        Args:
            locale (str): Language code of the locale.
        """
        if locale not in LocalManager.get_all_locales():
            return
        if locale.startswith("ext-"):
            extern = ExternalLocaleManager.get_external_locale(locale)
            if extern is not None:
                ExternalLocaleManager.delete_locale(extern)
            LocalManager.get_external_locales_folder().add(locale).remove()
        else:
            LocalManager.get_locales_folder().add(locale).remove()

        if core.core_data.config.get_str(core.ConfigKey.LOCALE) == locale:
            core.core_data.config.set(core.ConfigKey.LOCALE, "en")


@dataclasses.dataclass
class ExternalLocale:
    short_name: str
    name: str
    description: str
    author: str
    version: str
    git_repo: str | None = None

    def to_json(self) -> dict[str, Any]:
        return dataclasses.asdict(self)

    @staticmethod
    def from_json(json_data: dict[str, Any]) -> ExternalLocale | None:
        short_name = json_data.get("short_name")
        name = json_data.get("name")
        description = json_data.get("description")
        author = json_data.get("author")
        version = json_data.get("version")
        git_repo = json_data.get("git_repo")
        if (
            short_name is None
            or name is None
            or description is None
            or author is None
            or version is None
        ):
            return None
        return ExternalLocale(
            short_name,
            name,
            description,
            author,
            version,
            git_repo,
        )

    @staticmethod
    def from_git_repo(git_repo: str) -> ExternalLocale | None:
        repo = core.GitHandler().get_repo(git_repo)
        if repo is None:
            return None
        locale_json = repo.get_file(core.Path("locale.json"))
        if locale_json is None:
            return None
        json_data = core.JsonFile.from_data(locale_json).to_object()
        json_data["git_repo"] = git_repo
        return ExternalLocale.from_json(json_data)

    def get_new_version(self) -> bool:
        if self.git_repo is None:
            return False
        repo = core.GitHandler().get_repo(self.git_repo)
        if repo is None:
            return False
        with tempfile.TemporaryDirectory() as tmp:
            temp_dir = core.Path(tmp)
            success = repo.clone_to_temp(temp_dir)
            if not success:
                return False
            external_locale = ExternalLocaleManager.parse_external_locale(temp_dir)
            if external_locale is None:
                return False
            version = external_locale.version

            if version == self.version:
                return False

            self.name = external_locale.name
            self.short_name = external_locale.short_name
            self.description = external_locale.description
            self.author = external_locale.author
            self.version = version

        success = repo.pull()
        if not success:
            return False
        self.save()
        return True

    def save(self):
        ExternalLocaleManager.save_locale(self)

    def get_full_name(self) -> str:
        return f"ext-{self.author}-{self.short_name}"


class ExternalLocaleManager:
    @staticmethod
    def delete_locale(external_locale: ExternalLocale):
        if external_locale.git_repo is None:
            return
        folder = core.GitHandler.get_repo_folder().add(
            external_locale.git_repo.split("/")[-1]
        )
        folder.remove()

    @staticmethod
    def save_locale(
        external_locale: ExternalLocale,
    ):
        """Saves an external locale.

        Args:
            external_locale (ExternalLocale): External locale to save.
        """
        if external_locale.git_repo is None:
            return
        folder = LocalManager.get_external_locales_folder().add(
            external_locale.get_full_name()
        )
        folder.generate_dirs()

        repo = core.GitHandler().get_repo(external_locale.git_repo)
        if repo is None:
            return
        files_dir = repo.get_folder(core.Path("files"))
        if files_dir is None:
            return

        files_dir.copy_tree(folder)

        json_data = external_locale.to_json()
        folder.add("locale.json").write(core.JsonFile.from_object(json_data).to_data())

    @staticmethod
    def parse_external_locale(path: core.Path) -> ExternalLocale | None:
        """Parses an external locale.

        Args:
            path (core.Path): Path to the external locale.

        Returns:
            ExternalLocale: External locale.
        """
        if not path.exists():
            return None
        json_data = core.JsonFile.from_data(path.add("locale.json").read()).to_object()
        return ExternalLocale.from_json(json_data)

    @staticmethod
    def update_external_locale(external_locale: ExternalLocale):
        """Updates an external locale.

        Args:
            external_locale (ExternalLocale): External locale to update.
        """
        if external_locale.git_repo is None:
            return
        color.ColoredText.localize(
            "checking_for_locale_updates",
            locale_name=external_locale.name,
        )
        updated = external_locale.get_new_version()
        if updated:
            color.ColoredText.localize(
                "external_locale_updated",
                locale_name=external_locale.name,
                version=external_locale.version,
            )
        else:
            color.ColoredText.localize(
                "external_locale_no_update",
                locale_name=external_locale.name,
                version=external_locale.version,
            )
        print()

    @staticmethod
    def update_all_external_locales(_: Any = None):
        """Updates all external locales."""
        dirs = LocalManager.get_external_locales_folder().get_dirs()
        if not dirs:
            color.ColoredText.localize(
                "no_external_locales",
            )
            return
        if not core.GitHandler.is_git_installed():
            color.ColoredText.localize(
                "git_not_installed",
            )
            return
        for folder in dirs:
            locale = ExternalLocaleManager.parse_external_locale(folder)
            if locale is None:
                continue
            ExternalLocaleManager.update_external_locale(locale)

    @staticmethod
    def get_external_locale_config() -> ExternalLocale | None:
        """Gets the external locale from the config.

        Returns:
            ExternalLocale: External locale.
        """

        locale = core.core_data.config.get_str(core.ConfigKey.LOCALE)
        if not locale.startswith("ext-"):
            return None
        return ExternalLocaleManager.parse_external_locale(
            LocalManager.get_locale_folder(locale)
        )

    @staticmethod
    def get_external_locale(locale: str) -> ExternalLocale | None:
        """Gets the external locale from the code.

        Returns:
            ExternalLocale: External locale.
        """

        if not locale.startswith("ext-"):
            return None
        return ExternalLocaleManager.parse_external_locale(
            LocalManager.get_locale_folder(locale)
        )


# ============================================================
# FILE: log.py
# ============================================================
from __future__ import annotations

"""Module for handling logging"""
import traceback
from bcsfe import core
import time


class Logger:
    def __init__(self, path: core.Path | None):
        """
        Initializes a Logger object
        """
        if path is None:
            path = core.Path.get_documents_folder().add("bcsfe.log")
        self.log_file = path
        try:
            self.log_data = self.log_file.read(True).split(b"\n")
        except Exception as e:
            self.log_data = None

    def is_log_enabled(self) -> bool:
        return self.log_data is not None
        

    def get_time(self) -> str:
        """
        Returns the current time in the format: "HH:MM:SS"

        Returns:
            str: The current time
        """
        return time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())

    def log_debug(self, message: str):
        """
        Logs a debug message

        Args:
            message (str): The message to log
        """
        if self.log_data is None:
            return
        self.log_data.append(
            core.Data(f"[DEBUG]::{self.get_time()} - {message}")
        )
        self.write()

    def log_info(self, message: str):
        """
        Logs an info message

        Args:
            message (str): The message to log
        """
        if self.log_data is None:
            return
        self.log_data.append(
            core.Data(f"[INFO]::{self.get_time()} - {message}")
        )
        self.write()

    def log_warning(self, message: str):
        """
        Logs a warning message

        Args:
            message (str): The message to log
        """
        if self.log_data is None:
            return
        self.log_data.append(
            core.Data(f"[WARNING]::{self.get_time()} - {message}")
        )
        self.write()

    def log_error(self, message: str):
        """
        Logs an error message

        Args:
            message (str): The message to log
        """
        if self.log_data is None:
            return
        self.log_data.append(
            core.Data(f"[ERROR]::{self.get_time()} - {message}")
        )
        self.write()

    def log_exception(self, exception: Exception, extra_msg: str = ""):
        tb = traceback.format_exc()
        if tb == "NoneType: None\n":
            try:
                raise exception
            except Exception:
                tb = traceback.format_exc()

        self.log_error(
            f"{extra_msg}: {exception.__class__.__name__}: {exception}\n{tb}"
        )

    def write(self):
        """
        Writes the log data to the log file
        """
        if self.log_data is None:
            return
        self.log_file.write(
            core.Data.from_many(self.log_data, core.Data("\n")).strip()
        )

    def log_no_file_found(self, file_name: str):
        """
        Logs that a file was not found

        Args:
            fileName (str): The name of the file
        """
        self.log_warning(f"Could not find {file_name}")

    @staticmethod
    def get_traceback() -> str:
        """
        Gets the traceback of the last exception

        Returns:
            str: The traceback
        """
        tb = traceback.format_exc()
        if tb == "NoneType: None\n":
            return ""
        return tb


# ============================================================
# FILE: max_value_helper.py
# ============================================================
from __future__ import annotations
import enum
from typing import Any
from bcsfe import core


class MaxValueType(enum.Enum):
    CATFOOD = "catfood"
    XP = "xp"
    NORMAL_TICKETS = "normal_tickets"
    HUNDRED_MILLION_TICKETS = "100_million_tickets"
    RARE_TICKETS = "rare_tickets"
    PLATINUM_TICKETS = "platinum_tickets"
    LEGEND_TICKETS = "legend_tickets"
    NP = "np"
    LEADERSHIP = "leadership"
    BATTLE_ITEMS = "battle_items"
    CATAMINS = "catamins"
    CATSEYES = "catseyes"
    CATFRUIT = "catfruit"
    BASE_MATERIALS = "base_materials"
    LABYRINTH_MEDALS = "labyrinth_medals"
    TALENT_ORBS = "talent_orbs"
    TREASURE_LEVEL = "treasure_level"
    STAGE_CLEAR_COUNT = "stage_clear_count"
    ITF_TIMED_SCORE = "itf_timed_score"
    EVENT_TICKETS = "event_tickets"
    TREASURE_CHESTS = "treasure_chests"


class MaxValueHelper:
    def __init__(self):
        self.max_value_data = self.get_max_value_data()

    @staticmethod
    def convert_val_code(value_code: MaxValueType | str) -> str:
        if isinstance(value_code, MaxValueType):
            value_code = value_code.value
        return value_code

    def get_max_value_data(self) -> dict[str, Any]:
        file_path = core.Path("max_values.json", True)
        if not file_path.exists():
            return {}
        try:
            return core.JsonFile.from_data(file_path.read()).to_object()
        except core.JSONDecodeError:
            return {}

    def get(self, value_code: str | MaxValueType) -> int:
        try:
            return int(self.max_value_data.get(self.convert_val_code(value_code), 0))
        except ValueError:
            return 0

    def get_property(self, value_code: str | MaxValueType, property: str) -> int:
        try:
            return int(
                self.max_value_data.get(self.convert_val_code(value_code), {}).get(
                    property, 0
                )
            )
        except ValueError:
            return 0

    def get_old(self, value_code: str | MaxValueType) -> int:
        return self.get_property(value_code, "old")

    def get_new(self, value_code: str | MaxValueType) -> int:
        return self.get_property(value_code, "new")

# ============================================================
# FILE: theme_handler.py
# ============================================================
from __future__ import annotations
import dataclasses
import tempfile
from typing import Any
from bcsfe import core
from bcsfe.cli import color


class ThemeHandler:
    def __init__(self, theme_code: str | None = None):
        if theme_code is None:
            self.theme_code = core.core_data.config.get_str(
                core.ConfigKey.THEME
            )
        else:
            self.theme_code = theme_code

        self.theme_data = self.get_theme_data()

    @staticmethod
    def get_themes_folder() -> core.Path:
        return core.Path("themes", True).generate_dirs()

    @staticmethod
    def get_external_themes_folder() -> core.Path:
        return (
            core.Path.get_documents_folder()
            .add("external_themes")
            .generate_dirs()
        )

    @staticmethod
    def get_theme_path(theme_code: str) -> core.Path:
        if theme_code.startswith("ext-"):
            return ThemeHandler.get_external_themes_folder().add(
                theme_code + ".json"
            )
        return ThemeHandler.get_themes_folder().add(theme_code + ".json")

    def get_theme_data(self) -> dict[str, Any]:
        file_path = self.get_theme_path(self.theme_code)
        if not file_path.exists():
            return {}
        try:
            return core.JsonFile.from_data(file_path.read()).to_object()
        except core.JSONDecodeError:
            return {}

    def get_short_name(self) -> str:
        return self.theme_data.get("short_name", "")

    def get_name(self) -> str:
        return self.theme_data.get("name", "")

    def get_description(self) -> str:
        return self.theme_data.get("description", "")

    def get_author(self) -> str:
        return self.theme_data.get("author", "")

    def get_version(self) -> str:
        return self.theme_data.get("version", "")

    def get_git_repo(self) -> str | None:
        return self.theme_data.get("git_repo", None)

    def get_theme_colors(self) -> dict[str, Any]:
        return self.theme_data.get("colors", {})

    def get_theme_color(self, color_code: str) -> str:
        return self.get_theme_colors().get(color_code, "")

    def get_primary_color(self) -> str:
        return self.get_theme_color("primary")

    def get_secondary_color(self) -> str:
        return self.get_theme_color("secondary")

    def get_tertiary_color(self) -> str:
        return self.get_theme_color("tertiary")

    def get_quaternary_color(self) -> str:
        return self.get_theme_color("quaternary")

    def get_error_color(self) -> str:
        return self.get_theme_color("error")

    def get_warning_color(self) -> str:
        return self.get_theme_color("warning")

    def get_success_color(self) -> str:
        return self.get_theme_color("success")

    @staticmethod
    def get_all_themes() -> list[str]:
        themes = [
            file.get_file_name_without_extension()
            for file in ThemeHandler.get_themes_folder().get_paths_dir(
                regex=r".*\.json"
            )
        ]
        themes += [
            folder.get_file_name_without_extension()
            for folder in ThemeHandler.get_external_themes_folder().get_paths_dir(
                regex=r".*\.json"
            )
        ]
        return themes

    @staticmethod
    def remove_theme(theme_code: str):
        extern = ExternalThemeManager.get_external_theme(theme_code)
        if extern is not None:
            ExternalThemeManager.delete_theme(extern)

        ThemeHandler.get_theme_path(theme_code).remove()
        if theme_code == core.core_data.config.get_str(core.ConfigKey.THEME):
            core.core_data.config.set_default(core.ConfigKey.THEME)


@dataclasses.dataclass
class ExternalTheme:
    short_name: str
    name: str
    description: str
    author: str
    version: str
    colors: dict[str, Any]
    git_repo: str | None = None

    def to_json(self) -> dict[str, Any]:
        return dataclasses.asdict(self)

    @staticmethod
    def from_json(json_data: dict[str, Any]) -> ExternalTheme | None:
        try:
            return ExternalTheme(**json_data)
        except TypeError:
            return None

    @staticmethod
    def from_git_repo(git_repo: str) -> ExternalTheme | None:
        repo = core.GitHandler().get_repo(git_repo)
        if repo is None:
            return None
        theme_json = repo.get_file(core.Path("theme.json"))
        if theme_json is None:
            return None
        json_data = core.JsonFile.from_data(theme_json).to_object()
        json_data["git_repo"] = git_repo
        return ExternalTheme.from_json(json_data)

    def get_new_version(self) -> bool:
        if self.git_repo is None:
            return False
        repo = core.GitHandler().get_repo(self.git_repo)
        if repo is None:
            return False
        with tempfile.TemporaryDirectory() as tmp:
            temp_dir = core.Path(tmp)
            success = repo.clone_to_temp(temp_dir)
            if not success:
                return False
            external_theme = ExternalThemeManager.parse_external_theme(
                temp_dir.add("theme.json")
            )
            if external_theme is None:
                return False
            version = external_theme.version

            if version == self.version:
                return False

            self.name = external_theme.name
            self.short_name = external_theme.short_name
            self.description = external_theme.description
            self.author = external_theme.author
            self.colors = external_theme.colors
            self.version = version

        success = repo.pull()
        if not success:
            return False
        self.save()
        return True

    def save(self):
        ExternalThemeManager.save_theme(self)

    def get_full_name(self) -> str:
        return f"ext-{self.author}-{self.short_name}"


class ExternalThemeManager:
    @staticmethod
    def delete_theme(external_theme: ExternalTheme):
        if external_theme.git_repo is None:
            return
        folder = core.GitHandler.get_repo_folder().add(
            external_theme.git_repo.split("/")[-1]
        )
        folder.remove()

    @staticmethod
    def save_theme(
        external_theme: ExternalTheme,
    ):
        """Saves an external theme.

        Args:
            external_theme (ExternalTheme): External theme to save.
        """
        if external_theme.git_repo is None:
            return
        file = ThemeHandler.get_theme_path(external_theme.get_full_name())

        json_data = external_theme.to_json()
        file.write(core.JsonFile.from_object(json_data).to_data())

    @staticmethod
    def parse_external_theme(path: core.Path) -> ExternalTheme | None:
        """Parses an external theme.

        Args:
            path (core.Path): Path to the external theme.

        Returns:
            ExternalTheme: External theme.
        """
        json_data = core.JsonFile.from_data(path.read()).to_object()
        return ExternalTheme.from_json(json_data)

    @staticmethod
    def update_external_theme(external_theme: ExternalTheme):
        """Updates an external theme.

        Args:
            external_theme (ExternalTheme): External theme to update.
        """
        if external_theme.git_repo is None:
            return
        color.ColoredText.localize(
            "checking_for_theme_updates",
            theme_name=external_theme.name,
        )
        updated = external_theme.get_new_version()
        if updated:
            color.ColoredText.localize(
                "external_theme_updated",
                theme_name=external_theme.name,
                version=external_theme.version,
            )
        else:
            color.ColoredText.localize(
                "external_theme_no_update",
                theme_name=external_theme.name,
                version=external_theme.version,
            )
        print()

    @staticmethod
    def update_all_external_themes(_: Any = None):
        """Updates all external themes."""
        files = ThemeHandler.get_external_themes_folder().get_paths_dir()
        if not files:
            color.ColoredText.localize(
                "no_external_themes",
            )
            return
        if not core.GitHandler.is_git_installed():
            color.ColoredText.localize(
                "git_not_installed",
            )
            return
        for file in files:
            theme = ExternalThemeManager.parse_external_theme(file)
            if theme is None:
                continue
            ExternalThemeManager.update_external_theme(theme)

    @staticmethod
    def get_external_theme_config() -> ExternalTheme | None:
        """Gets the external theme from the config.

        Returns:
            ExternalTheme: External theme.
        """

        theme = core.core_data.config.get_str(core.ConfigKey.THEME)
        if not theme.startswith("ext-"):
            return None
        return ExternalThemeManager.parse_external_theme(
            ThemeHandler.get_theme_path(theme)
        )

    @staticmethod
    def get_external_theme(theme: str) -> ExternalTheme | None:
        """Gets the external theme from the theme code.

        Returns:
            ExternalTheme: External theme.
        """

        if not theme.startswith("ext-"):
            return None
        return ExternalThemeManager.parse_external_theme(
            ThemeHandler.get_theme_path(theme)
        )

