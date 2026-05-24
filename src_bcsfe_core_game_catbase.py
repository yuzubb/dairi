# === COMBINED FILE ===
# フォルダ: src_bcsfe_core_game_catbase
# 元ファイル(24件): __init__.py, beacon_base.py, cat.py, drop_chara.py, gambling.py, gatya.py, gatya_item.py, item_pack.py, login_bonuses.py, matatabi.py, medals.py, mission.py, my_sale.py, nyanko_club.py, officer_pass.py, playtime.py, powerup.py, scheme_items.py, special_skill.py, stamp.py, talent_orbs.py, unlock_popups.py, upgrade.py, user_rank_rewards.py

# ============================================================
# FILE: __init__.py
# ============================================================
from bcsfe.core.game.catbase import (
    gatya_item,
    stamp,
    cat,
    upgrade,
    special_skill,
    my_sale,
    gatya,
    user_rank_rewards,
    item_pack,
    login_bonuses,
    scheme_items,
    unlock_popups,
    beacon_base,
    mission,
    nyanko_club,
    officer_pass,
    medals,
    talent_orbs,
    matatabi,
    powerup,
    drop_chara,
    playtime,
    gambling,
)

__all__ = [
    "stamp",
    "cat",
    "upgrade",
    "special_skill",
    "my_sale",
    "gatya",
    "user_rank_rewards",
    "item_pack",
    "login_bonuses",
    "scheme_items",
    "unlock_popups",
    "beacon_base",
    "mission",
    "nyanko_club",
    "officer_pass",
    "medals",
    "talent_orbs",
    "gatya_item",
    "matatabi",
    "powerup",
    "drop_chara",
    "playtime",
    "gambling",
]


# ============================================================
# FILE: beacon_base.py
# ============================================================
from __future__ import annotations
from typing import Any
from bcsfe import core


class BeaconEventListScene:
    def __init__(
        self,
        int_dict: dict[int, int],
        str_dict: dict[int, list[str]],
        bool_dict: dict[int, bool],
    ):
        self.int_array = int_dict
        self.str_array = str_dict
        self.bool_array = bool_dict

    @staticmethod
    def init() -> BeaconEventListScene:
        return BeaconEventListScene({}, {}, {})

    @staticmethod
    def read(stream: core.Data) -> BeaconEventListScene:
        int_dict = {}
        str_dict = {}
        bool_dict = {}
        for _ in range(stream.read_int()):
            int_dict[stream.read_int()] = stream.read_int()
        for _ in range(stream.read_int()):
            str_dict[stream.read_int()] = stream.read_string_list()
        for _ in range(stream.read_int()):
            bool_dict[stream.read_int()] = stream.read_bool()
        return BeaconEventListScene(int_dict, str_dict, bool_dict)

    def write(self, stream: core.Data):
        stream.write_int(len(self.int_array))
        for key, value in self.int_array.items():
            stream.write_int(key)
            stream.write_int(value)
        stream.write_int(len(self.str_array))
        for key, value in self.str_array.items():
            stream.write_int(key)
            stream.write_string_list(value)
        stream.write_int(len(self.bool_array))
        for key, value in self.bool_array.items():
            stream.write_int(key)
            stream.write_bool(value)

    def serialize(self) -> dict[str, Any]:
        return {
            "int_array": self.int_array,
            "str_array": self.str_array,
            "bool_array": self.bool_array,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> BeaconEventListScene:
        return BeaconEventListScene(
            data.get("int_array", []),
            data.get("str_array", []),
            data.get("bool_array", []),
        )

    def __repr__(self):
        return f"BeaconEventListScene({self.int_array}, {self.str_array}, {self.bool_array})"

    def __str__(self):
        return f"BeaconEventListScene({self.int_array}, {self.str_array}, {self.bool_array})"


# ============================================================
# FILE: cat.py
# ============================================================
from __future__ import annotations
from typing import Any
from bcsfe import core


class SkillLevel:
    def __init__(
        self,
        id: int,
        levels: list[int],
    ):
        self.id = id
        self.levels = levels

    def get_total_levels(self) -> int:
        return len(self.levels)

    @staticmethod
    def from_row(row: core.Row):
        id = row[0].to_int()
        levels = row[1:].to_int_list()
        return SkillLevel(id, levels)


class SkillLevelData:
    def __init__(self, levels: list[SkillLevel] | None):
        self.levels = levels

    @staticmethod
    def from_game_data(save_file: core.SaveFile) -> SkillLevelData | None:
        gdg = core.core_data.get_game_data_getter(save_file)
        data = gdg.download("DataLocal", "SkillLevel.csv")
        if data is None:
            return None
        csv = core.CSV(data)
        levels: list[SkillLevel] = []
        for line in csv.lines[1:]:
            levels.append(SkillLevel.from_row(line))
        return SkillLevelData(levels)

    def get_skill_level(self, id: int) -> SkillLevel | None:
        if self.levels is None:
            return None
        for level in self.levels:
            if level.id == id:
                return level
        return None


class Skill:
    def __init__(
        self,
        ability_id: int,
        max_lv: int,
        min1: int,
        max1: int,
        min2: int,
        max2: int,
        min3: int,
        max3: int,
        min4: int,
        max4: int,
        text_id: int,
        lvid: int,
        name_id: int,
        limit: int,
    ):
        self.ability_id = ability_id
        self.max_lv = max_lv
        self.min1 = min1
        self.max1 = max1
        self.min2 = min2
        self.max2 = max2
        self.min3 = min3
        self.max3 = max3
        self.min4 = min4
        self.max4 = max4
        self.text_id = text_id
        self.lvid = lvid
        self.name_id = name_id
        self.limit = limit


class CatSkill:
    def __init__(
        self,
        cat_id: int,
        type_id: int,
        skills: list[Skill],
    ):
        self.cat_id = cat_id
        self.type_id = type_id
        self.skills = skills

    @staticmethod
    def from_row(row: core.Row):
        cat_id = row[0].to_int()
        type_id = row[1].to_int()
        skills: list[Skill] = []
        for i in range(2, len(row), 14):
            skill = Skill(
                row[i].to_int(),
                row[i + 1].to_int(),
                row[i + 2].to_int(),
                row[i + 3].to_int(),
                row[i + 4].to_int(),
                row[i + 5].to_int(),
                row[i + 6].to_int(),
                row[i + 7].to_int(),
                row[i + 8].to_int(),
                row[i + 9].to_int(),
                row[i + 10].to_int(),
                row[i + 11].to_int(),
                row[i + 12].to_int(),
                row[i + 13].to_int(),
            )
            skills.append(skill)
        return CatSkill(cat_id, type_id, skills)


class CatSkills:
    def __init__(self, skills: dict[int, CatSkill]):
        self.skills = skills

    @staticmethod
    def from_game_data(save_file: core.SaveFile) -> CatSkills | None:
        gdg = core.core_data.get_game_data_getter(save_file)
        data = gdg.download("DataLocal", "SkillAcquisition.csv")
        if data is None:
            return None
        csv = core.CSV(data)
        skills: dict[int, CatSkill] = {}
        for line in csv.lines[1:]:
            skill = CatSkill.from_row(line)
            skills[skill.cat_id] = skill
        return CatSkills(skills)

    def get_cat_skill(self, cat_id: int) -> CatSkill | None:
        return self.skills.get(cat_id)


class SkillNames:
    def __init__(self, names: dict[int, str]):
        self.names = names

    @staticmethod
    def from_game_data(save_file: core.SaveFile) -> SkillNames | None:
        gdg = core.core_data.get_game_data_getter(save_file)
        data = gdg.download("resLocal", "SkillDescriptions.csv")
        if data is None:
            return None
        csv = core.CSV(
            data, delimiter=core.Delimeter.from_country_code_res(save_file.cc)
        )
        names: dict[int, str] = {}
        for line in csv.lines[1:]:
            names[line[0].to_int()] = line[1].to_str()
        return SkillNames(names)

    def get_skill_name(self, skill_id: int) -> str | None:
        return self.names.get(skill_id)


class TalentData:
    def __init__(
        self,
        skill_names: SkillNames,
        skill_levels: SkillLevelData,
        cats: CatSkills,
    ):
        self.skill_names = skill_names
        self.skill_levels = skill_levels
        self.cats = cats

    @staticmethod
    def from_game_data(save_file: core.SaveFile) -> TalentData | None:
        skill_names = SkillNames.from_game_data(save_file)
        skill_levels = SkillLevelData.from_game_data(save_file)
        cats = CatSkills.from_game_data(save_file)
        if skill_names is None or skill_levels is None or cats is None:
            return None

        return TalentData(skill_names, skill_levels, cats)

    def get_skill_name(self, skill_id: int) -> str | None:
        return self.skill_names.get_skill_name(skill_id)

    def get_skill_level(self, skill_id: int) -> SkillLevel | None:
        return self.skill_levels.get_skill_level(skill_id)

    def get_cat_skill(self, cat_id: int) -> CatSkill | None:
        return self.cats.get_cat_skill(cat_id)

    def get_skill_from_cat(self, cat_id: int, skill_id: int) -> Skill | None:
        cat_skill = self.get_cat_skill(cat_id)
        if cat_skill is None:
            return None
        for skill in cat_skill.skills:
            if skill.ability_id == skill_id:
                return skill
        return None

    def get_talent_from_cat_skill(self, cat: core.Cat, skill_id: int) -> Talent | None:
        talents = cat.talents
        if talents is None:
            return None
        for talent in talents:
            if talent.id == skill_id:
                return talent
        return None

    def get_cat_skill_name(self, cat_id: int, skill_id: int) -> str | None:
        skill = self.get_skill_from_cat(cat_id, skill_id)
        if skill is None:
            return None
        return self.get_skill_name(skill.text_id)

    def get_cat_skill_level(self, cat_id: int, skill_id: int) -> SkillLevel | None:
        skill = self.get_skill_from_cat(cat_id, skill_id)
        if skill is None:
            return None
        return self.get_skill_level(skill.lvid)

    def get_cat_talents(
        self, cat: core.Cat
    ) -> tuple[list[str], list[int], list[int], list[int]] | None:
        talent_data_cat = self.get_cat_skill(cat.id)
        if talent_data_cat is None or cat.talents is None:
            return None
        # save_talent_data = cat.talents
        talent_names: list[str] = []
        max_levels: list[int] = []
        current_levels: list[int] = []
        ids: list[int] = []
        for skill in talent_data_cat.skills:
            name = self.get_skill_name(skill.text_id)
            talent = self.get_talent_from_cat_skill(cat, skill.ability_id)
            if name is None or talent is None:
                continue

            max_level = skill.max_lv
            if max_level == 0:
                max_level = 1

            max_levels.append(max_level)
            talent_names.append(name.split("<br>")[0])
            current_levels.append(talent.level)
            ids.append(skill.ability_id)

        return talent_names, max_levels, current_levels, ids


class Talent:
    def __init__(self, id: int, level: int):
        self.id = id
        self.level = level

    @staticmethod
    def init() -> Talent:
        return Talent(0, 0)

    def reset(self):
        self.level = 0

    @staticmethod
    def read(stream: core.Data):
        return Talent(stream.read_int(), stream.read_int())

    def write(self, stream: core.Data):
        stream.write_int(self.id)
        stream.write_int(self.level)

    def serialize(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "level": self.level,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> Talent:
        return Talent(
            data["id"],
            data["level"],
        )

    def __repr__(self):
        return f"Talent({self.id}, {self.level})"

    def __str__(self):
        return self.__repr__()


class NyankoPictureBookCatData:
    def __init__(
        self,
        cat_id: int,
        is_displayed_in_catguide: bool,
        limited: bool,
        total_forms: int,
        hint_display_type: int,
        scale_0: int,
        scale_1: int,
        scale_2: int,
        scale_3: int,
    ):
        self.cat_id = cat_id
        self.is_displayed_in_catguide = is_displayed_in_catguide
        self.limited = limited
        self.total_forms = total_forms
        self.hint_display_type = hint_display_type
        self.scale_0 = scale_0
        self.scale_1 = scale_1
        self.scale_2 = scale_2
        self.scale_3 = scale_3


class NyankoPictureBook:
    def __init__(self, save_file: core.SaveFile):
        self.save_file = save_file
        self.cats = self.get_cats()

    def get_cats(self) -> list[NyankoPictureBookCatData] | None:
        gdg = core.core_data.get_game_data_getter(self.save_file)
        data = gdg.download("DataLocal", "nyankoPictureBookData.csv")
        if data is None:
            return None
        csv = core.CSV(data)
        cats: list[NyankoPictureBookCatData] = []
        for i, line in enumerate(csv):
            cat = NyankoPictureBookCatData(
                i,
                line[0].to_bool(),
                line[1].to_bool(),
                line[2].to_int(),
                line[3].to_int(),
                line[4].to_int(),
                line[5].to_int(),
                line[6].to_int(),
                line[7].to_int(),
            )
            cats.append(cat)
        return cats

    def get_cat(self, cat_id: int) -> NyankoPictureBookCatData | None:
        if self.cats is None:
            return None
        for cat in self.cats:
            if cat.cat_id == cat_id:
                return cat
        return None

    def get_obtainable_cats(self) -> list[NyankoPictureBookCatData] | None:
        if self.cats is None:
            return None
        return [cat for cat in self.cats if cat.is_displayed_in_catguide]


class EvolveItem:
    """Represents an item used to evolve a unit."""

    def __init__(
        self,
        item_id: int,
        amount: int,
    ):
        """Initializes a new EvolveItem object.

        Args:
            item_id (int): The ID of the item.
            amount (int): The amount of the item.
        """
        self.item_id = item_id
        self.amount = amount

    def __str__(self) -> str:
        """Gets a string representation of the EvolveItem object.

        Returns:
            str: The string representation of the EvolveItem object.
        """
        return f"{self.item_id}:{self.amount}"

    def __repr__(self) -> str:
        """Gets a string representation of the EvolveItem object.

        Returns:
            str: The string representation of the EvolveItem object.
        """
        return str(self)


class EvolveItems:
    """Represents the items used to evolve a unit."""

    def __init__(self, evolve_items: list[EvolveItem]):
        """Initializes a new EvolveItems object.

        Args:
            evolve_items (list[EvolveItem]): The items used to evolve a unit.
        """
        self.evolve_items = evolve_items

    @staticmethod
    def from_unit_buy_list(raw_data: core.Row, start_index: int) -> EvolveItems:
        """Creates a new EvolveItems object from a row from unitbuy.csv.

        Args:
            raw_data (core.Row): The row from unitbuy.csv.

        Returns:
            EvolveItems: The EvolveItems object.
        """
        items: list[EvolveItem] = []
        for i in range(5):
            item_id = raw_data[start_index + i * 2].to_int()
            amount = raw_data[start_index + 1 + i * 2].to_int()
            items.append(EvolveItem(item_id, amount))
        return EvolveItems(items)


class UnitBuyCatData:
    def __init__(self, id: int, raw_data: core.Row):
        self.id = id
        self.assign(raw_data)

    def assign(self, raw_data: core.Row):
        self.stage_unlock = raw_data[0].to_int()
        self.purchase_cost = raw_data[1].to_int()
        self.upgrade_costs = [cost.to_int() for cost in raw_data[2:12]]
        self.unlock_source = raw_data[12].to_int()
        self.rarity = raw_data[13].to_int()
        self.position_order = raw_data[14].to_int()
        self.chapter_unlock = raw_data[15].to_int()
        self.sell_price = raw_data[16].to_int()
        self.gatya_rarity = raw_data[17].to_int()
        self.original_max_levels = raw_data[18].to_int(), raw_data[19].to_int()
        self.force_true_form_level = raw_data[20].to_int()
        self.second_form_unlock_level = raw_data[21].to_int()
        self.unknown_22 = raw_data[22].to_int()
        self.tf_id = raw_data[23].to_int()
        self.ff_id = raw_data[24].to_int()
        self.evolve_level_tf = raw_data[25].to_int()
        self.evolve_level_ff = raw_data[26].to_int()
        self.evolve_cost_tf = raw_data[27].to_int()
        self.evolve_items_tf = EvolveItems.from_unit_buy_list(raw_data, 28)
        self.evolve_cost_ff = raw_data[38].to_int()
        self.evolve_items_ff = EvolveItems.from_unit_buy_list(raw_data, 39)
        self.max_upgrade_level_no_catseye = raw_data[49].to_int()
        self.max_upgrade_level_catseye = raw_data[50].to_int()
        self.max_plus_upgrade_level = raw_data[51].to_int()
        self.unknown_52 = raw_data[52].to_int()
        self.unknown_53 = raw_data[53].to_int()
        self.unknown_54 = raw_data[54].to_int()
        self.unknown_55 = raw_data[55].to_int()
        self.catseye_usage_pattern = raw_data[56].to_int()
        self.game_version = raw_data[57].to_int()
        self.np_sell_price = raw_data[58].to_int()
        self.unknwon_59 = raw_data[59].to_int()
        self.unknown_60 = raw_data[60].to_int()
        self.egg_value = raw_data[61].to_int()
        self.egg_id = raw_data[62].to_int()


class UnitBuy:
    def __init__(self, save_file: core.SaveFile):
        self.save_file = save_file
        self.unit_buy = self.read_unit_buy()

    def read_unit_buy(self) -> list[UnitBuyCatData] | None:
        unit_buy: list[UnitBuyCatData] = []
        gdg = core.core_data.get_game_data_getter(self.save_file)
        data = gdg.download("DataLocal", "unitbuy.csv")
        if data is None:
            return None
        csv = core.CSV(data)
        for i, line in enumerate(csv):
            unit_buy.append(UnitBuyCatData(i, line))
        return unit_buy

    def get_unit_buy(self, id: int) -> UnitBuyCatData | None:
        if self.unit_buy is None:
            return None
        try:
            return self.unit_buy[id]
        except IndexError:
            return None

    def get_cat_rarity(self, id: int) -> int:
        unit_buy = self.get_unit_buy(id)
        if unit_buy is None:
            return -1
        return unit_buy.rarity


class UnitLimitCatData:
    def __init__(self, cat_id: int, values: list[int]):
        self.cat_id = cat_id
        self.values = values


class UnitLimit:
    def __init__(self, save_file: core.SaveFile):
        self.save_file = save_file
        self.unit_limit = self.read_unit_limit()

    def read_unit_limit(self) -> list[UnitLimitCatData] | None:
        unit_limit: list[UnitLimitCatData] = []
        gdg = core.core_data.get_game_data_getter(self.save_file)
        data = gdg.download("DataLocal", "unitlimit.csv")
        if data is None:
            return None
        csv = core.CSV(data)
        for i, line in enumerate(csv):
            unit_limit.append(UnitLimitCatData(i, line.to_int_list()))
        return unit_limit

    def get_unit_limit(self, id: int) -> UnitLimitCatData | None:
        if self.unit_limit is None:
            return None

        try:
            return self.unit_limit[id]
        except IndexError:
            return None


class Cat:
    def __init__(self, id: int, unlocked: int):
        self.id = id
        self.unlocked = unlocked
        self.talents: list[Talent] | None = None
        self.upgrade: core.Upgrade = core.Upgrade.init()
        self.current_form: int = 0
        self.unlocked_forms: int = 0
        self.gatya_seen: int = 0
        self.max_upgrade_level: core.Upgrade = core.Upgrade.init()
        self.catguide_collected: bool = False
        self.fourth_form: int = 0
        self.catseyes_used: int = 0

        self.names: list[str] | None = None

    def get_talent_from_id(self, id: int) -> Talent | None:
        for talent in self.talents or []:
            if talent.id == id:
                return talent
        return None

    def unlock(self, save_file: core.SaveFile):
        self.unlocked = 1
        self.gatya_seen = 1
        core.core_data.get_chara_drop(save_file).unlock_drops_from_cat_id(self.id)
        save_file.unlock_equip_menu()

    def remove(self, reset: bool = False, save_file: core.SaveFile | None = None):
        self.unlocked = 0
        if reset:
            self.reset()
            if save_file is not None:
                save_file.cats.chara_new_flags[self.id] = 0
                core.core_data.get_chara_drop(save_file).remove_drops_from_cat_id(
                    self.id
                )

    def true_form(self, save_file: core.SaveFile, set_current_form: bool = True):
        self.set_form(2, save_file, set_current_form)

    def set_form(
        self, form: int, save_file: core.SaveFile, set_current_form: bool = True
    ):
        if core.core_data.config.get_bool(core.ConfigKey.UNLOCK_CAT_ON_EDIT):
            self.unlock(save_file)
        self.unlocked_forms = form + 1
        if set_current_form:
            self.current_form = form

    def set_form_true(
        self,
        save_file: core.SaveFile,
        total_forms: int,
        set_current_form: bool = True,
        fourth_form: bool = False,
    ):
        if total_forms == 4 and self.unlocked_forms == 3 and fourth_form:
            self.unlock_fourth_form(save_file, set_current_form)
        elif total_forms >= 3:
            self.true_form(save_file, set_current_form)
        elif total_forms == 2:
            self.unlocked_forms = 0
            self.current_form = 1
        else:
            self.unlocked_forms = 0
            self.current_form = 0

    def remove_true_form(self):
        self.unlocked_forms = 0
        self.current_form = min(self.current_form, 1)
        self.fourth_form = 0

    def unlock_fourth_form(
        self, save_file: core.SaveFile, set_current_form: bool = True
    ):
        if set_current_form:
            self.current_form = 3
        if core.core_data.config.get_bool(core.ConfigKey.UNLOCK_CAT_ON_EDIT):
            self.unlock(save_file)
        self.fourth_form = 2

    def remove_fourth_form(self):
        self.current_form = min(self.current_form, 2)
        self.fourth_form = 0

    def set_upgrade(
        self,
        save_file: core.SaveFile,
        upgrade: core.Upgrade,
        only_plus: bool = False,
    ):
        if core.core_data.config.get_bool(core.ConfigKey.UNLOCK_CAT_ON_EDIT):
            self.unlock(save_file)
        base = upgrade.base
        plus = upgrade.plus
        if base != -1 and not only_plus:
            self.upgrade.base = upgrade.get_random_base()
        if plus != -1:
            self.upgrade.plus = upgrade.get_random_plus()

    def upgrade_base(self, save_file: core.SaveFile):
        if core.core_data.config.get_bool(core.ConfigKey.UNLOCK_CAT_ON_EDIT):
            self.unlock(save_file)
        self.upgrade.upgrade()

    def reset(self):
        self.unlocked = 0
        self.current_form = 0
        self.unlocked_forms = 0
        self.gatya_seen = 0
        self.catguide_collected = False
        self.fourth_form = 0
        self.catseyes_used = 0
        self.upgrade.reset()
        for talent in self.talents or []:
            talent.reset()

    @staticmethod
    def init(id: int) -> Cat:
        return Cat(id, 0)

    @staticmethod
    def read_unlocked(id: int, stream: core.Data):
        return Cat(id, stream.read_int())

    def write_unlocked(self, stream: core.Data):
        stream.write_int(self.unlocked)

    def read_upgrade(self, stream: core.Data):
        self.upgrade = core.Upgrade.read(stream)

    def write_upgrade(self, stream: core.Data):
        self.upgrade.write(stream)

    def read_current_form(self, stream: core.Data):
        self.current_form = stream.read_int()

    def write_current_form(self, stream: core.Data):
        stream.write_int(self.current_form)

    def read_unlocked_forms(self, stream: core.Data):
        self.unlocked_forms = stream.read_int()

    def write_unlocked_forms(self, stream: core.Data):
        stream.write_int(self.unlocked_forms)

    def read_gatya_seen(self, stream: core.Data):
        self.gatya_seen = stream.read_int()

    def write_gatya_seen(self, stream: core.Data):
        stream.write_int(self.gatya_seen)

    def read_max_upgrade_level(self, stream: core.Data):
        level = core.Upgrade.read(stream)
        self.max_upgrade_level = level

    def write_max_upgrade_level(self, stream: core.Data):
        self.max_upgrade_level.write(stream)

    def read_catguide_collected(self, stream: core.Data):
        self.catguide_collected = stream.read_bool()

    def write_catguide_collected(self, stream: core.Data):
        stream.write_bool(self.catguide_collected)

    def read_fourth_form(self, stream: core.Data):
        self.fourth_form = stream.read_int()

    def write_fourth_form(self, stream: core.Data):
        stream.write_int(self.fourth_form)

    def read_catseyes_used(self, stream: core.Data):
        self.catseyes_used = stream.read_int()

    def write_catseyes_used(self, stream: core.Data):
        stream.write_int(self.catseyes_used)

    def serialize(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "unlocked": self.unlocked,
            "upgrade": self.upgrade.serialize(),
            "current_form": self.current_form,
            "unlocked_forms": self.unlocked_forms,
            "gatya_seen": self.gatya_seen,
            "max_upgrade_level": self.max_upgrade_level.serialize(),
            "catguide_collected": self.catguide_collected,
            "fourth_form": self.fourth_form,
            "catseyes_used": self.catseyes_used,
            "talents": (
                [talent.serialize() for talent in self.talents]
                if self.talents is not None
                else None
            ),
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> Cat:
        cat = Cat(data["id"], data["unlocked"])
        cat.upgrade = core.Upgrade.deserialize(data["upgrade"])
        cat.current_form = data["current_form"]
        cat.unlocked_forms = data["unlocked_forms"]
        cat.gatya_seen = data["gatya_seen"]
        cat.max_upgrade_level = core.Upgrade.deserialize(data["max_upgrade_level"])
        cat.catguide_collected = data["catguide_collected"]
        cat.fourth_form = data["fourth_form"]
        cat.catseyes_used = data["catseyes_used"]
        cat.talents = (
            [Talent.deserialize(talent) for talent in data["talents"]]
            if data["talents"] is not None
            else None
        )
        return cat

    def __repr__(self) -> str:
        return f"Cat(id={self.id}, unlocked={self.unlocked}, upgrade={self.upgrade}, current_form={self.current_form}, unlocked_forms={self.unlocked_forms}, gatya_seen={self.gatya_seen}, max_upgrade_level={self.max_upgrade_level}, catguide_collected={self.catguide_collected}, fourth_form={self.fourth_form}, catseyes_used={self.catseyes_used}, talents={self.talents})"

    def __str__(self) -> str:
        return self.__repr__()

    def read_talents(self, stream: core.Data):
        self.talents = []
        for _ in range(stream.read_int()):
            self.talents.append(Talent.read(stream))

    def write_talents(self, stream: core.Data):
        if self.talents is None:
            return
        stream.write_int(len(self.talents))
        for talent in self.talents:
            talent.write(stream)

    def get_names_cls(self, save_file: core.SaveFile) -> list[str] | None:
        if self.names is None:
            self.names = Cat.get_names(self.id, save_file)
        return self.names

    @staticmethod
    def get_names(
        id: int,
        save_file: core.SaveFile,
    ) -> list[str] | None:
        file_name = f"Unit_Explanation{id + 1}_{core.core_data.get_lang(save_file)}.csv"
        data = core.core_data.get_game_data_getter(save_file).download(
            "resLocal", file_name
        )
        if data is None:
            return None
        csv = core.CSV(
            data,
            core.Delimeter.from_country_code_res(save_file.cc),
            remove_empty=False,
        )
        names: list[str] = []
        for line in csv.lines:
            names.append(line[0].to_str())

        return names


class StorageItem:
    def __init__(self, item_id: int):
        self.item_id = item_id
        self.item_type = 0

    @staticmethod
    def from_cat(cat_id: int) -> StorageItem:
        item = StorageItem(cat_id)
        item.item_type = 1
        return item

    @staticmethod
    def from_special_skill(special_skill_id: int) -> StorageItem:
        item = StorageItem(special_skill_id)
        item.item_type = 2
        return item

    @staticmethod
    def init() -> StorageItem:
        return StorageItem(0)

    @staticmethod
    def read_item_id(stream: core.Data):
        return StorageItem(stream.read_int())

    def write_item_id(self, stream: core.Data):
        stream.write_int(self.item_id)

    def read_item_type(self, stream: core.Data):
        self.item_type = stream.read_int()

    def write_item_type(self, stream: core.Data):
        stream.write_int(self.item_type)

    def serialize(self) -> dict[str, Any]:
        return {
            "item_id": self.item_id,
            "item_type": self.item_type,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> StorageItem:
        item = StorageItem(data.get("item_id", 0))
        item.item_type = data.get("item_type", 0)
        return item

    def __repr__(self) -> str:
        return f"StorageItem(item_id={self.item_id}, item_type={self.item_type})"

    def __str__(self) -> str:
        return f"StorageItem(item_id={self.item_id}, item_type={self.item_type})"


class Cats:
    def __init__(self, cats: list[Cat], total_storage_items: int = 0):
        self.cats = cats
        self.storage_items = [StorageItem.init() for _ in range(total_storage_items)]
        self.favourites: dict[int, bool] = {}
        self.chara_new_flags: dict[int, int] = {}
        self.unit_buy: UnitBuy | None = None
        self.unit_limit: UnitLimit | None = None
        self.nyanko_picture_book: NyankoPictureBook | None = None
        self.talent_data: TalentData | None = None

    def get_all_cats(self) -> list[Cat]:
        return self.cats

    @staticmethod
    def init(gv: core.GameVersion) -> Cats:
        total_cats = Cats.get_gv_cats(gv)
        if total_cats is None:
            total_cats = 0
        cats_l: list[Cat] = []
        for i in range(total_cats):
            cats_l.append(Cat.init(i))

        if gv < 110100:
            total_storage_items = 100
        else:
            total_storage_items = 0
        return Cats(cats_l, total_storage_items)

    @staticmethod
    def get_gv_cats(gv: core.GameVersion) -> int | None:
        if gv == 20:
            total_cats = 203
        elif gv == 21:
            total_cats = 214
        elif gv == 22:
            total_cats = 231
        elif gv == 23:
            total_cats = 241
        elif gv == 24:
            total_cats = 249
        elif gv == 25:
            total_cats = 260
        else:
            total_cats = None
        return total_cats

    def get_unlocked_cats(self) -> list[Cat]:
        return [cat for cat in self.cats if cat.unlocked]

    def get_non_unlocked_cats(self) -> list[Cat]:
        return [cat for cat in self.cats if not cat.unlocked]

    def get_non_gacha_cats(self, save_file: core.SaveFile) -> list[Cat]:
        unitbuy = self.read_unitbuy(save_file)
        cats: list[Cat] = []
        for cat in self.cats:
            unit_buy_data = unitbuy.get_unit_buy(cat.id)
            if unit_buy_data is None:
                continue

            if unit_buy_data.unlock_source != 2:
                cats.append(cat)

        return cats

    def read_unitbuy(self, save_file: core.SaveFile) -> UnitBuy:
        if self.unit_buy is None:
            self.unit_buy = UnitBuy(save_file)
        return self.unit_buy

    def read_unitlimit(self, save_file: core.SaveFile) -> UnitLimit:
        if self.unit_limit is None:
            self.unit_limit = UnitLimit(save_file)
        return self.unit_limit

    def read_nyanko_picture_book(self, save_file: core.SaveFile) -> NyankoPictureBook:
        if self.nyanko_picture_book is None:
            self.nyanko_picture_book = NyankoPictureBook(save_file)
        return self.nyanko_picture_book

    def read_talent_data(self, save_file: core.SaveFile) -> TalentData | None:
        if self.talent_data is None:
            self.talent_data = TalentData.from_game_data(save_file)
        return self.talent_data

    def get_cats_rarity(self, save_file: core.SaveFile, rarity: int) -> list[Cat]:
        unit_buy = self.read_unitbuy(save_file)
        return [cat for cat in self.cats if unit_buy.get_cat_rarity(cat.id) == rarity]

    def get_cats_name(
        self,
        save_file: core.SaveFile,
        search_name: str,
    ) -> list[Cat]:
        cats: list[Cat] = []
        for cat in self.cats:
            names = cat.get_names_cls(save_file)
            if names is None:
                continue
            for name in names:
                if search_name.lower() in name.lower():
                    cats.append(cat)
                    break
        return cats

    def get_cats_obtainable(self, save_file: core.SaveFile) -> list[Cat] | None:
        nyanko_picture_book = self.read_nyanko_picture_book(save_file)
        obtainable_cats = nyanko_picture_book.get_obtainable_cats()
        if obtainable_cats is None:
            return None
        ny_cats = [cat.cat_id for cat in obtainable_cats]
        cats: list[Cat] = []
        for cat in self.cats:
            if cat.id in ny_cats:
                cats.append(cat)
        return cats

    def get_cats_non_obtainable(self, save_file: core.SaveFile) -> list[Cat] | None:
        nyanko_picture_book = self.read_nyanko_picture_book(save_file)
        obtainable_cats = nyanko_picture_book.get_obtainable_cats()
        if obtainable_cats is None:
            return None
        ny_cats = [cat.cat_id for cat in obtainable_cats]
        cats: list[Cat] = []
        for cat in self.cats:
            if cat.id not in ny_cats:
                cats.append(cat)
        return cats

    def get_cats_gatya_banner(
        self, save_file: core.SaveFile, gatya_id: int
    ) -> list[core.Cat] | None:
        cat_ids = save_file.gatya.read_gatya_data_set(save_file).get_cat_ids(gatya_id)
        if cat_ids is None:
            return None
        return self.get_cats_by_ids(cat_ids)

    def true_form_cats(
        self,
        save_file: core.SaveFile,
        cats: list[Cat],
        force: bool = False,
        set_current_forms: bool = True,
    ):
        pic_book = self.read_nyanko_picture_book(save_file)
        for cat in cats:
            pic_book_cat = pic_book.get_cat(cat.id)
            if force:
                cat.true_form(save_file, set_current_form=set_current_forms)
            elif pic_book_cat is not None:
                cat.set_form_true(
                    save_file,
                    pic_book_cat.total_forms,
                    set_current_form=set_current_forms,
                )

    def fourth_form_cats(
        self,
        save_file: core.SaveFile,
        cats: list[Cat],
        force: bool = False,
        set_current_forms: bool = True,
    ):
        pic_book = self.read_nyanko_picture_book(save_file)
        for cat in cats:
            pic_book_cat = pic_book.get_cat(cat.id)
            if force:
                cat.unlock_fourth_form(save_file, set_current_form=set_current_forms)
            elif pic_book_cat is not None:
                cat.set_form_true(
                    save_file,
                    pic_book_cat.total_forms,
                    set_current_form=set_current_forms,
                    fourth_form=True,
                )

    def get_cats_by_ids(self, ids: list[int]) -> list[Cat]:
        cats: list[Cat] = []
        for cat in self.cats:
            if cat.id in ids:
                cats.append(cat)
        return cats

    def get_cat_by_id(self, id: int) -> Cat | None:
        for cat in self.cats:
            if cat.id == id:
                return cat
        return None

    @staticmethod
    def get_rarity_names(save_file: core.SaveFile) -> list[str]:
        localizable = save_file.get_localizable()
        rarity_names: list[str] = []
        rarity_index = 1
        while True:
            rarity_name = localizable.get(f"rarity_name_{rarity_index}")
            if rarity_name is None:
                break
            rarity_names.append(rarity_name)
            rarity_index += 1
        return rarity_names

    @staticmethod
    def read_unlocked(stream: core.Data, gv: core.GameVersion) -> Cats:
        total_cats = Cats.get_gv_cats(gv)
        if total_cats is None:
            total_cats = stream.read_int()
        cats_l: list[Cat] = []
        for i in range(total_cats):
            cats_l.append(Cat.read_unlocked(i, stream))
        return Cats(cats_l)

    def write_unlocked(self, stream: core.Data, gv: core.GameVersion):
        total_cats = Cats.get_gv_cats(gv)
        if total_cats is None:
            stream.write_int(len(self.cats))
        for cat in self.cats:
            cat.write_unlocked(stream)

    def read_upgrade(self, stream: core.Data, gv: core.GameVersion):
        total_cats = Cats.get_gv_cats(gv)
        if total_cats is None:
            total_cats = stream.read_int()
        for cat in self.cats:
            cat.read_upgrade(stream)

    def write_upgrade(self, stream: core.Data, gv: core.GameVersion):
        total_cats = Cats.get_gv_cats(gv)
        if total_cats is None:
            stream.write_int(len(self.cats))
        for cat in self.cats:
            cat.write_upgrade(stream)

    def read_current_form(self, stream: core.Data, gv: core.GameVersion):
        total_cats = Cats.get_gv_cats(gv)
        if total_cats is None:
            total_cats = stream.read_int()
        for cat in self.cats:
            cat.read_current_form(stream)

    def write_current_form(self, stream: core.Data, gv: core.GameVersion):
        total_cats = Cats.get_gv_cats(gv)
        if total_cats is None:
            stream.write_int(len(self.cats))
        for cat in self.cats:
            cat.write_current_form(stream)

    def read_unlocked_forms(self, stream: core.Data, gv: core.GameVersion):
        total_cats = Cats.get_gv_cats(gv)
        if total_cats is None:
            total_cats = stream.read_int()
        for cat in self.cats:
            cat.read_unlocked_forms(stream)

    def write_unlocked_forms(self, stream: core.Data, gv: core.GameVersion):
        total_cats = Cats.get_gv_cats(gv)
        if total_cats is None:
            stream.write_int(len(self.cats))
        for cat in self.cats:
            cat.write_unlocked_forms(stream)

    def read_gatya_seen(self, stream: core.Data, gv: core.GameVersion):
        total_cats = Cats.get_gv_cats(gv)
        if total_cats is None:
            total_cats = stream.read_int()
        for cat in self.cats:
            cat.read_gatya_seen(stream)

    def write_gatya_seen(self, stream: core.Data, gv: core.GameVersion):
        total_cats = Cats.get_gv_cats(gv)
        if total_cats is None:
            stream.write_int(len(self.cats))
        for cat in self.cats:
            cat.write_gatya_seen(stream)

    def read_max_upgrade_levels(self, stream: core.Data, gv: core.GameVersion):
        total_cats = Cats.get_gv_cats(gv)
        if total_cats is None:
            total_cats = stream.read_int()
        for cat in self.cats:
            cat.read_max_upgrade_level(stream)

    def write_max_upgrade_levels(self, stream: core.Data, gv: core.GameVersion):
        total_cats = Cats.get_gv_cats(gv)
        if total_cats is None:
            stream.write_int(len(self.cats))
        for cat in self.cats:
            cat.write_max_upgrade_level(stream)

    def read_storage(self, stream: core.Data, gv: core.GameVersion):
        if gv < 110100:
            total_storage = 100
        else:
            total_storage = stream.read_short()
        self.storage_items: list[StorageItem] = []
        for _ in range(total_storage):
            self.storage_items.append(StorageItem.read_item_id(stream))
        for item in self.storage_items:
            item.read_item_type(stream)

    def write_storage(self, stream: core.Data, gv: core.GameVersion):
        if gv >= 110100:
            stream.write_short(len(self.storage_items))
        for item in self.storage_items:
            item.write_item_id(stream)
        for item in self.storage_items:
            item.write_item_type(stream)

    def read_catguide_collected(self, stream: core.Data):
        total_cats = stream.read_int()
        for i in range(total_cats):
            self.cats[i].read_catguide_collected(stream)

    def write_catguide_collected(self, stream: core.Data):
        stream.write_int(len(self.cats))
        for cat in self.cats:
            cat.write_catguide_collected(stream)

    def read_fourth_forms(self, stream: core.Data):
        total_cats = stream.read_int()
        for i in range(total_cats):
            self.cats[i].read_fourth_form(stream)

    def read_catseyes_used(self, stream: core.Data):
        total_cats = stream.read_int()
        for i in range(total_cats):
            self.cats[i].read_catseyes_used(stream)

    def write_catseyes_used(self, stream: core.Data):
        stream.write_int(len(self.cats))
        for cat in self.cats:
            cat.write_catseyes_used(stream)

    def write_fourth_forms(self, stream: core.Data):
        stream.write_int(len(self.cats))
        for cat in self.cats:
            cat.write_fourth_form(stream)

    def read_favorites(self, stream: core.Data):
        self.favourites: dict[int, bool] = {}
        total_cats = stream.read_int()
        for _ in range(total_cats):
            cat_id = stream.read_int()
            self.favourites[cat_id] = stream.read_bool()

    def write_favorites(self, stream: core.Data):
        stream.write_int(len(self.favourites))
        for cat_id, is_favourite in self.favourites.items():
            stream.write_int(cat_id)
            stream.write_bool(is_favourite)

    def read_chara_new_flags(self, stream: core.Data):
        self.chara_new_flags: dict[int, int] = {}
        total_cats = stream.read_int()
        for _ in range(total_cats):
            cat_id = stream.read_int()
            self.chara_new_flags[cat_id] = stream.read_int()

    def write_chara_new_flags(self, stream: core.Data):
        stream.write_int(len(self.chara_new_flags))
        for cat_id, new_flag in self.chara_new_flags.items():
            stream.write_int(cat_id)
            stream.write_int(new_flag)

    def read_talents(self, stream: core.Data):
        total_cats = stream.read_int()
        for _ in range(total_cats):
            cat_id = stream.read_int()
            if cat_id < 0 or cat_id >= len(self.cats):
                cat = Cat.init(cat_id)
                cat.read_talents(stream)
                continue
            self.cats[cat_id].read_talents(stream)

    def write_talents(self, stream: core.Data):
        total_talents = 0
        for cat in self.cats:
            total_talents += 1 if cat.talents is not None else 0
        stream.write_int(total_talents)
        for cat in self.cats:
            if cat.talents is None:
                continue
            stream.write_int(cat.id)
            cat.write_talents(stream)

    def serialize(self) -> dict[str, Any]:
        return {
            "cats": [cat.serialize() for cat in self.cats],
            "storage_items": [item.serialize() for item in self.storage_items],
            "favorites": self.favourites,
            "chara_new_flags": self.chara_new_flags,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> Cats:
        cats_l = [Cat.deserialize(cat) for cat in data.get("cats", [])]
        cats = Cats(cats_l)
        cats.storage_items = [
            StorageItem.deserialize(item) for item in data.get("storage_items", [])
        ]
        cats.favourites = data.get("favorites", {})
        cats.chara_new_flags = data.get("chara_new_flags", {})
        return cats

    def __repr__(self) -> str:
        return f"Cats(cats={self.cats}, storage_items={self.storage_items}, favourites={self.favourites}, chara_new_flags={self.chara_new_flags})"

    def __str__(self) -> str:
        return self.__repr__()


# ============================================================
# FILE: drop_chara.py
# ============================================================
from __future__ import annotations
from dataclasses import dataclass

from bcsfe import core


@dataclass
class Drop:
    stage_id: int
    save_id: int
    chara_id: int


class CharaDrop:
    def __init__(self, save_file: core.SaveFile):
        self.save_file = save_file
        self.drops = self.get_drops()

    def get_drops(self) -> list[Drop] | None:
        gdg = core.core_data.get_game_data_getter(self.save_file)
        data = gdg.download("DataLocal", "drop_chara.csv")
        if data is None:
            return None
        csv = core.CSV(data)
        drops: list[Drop] = []
        for line in csv.lines[1:]:
            drops.append(
                Drop(
                    stage_id=line[0].to_int(),
                    save_id=line[1].to_int(),
                    chara_id=line[2].to_int(),
                )
            )

        return drops

    def get_drop(self, stage_id: int) -> Drop | None:
        if self.drops is None:
            return None
        for drop in self.drops:
            if drop.stage_id == stage_id:
                return drop

        return None

    def get_drops_from_chara_id(self, chara_id: int) -> list[Drop] | None:
        if self.drops is None:
            return None
        drops: list[Drop] = []
        for drop in self.drops:
            if drop.chara_id == chara_id:
                drops.append(drop)

        return drops

    def unlock_drops_from_cat_id(self, cat_id: int) -> None:
        drops = self.get_drops_from_chara_id(cat_id)
        if drops is None:
            return
        for drop in drops:
            try:
                self.save_file.unit_drops[drop.save_id] = 1
            except IndexError:
                pass

    def remove_drops_from_cat_id(self, cat_id: int) -> None:
        drops = self.get_drops_from_chara_id(cat_id)
        if drops is None:
            return
        for drop in drops:
            try:
                self.save_file.unit_drops[drop.save_id] = 0
            except IndexError:
                pass


# ============================================================
# FILE: gambling.py
# ============================================================
from __future__ import annotations
from bcsfe import core
from typing import Any

from bcsfe.cli import color


class GamblingEvent:
    def __init__(
        self,
        completed: dict[int, bool],
        values: dict[int, dict[int, int]],
        start_times: dict[int, int | float],
    ):
        self.completed = completed
        self.values = values
        self.start_times = start_times

    @staticmethod
    def init() -> GamblingEvent:
        return GamblingEvent({}, {}, {})

    @staticmethod
    def read(data: core.Data, game_version: core.GameVersion) -> GamblingEvent:
        total = data.read_short()
        completed: dict[int, bool] = {}

        for _ in range(total):
            key = data.read_short()
            completed[key] = data.read_bool()

        total = data.read_short()
        values: dict[int, dict[int, int]] = {}

        for _ in range(total):
            key = data.read_short()
            if key not in values:
                values[key] = {}

            total2 = data.read_short()
            for _ in range(total2):
                key2 = data.read_short()

                values[key][key2] = data.read_short()

        total = data.read_short()
        start_times: dict[int, int | float] = {}

        for _ in range(total):
            key = data.read_short()

            if game_version < 90100:
                value = data.read_double()
            else:
                value = data.read_int()

            start_times[key] = value

        return GamblingEvent(completed, values, start_times)

    def write(self, data: core.Data, game_version: core.GameVersion):
        data.write_short(len(self.completed))
        data.write_short_bool_dict(self.completed, write_length=False)

        data.write_short(len(self.values))

        for key, value in self.values.items():
            data.write_short(key)
            data.write_short(len(value))

            for key2, value2 in value.items():
                data.write_short(key2)
                data.write_short(value2)

        data.write_short(len(self.start_times))
        for key, value in self.start_times.items():
            data.write_short(key)

            # this is a bad conversion, since float is timestamp i assume and int as the date as YYYMMDD. FIXME
            if game_version < 90100:
                data.write_double(float(value))
            else:
                data.write_int(int(value))

    def serialize(self) -> dict[str, Any]:
        return {
            "completed": self.completed,
            "values": self.values,
            "start_times": self.start_times,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> GamblingEvent:
        return GamblingEvent(
            data.get("completed", {}),
            data.get("values", {}),
            data.get("start_times", {}),
        )

    def reset(self):
        self.completed = {}
        self.values = {}
        # TODO: check start times
        self.start_times = {}

    @staticmethod
    def reset_events(save_file: core.SaveFile):
        save_file.wildcat_slots.reset()
        color.ColoredText.localize("reset_wildcat_slots")
        save_file.cat_scratcher.reset()
        color.ColoredText.localize("reset_cat_scratcher")


# ============================================================
# FILE: gatya.py
# ============================================================
from __future__ import annotations
import enum
from typing import Any, Callable
from bcsfe import core
from bcsfe.cli import dialog_creator, color


class Gatya:
    def __init__(self, rare_seed: int, normal_seed: int):
        self.rare_seed = rare_seed
        self.normal_seed = normal_seed
        self.event_seed = 0
        self.stepup_stage_3_cooldown = 0
        self.previous_normal_roll = 0
        self.previous_normal_roll_type = 0
        self.previous_rare_roll = 0
        self.previous_rare_roll_type = 0
        self.unknown1 = False
        self.roll_single = False
        self.roll_multi = False
        self.trade_progress = 0
        self.step_up_stages: dict[int, int] = {}
        self.stepup_durations: dict[int, float] = {}

        self.gatya_data_set: GatyaDataSet | None = None

    @staticmethod
    def init() -> Gatya:
        return Gatya(0, 0)

    @staticmethod
    def read_rare_normal_seed(data: core.Data, gv: core.GameVersion) -> Gatya:
        if gv < 33:
            return Gatya(data.read_ulong(), data.read_ulong())
        return Gatya(data.read_uint(), data.read_uint())

    def read_event_seed(self, data: core.Data, gv: core.GameVersion):
        if gv < 33:
            self.event_seed = data.read_ulong()
        else:
            self.event_seed = data.read_uint()

    def write_rare_normal_seed(self, data: core.Data):
        data.write_uint(self.rare_seed)
        data.write_uint(self.normal_seed)

    def write_event_seed(self, data: core.Data):
        data.write_uint(self.event_seed)

    def read2(self, data: core.Data):
        self.stepup_stage_3_cooldown = data.read_int()
        self.previous_normal_roll = data.read_int()
        self.previous_normal_roll_type = data.read_int()
        self.previous_rare_roll = data.read_int()
        self.previous_rare_roll_type = data.read_int()
        self.unknown1 = data.read_bool()
        self.roll_single = data.read_bool()
        self.roll_multi = data.read_bool()

    def write2(self, data: core.Data):
        data.write_int(self.stepup_stage_3_cooldown)
        data.write_int(self.previous_normal_roll)
        data.write_int(self.previous_normal_roll_type)
        data.write_int(self.previous_rare_roll)
        data.write_int(self.previous_rare_roll_type)
        data.write_bool(self.unknown1)
        data.write_bool(self.roll_single)
        data.write_bool(self.roll_multi)

    def read_trade_progress(self, data: core.Data):
        self.trade_progress = data.read_int()

    def write_trade_progress(self, data: core.Data):
        data.write_int(self.trade_progress)

    def read_stepup(self, data: core.Data):
        self.step_up_stages: dict[int, int] = {}
        total = data.read_int()
        for _ in range(total):
            key = data.read_int()
            self.step_up_stages[key] = data.read_int()

        self.stepup_durations: dict[int, float] = {}
        total = data.read_int()
        for _ in range(total):
            key = data.read_int()
            self.stepup_durations[key] = data.read_double()

    def write_stepup(self, data: core.Data):
        data.write_int(len(self.step_up_stages))
        for id, stage in self.step_up_stages.items():
            data.write_int(id)
            data.write_int(stage)

        data.write_int(len(self.stepup_durations))
        for id, duration in self.stepup_durations.items():
            data.write_int(id)
            data.write_double(duration)

    def serialize(self) -> dict[str, Any]:
        return {
            "rare_seed": self.rare_seed,
            "normal_seed": self.normal_seed,
            "stepup_stage_3_cooldown": self.stepup_stage_3_cooldown,
            "previous_normal_roll": self.previous_normal_roll,
            "previous_normal_roll_type": self.previous_normal_roll_type,
            "previous_rare_roll": self.previous_rare_roll,
            "previous_rare_roll_type": self.previous_rare_roll_type,
            "unknown1": self.unknown1,
            "roll_single": self.roll_single,
            "roll_multi": self.roll_multi,
            "trade_progress": self.trade_progress,
            "event_seed": self.event_seed,
            "step_up_stages": self.step_up_stages,
            "stepup_durations": self.stepup_durations,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> Gatya:
        gatya = Gatya(data.get("rare_seed", 0), data.get("normal_seed", 0))
        gatya.stepup_stage_3_cooldown = data.get("stepup_stage_3_cooldown", 0)
        gatya.previous_normal_roll = data.get("previous_normal_roll", 0)
        gatya.previous_normal_roll_type = data.get("previous_normal_roll_type", 0)
        gatya.previous_rare_roll = data.get("previous_rare_roll", 0)
        gatya.previous_rare_roll_type = data.get("previous_rare_roll_type", 0)
        gatya.unknown1 = data.get("unknown1", False)
        gatya.roll_single = data.get("roll_single", False)
        gatya.roll_multi = data.get("roll_multi", False)
        gatya.trade_progress = data.get("trade_progress", 0)
        gatya.event_seed = data.get("event_seed", 0)
        gatya.step_up_stages = data.get("step_up_stages", {})
        gatya.stepup_durations = data.get("stepup_durations", {})
        return gatya

    def __repr__(self) -> str:
        return f"Gatya({self.serialize()})"

    def __str__(self) -> str:
        return f"Gatya({self.serialize()})"

    def edit_rare_gatya_seed(self):
        self.rare_seed = dialog_creator.SingleEditor(
            "rare_gatya_seed",
            self.rare_seed,
            None,
            localized_item=True,
            signed=False,
        ).edit()

    def edit_normal_gatya_seed(self):
        self.normal_seed = dialog_creator.SingleEditor(
            "normal_gatya_seed",
            self.normal_seed,
            None,
            localized_item=True,
            signed=False,
        ).edit()

    def edit_event_gatya_seed(self):
        self.event_seed = dialog_creator.SingleEditor(
            "event_gatya_seed",
            self.event_seed,
            None,
            localized_item=True,
            signed=False,
        ).edit()

    def read_gatya_data_set(self, save_file: core.SaveFile) -> GatyaDataSet:
        if self.gatya_data_set is not None:
            return self.gatya_data_set
        self.gatya_data_set = GatyaDataSet(save_file)
        return self.gatya_data_set


class GatyaDataSet:
    def __init__(self, save_file: core.SaveFile):
        self.save_file = save_file
        self.gatya_data_set = self.load_gatya_data_set("R", 1)

    def load_gatya_data_set(self, rarity: str, id: int) -> list[list[int]] | None:
        file_name = f"GatyaDataSet{rarity.upper()[0]}{id}.csv"
        gdg = core.core_data.get_game_data_getter(self.save_file)
        data = gdg.download("DataLocal", file_name)
        if data is None:
            return None
        csv = core.CSV(data)
        dt: list[list[int]] = []
        for line in csv:
            cat_ids: list[int] = []
            for cat_id in line:
                cat_id = cat_id.to_int()
                if cat_id != -1:
                    cat_ids.append(cat_id)
            dt.append(cat_ids)
        return dt

    def get_cat_ids(self, gatya_id: int) -> list[int] | None:
        if self.gatya_data_set is None:
            return None
        try:
            return self.gatya_data_set[gatya_id]
        except IndexError:
            return None


class GatyaInfo:
    def __init__(self, gatya_id: int, cc: core.CountryCode, type_str: str = "R"):
        self.gatya_id = gatya_id
        self.cc = cc
        self.gatya_data_set: GatyaDataSet | None = None
        self.type = type_str
        self.data: core.Data | None = None

    def get_id_str(self) -> str:
        return f"{self.gatya_id:03}"

    def get_cc_str(self) -> str:
        if self.cc == core.CountryCode("jp"):
            return ""
        return self.cc.get_patching_code() + "/"

    def get_url(self) -> str:
        return f"https://ponosgames.com/information/appli/battlecats/gacha/rare/{self.get_cc_str()}{self.type}{self.get_id_str()}.html"

    def download_data(self) -> core.Data | None:
        url = self.get_url()

        response = core.RequestHandler(url).get()
        if response is None:
            return
        data = core.Data(response.content)

        self.save_data(data)
        return data

    def get_file_path(self) -> core.Path:
        return (
            core.Path.get_documents_folder()
            .add("other_game_data")
            .add(self.cc.get_code())
            .add("gatya_info")
            .generate_dirs()
            .add(f"{self.type}{self.get_id_str()}.html")
        )

    def save_data(self, data: core.Data):
        try:
            data.to_file(self.get_file_path())
        except Exception as e:
            color.ColoredText.localize("save_gatya_error", error=e)
        self.data = data

    def load_data_from_file(self) -> core.Data | None:
        if not self.get_file_path().exists():
            return None
        return core.Data.from_file(self.get_file_path())

    def get_data(self) -> core.Data | None:
        if self.data is not None:
            return self.data
        data = self.load_data_from_file()
        if data is None:
            data = self.download_data()
        return data

    def get_name(self) -> str | None:
        data = self.get_data()
        if data is None:
            return None
        # find <h2>...</h2>
        data = data.get_bytes()
        h2 = data.find(b"<h2>")
        if h2 == -1:
            return None
        h2_end = data.find(b"</h2>", h2)
        if h2_end == -1:
            return None
        text = data[h2 + 4 : h2_end].decode("utf-8")
        # remove <span...</span>
        span = text.find("<span")
        if span == -1:
            return text
        span_end = text.find("</span>", span)
        if span_end == -1:
            return text
        return text[:span] + text[span_end + 7 :]


class GatyaInfos:
    def __init__(self, save_file: core.SaveFile, type_str: str = "R", set_id: int = 1):
        self.save_file = save_file
        self.type = type_str
        self.set_id = set_id
        self.gatya_data_set = GatyaDataSet(save_file).load_gatya_data_set(
            type_str, set_id
        )
        self.infos: list[GatyaInfo] = []
        self.got_all = False

    def get_all(
        self,
        threaded: bool = True,
        print_progress: bool = True,
        max_threads: int = 16,
    ):
        if self.gatya_data_set is None:
            return
        all_ids = len(self.gatya_data_set)
        if threaded:
            funcs: list[Callable[..., Any]] = []
            args: list[list[Any]] = []
            for id in range(all_ids):
                funcs.append(self.get)
                args.append([id, print_progress])
            core.thread_run_many(funcs, args, max_threads=max_threads)

        else:
            for id in range(all_ids):
                self.infos.append(self.get(id, print_progress=print_progress))

        self.got_all = True

    def get(self, gatya_id: int, print_progress: bool):
        if print_progress:
            color.ColoredText.localize(
                "gatya_info_progress",
                current=len(self.infos or []) + 1,
                total=len(self.gatya_data_set or []),
            )
        info = GatyaInfo(gatya_id, self.save_file.cc, self.type)
        info.get_data()
        self.infos.append(info)
        return info

    def get_info(self, gatya_id: int) -> GatyaInfo | None:
        if self.infos:
            return self.infos[gatya_id]
        return None

    def get_all_names(self) -> dict[int, str]:
        if not self.got_all:
            self.get_all(True, max_threads=64)
        names: dict[int, str] = {}
        for info in self.infos:
            names[
                info.gatya_id
            ] = info.get_name() or core.core_data.local_manager.get_key(
                "unknown_banner"
            )

        return names


class GatyaDataOptionSet:
    def __init__(
        self,
        id: int,
        banner_on: bool,
        ticket_item_id: int,
        anim_id: int,
        button_cut_id: int,
        series_id: int,
        menu_cut_id: int,
        char_id: int | None,
        wait_maanim: bool | None,
    ):
        self.id = id
        self.banner_on = banner_on
        self.ticket_item_id = ticket_item_id
        self.anim_id = anim_id
        self.button_cut_id = button_cut_id
        self.series_id = series_id
        self.menu_cut_id = menu_cut_id
        self.char_id = char_id
        self.wait_maanim = wait_maanim

    @staticmethod
    def from_csv_row(row: core.Row) -> GatyaDataOptionSet:
        return GatyaDataOptionSet(
            row.next_int(),
            row.next_bool(),
            row.next_int(),
            row.next_int(),
            row.next_int(),
            row.next_int(),
            row.next_int(),
            row.next_int_opt(),
            row.next_bool_opt(),
        )


class GatyaEventType(enum.Enum):
    NORMAL = "N"
    RARE = "R"
    EVENT = "E"


class GatyaDataOption:
    def __init__(self, sets: list[GatyaDataOptionSet]):
        self.sets = sets

    def get(self, set_id: int) -> GatyaDataOptionSet | None:
        for gset in self.sets:
            if gset.id == set_id:
                return gset

        return None

    @staticmethod
    def from_csv(csv: core.CSV) -> GatyaDataOption:
        sets: list[GatyaDataOptionSet] = []
        csv.read_line()  # skip headers
        for row in csv:
            sets.append(GatyaDataOptionSet.from_csv_row(row))

        return GatyaDataOption(sets)

    @staticmethod
    def from_data(data: core.Data) -> GatyaDataOption:
        return GatyaDataOption.from_csv(core.CSV(data, "\t"))

    @staticmethod
    def get_filename(event_type: GatyaEventType) -> str:
        return f"GatyaData_Option_Set{event_type.value}.tsv"

    @staticmethod
    def read(
        save_file: core.SaveFile, e_type: GatyaEventType
    ) -> GatyaDataOption | None:
        gdg = core.core_data.get_game_data_getter(save_file)

        data = gdg.download("DataLocal", GatyaDataOption.get_filename(e_type))
        if data is None:
            return None

        return GatyaDataOption.from_data(data)


# ============================================================
# FILE: gatya_item.py
# ============================================================
from __future__ import annotations
import enum
from bcsfe import core


class GatyaItemNames:
    def __init__(self, save_file: core.SaveFile):
        self.save_file = save_file
        self.names = self.__get_names()

    def __get_names(self) -> list[str] | None:
        gdg = core.core_data.get_game_data_getter(self.save_file)
        data = gdg.download("resLocal", "GatyaitemName.csv")
        if data is None:
            return None
        csv = core.CSV(
            data, core.Delimeter.from_country_code_res(self.save_file.cc)
        )
        names: list[str] = []
        for line in csv:
            names.append(line[0].to_str())

        return names

    def get_name(self, index: int) -> str | None:
        if self.names is None:
            return None
        try:
            return self.names[index]
        except IndexError:
            return core.core_data.local_manager.get_key(
                "gatya_item_unknown_name", index=index
            )


class GatyaItemBuyItem:
    def __init__(
        self,
        id: int,
        rarity: int,
        reflect_or_storage: bool,
        price: int,
        stage_drop_id: int,
        quantity: int,
        server_id: int,
        category: int,
        index: int,
        src_item_id: int,
        main_menu_type: int,
        gatya_ticket_id: int,
        comment: str,
    ):
        self.id = id
        self.rarity = rarity
        self.reflect_or_storage = reflect_or_storage
        self.price = price
        self.stage_drop_id = stage_drop_id
        self.quantity = quantity
        self.server_id = server_id
        self.category = category
        self.index = index
        self.src_item_id = src_item_id
        self.main_menu_type = main_menu_type
        self.gatya_ticket_id = gatya_ticket_id
        self.comment = comment

class GatyaItemCategory(enum.Enum):
    MISC = 0
    EVENT_TICKETS = 1
    SPECIAL_SKILLS = 2
    BATTLE_ITEMS = 3
    EVOLVE_ITEMS = 4
    CATSEYES = 5
    CATAMINS = 6
    BASE_MATERIALS = 7
    LUCKY_TICKETS_1 = 8
    ENDLESS_ITEMS = 9
    LUCKY_TICKETS_2 = 10
    LABYRINTH_MEDALS = 11
    TREASURE_CHESTS = 12

class GatyaItemBuy:
    def __init__(self, save_file: core.SaveFile):
        self.save_file = save_file
        self.buy = self.get_buy()

    def get_buy(self) -> list[GatyaItemBuyItem] | None:
        gdg = core.core_data.get_game_data_getter(self.save_file)
        data = gdg.download("DataLocal", "Gatyaitembuy.csv")
        if data is None:
            return None
        csv = core.CSV(data)
        buy: list[GatyaItemBuyItem] = []
        for i, line in enumerate(csv.lines[1:]):
            try:
                buy.append(
                    GatyaItemBuyItem(
                        i,
                        line[0].to_int(),
                        line[1].to_bool(),
                        line[2].to_int(),
                        line[3].to_int(),
                        line[4].to_int(),
                        line[5].to_int(),
                        line[6].to_int(),
                        line[7].to_int(),
                        line[8].to_int(),
                        line[9].to_int(),
                        line[10].to_int(),
                        line[11].to_str(),
                    )
                )
            except IndexError:
                pass

        return buy

    def sort_by_index(self, items: list[GatyaItemBuyItem]):
        items.sort(key=lambda x: x.index)
        return items

    def get_by_category(self, category: int | GatyaItemCategory) -> list[GatyaItemBuyItem] | None:
        if self.buy is None:
            return None
        if isinstance(category, GatyaItemCategory):
            category = category.value
        return self.sort_by_index(
            [item for item in self.buy if item.category == category]
        )

    def get_names_by_category(self, category: int | GatyaItemCategory) -> list[tuple[GatyaItemBuyItem, str | None]] | None:
        items = self.get_by_category(category)
        if items is None:
            return None

        names = GatyaItemNames(self.save_file)

        return [(item, names.get_name(item.id)) for item in items]

    def get(self, item_id: int) -> GatyaItemBuyItem | None:
        if self.buy is None:
            return None
        if item_id < 0 or item_id >= len(self.buy):
            return None

        return self.buy[item_id]

    def get_by_server_id(self, server_id: int) -> GatyaItemBuyItem | None:
        if self.buy is None:
            return None
        for item in self.buy:
            if item.server_id == server_id:
                return item

        return None


# ============================================================
# FILE: item_pack.py
# ============================================================
from __future__ import annotations
from typing import Any
from bcsfe import core


class PurchasedPack:
    def __init__(self, purchased: bool):
        self.purchased = purchased

    @staticmethod
    def init() -> PurchasedPack:
        return PurchasedPack(False)

    @staticmethod
    def read(stream: core.Data) -> PurchasedPack:
        purchased = stream.read_bool()
        return PurchasedPack(purchased)

    def write(self, stream: core.Data):
        stream.write_bool(self.purchased)

    def serialize(self) -> bool:
        return self.purchased

    @staticmethod
    def deserialize(data: bool) -> PurchasedPack:
        return PurchasedPack(data)

    def __repr__(self) -> str:
        return f"PurchasedPack(purchased={self.purchased!r})"

    def __str__(self) -> str:
        return self.__repr__()


class PurchaseSet:
    def __init__(self, purchases: dict[str, PurchasedPack]):
        self.purchases = purchases

    @staticmethod
    def init() -> PurchaseSet:
        return PurchaseSet({})

    @staticmethod
    def read(stream: core.Data) -> PurchaseSet:
        total = stream.read_int()
        purchases: dict[str, PurchasedPack] = {}
        for _ in range(total):
            key = stream.read_string()
            purchases[key] = PurchasedPack.read(stream)
        return PurchaseSet(purchases)

    def write(self, stream: core.Data):
        stream.write_int(len(self.purchases))
        for key, purchase in self.purchases.items():
            stream.write_string(key)
            purchase.write(stream)

    def serialize(self) -> dict[str, Any]:
        return {
            key: purchase.serialize()
            for key, purchase in self.purchases.items()
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> PurchaseSet:
        return PurchaseSet(
            {
                key: PurchasedPack.deserialize(purchase)
                for key, purchase in data.items()
            },
        )

    def __repr__(self) -> str:
        return f"PurchaseSet(purchases={self.purchases!r})"

    def __str__(self) -> str:
        return self.__repr__()


class Purchases:
    def __init__(self, purchases: dict[int, PurchaseSet]):
        self.purchases = purchases

    @staticmethod
    def init() -> Purchases:
        return Purchases({})

    @staticmethod
    def read(stream: core.Data) -> Purchases:
        total = stream.read_int()
        purchases: dict[int, PurchaseSet] = {}
        for _ in range(total):
            key = stream.read_int()
            purchases[key] = PurchaseSet.read(stream)

        return Purchases(purchases)

    def write(self, stream: core.Data):
        stream.write_int(len(self.purchases))
        for key, purchase in self.purchases.items():
            stream.write_int(key)
            purchase.write(stream)

    def serialize(self) -> dict[int, Any]:
        return {
            key: purchase.serialize()
            for key, purchase in self.purchases.items()
        }

    @staticmethod
    def deserialize(data: dict[int, Any]) -> Purchases:
        return Purchases(
            {
                key: PurchaseSet.deserialize(purchase)
                for key, purchase in data.items()
            },
        )

    def __repr__(self) -> str:
        return f"Purchases(purchases={self.purchases!r})"

    def __str__(self) -> str:
        return self.__repr__()


class ItemPack:
    def __init__(self, purchases: Purchases):
        self.purchases = purchases
        self.displayed_packs: dict[int, bool] = {}
        self.three_days_started: bool = False
        self.three_days_end_timestamp: float = 0.0

    @staticmethod
    def init() -> ItemPack:
        return ItemPack(Purchases.init())

    @staticmethod
    def read(stream: core.Data) -> ItemPack:
        return ItemPack(Purchases.read(stream))

    def write(self, stream: core.Data):
        self.purchases.write(stream)

    def read_displayed_packs(self, stream: core.Data) -> None:
        total = stream.read_int()
        displayed_packs: dict[int, bool] = {}
        for _ in range(total):
            key = stream.read_int()
            displayed_packs[key] = stream.read_bool()

        self.displayed_packs = displayed_packs

    def write_displayed_packs(self, stream: core.Data) -> None:
        stream.write_int(len(self.displayed_packs))
        for key, displayed in self.displayed_packs.items():
            stream.write_int(key)
            stream.write_bool(displayed)

    def read_three_days(self, stream: core.Data) -> None:
        self.three_days_started = stream.read_bool()
        self.three_days_end_timestamp = stream.read_double()

    def write_three_days(self, stream: core.Data) -> None:
        stream.write_bool(self.three_days_started)
        stream.write_double(self.three_days_end_timestamp)

    def serialize(self) -> dict[str, Any]:
        return {
            "purchases": self.purchases.serialize(),
            "displayed_packs": self.displayed_packs,
            "three_days_started": self.three_days_started,
            "three_days_end_timestamp": self.three_days_end_timestamp,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> ItemPack:
        item_pack = ItemPack(Purchases.deserialize(data.get("purchases", {})))
        item_pack.displayed_packs = data.get("displayed_packs", {})
        item_pack.three_days_started = data.get("three_days_started", False)
        item_pack.three_days_end_timestamp = data.get(
            "three_days_end_timestamp", 0.0
        )
        return item_pack

    def __repr__(self) -> str:
        return f"ItemPack(purchases={self.purchases!r}, displayed_packs={self.displayed_packs!r}, three_days_started={self.three_days_started!r}, three_days_end_timestamp={self.three_days_end_timestamp!r})"

    def __str__(self) -> str:
        return self.__repr__()


# ============================================================
# FILE: login_bonuses.py
# ============================================================
from __future__ import annotations
from typing import Any
from bcsfe import core


class Login:
    def __init__(self, count: int):
        self.count = count

    @staticmethod
    def init() -> Login:
        return Login(0)

    @staticmethod
    def read(stream: core.Data) -> Login:
        count = stream.read_int()
        return Login(count)

    def write(self, stream: core.Data):
        stream.write_int(self.count)

    def serialize(self) -> int:
        return self.count

    @staticmethod
    def deserialize(data: int) -> Login:
        return Login(data)

    def __repr__(self):
        return f"Login({self.count})"

    def __str__(self):
        return f"Login({self.count})"


class Logins:
    def __init__(self, logins: list[Login]):
        self.logins = logins

    @staticmethod
    def init() -> Logins:
        return Logins([])

    @staticmethod
    def read(stream: core.Data) -> Logins:
        total = stream.read_int()
        logins: list[Login] = []
        for _ in range(total):
            logins.append(Login.read(stream))
        return Logins(logins)

    def write(self, stream: core.Data):
        stream.write_int(len(self.logins))
        for login in self.logins:
            login.write(stream)

    def serialize(self) -> list[int]:
        return [login.serialize() for login in self.logins]

    @staticmethod
    def deserialize(data: list[int]) -> Logins:
        return Logins([Login.deserialize(login) for login in data])

    def __repr__(self):
        return f"Logins({self.logins})"

    def __str__(self):
        return f"Logins({self.logins})"


class LoginSets:
    def __init__(self, logins: list[Logins]):
        self.logins = logins

    @staticmethod
    def init() -> LoginSets:
        return LoginSets([])

    @staticmethod
    def read(stream: core.Data) -> LoginSets:
        total = stream.read_int()
        logins: list[Logins] = []
        for _ in range(total):
            logins.append(Logins.read(stream))
        return LoginSets(logins)

    def write(self, stream: core.Data):
        stream.write_int(len(self.logins))
        for login in self.logins:
            login.write(stream)

    def serialize(self) -> list[list[int]]:
        return [login.serialize() for login in self.logins]

    @staticmethod
    def deserialize(data: list[list[int]]) -> LoginSets:
        return LoginSets([Logins.deserialize(login) for login in data])

    def __repr__(self):
        return f"LoginSets({self.logins})"

    def __str__(self):
        return f"LoginSets({self.logins})"


class LoginBonus:
    def __init__(
        self,
        old_logins: LoginSets | None = None,
        logins: dict[int, Login] | None = None,
    ):
        self.old_logins = old_logins
        self.logins = logins

    @staticmethod
    def init(gv: core.GameVersion) -> LoginBonus:
        if gv < 80000:
            return LoginBonus(old_logins=LoginSets.init())
        else:
            return LoginBonus(logins={})

    @staticmethod
    def read(stream: core.Data, gv: core.GameVersion) -> LoginBonus:
        if gv < 80000:
            logins_old = LoginSets.read(stream)
            return LoginBonus(logins_old)
        else:
            total = stream.read_int()
            logins: dict[int, Login] = {}
            for _ in range(total):
                id = stream.read_int()
                logins[id] = Login.read(stream)
            return LoginBonus(logins=logins)

    def write(self, stream: core.Data, gv: core.GameVersion):
        if gv < 80000:
            (self.old_logins or LoginSets([])).write(stream)
        elif gv >= 80000:
            logins = self.logins or {}
            stream.write_int(len(logins))
            for id, login in logins.items():
                stream.write_int(id)
                login.write(stream)

    def serialize(
        self,
    ) -> dict[str, Any]:
        if self.old_logins is not None:
            return {"old_logins": self.old_logins.serialize()}
        elif self.logins is not None:
            return {
                "logins": {
                    id: login.serialize() for id, login in self.logins.items()
                }
            }
        else:
            return {}

    @staticmethod
    def deserialize(data: dict[str, Any]) -> LoginBonus:
        if "old_logins" in data:
            return LoginBonus(
                old_logins=LoginSets.deserialize(data["old_logins"])
            )
        elif "logins" in data:
            return LoginBonus(
                logins={
                    int(id): Login.deserialize(login)
                    for id, login in data["logins"].items()
                }
            )
        else:
            return LoginBonus()

    def __repr__(self):
        return f"LoginBonus({self.old_logins}, {self.logins})"

    def __str__(self):
        return f"LoginBonus({self.old_logins}, {self.logins})"

    def get_login(self, id: int) -> Login | None:
        if self.logins is not None:
            return self.logins.get(id)
        else:
            return None


# ============================================================
# FILE: matatabi.py
# ============================================================
from __future__ import annotations
from bcsfe import core


class Fruit:
    def __init__(
        self,
        id: int,
        seed: bool,
        group: int,
        sort: int,
        require: int | None = None,
        text: str | None = None,
        grow_up: list[int] | None = None,
    ):
        self.id = id
        self.seed = seed
        self.group = group
        self.sort = sort
        self.require = require
        self.text = text
        self.grow_up = grow_up


class Matatabi:
    def __init__(self, save_file: core.SaveFile):
        self.save_file = save_file
        self.matatabi = self.__get_matatabi()
        self.gatya_item_names = core.core_data.get_gatya_item_names(
            self.save_file
        )

    def __get_matatabi(self) -> list[Fruit] | None:
        gdg = core.core_data.get_game_data_getter(self.save_file)
        data = gdg.download("DataLocal", "Matatabi.tsv")
        if data is None:
            return None
        csv = core.CSV(data, "\t")
        matatabi: list[Fruit] = []
        for line in csv.lines[1:]:
            id = line[0].to_int()
            seed = line[1].to_bool()
            group = line[2].to_int()
            sort = line[3].to_int()
            if len(line) > 4:
                require = line[4].to_int()
            else:
                require = None
            if len(line) > 5:
                text = line[5].to_str()
            else:
                text = None
            if len(line) > 6:
                grow_up = [item.to_int() for item in line[6:]]
            else:
                grow_up = None
            matatabi.append(
                Fruit(id, seed, group, sort, require, text, grow_up)
            )

        return matatabi

    def get_names(self) -> list[str | None] | None:
        if self.matatabi is None:
            return None

        ids = [fruit.id for fruit in self.matatabi]
        names = [self.gatya_item_names.get_name(id) for id in ids]
        return names


# ============================================================
# FILE: medals.py
# ============================================================
from __future__ import annotations
from typing import Any
from bcsfe import core
from bcsfe.cli import color, dialog_creator


class Medals:
    def __init__(
        self,
        u1: int,
        u2: int,
        u3: int,
        medal_data_1: list[int],
        medal_data_2: dict[int, int],
        ub: bool,
    ):
        self.u1 = u1
        self.u2 = u2
        self.u3 = u3
        self.medal_data_1 = medal_data_1
        self.medal_data_2 = medal_data_2
        self.ub = ub

    @staticmethod
    def init() -> Medals:
        return Medals(0, 0, 0, [], {}, False)

    @staticmethod
    def read(data: core.Data) -> Medals:
        u1 = data.read_int()
        u2 = data.read_int()
        u3 = data.read_int()
        total_medals = data.read_short()
        medal_data_1 = data.read_short_list(total_medals)
        total_medals = data.read_short()
        medal_data_2: dict[int, int] = {}
        for _ in range(total_medals):
            key = data.read_short()
            value = data.read_byte()
            medal_data_2[key] = value
        ub = data.read_bool()
        return Medals(u1, u2, u3, medal_data_1, medal_data_2, ub)

    def write(self, data: core.Data) -> None:
        data.write_int(self.u1)
        data.write_int(self.u2)
        data.write_int(self.u3)
        data.write_short(len(self.medal_data_1))
        data.write_short_list(self.medal_data_1, write_length=False)
        data.write_short(len(self.medal_data_2))
        for key, value in self.medal_data_2.items():
            data.write_short(key)
            data.write_byte(value)
        data.write_bool(self.ub)

    def serialize(self) -> dict[str, Any]:
        return {
            "u1": self.u1,
            "u2": self.u2,
            "u3": self.u3,
            "medal_data_1": self.medal_data_1,
            "medal_data_2": self.medal_data_2,
            "ub": self.ub,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> Medals:
        return Medals(
            data.get("u1", 0),
            data.get("u2", 0),
            data.get("u3", 0),
            data.get("medal_data_1", []),
            data.get("medal_data_2", {}),
            data.get("ub", False),
        )

    def __repr__(self) -> str:
        return (
            f"Medals(u1={self.u1}, u2={self.u2}, u3={self.u3}, "
            f"medal_data_1={self.medal_data_1}, medal_data_2={self.medal_data_2}, "
            f"ub={self.ub})"
        )

    def __str__(self) -> str:
        return self.__repr__()

    def has_medal(self, medal_id: int) -> bool:
        return medal_id in self.medal_data_1

    @staticmethod
    def edit_medals(save_file: core.SaveFile):
        medals = save_file.medals
        medal_names = core.core_data.get_medal_names(save_file)
        if medal_names.medal_names is None:
            return
        options = ["add_medals", "remove_medals"]
        choice = dialog_creator.ChoiceInput.from_reduced(
            options, dialog="medal_add_remove_dialog", single_choice=True
        ).single_choice()
        if choice is None:
            return
        choice -= 1
        add_medals = choice == 0

        medals_to_choose_from: list[tuple[int, str]] = []
        for i, medal in enumerate(medal_names.medal_names):
            if len(medal) == 0:
                continue
            if medals.has_medal(i) == add_medals:
                continue
            key = "medal_string"
            string = core.core_data.local_manager.get_key(
                key, medal_name=medal[0], medal_req=medal[1]
            )
            medals_to_choose_from.append((i, string))
        if len(medals_to_choose_from) == 0:
            return
        options = [medal[1] for medal in medals_to_choose_from]
        choices, _ = dialog_creator.ChoiceInput.from_reduced(
            options, dialog="select_medals"
        ).multiple_choice()
        if choices is None:
            return
        for choice in choices:
            medal_id = medals_to_choose_from[choice][0]
            if add_medals:
                medals.add_medal(medal_id)
            else:
                medals.remove_medal(medal_id)

        if add_medals:
            color.ColoredText.localize("medals_added")
        else:
            color.ColoredText.localize("medals_removed")

    def add_medal(self, medal_id: int) -> None:
        if self.has_medal(medal_id):
            return
        self.medal_data_1.append(medal_id)
        self.medal_data_2[medal_id] = 0

    def remove_medal(self, medal_id: int) -> None:
        if medal_id in self.medal_data_2:
            del self.medal_data_2[medal_id]
        if medal_id in self.medal_data_1:
            self.medal_data_1.remove(medal_id)


class MedalNames:
    def __init__(self, save_file: core.SaveFile):
        self.save_file = save_file
        self.medal_names = self.get_medal_names()

    def get_medal_names(self) -> list[list[str]] | None:
        file_name = "medalname.tsv"
        gdg = core.core_data.get_game_data_getter(self.save_file)
        data = gdg.download("resLocal", file_name)
        if data is None:
            return None
        csv = core.CSV(data, delimiter="\t")
        names: list[list[str]] = []
        for row in csv:
            names.append(row.to_str_list())
        return names

    def get_medal_name(self, medal_id: int) -> list[str] | None:
        if self.medal_names is None:
            return None
        if medal_id < 0 or medal_id >= len(self.medal_names):
            return []
        return self.medal_names[medal_id]


# ============================================================
# FILE: mission.py
# ============================================================
from __future__ import annotations
from typing import Any

from bcsfe import core
from bcsfe.cli import color, dialog_creator


class Mission:
    def __init__(
        self,
        clear_state: int | None = None,
        requirement: int | None = None,
        progress_type: int | None = None,
        gamatoto_value: int | None = None,
        nyancombo_value: int | None = None,
        user_rank_value: int | None = None,
        expiry_value: int | None = None,
        preparing_value: int | bool | None = None,
    ):
        self.clear_state = clear_state
        self.requirement = requirement
        self.progress_type = progress_type
        self.gamatoto_value = gamatoto_value
        self.nyancombo_value = nyancombo_value
        self.user_rank_value = user_rank_value
        self.expiry_value = expiry_value
        self.preparing_value = preparing_value

    @staticmethod
    def init() -> Mission:
        return Mission(
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        )

    def serialize(self) -> dict[str, Any]:
        return {
            "clear_state": self.clear_state,
            "requirement": self.requirement,
            "progress_type": self.progress_type,
            "gamatoto_value": self.gamatoto_value,
            "nyancombo_value": self.nyancombo_value,
            "user_rank_value": self.user_rank_value,
            "expiry_value": self.expiry_value,
            "preparing_value": self.preparing_value,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> Mission:
        return Mission(
            data["clear_state"],
            data["requirement"],
            data["progress_type"],
            data["gamatoto_value"],
            data["nyancombo_value"],
            data["user_rank_value"],
            data["expiry_value"],
            data["preparing_value"],
        )

    def __repr__(self):
        return f"Mission({self.clear_state}, {self.requirement}, {self.progress_type}, {self.gamatoto_value}, {self.nyancombo_value}, {self.user_rank_value}, {self.expiry_value}, {self.preparing_value})"

    def __str__(self):
        return self.__repr__()


class Missions:
    def __init__(
        self,
        clear_states: dict[int, int],
        requirements: dict[int, int],
        progress_types: dict[int, int],
        gamatoto_values: dict[int, int],
        nyancombo_values: dict[int, int],
        user_rank_values: dict[int, int],
        expiry_values: dict[int, int],
        preparing_values: dict[int, int | bool],
    ):
        self.clear_states = clear_states
        self.requirements = requirements
        self.progress_types = progress_types
        self.gamatoto_values = gamatoto_values
        self.nyancombo_values = nyancombo_values
        self.user_rank_values = user_rank_values
        self.expiry_values = expiry_values
        self.preparing_values = preparing_values
        self.weekly_missions: dict[int, bool] = {}

    @staticmethod
    def init() -> Missions:
        return Missions(
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
        )

    @staticmethod
    def read(stream: core.Data, gv: core.GameVersion) -> Missions:
        clear_states: dict[int, int] = stream.read_int_int_dict()
        requirements: dict[int, int] = stream.read_int_int_dict()
        progress_types: dict[int, int] = stream.read_int_int_dict()
        gamatoto_values: dict[int, int] = stream.read_int_int_dict()
        nyancombo_values: dict[int, int] = stream.read_int_int_dict()
        user_rank_values: dict[int, int] = stream.read_int_int_dict()
        expiry_values: dict[int, int] = stream.read_int_int_dict()
        preparing_values: dict[int, int | bool] = {}

        for _ in range(stream.read_int()):
            key = stream.read_int()
            if gv < 90300:
                preparing_values[key] = stream.read_bool()
            else:
                preparing_values[key] = stream.read_int()

        return Missions(
            clear_states,
            requirements,
            progress_types,
            gamatoto_values,
            nyancombo_values,
            user_rank_values,
            expiry_values,
            preparing_values,
        )

    def write(self, stream: core.Data, gv: core.GameVersion):
        stream.write_int_int_dict(self.clear_states)
        stream.write_int_int_dict(self.requirements)
        stream.write_int_int_dict(self.progress_types)
        stream.write_int_int_dict(self.gamatoto_values)
        stream.write_int_int_dict(self.nyancombo_values)
        stream.write_int_int_dict(self.user_rank_values)
        stream.write_int_int_dict(self.expiry_values)

        stream.write_int(len(self.preparing_values))
        for key, value in self.preparing_values.items():
            stream.write_int(key)
            if gv < 90300:
                stream.write_bool(bool(value))
            else:
                stream.write_int(int(value))

    def read_weekly_missions(self, stream: core.Data):
        self.weekly_missions: dict[int, bool] = {}
        for _ in range(stream.read_int()):
            key = stream.read_int()
            self.weekly_missions[key] = stream.read_bool()

    def write_weekly_missions(self, stream: core.Data):
        stream.write_int(len(self.weekly_missions))
        for key, value in self.weekly_missions.items():
            stream.write_int(key)
            stream.write_bool(value)

    def serialize(self) -> dict[str, Any]:
        return {
            "clear_states": self.clear_states,
            "requirements": self.requirements,
            "progress_types": self.progress_types,
            "gamatoto_values": self.gamatoto_values,
            "nyancombo_values": self.nyancombo_values,
            "user_rank_values": self.user_rank_values,
            "expiry_values": self.expiry_values,
            "preparing_values": self.preparing_values,
            "weekly_missions": self.weekly_missions,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]):
        missions = Missions(
            data.get("clear_states", {}),
            data.get("requirements", {}),
            data.get("progress_types", {}),
            data.get("gamatoto_values", {}),
            data.get("nyancombo_values", {}),
            data.get("user_rank_values", {}),
            data.get("expiry_values", {}),
            data.get("preparing_values", {}),
        )
        missions.weekly_missions = data.get("weekly_missions", {})
        return missions

    def __repr__(self):
        return f"<Missions {self.serialize()}>"

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def edit_missions(save_file: core.SaveFile):
        missions = save_file.missions

        names = core.core_data.get_mission_names(save_file)
        conditions = core.core_data.get_mission_conditions(save_file)
        if names.names is None or conditions.conditions is None:
            return
        options: list[str] = []
        mssion_ids: list[int] = []
        for mission_id, name in names.names.items():
            if mission_id in missions.clear_states:
                name = name.split("<br>")[0]
                condition = conditions.conditions.get(mission_id)
                if not condition:
                    continue
                name = name.replace("%d", str(condition.progress_count))
                if "%@" in name and len(condition.conditions_value) > 2:
                    name = name.replace(
                        "%@", str(condition.conditions_value[2])
                    )
                options.append(name)
                mssion_ids.append(mission_id)

        re_claim = dialog_creator.ChoiceInput.from_reduced(
            ["complete_reward", "complete_claim", "uncomplete"],
            dialog="select_mission_claim",
            single_choice=True,
        ).single_choice()
        if re_claim is None:
            return
        re_claim -= 1

        choices, _ = dialog_creator.ChoiceInput.from_reduced(
            options, dialog="select_missions"
        ).multiple_choice(localized_options=False)
        if choices is None:
            return
        for choice in choices:
            mission_id = mssion_ids[choice]
            if re_claim == 0:
                missions.clear_states[mission_id] = 2
                condition = conditions.get_condition(mission_id)
                if condition is not None:
                    missions.requirements[mission_id] = condition.progress_count
            elif re_claim == 1:
                missions.clear_states[mission_id] = 4
                condition = conditions.get_condition(mission_id)
                if condition is not None:
                    missions.requirements[mission_id] = condition.progress_count
            elif re_claim == 2:
                missions.clear_states[mission_id] = 0
                if mission_id in missions.requirements:
                    missions.requirements[mission_id] = 0

        color.ColoredText.localize("missions_edited")


class MissionCondition:
    def __init__(
        self,
        mission_id: int,
        mission_type: int,
        conditions_type: int,
        progress_count: int,
        conditions_value: list[int],
    ):
        self.mission_id = mission_id
        self.mission_type = mission_type
        self.conditions_type = conditions_type
        self.progress_count = progress_count
        self.conditions_value = conditions_value


class MissionConditions:
    def __init__(self, save: core.SaveFile):
        self.save = save
        self.conditions = self.get_conditions()

    def get_conditions(self) -> dict[int, MissionCondition] | None:
        file_name = "Mission_Condition.csv"
        gdg = core.core_data.get_game_data_getter(self.save)
        file = gdg.download("DataLocal", file_name)
        if file is None:
            return None
        csv = core.CSV(file)
        conditions: dict[int, MissionCondition] = {}
        for row in csv:
            conditions[row[0].to_int()] = MissionCondition(
                row[0].to_int(),
                row[1].to_int(),
                row[2].to_int(),
                row[3].to_int(),
                row[4:].to_int_list(),
            )
        return conditions

    def get_condition(self, mission_id: int) -> MissionCondition | None:
        if self.conditions is None:
            return None
        return self.conditions.get(mission_id)


class MissionNames:
    def __init__(self, save: core.SaveFile):
        self.save = save
        self.names = self.get_names()

    def get_names(self) -> dict[int, str] | None:
        file_name = "Mission_Name.csv"
        gdg = core.core_data.get_game_data_getter(self.save)
        file = gdg.download("resLocal", file_name)
        if file is None:
            return None
        csv = core.CSV(
            file, delimiter=core.Delimeter.from_country_code_res(self.save.cc)
        )
        names: dict[int, str] = {}
        for row in csv:
            names[row[0].to_int()] = row[1].to_str()
        return names


# ============================================================
# FILE: my_sale.py
# ============================================================
from __future__ import annotations
from typing import Any
from bcsfe import core


class MySale:
    def __init__(self, dict_1: dict[int, int], dict_2: dict[int, bool]):
        self.dict_1 = dict_1
        self.dict_2 = dict_2

    @staticmethod
    def init() -> MySale:
        return MySale({}, {})

    @staticmethod
    def read_bonus_hash(stream: core.Data):
        variable_length = stream.read_variable_length_int()
        dict_1 = {}
        for _ in range(variable_length):
            key = stream.read_variable_length_int()
            value = stream.read_variable_length_int()
            dict_1[key] = value

        variable_length = stream.read_variable_length_int()
        dict_2 = {}
        for _ in range(variable_length):
            key = stream.read_variable_length_int()
            value = stream.read_byte()
            dict_2[key] = value

        return MySale(dict_1, dict_2)

    def write_bonus_hash(self, stream: core.Data):
        stream.write_variable_length_int(len(self.dict_1))
        for key, value in self.dict_1.items():
            stream.write_variable_length_int(key)
            stream.write_variable_length_int(value)

        stream.write_variable_length_int(len(self.dict_2))
        for key, value in self.dict_2.items():
            stream.write_variable_length_int(key)
            stream.write_byte(value)

    def serialize(self) -> dict[str, Any]:
        return {
            "dict_1": self.dict_1,
            "dict_2": self.dict_2,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> MySale:
        return MySale(data.get("dict_1", {}), data.get("dict_2", {}))

    def __repr__(self) -> str:
        return f"MySale(dict_1={self.dict_1}, dict_2={self.dict_2})"

    def __str__(self) -> str:
        return f"MySale(dict_1={self.dict_1}, dict_2={self.dict_2})"


# ============================================================
# FILE: nyanko_club.py
# ============================================================
from __future__ import annotations
import datetime
import random
import time
from typing import Any

from bcsfe import core
from bcsfe.cli import dialog_creator, color


class NyankoClub:
    def __init__(
        self,
        officer_id: int,
        total_renewal_times: int,
        start_date_now: float,
        end_date_now: float,
        start_date_next: float,
        end_date_next: float,
        start_date_total: float,
        end_date_total: float,
        time_error_end: float,
        total_state_updates: int,
        login_bonus_date: float,
        claimed_rewards: dict[int, int],
        remaing_days_popup: float,
        first_popup_flag: bool,
        badge_flag: bool | None = None,
    ):
        self.officer_id = officer_id
        self.total_renewal_times = total_renewal_times
        self.start_date_now = start_date_now
        self.end_date_now = end_date_now
        self.start_date_next = start_date_next
        self.end_date_next = end_date_next
        self.start_date_total = start_date_total
        self.end_date_total = end_date_total
        self.time_error_end = time_error_end
        self.total_state_updates = total_state_updates
        self.login_bonus_date = login_bonus_date
        self.claimed_rewards = claimed_rewards
        self.remaing_days_popup = remaing_days_popup
        self.first_popup_flag = first_popup_flag
        self.badge_flag = badge_flag

    @staticmethod
    def init() -> NyankoClub:
        return NyankoClub(
            0,
            0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0,
            0.0,
            {},
            0.0,
            False,
            False,
        )

    @staticmethod
    def read(data: core.Data, gv: core.GameVersion) -> NyankoClub:
        officer_id = data.read_int()
        total_renewal_times = data.read_int()
        start_date_now = data.read_double()
        end_date_now = data.read_double()
        start_date_next = data.read_double()
        end_date_next = data.read_double()
        start_date_total = data.read_double()
        end_date_total = data.read_double()
        time_error_end = data.read_double()
        total_state_updates = data.read_int()
        login_bonus_date = data.read_double()
        claimed_rewards = data.read_int_int_dict()
        remaing_days_popup = data.read_double()
        first_popup_flag = data.read_bool()
        if gv >= 80100:
            badge_flag = data.read_bool()
        else:
            badge_flag = None
        return NyankoClub(
            officer_id,
            total_renewal_times,
            start_date_now,
            end_date_now,
            start_date_next,
            end_date_next,
            start_date_total,
            end_date_total,
            time_error_end,
            total_state_updates,
            login_bonus_date,
            claimed_rewards,
            remaing_days_popup,
            first_popup_flag,
            badge_flag,
        )

    def write(self, data: core.Data, gv: core.GameVersion):
        data.write_int(self.officer_id)
        data.write_int(self.total_renewal_times)
        data.write_double(self.start_date_now)
        data.write_double(self.end_date_now)
        data.write_double(self.start_date_next)
        data.write_double(self.end_date_next)
        data.write_double(self.start_date_total)
        data.write_double(self.end_date_total)
        data.write_double(self.time_error_end)
        data.write_int(self.total_state_updates)
        data.write_double(self.login_bonus_date)
        data.write_int_int_dict(self.claimed_rewards)
        data.write_double(self.remaing_days_popup)
        data.write_bool(self.first_popup_flag)
        if gv >= 80100:
            data.write_bool(self.badge_flag or False)

    def serialize(self) -> dict[str, Any]:
        return {
            "officer_id": self.officer_id,
            "total_renewal_times": self.total_renewal_times,
            "start_date_now": self.start_date_now,
            "end_date_now": self.end_date_now,
            "start_date_next": self.start_date_next,
            "end_date_next": self.end_date_next,
            "start_date_total": self.start_date_total,
            "end_date_total": self.end_date_total,
            "time_error_end": self.time_error_end,
            "total_state_updates": self.total_state_updates,
            "login_bonus_date": self.login_bonus_date,
            "claimed_rewards": self.claimed_rewards,
            "remaing_days_popup": self.remaing_days_popup,
            "first_popup_flag": self.first_popup_flag,
            "badge_flag": self.badge_flag,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> NyankoClub:
        return NyankoClub(
            data.get("officer_id", 0),
            data.get("total_renewal_times", 0),
            data.get("start_date_now", 0.0),
            data.get("end_date_now", 0.0),
            data.get("start_date_next", 0.0),
            data.get("end_date_next", 0.0),
            data.get("start_date_total", 0.0),
            data.get("end_date_total", 0.0),
            data.get("time_error_end", 0.0),
            data.get("total_state_updates", 0),
            data.get("login_bonus_date", 0.0),
            data.get("claimed_rewards", {}),
            data.get("remaing_days_popup", 0.0),
            data.get("first_popup_flag", False),
            data.get("badge_flag", False),
        )

    def __repr__(self):
        return f"<NyankoClub {self.officer_id}>"

    def __str__(self):
        return f"NyankoClub {self.officer_id}"

    def get_gold_pass(
        self, officer_id: int, total_days: int, save_file: core.SaveFile
    ):
        self.officer_id = officer_id
        start_date_now = int(time.time())
        end_date_now = (
            start_date_now + datetime.timedelta(days=total_days).total_seconds()
        )
        end_date_total = (
            start_date_now
            + datetime.timedelta(days=total_days * 2).total_seconds()
        )

        self.total_renewal_times = 2
        self.start_date_now = start_date_now
        self.end_date_now = end_date_now

        self.start_date_next = end_date_now
        self.end_date_next = end_date_total

        self.start_date_total = start_date_now
        self.end_date_total = end_date_total

        self.time_error_end = start_date_now

        self.total_state_updates = 2

        self.login_bonus_date = end_date_now

        self.remaing_days_popup = 0.0
        self.first_popup_flag = True
        self.badge_flag = False

        login = save_file.logins.get_login(5100)
        if login is not None:
            login.count = 0

        self.claimed_rewards = {}

    def remove_gold_pass(self, save_file: core.SaveFile):
        self.officer_id = -1
        self.total_renewal_times = 0
        self.start_date_now = 0.0
        self.end_date_now = 0.0
        self.start_date_next = 0.0
        self.end_date_next = 0.0
        self.start_date_total = 0.0
        self.end_date_total = 0.0
        self.time_error_end = 0.0
        self.total_state_updates = 0
        self.login_bonus_date = 0.0
        self.remaing_days_popup = 0.0
        self.first_popup_flag = False
        self.badge_flag = False

        login = save_file.logins.get_login(5100)
        if login is not None:
            login.count = 0

        self.claimed_rewards = {}

    @staticmethod
    def get_random_officer_id() -> int:
        return random.randint(1, 2**16 - 1)

    @staticmethod
    def edit_gold_pass(save_file: core.SaveFile):
        club = save_file.officer_pass.gold_pass

        officer_id = color.ColoredInput().localize("gold_pass_dialog").strip()
        if not officer_id:
            officer_id = NyankoClub.get_random_officer_id()

        if officer_id == "-1":
            officer_id = -1
        else:
            try:
                officer_id = int(officer_id)
            except ValueError:
                officer_id = NyankoClub.get_random_officer_id()
            officer_id = dialog_creator.IntInput().clamp_value(officer_id)

        if officer_id == -1:
            club.remove_gold_pass(save_file)
            color.ColoredText.localize("gold_pass_remove_success")
        else:
            club.get_gold_pass(officer_id, 30, save_file)
            color.ColoredText.localize("gold_pass_get_success", id=officer_id)


# ============================================================
# FILE: officer_pass.py
# ============================================================
from __future__ import annotations
from typing import Any
from bcsfe import core
from bcsfe.cli import color


class OfficerPass:
    def __init__(self, play_time: int):
        self.play_time = play_time
        self.gold_pass = core.NyankoClub.init()
        self.cat_id = 0
        self.cat_form = 0

    @staticmethod
    def init() -> OfficerPass:
        return OfficerPass(0)

    @staticmethod
    def read(data: core.Data) -> OfficerPass:
        play_time = data.read_int()
        return OfficerPass(play_time)

    def write(self, data: core.Data):
        if self.play_time > 2**31 - 1:
            self.play_time = 2**31 - 1
        data.write_int(self.play_time)

    def read_gold_pass(self, data: core.Data, gv: core.GameVersion):
        self.gold_pass = core.NyankoClub.read(data, gv)

    def write_gold_pass(self, data: core.Data, gv: core.GameVersion):
        self.gold_pass.write(data, gv)

    def read_cat_data(self, data: core.Data):
        self.cat_id = data.read_short()
        self.cat_form = data.read_short()

    def write_cat_data(self, data: core.Data):
        data.write_short(self.cat_id)
        data.write_short(self.cat_form)

    def serialize(self) -> dict[str, Any]:
        return {
            "play_time": self.play_time,
            "gold_pass": self.gold_pass.serialize(),
            "cat_id": self.cat_id,
            "cat_form": self.cat_form,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> OfficerPass:
        officer_pass = OfficerPass(
            data.get("play_time", 0),
        )
        officer_pass.gold_pass = core.NyankoClub.deserialize(
            data.get("gold_pass", {})
        )
        officer_pass.cat_id = data.get("cat_id", 0)
        officer_pass.cat_form = data.get("cat_form", 0)
        return officer_pass

    def __repr__(self):
        return f"OfficerPass({self.play_time}, {self.gold_pass}, {self.cat_id}, {self.cat_form})"

    def __str__(self):
        return self.__repr__()

    def reset(self, save_file: core.SaveFile):
        self.cat_id = 0
        self.cat_form = 0
        self.play_time = 0
        self.gold_pass.remove_gold_pass(save_file)

    @staticmethod
    def fix_crash(save_file: core.SaveFile):
        officer_pass = save_file.officer_pass
        officer_pass.reset(save_file)

        color.ColoredText.localize("officer_pass_fixed")


# ============================================================
# FILE: playtime.py
# ============================================================
from __future__ import annotations
from dataclasses import dataclass

from bcsfe import core
from bcsfe.cli import color, dialog_creator


@dataclass
class PlayTime:
    frames: int

    @staticmethod
    def get_fps() -> int:
        return 30

    @property
    def seconds(self) -> int:
        return self.frames // self.get_fps()

    @property
    def minutes(self) -> int:
        return self.seconds // 60

    @property
    def hours(self) -> int:
        return self.minutes // 60

    @property
    def just_seconds(self) -> int:
        return self.seconds % 60

    @property
    def just_minutes(self) -> int:
        return self.minutes % 60

    @property
    def just_hours(self) -> int:
        return self.hours % 60

    @staticmethod
    def from_hours(hours: int) -> PlayTime:
        return PlayTime(hours * 60 * 60 * PlayTime.get_fps())

    @staticmethod
    def from_minutes(minutes: int) -> PlayTime:
        return PlayTime(minutes * 60 * PlayTime.get_fps())

    @staticmethod
    def from_seconds(seconds: int) -> PlayTime:
        return PlayTime(seconds * PlayTime.get_fps())

    @staticmethod
    def from_hours_mins_secs(
        hours: int, minutes: int, seconds: int
    ) -> PlayTime:
        return (
            PlayTime.from_hours(hours)
            + PlayTime.from_minutes(minutes)
            + PlayTime.from_seconds(seconds)
        )

    def __add__(self, other: PlayTime) -> PlayTime:
        return PlayTime(self.frames + other.frames)


def edit(save_file: core.SaveFile):
    play_time = PlayTime(save_file.officer_pass.play_time)
    color.ColoredText.localize(
        "playtime_current",
        hours=play_time.hours,
        minutes=play_time.just_minutes,
        seconds=play_time.just_seconds,
        frames=play_time.frames,
    )
    hours, _ = dialog_creator.IntInput().get_input("playtime_hours_prompt", {})
    if hours is None:
        return
    minutes, _ = dialog_creator.IntInput().get_input(
        "playtime_minutes_prompt", {}
    )
    if minutes is None:
        return
    seconds, _ = dialog_creator.IntInput().get_input(
        "playtime_seconds_prompt", {}
    )
    if seconds is None:
        return

    play_time = PlayTime.from_hours_mins_secs(hours, minutes, seconds)
    save_file.officer_pass.play_time = play_time.frames
    color.ColoredText.localize(
        "playtime_edited",
        hours=play_time.hours,
        minutes=play_time.just_minutes,
        seconds=play_time.just_seconds,
        frames=play_time.frames,
    )


# ============================================================
# FILE: powerup.py
# ============================================================
from __future__ import annotations

from bcsfe import core


class PowerUpHelper:
    def __init__(self, cat: core.Cat, save_file: core.SaveFile):
        self.cat = cat
        self.save_file = save_file
        self.unit_limit = self.save_file.cats.read_unitlimit(
            self.save_file
        ).get_unit_limit(self.cat.id)
        self.all_unit_buy = self.save_file.cats.read_unitbuy(self.save_file)
        self.unit_buy = self.all_unit_buy.get_unit_buy(self.cat.id)
        self.rank_gifts = self.save_file.user_rank_rewards.read_rank_gifts(
            self.save_file
        )
        self.max_upgrade_level = self.__get_max_upgrade_level_check()

    def get_current_max_level(self) -> int | None:
        if self.unit_buy is None:
            return None
        return min(
            self.unit_buy.original_max_levels[0] + self.max_upgrade_level,
            self.unit_buy.max_upgrade_level_catseye,
        )

    def has_strict_upgrade(self) -> bool:
        return core.core_data.config.get_bool(core.ConfigKey.STRICT_UPGRADE)

    def get_upgrade_state_check(self) -> int:
        if not self.has_strict_upgrade():
            return 100000
        return self.save_file.upgrade_state

    def get_user_rank_check(self) -> int:
        if not self.has_strict_upgrade():
            return 1000000
        return self.save_file.calculate_user_rank()

    def __get_max_upgrade_level_check(self) -> int:
        if self.unit_limit is None:
            return self.cat.max_upgrade_level.base

        rewards = self.save_file.user_rank_rewards
        self.cat.max_upgrade_level.reset()

        strict_upgrade = self.has_strict_upgrade()

        for reward_id in range(len(rewards.rewards)):
            rank_gift = self.rank_gifts.get_by_id(reward_id)
            if rank_gift is None:
                continue
            user_rank_reward = rewards.rewards[reward_id]
            if not user_rank_reward.claimed and strict_upgrade:
                continue
            for present in rank_gift.rewards:
                if present[0] >= 1000 and present[0] <= 1599:
                    for limit in self.unit_limit.values:
                        if limit == present[0]:
                            self.cat.max_upgrade_level.increment_base(
                                present[1]
                            )
                elif present[0] >= 4000 and present[0] <= 4599:
                    for limit in self.unit_limit.values:
                        if limit == present[0]:
                            self.cat.max_upgrade_level.increment_plus(
                                present[1]
                            )

        return self.cat.max_upgrade_level.base

    def can_power_up(self) -> bool:
        if self.unit_buy is None:
            return False
        base_level = self.cat.upgrade.get_base()
        current_max_level = self.get_current_max_level()
        if current_max_level is None:
            return False

        if base_level >= current_max_level or (
            (
                self.get_upgrade_state_check() > 1
                or base_level == self.unit_buy.unknown_22
            )
            and self.get_upgrade_state_check() < 2
        ):
            return (
                self.unit_buy.rarity != 0
                and base_level >= self.unit_buy.max_upgrade_level_no_catseye
                and base_level < self.unit_buy.max_upgrade_level_catseye
                and base_level < current_max_level
            )
        return True

    def can_use_catseye(self) -> bool:
        if self.unit_buy is None:
            return False

        base_level = self.cat.upgrade.get_base()
        return (
            self.unit_buy.rarity != 0
            and base_level >= self.unit_buy.max_upgrade_level_no_catseye
            and self.unit_buy.max_upgrade_level_no_catseye != -1
            and self.get_user_rank_check() >= 1600
        )

    def upgrade_cat(self, force: bool = False) -> bool:
        if force:
            self.cat.upgrade_base(self.save_file)
            return True
        if self.unit_buy is None:
            return False
        current_max_level = self.get_current_max_level()
        if current_max_level is None:
            return False

        if self.can_power_up():
            self.cat.upgrade_base(self.save_file)
            return True

        if (
            self.can_use_catseye()
            and self.unit_buy.max_upgrade_level_no_catseye <= current_max_level
        ):
            if (
                self.cat.upgrade.get_base()
                < self.unit_buy.max_upgrade_level_catseye
            ):
                self.cat.upgrade_base(self.save_file)
                self.cat.catseyes_used += 1
                self.cat.max_upgrade_level.upgrade()
                return True
            return False
        return False

    def get_max_max_base_upgrade_level(self) -> int:
        max_level = 0
        if self.all_unit_buy.unit_buy is None:
            return 90
        for unit_buy in self.all_unit_buy.unit_buy:
            if unit_buy.max_upgrade_level_catseye > max_level:
                max_level = unit_buy.max_upgrade_level_catseye
        return max_level

    def get_max_max_plus_upgrade_level(self) -> int:
        max_level = 0
        if self.all_unit_buy.unit_buy is None:
            return 90
        for unit_buy in self.all_unit_buy.unit_buy:
            if unit_buy.max_plus_upgrade_level > max_level:
                max_level = unit_buy.max_plus_upgrade_level
        return max_level

    def get_max_possible_base(self) -> int:
        if self.unit_buy is None:
            return 90
        return self.unit_buy.max_upgrade_level_catseye

    def get_max_possible_plus(self) -> int:
        if self.unit_buy is None:
            return 90
        return self.unit_buy.max_plus_upgrade_level

    def reset_upgrade(self):
        self.cat.upgrade.base = 0
        self.cat.catseyes_used = 0

    def upgrade_by(self, amount: int):
        if amount == -1:
            return
        for _ in range(amount):
            did_upgrade = self.upgrade_cat()
            if not did_upgrade:
                break

    def max_upgrade(self):
        while self.upgrade_cat():
            pass


# ============================================================
# FILE: scheme_items.py
# ============================================================
from __future__ import annotations
from bcsfe import core
from bcsfe.cli import dialog_creator, color


class SchemeDataItem:
    def __init__(
        self,
        id: int,
        type: int,
        type_id: int,
        item_id: int,
        number: int,
        type_id2: int | None = None,
        item_id2: int | None = None,
        number2: int | None = None,
        type_id3: int | None = None,
        item_id3: int | None = None,
        number3: int | None = None,
    ):
        self.id = id
        self.type = type
        self.type_id = type_id
        self.item_id = item_id
        self.number = number
        self.type_id2 = type_id2
        self.item_id2 = item_id2
        self.number2 = number2
        self.type_id3 = type_id3
        self.item_id3 = item_id3
        self.number3 = number3

    def is_cat(self) -> bool:
        return self.type_id == 1

    def get_name(self, localizable: core.Localizable) -> str | None:
        key = f"scheme_popup_{self.id}"
        name = localizable.get(key)
        if name is None:
            return None
        return name.replace("<flash>,", "").replace("<flash>", "")


class SchemeItems:
    def __init__(self, to_obtain: list[int], received: list[int]):
        self.to_obtain = to_obtain
        self.received = received

    @staticmethod
    def init() -> SchemeItems:
        return SchemeItems([], [])

    @staticmethod
    def read(stream: core.Data) -> SchemeItems:
        total = stream.read_int()
        to_obtain: list[int] = []
        for _ in range(total):
            to_obtain.append(stream.read_int())

        total = stream.read_int()
        received: list[int] = []
        for _ in range(total):
            received.append(stream.read_int())

        return SchemeItems(to_obtain, received)

    def write(self, stream: core.Data):
        stream.write_int(len(self.to_obtain))
        for item in self.to_obtain:
            stream.write_int(item)

        stream.write_int(len(self.received))
        for item in self.received:
            stream.write_int(item)

    def serialize(self) -> dict[str, list[int]]:
        return {"to_obtain": self.to_obtain, "received": self.received}

    @staticmethod
    def deserialize(data: dict[str, list[int]]) -> SchemeItems:
        return SchemeItems(data.get("to_obtain", []), data.get("received", []))

    def __repr__(self) -> str:
        return f"SchemeItems(to_obtain={self.to_obtain!r}, received={self.received!r})"

    def __str__(self) -> str:
        return self.__repr__()

    def edit(self, save_file: core.SaveFile):
        item_names = core.core_data.get_gatya_item_names(save_file)
        localizable = save_file.get_localizable()
        scheme_data = core.core_data.get_game_data_getter(save_file).download(
            "DataLocal", "schemeItemData.tsv"
        )
        if scheme_data is None:
            return
        csv = core.CSV(scheme_data, "\t")
        scheme_items: dict[int, SchemeDataItem] = {}
        for line in csv.lines[1:]:
            scheme_items[line[0].to_int()] = SchemeDataItem(
                line[0].to_int(),
                line[1].to_int(),
                line[2].to_int(),
                line[3].to_int(),
                line[4].to_int(),
                line[5].to_int(),
                line[6].to_int(),
                line[7].to_int(),
                line[8].to_int(),
                line[9].to_int(),
                line[10].to_int(),
            )

        options: list[str] = []
        for item in scheme_items.values():
            scheme_name = item.get_name(localizable)
            if scheme_name is None:
                return
            string = "\n\t"
            if item.is_cat():
                cat_names = core.Cat.get_names(item.item_id, save_file)
                if cat_names:
                    cat_name = cat_names[0]
                    string += scheme_name.replace("%@", cat_name)
            else:
                item_name = item_names.get_name(item.item_id)
                if item_name:
                    string += scheme_name
                    first_index = string.find("%@")
                    second_index = string.find("%@", first_index + 1)
                    string = (
                        string[:first_index]
                        + str(item.number)
                        + " "
                        + item_name
                        + string[second_index + 2 :]
                    )
            string = string.replace("<br>", "\n\t")
            options.append(string)

        choice = dialog_creator.ChoiceInput.from_reduced(
            ["gain_scheme_items", "remove_scheme_items"],
            dialog="gain_remove_scheme_items",
        ).single_choice()
        if choice is None:
            return

        choice -= 1

        if choice == 0:
            self.add_scheme_items(options, scheme_items)
        elif choice == 1:
            self.remove_scheme_items(options, scheme_items)

    def add_scheme_items(
        self,
        options: list[str],
        scheme_items: dict[int, SchemeDataItem],
    ):
        scheme_ids, _ = dialog_creator.ChoiceInput.from_reduced(
            options,
            dialog="scheme_items_select_gain",
        ).multiple_choice()
        if scheme_ids is None:
            return
        for option_id in scheme_ids:
            scheme_id = list(scheme_items.keys())[option_id]
            if scheme_id not in self.to_obtain:
                self.to_obtain.append(scheme_id)
            if scheme_id in self.received:
                self.received.remove(scheme_id)

        color.ColoredText.localize("scheme_items_edit_success")

    def remove_scheme_items(
        self,
        options: list[str],
        scheme_items: dict[int, SchemeDataItem],
    ):
        scheme_ids, _ = dialog_creator.ChoiceInput.from_reduced(
            options,
            dialog="scheme_items_select_remove",
        ).multiple_choice()
        if scheme_ids is None:
            return
        for option_id in scheme_ids:
            scheme_id = list(scheme_items.keys())[option_id]
            if scheme_id in self.to_obtain:
                self.to_obtain.remove(scheme_id)
            if scheme_id in self.received:
                self.received.remove(scheme_id)

        color.ColoredText.localize("scheme_items_edit_success")


# ============================================================
# FILE: special_skill.py
# ============================================================
from __future__ import annotations, division
from bcsfe import core

from typing import Any

from bcsfe.cli import dialog_creator, color


class SpecialSkill:
    def __init__(self, upg: core.Upgrade):
        self.upgrade = upg
        self.seen = 0
        self.max_upgrade_level = core.Upgrade(0, 0)

    @staticmethod
    def init() -> SpecialSkill:
        return SpecialSkill(core.Upgrade(0, 0))

    @staticmethod
    def read_upgrade(stream: core.Data) -> SpecialSkill:
        up = core.Upgrade.read(stream)
        return SpecialSkill(up)

    def write_upgrade(self, stream: core.Data):
        self.upgrade.write(stream)

    def read_seen(self, stream: core.Data):
        self.seen = stream.read_int()

    def write_seen(self, stream: core.Data):
        stream.write_int(self.seen)

    def read_max_upgrade_level(self, stream: core.Data):
        level = core.Upgrade.read(stream)
        self.max_upgrade_level = level

    def write_max_upgrade_level(self, stream: core.Data):
        self.max_upgrade_level.write(stream)

    def serialize(self) -> dict[str, Any]:
        return {
            "upgrade": self.upgrade.serialize(),
            "seen": self.seen,
            "max_upgrade_level": self.max_upgrade_level.serialize(),
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> SpecialSkill:
        skill = SpecialSkill(core.Upgrade.deserialize(data.get("upgrade", {})))
        skill.seen = data.get("seen", 0)
        skill.max_upgrade_level = core.Upgrade.deserialize(
            data.get("max_upgrade_level", {})
        )
        return skill

    def __repr__(self) -> str:
        return f"Skill(upgrade={self.upgrade}, seen={self.seen}, max_upgrade_level={self.max_upgrade_level})"

    def __str__(self) -> str:
        return self.__repr__()

    def set_upgrade(
        self,
        upgrade: core.Upgrade,
        only_plus: bool = False,
        max_base: int | None = None,
        max_plus: int | None = None,
    ):
        if max_base is not None:
            upgrade.base = min(upgrade.base, max_base)
        if max_plus is not None:
            upgrade.plus = min(upgrade.plus, max_plus)

        base = upgrade.base
        plus = upgrade.plus

        if base != -1 and not only_plus:
            self.upgrade.base = upgrade.get_random_base(max_base)
        if plus != -1:
            self.upgrade.plus = upgrade.get_random_plus(max_plus)


class SpecialSkills:
    def __init__(self, skills: list[SpecialSkill]):
        self.skills = skills

    def get_upgrade(self, valid_skill_id: int) -> SpecialSkill:
        if valid_skill_id >= 1:
            valid_skill_id += 1

        return self.skills[valid_skill_id]

    def set_upgrade(
        self,
        valid_skill_id: int,
        upgrade: core.Upgrade,
        max_base: int | None = None,
        max_plus: int | None = None,
    ):
        u = upgrade.copy()
        valid_skills = self.get_valid_skills()
        valid_skills[valid_skill_id].set_upgrade(
            u, max_base=max_base, max_plus=max_plus
        )

        if (
            valid_skill_id == 0
        ):  # if it is a cat cannon power upgrade, mirror the upgrade to the hidden cat cannon power special skill
            self.skills[1].set_upgrade(u, max_base=max_base, max_plus=max_plus)

    @staticmethod
    def init() -> SpecialSkills:
        skills = [SpecialSkill.init() for _ in range(11)]
        return SpecialSkills(skills)

    def get_valid_skills(self) -> list[SpecialSkill]:
        new_skills: list[SpecialSkill] = []
        for i, skill in enumerate(self.skills):
            if i == 1:
                continue
            new_skills.append(skill)

        return new_skills

    @staticmethod
    def read_upgrades(stream: core.Data) -> SpecialSkills:
        total_skills = 11

        skills: list[SpecialSkill] = []
        for _ in range(total_skills):
            skills.append(SpecialSkill.read_upgrade(stream))

        return SpecialSkills(skills)

    def write_upgrades(self, stream: core.Data):
        for skill in self.skills:
            skill.write_upgrade(stream)

    def read_gatya_seen(self, stream: core.Data):
        for skill in self.get_valid_skills():
            skill.read_seen(stream)

    def write_gatya_seen(self, stream: core.Data):
        for skill in self.get_valid_skills():
            skill.write_seen(stream)

    def read_max_upgrade_levels(self, stream: core.Data):
        for skill in self.skills:
            skill.read_max_upgrade_level(stream)

    def write_max_upgrade_levels(self, stream: core.Data):
        for skill in self.skills:
            skill.write_max_upgrade_level(stream)

    def serialize(self) -> list[dict[str, Any]]:
        return [skill.serialize() for skill in self.skills]

    @staticmethod
    def deserialize(data: list[dict[str, Any]]) -> SpecialSkills:
        skills = SpecialSkills([])
        for skill in data:
            skills.skills.append(SpecialSkill.deserialize(skill))

        return skills

    def __repr__(self) -> str:
        return f"Skills(skills={self.skills})"

    def __str__(self) -> str:
        return f"Skills(skills={self.skills})"

    def edit(self, save_file: core.SaveFile):
        names_o = core.core_data.get_gatya_item_names(save_file)
        items = core.core_data.get_gatya_item_buy(save_file).get_by_category(2)
        if items is None:
            return
        names: list[str] = []
        for item in items:
            name = names_o.get_name(item.id)
            if name is None:
                return
            names.append(name)
        ids, _ = dialog_creator.ChoiceInput.from_reduced(
            names, [], {}, "special_skills_dialog"
        ).multiple_choice()
        if not ids:
            return
        skills = self.get_valid_skills()
        if len(ids) == 1:
            option_id = 0
        else:
            options: list[str] = [
                "upgrade_individual_skill",
                "upgrade_all_skills",
            ]
            option_id = dialog_creator.ChoiceInput(
                options, options, [], {}, "upgrade_skills_select_mod", True
            ).single_choice()
            if option_id is None:
                return
            option_id -= 1

        ability_data = core.core_data.get_ability_data(save_file)
        if ability_data.ability_data is None:
            return
        success = False
        if option_id == 0:
            for id in ids:
                color.ColoredText.localize(
                    "selected_skill_upgrades",
                    name=names[id],
                    base_level=skills[id].upgrade.base + 1,
                    plus_level=skills[id].upgrade.plus,
                )
                ability = ability_data.get_ability_data_item(id)
                if ability is None:
                    continue
                upgrade, should_exit = core.Upgrade.get_user_upgrade(
                    ability.max_base_level - 1, ability.max_plus_level
                )
                if should_exit:
                    return
                if upgrade is not None:
                    self.set_upgrade(id, upgrade)
                    color.ColoredText.localize(
                        "selected_skill_upgraded",
                        name=names[id],
                        base_level=skills[id].upgrade.base + 1,
                        plus_level=skills[id].upgrade.plus,
                    )
                    success = True

        elif option_id == 1:
            max_base_level = max(
                [ability.max_base_level for ability in ability_data.ability_data]
            )
            max_plus_level = max(
                [ability.max_plus_level for ability in ability_data.ability_data]
            )
            upgrade, should_exit = core.Upgrade.get_user_upgrade(
                max_base_level - 1, max_plus_level
            )
            if should_exit or upgrade is None:
                return
            disable_maxes = core.core_data.config.get_bool(core.ConfigKey.DISABLE_MAXES)
            for id in ids:
                max_base_level = ability_data.ability_data[id].max_base_level - 1
                max_plus_level = ability_data.ability_data[id].max_plus_level
                if disable_maxes:
                    max_base_level = None
                    max_plus_level = None

                self.set_upgrade(
                    id,
                    upgrade.copy(),
                    max_base=max_base_level,
                    max_plus=max_plus_level,
                )

                color.ColoredText.localize(
                    "selected_skill_upgraded",
                    name=names[id],
                    base_level=skills[id].upgrade.base + 1,
                    plus_level=skills[id].upgrade.plus,
                )
            success = True

        if success:
            color.ColoredText.localize("skills_edited")

    def get_from_id(self, id: int, only_valid: bool = True) -> SpecialSkill | None:
        if only_valid:
            skills = self.get_valid_skills()
        else:
            skills = self.skills
        if id >= len(skills) or id < 0:
            return None
        return skills[id]


class AbilityDataItem:
    def __init__(
        self,
        index: int,
        sell_price: int,
        gatya_rarity: int,
        max_base_level: int,
        max_plus_level: int,
        chapter_1_to_2_max_level: int,
    ):
        self.index = index
        self.sell_price = sell_price
        self.gatya_rarity = gatya_rarity
        self.max_base_level = max_base_level
        self.max_plus_level = max_plus_level
        self.chapter_1_to_2_max_level = chapter_1_to_2_max_level


class AbilityData:
    def __init__(self, save_file: core.SaveFile):
        self.save_file = save_file
        self.ability_data = self.get_ability_data()

    def get_ability_data(self) -> list[AbilityDataItem] | None:
        gdg = core.core_data.get_game_data_getter(self.save_file)
        data = gdg.download("DataLocal", "AbilityData.csv")
        if data is None:
            return None
        csv = core.CSV(data)
        ability_data: list[AbilityDataItem] = []
        for i, row in enumerate(csv):
            ability_data.append(
                AbilityDataItem(
                    i,
                    row[0].to_int(),
                    row[1].to_int(),
                    row[2].to_int(),
                    row[3].to_int(),
                    row[4].to_int(),
                )
            )
        return ability_data

    def get_ability_data_item(self, item_id: int) -> AbilityDataItem | None:
        if self.ability_data is None:
            return None
        return self.ability_data[item_id]


# ============================================================
# FILE: stamp.py
# ============================================================
from __future__ import annotations
from typing import Any
from bcsfe import core


class StampData:
    def __init__(
        self,
        current_stamp: int,
        collected_stamp: list[int],
        unknown: int,
        daily_reward: int,
    ):
        self.current_stamp = current_stamp
        self.collected_stamp = collected_stamp
        self.unknown = unknown
        self.daily_reward = daily_reward

    @staticmethod
    def init() -> StampData:
        return StampData(0, [0] * 30, 0, 0)

    @staticmethod
    def read(stream: core.Data) -> StampData:
        current_stamp = stream.read_int()
        collected_stamp = stream.read_int_list(30)
        unknown = stream.read_int()
        daily_reward = stream.read_int()
        return StampData(current_stamp, collected_stamp, unknown, daily_reward)

    def write(self, stream: core.Data):
        stream.write_int(self.current_stamp)
        stream.write_int_list(self.collected_stamp, write_length=False)
        stream.write_int(self.unknown)
        stream.write_int(self.daily_reward)

    def serialize(self) -> dict[str, Any]:
        return {
            "current_stamp": self.current_stamp,
            "collected_stamp": self.collected_stamp,
            "unknown": self.unknown,
            "daily_reward": self.daily_reward,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> StampData:
        return StampData(
            data.get("current_stamp", 0),
            data.get("collected_stamp", []),
            data.get("unknown", 0),
            data.get("daily_reward", 0),
        )

    def __repr__(self):
        return f"StampData({self.current_stamp}, {self.collected_stamp}, {self.unknown}, {self.daily_reward})"

    def __str__(self):
        return f"StampData({self.current_stamp}, {self.collected_stamp}, {self.unknown}, {self.daily_reward})"


# ============================================================
# FILE: talent_orbs.py
# ============================================================
from __future__ import annotations
from typing import Any
from bcsfe import core
from bcsfe.cli import color, dialog_creator


class TalentOrb:
    def __init__(self, id: int, value: int):
        self.id = id
        self.value = value

    @staticmethod
    def init() -> TalentOrb:
        return TalentOrb(
            0,
            0,
        )

    @staticmethod
    def read(stream: core.Data, gv: core.GameVersion) -> TalentOrb:
        id = stream.read_short()
        if gv < 110400:
            value = stream.read_byte()
        else:
            value = stream.read_short()
        return TalentOrb(id, value)

    def write(self, stream: core.Data, gv: core.GameVersion):
        stream.write_short(self.id)
        if gv < 110400:
            stream.write_byte(self.value)
        else:
            stream.write_short(self.value)

    def serialize(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "value": self.value,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> TalentOrb:
        return TalentOrb(data.get("id", 0), data.get("value", 0))

    def __repr__(self):
        return f"Orb({self.id}, {self.value})"

    def __str__(self):
        return self.__repr__()


class TalentOrbs:
    def __init__(self, orbs: dict[int, TalentOrb]):
        self.orbs = orbs

    @staticmethod
    def init() -> TalentOrbs:
        return TalentOrbs({})

    @staticmethod
    def read(stream: core.Data, gv: core.GameVersion) -> TalentOrbs:
        length = stream.read_short()
        orbs: dict[int, TalentOrb] = {}
        for _ in range(length):
            orb = TalentOrb.read(stream, gv)
            orbs[orb.id] = orb
        return TalentOrbs(orbs)

    def write(self, stream: core.Data, gv: core.GameVersion):
        stream.write_short(len(self.orbs))
        for orb in self.orbs.values():
            orb.write(stream, gv)

    def serialize(self) -> list[dict[str, Any]]:
        return [orb.serialize() for orb in self.orbs.values()]

    @staticmethod
    def deserialize(data: list[dict[str, Any]]) -> TalentOrbs:
        return TalentOrbs(
            {orb.get("id", 0): TalentOrb.deserialize(orb) for orb in data}
        )

    def __repr__(self):
        return f"TalentOrbs({self.orbs})"

    def __str__(self):
        return self.__repr__()

    def set_orb(self, id: int, value: int):
        self.orbs[id] = TalentOrb(id, value)


class RawOrbInfo:
    def __init__(
        self,
        orb_id: int,
        rank_id: int,
        effect_id: int,
        value: list[int],
        target_id: int | None,
    ):
        self.orb_id = orb_id
        self.rank_id = rank_id
        self.effect_id = effect_id
        self.value = value
        self.target_id = target_id


class OrbInfo:
    def __init__(
        self,
        raw_orb_info: RawOrbInfo,
        rank: str,
        target: str | None,
        effect: str,
    ):
        self.raw_orb_info = raw_orb_info
        self.rank = rank
        self.target = target
        self.effect = effect

    def __str__(self) -> str:
        """Get the string representation of the OrbInfo

        Returns:
            str: The string representation of the OrbInfo
        """
        target_color = color_from_enemy_type(self.raw_orb_info.target_id)
        rank_color = color_from_grade(self.raw_orb_info.rank_id)
        effect_color = color_from_effect(self.raw_orb_info.effect_id)
        effect_text = self.effect.replace("%@", "{}")
        effect_text = f"<{effect_color}>{effect_text}</>"
        target = self.target
        effect = effect_text.format(
            f"<{rank_color}>{self.rank}</>",
            f"<{target_color}>{target}</>" if target else "",
        )
        return f"{effect}"

    def to_colortext(self) -> str:
        """Get the string representation of the OrbInfo with color

        Returns:
            str: The string representation of the OrbInfo with color
        """
        return str(self)

    @staticmethod
    def create_unknown(orb_id: int) -> OrbInfo:
        """Create an unknown OrbInfo

        Args:
            orb_id (int): The id of the orb

        Returns:
            OrbInfo: The unknown OrbInfo
        """
        return OrbInfo(
            RawOrbInfo(orb_id, 0, 0, [], 0),
            "???",
            "",
            "%@:%@",
        )


class OrbInfoList:
    equipment_data_file_name = "DataLocal/equipmentlist.json"
    grade_list_file_name = "DataLocal/equipmentgrade.csv"
    attribute_list_file_name = "resLocal/attribute_explonation.tsv"
    effect_list_file_name = "resLocal/equipment_explonation.tsv"

    def __init__(self, orb_info_list: list[OrbInfo]):
        """Initialize the OrbInfoList class

        Args:
            orb_info_list (list[OrbInfo]): The list of OrbInfo
        """
        self.orb_info_list = orb_info_list

    @staticmethod
    def create(save_file: core.SaveFile) -> OrbInfoList | None:
        """Create an OrbInfoList

        Args:
            save_file (core.SaveFile): The save file

        Returns:
            OrbInfoList | None: The OrbInfoList
        """
        gdg = core.core_data.get_game_data_getter(save_file)
        json_data_file = gdg.download_from_path(OrbInfoList.equipment_data_file_name)
        grade_list_file = gdg.download_from_path(OrbInfoList.grade_list_file_name)
        attribute_list_file = gdg.download_from_path(
            OrbInfoList.attribute_list_file_name
        )
        equipment_list_file = gdg.download_from_path(OrbInfoList.effect_list_file_name)
        if (
            json_data_file is None
            or grade_list_file is None
            or attribute_list_file is None
            or equipment_list_file is None
        ):
            return None
        raw_orbs = OrbInfoList.parse_json_data(json_data_file)
        if raw_orbs is None:
            return None
        orbs = OrbInfoList.load_names(
            raw_orbs, grade_list_file, attribute_list_file, equipment_list_file
        )
        return OrbInfoList(orbs)

    @staticmethod
    def parse_json_data(json_data: core.Data) -> list[RawOrbInfo] | None:
        """Parse the json data of the equipment

        Args:
            json_data (core.Data): The json data

        Returns:
            list[RawOrbInfo]: The list of RawOrbInfo
        """
        try:
            data: dict[str, Any] = core.JsonFile.from_data(json_data).to_object()
        except core.JSONDecodeError:
            return None
        orb_info_list: list[RawOrbInfo] = []
        for id, orb in enumerate(data["ID"]):
            grade_id = orb["gradeID"]
            content = orb["content"]
            value = orb["value"]
            attribute = orb.get("attribute")
            orb_info_list.append(RawOrbInfo(id, grade_id, content, value, attribute))
        return orb_info_list

    @staticmethod
    def load_names(
        raw_orb_info: list[RawOrbInfo],
        grade_data: core.Data,
        attribute_data: core.Data,
        effect_data: core.Data,
    ) -> list[OrbInfo]:
        """Load the names of the equipment

        Args:
            raw_orb_info (list[RawOrbInfo]): The list of RawOrbInfo
            grade_data (core.Data): Raw data of the grade list
            attribute_data (core.Data): Raw data of the attribute list
            effect_data (core.Data): Raw data of the effect list

        Returns:
            list[OrbInfo]: The list of OrbInfo
        """
        grade_csv = core.CSV(grade_data)
        attribute_tsv = core.CSV(attribute_data, "\t")
        effect_csv = core.CSV(effect_data, "\t")
        orb_info_list: list[OrbInfo] = []
        for orb in raw_orb_info:
            grade = grade_csv[orb.rank_id][3].to_str()
            effect = effect_csv[orb.effect_id][0].to_str()

            if orb.target_id is not None:
                attribute = attribute_tsv[orb.target_id][0].to_str()
            else:
                attribute = None

            orb_info_list.append(OrbInfo(orb, grade, attribute, effect))
        return orb_info_list

    def get_orb_info(self, orb_id: int) -> OrbInfo | None:
        """Get the OrbInfo from the id

        Args:
            orb_id (int): The id of the orb

        Returns:
            OrbInfo | None: The OrbInfo
        """
        try:
            return self.orb_info_list[orb_id]
        except IndexError:
            return None

    def get_orb_from_components(
        self,
        grade: str,
        attribute: str | None,
        effect: str,
    ) -> OrbInfo | None:
        """Get the OrbInfo from the components

        Args:
            grade (str): The grade of the orb
            attribute (str | None): The attribute of the orb. None if applies to all attributes
            effect (str): The effect of the orb

        Returns:
            OrbInfo | None: The OrbInfo
        """
        for orb in self.orb_info_list:
            if orb.rank == grade and orb.target == attribute and orb.effect == effect:
                return orb
        return None

    def does_match_orb_str(self, str_1: str | None, str_2: str | None) -> bool:
        if str_2 == "*":
            return True

        if str_1 is None:
            return str_2 is None
        if str_2 is None:
            return False

        return str_1.lower() == str_2.lower()

    def get_orbs_from_component_fuzzy(
        self,
        grade: str,
        attribute: str | None,
        effect: str,
    ) -> list[OrbInfo]:
        """Get the OrbInfo from the components matching the first word of the effect and lowercased

        Args:
            grade (str): The grade of the orb
            attribute (str | None): The attribute of the orb. None if all
            effect (str): The effect of the orb

        Returns:
            list[OrbInfo]: The list of OrbInfo
        """
        orbs: list[OrbInfo] = []
        for orb in self.orb_info_list:
            if (
                (orb.rank.lower() == grade.lower() or grade == "*")
                and (self.does_match_orb_str(orb.target, attribute))
                and (orb.effect == effect or effect == "*")
            ):
                orbs.append(orb)
        return orbs

    def get_all_grades(self) -> list[str]:
        """Get all the grades

        Returns:
            list[str]: The list of grades
        """

        data = list(
            set([(orb.rank, orb.raw_orb_info.rank_id) for orb in self.orb_info_list])
        )

        data.sort(key=lambda id: id[1])

        return [orb[0] for orb in data]

    def get_all_attributes(self) -> list[str | None]:
        """Get all the attributes

        Returns:
            list[str]: The list of attributes
        """

        data = list(
            set(
                [
                    (orb.target, orb.raw_orb_info.target_id)
                    for orb in self.orb_info_list
                    if orb.target is not None and orb.raw_orb_info.target_id is not None
                ]
            )
        )

        data.sort(key=lambda id: id[1])

        return [orb[0] for orb in data]

    def get_all_effects(self) -> list[str]:
        """Get all the effects

        Returns:
            list[str]: The list of effects
        """

        data = list(
            set(
                [(orb.effect, orb.raw_orb_info.effect_id) for orb in self.orb_info_list]
            )
        )

        data.sort(key=lambda id: id[1])

        return [orb[0] for orb in data]


class SaveOrb:
    """Represents a saved orb in the save file"""

    def __init__(self, orb: OrbInfo, count: int):
        """Initialize the SaveOrb class

        Args:
            orb (OrbInfo): The OrbInfo
            count (int): The amount of the orb
        """
        self.count = count
        self.orb = orb


def color_from_enemy_type(target_id: int | None) -> str:
    if target_id is None:
        return color.ColorHex.WHITE
    if target_id == 0:
        return color.ColorHex.RED
    elif target_id == 1:
        return color.ColorHex.GREEN
    elif target_id == 2:
        return color.ColorHex.DARK_GREY
    elif target_id == 3:
        return color.ColorHex.LIGHT_GREY
    elif target_id == 4:
        return color.ColorHex.YELLOW
    elif target_id == 5:
        return color.ColorHex.BLUE
    elif target_id == 6:
        return color.ColorHex.MAGENTA
    elif target_id == 7:
        return color.ColorHex.DARK_GREEN
    elif target_id == 8:
        return color.ColorHex.WHITE
    elif target_id == 9:
        return color.ColorHex.DARK_MAGENTA
    elif target_id == 10:
        return color.ColorHex.ORANGE
    elif target_id == 11:
        return color.ColorHex.CYAN
    return color.ColorHex.BLACK


def color_from_grade(grade_id: int) -> str:
    if grade_id == 0:
        return color.ColorHex.RED
    elif grade_id == 1:
        return color.ColorHex.ORANGE
    elif grade_id == 2:
        return color.ColorHex.YELLOW
    elif grade_id == 3:
        return color.ColorHex.GREEN
    elif grade_id == 4:
        return color.ColorHex.BLUE
    return color.ColorHex.BLACK


def color_from_effect(effect_id: int):
    if effect_id == 0:
        return color.ColorHex.RED
    elif effect_id == 1:
        return color.ColorHex.GREEN
    elif effect_id == 2:
        return color.ColorHex.DARK_GREY
    elif effect_id == 3:
        return color.ColorHex.LIGHT_GREY
    elif effect_id == 4:
        return color.ColorHex.YELLOW
    elif effect_id == 5:
        return color.ColorHex.BLUE
    elif effect_id == 6:
        return color.ColorHex.MAGENTA
    elif effect_id == 7:
        return color.ColorHex.DARK_GREEN
    elif effect_id == 8:
        return color.ColorHex.WHITE
    elif effect_id == 9:
        return color.ColorHex.DARK_MAGENTA
    elif effect_id == 10:
        return color.ColorHex.ORANGE

    return color.ColorHex.BLACK


class SaveOrbs:
    def __init__(
        self,
        orbs: dict[int, SaveOrb],
        orb_info_list: OrbInfoList,
    ):
        """Initialize the SaveOrbs class

        Args:
            orbs (dict[int, SaveOrb]): The orbs
            orb_info_list (OrbInfoList): The orb info list
        """
        self.orbs = orbs
        self.orb_info_list = orb_info_list

    @staticmethod
    def from_save_file(save_file: core.SaveFile) -> SaveOrbs | None:
        """Create a SaveOrbs from the save stats

        Args:
            save_file (core.SaveFile): The save file

        Returns:
            SaveOrbs | None: The SaveOrbs
        """
        orb_info_list = OrbInfoList.create(save_file)
        if orb_info_list is None:
            return None
        orbs: dict[int, SaveOrb] = {}
        for orb_id, orb in save_file.talent_orbs.orbs.items():
            try:
                orb_info = orb_info_list.orb_info_list[int(orb_id)]
            except IndexError:
                orb_info = OrbInfo.create_unknown(int(orb_id))
            orbs[int(orb_id)] = SaveOrb(orb_info, orb.value)

        return SaveOrbs(orbs, orb_info_list)

    def print(self):
        """Print the orbs as a formatted list"""
        self.sort_orbs()
        total_orbs = sum([orb.count for orb in self.orbs.values()])
        color.ColoredText.localize("total_current_orbs", total_orbs=total_orbs)
        color.ColoredText.localize(
            "total_current_orb_types", total_types=len(self.orbs)
        )
        color.ColoredText.localize("current_orbs")
        for orb in self.orbs.values():
            color.ColoredText(f"<@q>{orb.count}</> {orb.orb.to_colortext()}")

    def sort_orbs(self):
        """Sort the orbs by attribute, effect, grade and id in that order with attribute being the most important"""
        orbs = list(self.orbs.values())
        orbs.sort(key=lambda orb: orb.orb.raw_orb_info.orb_id)
        orbs.sort(key=lambda orb: orb.orb.raw_orb_info.rank_id)
        orbs.sort(key=lambda orb: orb.orb.raw_orb_info.effect_id)
        orbs.sort(key=lambda orb: orb.orb.raw_orb_info.target_id or -1)

    def localize_attribute(self, attribute: str | None) -> str | None:
        if attribute is not None:
            return attribute

    def edit(self):
        """Edit the orbs"""
        # this code sucks quit a lot, but it works and i can't be bothered making it better atm
        self.print()
        all_grades = self.orb_info_list.get_all_grades()
        all_grades = [grade for grade in all_grades]
        all_grades.sort()
        all_attributes = self.orb_info_list.get_all_attributes()
        all_attributes = [
            self.localize_attribute(attribute) or ""
            for attribute in all_attributes
            if attribute
        ]
        all_attributes.sort()
        all_effects = self.orb_info_list.get_all_effects()
        all_effects.sort()
        all_effects_str = [
            effect.lower().replace("%@", "").replace(":", "").strip() + f" ({i})"
            for (i, effect) in enumerate(all_effects)
        ]
        all_effect_ids = [i for i in range(len(all_effects))]

        all_grades_str = "".join(
            f"<{color_from_grade(self.orb_info_list.get_all_grades().index(grade))}>{grade}</>,"
            for grade in all_grades
        )

        all_attributes_str = "".join(
            f"<{color_from_enemy_type(self.orb_info_list.get_all_attributes().index(attribute))}>{attribute}</>,"
            for attribute in all_attributes
        )

        all_effects_str = "".join(
            f"<{color_from_effect(self.orb_info_list.get_all_effects().index(effect))}>{effect_str}</>,"
            for effect_str, effect in zip(all_effects_str, all_effects)
        )

        color.ColoredText.localize(
            "edit_orbs_help",
            escape=False,
            all_grades_str=all_grades_str,
            all_attributes_str=all_attributes_str,
            all_effects_str=all_effects_str,
        )

        orb_input_selection = (
            color.ColoredInput()
            .localize("orb_select")
            .lower()
            .replace("angle", "angel")
            .split(",")
        )
        if orb_input_selection == [core.core_data.local_manager.get_key("quit_key")]:
            return

        orb_selection: list[OrbInfo] = []

        for orb_input in orb_input_selection:
            grade = None
            attribute = None
            effect = None
            orb_input = orb_input.strip()
            parts = orb_input.split(" ")
            parts = [part.lower() for part in parts if part != ""]
            if len(parts) == 0:
                continue
            if parts[0] == "*":
                orb_selection = self.orb_info_list.orb_info_list
                break
            for available_grade in all_grades:
                if available_grade.lower() in parts:
                    grade = available_grade
                    break
            for available_attribute in all_attributes:
                if available_attribute.lower() in parts:
                    attribute = available_attribute
                    break
            for available_effect in all_effect_ids:
                if str(available_effect) in parts:
                    effect = all_effects[available_effect]
                    break
            if grade is None:
                grade = "*"
            if attribute is None:
                attribute = "*"
            if effect is None:
                effect = "*"
            orbs = self.orb_info_list.get_orbs_from_component_fuzzy(
                grade, attribute, effect
            )
            orb_selection.extend(orbs)

        orb_selection = list(set(orb_selection))
        orb_selection.sort(key=lambda orb: orb.raw_orb_info.orb_id)
        orb_selection.sort(key=lambda orb: orb.raw_orb_info.rank_id)
        orb_selection.sort(key=lambda orb: orb.raw_orb_info.effect_id)
        orb_selection.sort(key=lambda orb: orb.raw_orb_info.target_id or -1)

        color.ColoredText.localize("selected_orbs")

        for orb in orb_selection:
            color.ColoredText(orb.to_colortext())

        max_orbs = core.core_data.max_value_manager.get("talent_orbs")

        if len(orb_selection) == 0:
            return
        if len(orb_selection) == 1:
            individual = True
        else:
            individual = dialog_creator.ChoiceInput.from_reduced(
                ["individual", "edit_all_at_once"],
                dialog="edit_orbs_individually",
                single_choice=True,
            ).single_choice()
            if individual is None:
                return
            individual = True if individual == 1 else False
        if individual:
            for orb in orb_selection:
                orb_id = orb.raw_orb_info.orb_id
                try:
                    orb_count = self.orbs[orb_id].count
                except KeyError:
                    orb_count = 0

                orb_count = dialog_creator.SingleEditor(
                    orb.to_colortext(), orb_count, max_orbs
                ).edit(escape_text=False)

                self.orbs[orb_id] = SaveOrb(orb, orb_count)

        else:
            int_input = dialog_creator.IntInput(max_orbs)
            orb_count = int_input.get_input_locale_while(
                "edit_orbs_all", {"max": max_orbs}, escape=False
            )
            if orb_count is None:
                return
            orb_count = int_input.clamp_value(orb_count)
            for orb in orb_selection:
                orb_id = orb.raw_orb_info.orb_id
                self.orbs[orb_id] = SaveOrb(orb, orb_count)

        self.print()

    def save(self, save_file: core.SaveFile):
        """Save the orbs to the save_stats

        Args:
            save_file (core.SaveFile): The save_stats to save the orbs to
        """
        for orb_id, orb in self.orbs.items():
            save_file.talent_orbs.orbs[orb_id] = core.TalentOrb(orb_id, orb.count)

    @staticmethod
    def edit_talent_orbs(save_file: core.SaveFile):
        """Edit the talent orbs

        Args:
            save_file (core.SaveFile): The save_stats to edit the orbs of

        """
        save_orbs = SaveOrbs.from_save_file(save_file)
        if save_orbs is None:
            color.ColoredText.localize("failed_to_load_orbs")
            return None
        save_orbs.edit()
        save_orbs.save(save_file)


# ============================================================
# FILE: unlock_popups.py
# ============================================================
from __future__ import annotations
from bcsfe import core


class Popup:
    def __init__(self, seen: bool):
        self.seen = seen

    @staticmethod
    def init() -> Popup:
        return Popup(False)

    @staticmethod
    def read(stream: core.Data) -> Popup:
        seen = stream.read_bool()
        return Popup(seen)

    def write(self, stream: core.Data):
        stream.write_bool(self.seen)

    def serialize(self) -> bool:
        return self.seen

    @staticmethod
    def deserialize(data: bool) -> Popup:
        return Popup(data)

    def __repr__(self) -> str:
        return f"Popup(seen={self.seen!r})"

    def __str__(self) -> str:
        return self.__repr__()


class UnlockPopups:
    def __init__(self, popups: dict[int, Popup]):
        self.popups = popups

    @staticmethod
    def init() -> UnlockPopups:
        return UnlockPopups({})

    @staticmethod
    def read(stream: core.Data) -> UnlockPopups:
        total = stream.read_int()
        popups: dict[int, Popup] = {}
        for _ in range(total):
            key = stream.read_int()
            popups[key] = Popup.read(stream)
        return UnlockPopups(popups)

    def write(self, stream: core.Data):
        stream.write_int(len(self.popups))
        for key, popup in self.popups.items():
            stream.write_int(key)
            popup.write(stream)

    def serialize(self) -> dict[int, bool]:
        return {key: popup.serialize() for key, popup in self.popups.items()}

    @staticmethod
    def deserialize(data: dict[int, bool]) -> UnlockPopups:
        return UnlockPopups(
            {int(key): Popup.deserialize(popup) for key, popup in data.items()}
        )

    def __repr__(self) -> str:
        return f"Popups(popups={self.popups!r})"

    def __str__(self) -> str:
        return self.__repr__()


class UnlockPopupLine:
    def __init__(
        self,
        popup_id: int,
        enabled: bool,
        conditions: int,
        stage: int,
        map_conditions: int,
        user_rank: int,
        get_char_id1: int,
        get_char_id2: int,
        os_id: int,
        unlock_eye_1_id: int,
        add_level1: int,
        unlock_eye_2_id: int,
        add_level2: int,
        unlock_plus_id: int,
        add_level: int,
        skill_id: int,
        item_id: int,
        num: int,
        help_enabled: bool,
    ):
        self.popup_id = popup_id
        self.enabled = enabled
        self.conditions = conditions
        self.stage = stage
        self.map_conditions = map_conditions
        self.user_rank = user_rank
        self.get_char_id1 = get_char_id1
        self.get_char_id2 = get_char_id2
        self.os_id = os_id
        self.unlock_eye_1_id = unlock_eye_1_id
        self.add_level1 = add_level1
        self.unlock_eye_2_id = unlock_eye_2_id
        self.add_level2 = add_level2
        self.unlock_plus_id = unlock_plus_id
        self.add_level = add_level
        self.skill_id = skill_id
        self.item_id = item_id
        self.num = num
        self.help_enabled = help_enabled

    @staticmethod
    def from_csv_row(row: core.Row) -> UnlockPopupLine:
        return UnlockPopupLine(
            row.next_int(),
            row.next_bool(),
            row.next_int(),
            row.next_int(),
            row.next_int(),
            row.next_int(),
            row.next_int(),
            row.next_int(),
            row.next_int(),
            row.next_int(),
            row.next_int(),
            row.next_int(),
            row.next_int(),
            row.next_int(),
            row.next_int(),
            row.next_int(),
            row.next_int(),
            row.next_int(),
            row.next_bool(),
        )


class UnlockPopupData:
    def __init__(self, popups: list[UnlockPopupLine]):
        self.popups = popups

    @staticmethod
    def from_csv(csv: core.CSV) -> UnlockPopupData:
        popups: list[UnlockPopupLine] = []
        for line in csv.lines[1:]:
            popups.append(UnlockPopupLine.from_csv_row(line))

        return UnlockPopupData(popups)

    @staticmethod
    def from_save(save_file: core.SaveFile) -> UnlockPopupData | None:
        gdg = core.core_data.get_game_data_getter(save_file)
        data = gdg.download("DataLocal", "unlockPopup.tsv")
        if data is None:
            return None

        csv = core.CSV(data, "\t")

        return UnlockPopupData.from_csv(csv)


# ============================================================
# FILE: upgrade.py
# ============================================================
from __future__ import annotations
import random
from typing import Any
from bcsfe import core
from bcsfe.cli import color


class Upgrade:
    def __init__(self, plus: int, base: int):
        self.plus = plus
        self.base = base

        self.base_range = None
        self.plus_range = None

    def get_base(self) -> int:
        return self.base + 1

    def get_total(self) -> int:
        return self.get_base() + self.get_plus()

    def get_plus(self) -> int:
        return self.plus

    def upgrade(self):
        self.base += 1

    def increment_base(self, amount: int):
        self.base += amount

    def increment_plus(self, amount: int):
        self.plus += amount

    def get_random_base(self, max_base: int | None = None) -> int:
        if self.base_range is None:
            return self.base
        base = random.randint(self.base_range[0], self.base_range[1])
        if max_base is not None:
            base = min(base, max_base)
        return base

    def get_random_plus(self, max_plus: int | None = None) -> int:
        if self.plus_range is None:
            return self.plus
        plus = random.randint(self.plus_range[0], self.plus_range[1])
        if max_plus is not None:
            plus = min(plus, max_plus)
        return plus

    @staticmethod
    def read(stream: core.Data) -> Upgrade:
        plus = stream.read_ushort()
        base = stream.read_ushort()

        return Upgrade(plus, base)

    def write(self, stream: core.Data):
        stream.write_ushort(self.plus)
        stream.write_ushort(self.base)

    def serialize(self) -> dict[str, Any]:
        return {
            "plus": self.plus,
            "base": self.base,
        }

    @staticmethod
    def init() -> Upgrade:
        return Upgrade(0, 0)

    def reset(self):
        self.plus = 0
        self.base = 0

    @staticmethod
    def deserialize(data: dict[str, Any]) -> Upgrade:
        return Upgrade(data.get("plus", 0), data.get("base", 0))

    def __repr__(self) -> str:
        return f"Upgrade(plus={self.plus}, base={self.base})"

    def __str__(self) -> str:
        return f"Upgrade(plus={self.plus}, base={self.base})"

    @staticmethod
    def get_user_upgrade(
        max_pos_base: int,
        max_pos_plus: int,
    ) -> tuple[Upgrade | None, bool]:
        disable_maxes = core.core_data.config.get_bool(core.ConfigKey.DISABLE_MAXES)
        if disable_maxes:
            max_pos_base = 50_000
            max_pos_plus = 50_000
        color.ColoredText.localize(
            "max_upgrade", max_base=max_pos_base + 1, max_plus=max_pos_plus
        )
        usr_input = color.ColoredInput().localize("upgrade_input")
        if usr_input == core.core_data.local_manager.get_key("quit_key"):
            return None, True
        # example:
        # 10+20 = Upgrade(base=9, plus=20)
        # 10+ = Upgrade(base=9, plus=-1) # -1 means no change
        # +20 = Upgrade(base=-1, plus=20) # -1 means no change
        # 10 = Upgrade(base=9, plus=0)
        # 5-10+20-30 = Upgrade(base=random.randint(4, 9), plus=random.randint(20, 30))
        # 5-10+ = Upgrade(base=random.randint(4, 9), plus=-1)
        # +20-30 = Upgrade(base=-1, plus=random.randint(20, 30))
        # max+max = Upgrade(base=50000, plus=50000)

        parts = usr_input.split("+")
        if len(parts) == 1:
            base = parts[0]
            plus = "0"
        else:
            base = parts[0]
            plus = parts[1]

        min_base, max_base = None, None
        min_plus, max_plus = None, None

        max_text = core.core_data.local_manager.get_key("max")

        if not base:
            base_int = -1
        else:
            range_parts = base.split("-")
            if len(range_parts) == 1:
                if range_parts[0].strip() == max_text:
                    min_base = max_pos_base
                    max_base = max_pos_base
                else:
                    try:
                        min_base = int(range_parts[0]) - 1
                        max_base = min_base
                    except ValueError:
                        color.ColoredText.localize("invalid_upgrade_base", base=base)
                        return None, False
            else:
                try:
                    min_base = int(range_parts[0]) - 1
                    max_base = int(range_parts[1]) - 1
                except ValueError:
                    color.ColoredText.localize(
                        "invalid_upgrade_base_random",
                        min=range_parts[0],
                        max=range_parts[1],
                    )
                    return None, False

            base_int = (min_base + max_base) // 2

        if not plus:
            plus_int = -1
        else:
            range_parts = plus.split("-")
            if len(range_parts) == 1:
                if range_parts[0].strip() == max_text:
                    min_plus = max_pos_plus
                    max_plus = max_pos_plus
                else:
                    try:
                        min_plus = int(range_parts[0])
                        max_plus = min_plus
                    except ValueError:
                        color.ColoredText.localize("invalid_upgrade_plus", plus=plus)
                        return None, False
            else:
                try:
                    min_plus = int(range_parts[0])
                    max_plus = int(range_parts[1])
                except ValueError:
                    color.ColoredText.localize(
                        "invalid_upgrade_plus_random",
                        min=range_parts[0],
                        max=range_parts[1],
                    )
                    return None, False

            plus_int = (min_plus + max_plus) // 2

        upgrade = Upgrade(plus_int, base_int)
        upgrade.base_range = (
            max(0, min(min_base or base_int, max_pos_base)),
            max(0, min(max_base or base_int, max_pos_base)),
        )
        upgrade.plus_range = (
            max(0, min(min_plus or plus_int, max_pos_plus)),
            max(0, min(max_plus or plus_int, max_pos_plus)),
        )
        return upgrade, False

    def copy(self) -> Upgrade:
        upgrade = Upgrade(self.plus, self.base)
        upgrade.base_range = self.base_range
        upgrade.plus_range = self.plus_range
        return upgrade


# ============================================================
# FILE: user_rank_rewards.py
# ============================================================
from __future__ import annotations
from bcsfe import core
from bcsfe.cli import dialog_creator, color


class RankGift:
    def __init__(
        self, index: int, threshold: int, rewards: list[tuple[int, int]]
    ):
        self.index = index
        self.threshold = threshold
        self.rewards = rewards

    def get_name(
        self, rank_gift_descriptions: RankGiftDescriptions
    ) -> str | None:
        return rank_gift_descriptions.get_name(self.threshold)


class RankGifts:
    def __init__(self, save_file: core.SaveFile):
        self.save_file = save_file
        self.rank_gift = self.read_rank_gift()

    def read_rank_gift(self) -> list[RankGift] | None:
        rank_gift: list[RankGift] = []
        gdg = core.core_data.get_game_data_getter(self.save_file)
        data = gdg.download("DataLocal", "rankGift.csv")
        if data is None:
            return None
        csv = core.CSV(data)
        for i, line in enumerate(csv):
            rewards: list[tuple[int, int]] = []
            for col in range(1, len(line), 2):
                value = line[col].to_int()
                if value == -1:
                    break
                rewards.append((value, line[col + 1].to_int()))
            rank_gift.append(RankGift(i, line[0].to_int(), rewards))
        return rank_gift

    def get_rank_gift(self, user_rank: int) -> RankGift | None:
        if self.rank_gift is None:
            return None
        for rank_gift in self.rank_gift:
            if rank_gift.threshold == user_rank:
                return rank_gift
        return None

    def get_all_rank_gifts(self, user_rank: int) -> list[RankGift] | None:
        if self.rank_gift is None:
            return None
        return [
            rank_gift
            for rank_gift in self.rank_gift
            if rank_gift.threshold <= user_rank
        ]

    def get_by_id(self, id: int) -> RankGift | None:
        if self.rank_gift is None:
            return None
        if id >= len(self.rank_gift) or id < 0:
            return None
        return self.rank_gift[id]

    def get_all_unlocked(self, user_rank: int) -> list[RankGift] | None:
        if self.rank_gift is None:
            return None

        return [
            rank_gift
            for rank_gift in self.rank_gift
            if rank_gift.threshold <= user_rank
        ]


class RankGiftDescription:
    def __init__(self, index: int, threshold: int, description: str):
        self.index = index
        self.threshold = threshold
        self.description = description


class RankGiftDescriptions:
    def __init__(self, save_file: core.SaveFile):
        self.save_file = save_file
        self.rank_gift_descriptions = self.read_rank_gift_descriptions()

    def read_rank_gift_descriptions(self) -> list[RankGiftDescription] | None:
        rank_gift_descriptions: list[RankGiftDescription] = []
        gdg = core.core_data.get_game_data_getter(self.save_file)
        data = gdg.download("resLocal", "user_info.tsv")
        if data is None:
            return None
        csv = core.CSV(data, delimiter="\t")
        for i, line in enumerate(csv):
            rank_gift_descriptions.append(
                RankGiftDescription(i, line[0].to_int(), line[1].to_str())
            )
        return rank_gift_descriptions

    def get_name(self, user_rank: int) -> str | None:
        if self.rank_gift_descriptions is None:
            return None
        for rank_gift_description in self.rank_gift_descriptions:
            if rank_gift_description.threshold == user_rank:
                return rank_gift_description.description
        return None


class Reward:
    def __init__(self, claimed: bool):
        self.claimed = claimed

    @staticmethod
    def init() -> Reward:
        return Reward(False)

    @staticmethod
    def read(stream: core.Data) -> Reward:
        return Reward(stream.read_bool())

    def write(self, stream: core.Data):
        stream.write_bool(self.claimed)

    def serialize(self) -> bool:
        return self.claimed

    @staticmethod
    def deserialize(data: bool) -> Reward:
        return Reward(data)

    def __repr__(self) -> str:
        return f"Reward(claimed={self.claimed})"

    def __str__(self) -> str:
        return self.__repr__()


class UserRankRewards:
    def __init__(self, rewards: list[Reward]):
        self.rewards = rewards
        self.rank_gifts: RankGifts | None = None

    def read_rank_gifts(self, save_file: core.SaveFile) -> RankGifts:
        if self.rank_gifts is None:
            self.rank_gifts = RankGifts(save_file)
        return self.rank_gifts

    @staticmethod
    def init(gv: core.GameVersion) -> UserRankRewards:
        if gv >= 30:
            total = 0
        else:
            total = 50
        rewards = [Reward.init() for _ in range(total)]
        return UserRankRewards(rewards)

    @staticmethod
    def read(stream: core.Data, gv: core.GameVersion) -> UserRankRewards:
        if gv >= 30:
            total = stream.read_int()
        else:
            total = 50
        rewards: list[Reward] = []
        for _ in range(total):
            rewards.append(Reward.read(stream))
        return UserRankRewards(rewards)

    def write(self, stream: core.Data, gv: core.GameVersion):
        if gv >= 30:
            stream.write_int(len(self.rewards))
        for reward in self.rewards:
            reward.write(stream)

    def serialize(self) -> list[bool]:
        return [reward.serialize() for reward in self.rewards]

    @staticmethod
    def deserialize(data: list[bool]) -> UserRankRewards:
        return UserRankRewards([Reward.deserialize(reward) for reward in data])

    def __repr__(self) -> str:
        return f"Rewards(rewards={self.rewards})"

    def __str__(self) -> str:
        return self.__repr__()

    def set_claimed(self, index: int, claimed: bool):
        self.rewards[index].claimed = claimed

    def edit(self, save_file: core.SaveFile):
        claim_choice = dialog_creator.ChoiceInput.from_reduced(
            ["claim", "unclaim", "fix_claimed"],
            dialog="claim_or_unclaim_ur",
            single_choice=True,
        ).single_choice()

        if claim_choice is None:
            return

        claim_choice -= 1

        rank_gifts = core.core_data.get_rank_gifts(save_file)
        if rank_gifts.rank_gift is None:
            return

        user_rank = save_file.calculate_user_rank()

        if claim_choice == 2:
            for rank_gift in rank_gifts.rank_gift:
                reward = self.rewards[rank_gift.index]
                if rank_gift.threshold > user_rank:
                    reward.claimed = False

            color.ColoredText.localize("ur_fix_claimed_success")
            return

        selected_rank_gifts: list[RankGift] = rank_gifts.rank_gift.copy()
        descriptions = core.core_data.get_rank_gift_descriptions(save_file)

        selected_rank_gifts.sort(key=lambda rank_gift: rank_gift.threshold)

        new_selected_rank_gifts: list[RankGift] = []

        for rank_gift in selected_rank_gifts:
            reward = self.rewards[rank_gift.index]
            if reward.claimed and claim_choice == 0:
                continue
            if not reward.claimed and claim_choice == 1:
                continue
            if rank_gift.threshold > user_rank:
                continue
            new_selected_rank_gifts.append(rank_gift)

        selected_rank_gifts = new_selected_rank_gifts

        selected_descriptions: list[str] = []
        for rank_gift in selected_rank_gifts:
            name = rank_gift.get_name(descriptions)
            if name is None:
                return
            description = name.replace("<br>", " ")
            # remove span tags
            start = description.find("<")
            while start != -1:
                end = description.find(">")
                description = description[:start] + description[end + 1 :]
                start = description.find("<")

            selected_descriptions.append(
                core.core_data.local_manager.get_key(
                    "ur_string",
                    description=description,
                    rank=rank_gift.threshold,
                )
            )

        ids, _ = dialog_creator.ChoiceInput.from_reduced(
            selected_descriptions, dialog="select_ur"
        ).multiple_choice(localized_options=False)
        if ids is None:
            return
        for id in ids:
            index = selected_rank_gifts[id].index
            self.set_claimed(index, claim_choice == 0)

        if claim_choice == 0:
            color.ColoredText.localize("ur_claimed_success")
        else:
            color.ColoredText.localize("ur_unclaimed_success")


def edit_user_rank_rewards(save_file: core.SaveFile):
    user_rank_rewards = save_file.user_rank_rewards
    user_rank_rewards.edit(save_file)

