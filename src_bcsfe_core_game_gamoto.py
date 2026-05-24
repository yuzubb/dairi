# === COMBINED FILE ===
# フォルダ: src_bcsfe_core_game_gamoto
# 元ファイル(6件): __init__.py, base_materials.py, cat_shrine.py, catamins.py, gamatoto.py, ototo.py

# ============================================================
# FILE: __init__.py
# ============================================================
from bcsfe.core.game.gamoto import (
    catamins,
    gamatoto,
    base_materials,
    ototo,
    cat_shrine,
)

__all__ = ["catamins", "gamatoto", "base_materials", "ototo", "cat_shrine"]


# ============================================================
# FILE: base_materials.py
# ============================================================
from __future__ import annotations
from bcsfe import core
from bcsfe.cli import dialog_creator


class Material:
    def __init__(self, amount: int):
        self.amount = amount

    @staticmethod
    def init() -> Material:
        return Material(0)

    @staticmethod
    def read(stream: core.Data) -> Material:
        amount = stream.read_int()
        return Material(amount)

    def write(self, stream: core.Data):
        stream.write_int(self.amount)

    def serialize(self) -> int:
        return self.amount

    @staticmethod
    def deserialize(data: int) -> Material:
        return Material(data)

    def __repr__(self) -> str:
        return f"Material(amount={self.amount!r})"

    def __str__(self) -> str:
        return self.__repr__()


class BaseMaterials:
    def __init__(self, materials: list[Material]):
        self.materials = materials

    @staticmethod
    def init() -> BaseMaterials:
        return BaseMaterials([])

    @staticmethod
    def read(stream: core.Data) -> BaseMaterials:
        total = stream.read_int()
        materials: list[Material] = []
        for _ in range(total):
            materials.append(Material.read(stream))
        return BaseMaterials(materials)

    def write(self, stream: core.Data):
        stream.write_int(len(self.materials))
        for material in self.materials:
            material.write(stream)

    def serialize(self) -> list[int]:
        return [material.serialize() for material in self.materials]

    @staticmethod
    def deserialize(data: list[int]) -> BaseMaterials:
        return BaseMaterials(
            [Material.deserialize(material) for material in data]
        )

    def __repr__(self) -> str:
        return f"Materials(materials={self.materials!r})"

    def __str__(self) -> str:
        return self.__repr__()

    def edit_base_materials(self, save_file: core.SaveFile):
        names = core.core_data.get_gatya_item_names(save_file).names
        items = core.core_data.get_gatya_item_buy(save_file).get_by_category(7)
        if items is None:
            return
        if names is None:
            return
        names = [names[item.id] for item in items]
        base_materials = [
            base_material.amount for base_material in self.materials
        ]
        values = dialog_creator.MultiEditor.from_reduced(
            "base_materials",
            names,
            base_materials,
            core.core_data.max_value_manager.get("base_materials"),
            group_name_localized=True,
        ).edit()
        self.materials = [Material(value) for value in values]


# ============================================================
# FILE: cat_shrine.py
# ============================================================
from __future__ import annotations
from typing import Any
from bcsfe import core
from bcsfe.cli import color, dialog_creator


class CatShrine:
    def __init__(
        self,
        unknown: bool,
        stamp_1: float,
        stamp_2: float,
        shrine_gone: bool,
        flags: list[int],
        xp_offering: int,
    ):
        self.unknown = unknown
        self.stamp_1 = stamp_1
        self.stamp_2 = stamp_2
        self.shrine_gone = shrine_gone
        self.flags = flags
        self.xp_offering = xp_offering
        self.dialogs = 0

    @staticmethod
    def init() -> CatShrine:
        return CatShrine(False, 0.0, 0.0, False, [], 0)

    @staticmethod
    def read(stream: core.Data) -> CatShrine:
        unknown = stream.read_bool()
        stamp_1 = stream.read_double()
        stamp_2 = stream.read_double()
        shrine_gone = stream.read_bool()
        flags = stream.read_byte_list(length=stream.read_byte())
        xp_offering = stream.read_long()
        return CatShrine(unknown, stamp_1, stamp_2, shrine_gone, flags, xp_offering)

    def write(self, stream: core.Data):
        stream.write_bool(self.unknown)
        stream.write_double(self.stamp_1)
        stream.write_double(self.stamp_2)
        stream.write_bool(self.shrine_gone)
        stream.write_byte(len(self.flags))
        stream.write_byte_list(self.flags, write_length=False)
        stream.write_long(self.xp_offering)

    def read_dialogs(self, stream: core.Data):
        self.dialogs = stream.read_int()

    def write_dialogs(self, stream: core.Data):
        stream.write_int(self.dialogs)

    def serialize(self) -> dict[str, Any]:
        return {
            "unknown": self.unknown,
            "stamp_1": self.stamp_1,
            "stamp_2": self.stamp_2,
            "shrine_gone": self.shrine_gone,
            "flags": self.flags,
            "xp_offering": self.xp_offering,
            "dialogs": self.dialogs,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> CatShrine:
        shrine = CatShrine(
            data.get("unknown", False),
            data.get("stamp_1", 0.0),
            data.get("stamp_2", 0.0),
            data.get("shrine_gone", False),
            data.get("flags", []),
            data.get("xp_offering", 0),
        )
        shrine.dialogs = data.get("dialogs", 0)
        return shrine

    def __repr__(self):
        return (
            f"CatShrine("
            f"unknown={self.unknown}, "
            f"stamp_1={self.stamp_1}, "
            f"stamp_2={self.stamp_2}, "
            f"shrine_gone={self.shrine_gone}, "
            f"flags={self.flags}, "
            f"xp_offering={self.xp_offering}, "
            f"dialogs={self.dialogs}"
            f")"
        )

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def edit_catshrine(save_file: core.SaveFile):
        shrine = save_file.cat_shrine
        options = [
            "shrine_level",
            "shrine_xp",
            "make_catshrine_appear",
            "make_catshrine_disappear",
        ]
        choice = dialog_creator.ChoiceInput.from_reduced(
            options, dialog="cat_shrine_choice_dialog", single_choice=True
        ).single_choice()
        if choice is None:
            return
        choice -= 1

        if choice == 2:
            shrine.shrine_gone = False

            shrine.stamp_1 = 0.0
            shrine.stamp_2 = 0.0
            color.ColoredText.localize("cat_shrine_edited")
            return
        elif choice == 3:
            shrine.shrine_gone = True
            color.ColoredText.localize("cat_shrine_edited")
            return

        data = core.core_data.get_cat_shrine_levels(save_file)

        xp = shrine.xp_offering
        level = data.get_level_from_xp(xp)

        color.ColoredText.localize("current_shrine_xp_level", level=level, xp=xp)

        if choice == 0:
            max_level = data.get_max_level()
            if max_level is None:
                return
            level = dialog_creator.IntInput(
                min=1, max=max_level
            ).get_input_locale_while("shrine_level_dialog", {"max_level": max_level})
            if level is None:
                return
            shrine.xp_offering = data.get_xp_from_level(level)
        elif choice == 1:
            max_xp = data.get_max_xp()
            if max_xp is None:
                return
            xp = dialog_creator.IntInput(min=0, max=max_xp).get_input_locale_while(
                "shrine_xp_dialog", {"max_xp": max_xp}
            )
            if xp is None:
                return
            shrine.xp_offering = xp

        xp = shrine.xp_offering
        if xp is None:
            return
        level = data.get_level_from_xp(xp)
        if level is None:
            return

        shrine.dialogs = level - 1
        shrine.shrine_gone = False
        shrine.stamp_1 = 0.0
        shrine.stamp_2 = 0.0

        color.ColoredText.localize("current_shrine_xp_level", level=level, xp=xp)

        color.ColoredText.localize("cat_shrine_edited")


class CatShrineLevels:
    def __init__(self, save_file: core.SaveFile):
        self.save_file = save_file
        self.boundaries = self.get_boundaries()

    def get_boundaries(self) -> list[int] | None:
        file_name = "jinja_level.csv"
        gdg = core.core_data.get_game_data_getter(self.save_file)
        data = gdg.download("resLocal", file_name)
        if data is None:
            return None
        csv = core.CSV(
            data,
            delimiter=core.Delimeter.from_country_code_res(self.save_file.cc),
        )
        boundaries: list[int] = []
        counter = 0
        for row in csv:
            xp = row[0].to_int()
            counter += xp
            boundaries.append(counter)

        return boundaries

    def get_level_from_xp(self, xp: int) -> int | None:
        if self.boundaries is None:
            return None
        for i, boundary in enumerate(self.boundaries):
            if xp < boundary:
                return i + 1
        return len(self.boundaries)

    def get_xp_from_level(self, level: int) -> int | None:
        if self.boundaries is None:
            return None
        if level < 1:
            return 0
        if level > len(self.boundaries):
            return self.get_max_xp()
        return self.boundaries[level - 2]

    def get_max_level(self) -> int | None:
        if self.boundaries is None:
            return None
        return len(self.boundaries)

    def get_max_xp(self) -> int | None:
        if self.boundaries is None:
            return None
        return max(self.boundaries)


# ============================================================
# FILE: catamins.py
# ============================================================
from __future__ import annotations
from bcsfe import core


class Catamin:
    def __init__(self, amount: int):
        self.amount = amount

    @staticmethod
    def read(stream: core.Data) -> Catamin:
        amount = stream.read_int()
        return Catamin(amount)

    def write(self, stream: core.Data):
        stream.write_int(self.amount)

    def serialize(self) -> int:
        return self.amount

    @staticmethod
    def deserialize(data: int) -> Catamin:
        return Catamin(data)

    def __repr__(self):
        return f"Catamin({self.amount})"

    def __str__(self):
        return f"Catamin({self.amount})"


class Catamins:
    def __init__(self, catamins: list[Catamin]):
        self.catamins = catamins

    @staticmethod
    def read(stream: core.Data) -> Catamins:
        total = stream.read_int()
        catamins: list[Catamin] = []
        for _ in range(total):
            catamins.append(Catamin.read(stream))
        return Catamins(catamins)

    def write(self, stream: core.Data):
        stream.write_int(len(self.catamins))
        for catamin in self.catamins:
            catamin.write(stream)

    def serialize(self) -> list[int]:
        return [catamin.serialize() for catamin in self.catamins]

    @staticmethod
    def deserialize(data: list[int]) -> Catamins:
        return Catamins([Catamin.deserialize(catamin) for catamin in data])

    def __repr__(self):
        return f"Catamins({self.catamins})"

    def __str__(self):
        return f"Catamins({self.catamins})"


# ============================================================
# FILE: gamatoto.py
# ============================================================
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from bcsfe import core
from bcsfe.cli import color, dialog_creator


@dataclass
class MemberName:
    member_id: int
    rarity: int
    bonus: int
    name: str
    rarity_name: str
    description: list[str]


class GamatotoMembersName:
    def __init__(self, save_file: core.SaveFile):
        self.save_file = save_file
        self.members = self.read_members()

    def read_members(self) -> list[MemberName] | None:
        members: list[MemberName] = []
        gdg = core.core_data.get_game_data_getter(self.save_file)
        data = gdg.download(
            "resLocal",
            f"GamatotoExpedition_Members_name_{core.core_data.get_lang(self.save_file)}.csv",
        )
        if data is None:
            return None
        csv = core.CSV(
            data,
            delimiter=core.Delimeter.from_country_code_res(self.save_file.cc),
            remove_empty=False,
        )
        for line in csv.lines[1:]:
            if line[0].to_int() == -1:
                continue
            members.append(
                MemberName(
                    line[0].to_int(),
                    line[1].to_int(),
                    line[2].to_int(),
                    line[3].to_str(),
                    line[4].to_str(),
                    line[5:].to_str_list(),
                )
            )
        return members

    def get_member(self, member_id: int) -> MemberName | None:
        if self.members is None:
            return None
        for member in self.members:
            if member.member_id == member_id:
                return member
        return None

    def get_members_from_ids(self, ids: list[int]) -> list[MemberName | None]:
        return [self.get_member(id) for id in ids]

    def get_all_rarity(self, rarity: int) -> list[MemberName] | None:
        if self.members is None:
            return None

        return [member for member in self.members if member.rarity == rarity]

    def get_members_from_helpers(
        self, helpers: Helpers
    ) -> list[MemberName | None]:
        return self.get_members_from_ids(
            [helper.id for helper in helpers.helpers if helper.is_valid()]
        )

    def get_all_rarity_names(self) -> list[str] | None:
        if self.members is None:
            return None
        names: dict[int, str] = {}
        for member in self.members:
            names[member.rarity] = member.rarity_name
        return [names[i] for i in range(len(names))]


@dataclass
class GamatotoLevel:
    level: int
    xp_needed: int
    discovery_bonus: int
    skin: int


@dataclass
class GamatotoLimit:
    max_level: int
    total_stages: int
    total_helpers: int


class GamatotoLevels:
    def __init__(self, save_file: core.SaveFile):
        self.save_file = save_file
        self.levels = self.read_levels()
        self.limit = self.read_max_level()

    def read_levels(self) -> list[GamatotoLevel] | None:
        levels: list[GamatotoLevel] = []
        gdg = core.core_data.get_game_data_getter(self.save_file)
        data = gdg.download("DataLocal", "GamatotoExpedition.csv")
        if data is None:
            return None
        csv = core.CSV(data)
        for i, line in enumerate(csv):
            levels.append(
                GamatotoLevel(
                    i + 1, line[0].to_int(), line[1].to_int(), line[2].to_int()
                )
            )
        return levels

    def read_max_level(self) -> GamatotoLimit | None:
        gdg = core.core_data.get_game_data_getter(self.save_file)
        data = gdg.download("DataLocal", "GamatotoExpedition_Limit.csv")
        if data is None:
            return None
        csv = core.CSV(data)
        line = csv[0]
        return GamatotoLimit(
            line[0].to_int(), line[1].to_int(), line[2].to_int()
        )

    def get_level(self, level: int) -> GamatotoLevel | None:
        if self.levels is None:
            return None
        if level < 1:
            return None
        return self.levels[level - 1]

    def get_all_levels(self) -> list[GamatotoLevel] | None:
        return self.levels

    def get_level_from_xp(self, xp: int) -> GamatotoLevel | None:
        if self.levels is None or self.limit is None:
            return None
        for level in self.levels:
            if level.level >= self.limit.max_level:
                break
            if level.xp_needed == -1:
                continue
            if xp < level.xp_needed:
                return level
        if self.limit.max_level >= len(self.levels):
            return self.levels[-1]
        return self.levels[self.limit.max_level - 1]

    def get_xp_from_level(self, level: int) -> int | None:
        if self.levels is None:
            return None
        level -= 1
        if level < 1:
            return 0
        return self.levels[level - 1].xp_needed

    def get_max_level(self) -> int | None:
        if self.limit is None:
            return None
        return self.limit.max_level

    def get_total_stages(self) -> int | None:
        if self.limit is None:
            return None
        return self.limit.total_stages

    def get_total_helpers(self) -> int | None:
        if self.limit is None:
            return None
        return self.limit.total_helpers


class Helper:
    def __init__(self, id: int):
        self.id = id

    @staticmethod
    def init() -> Helper:
        return Helper(-1)

    @staticmethod
    def read(stream: core.Data) -> Helper:
        id = stream.read_int()
        return Helper(id)

    def write(self, stream: core.Data):
        stream.write_int(self.id)

    def serialize(self) -> int:
        return self.id

    @staticmethod
    def deserialize(data: int) -> Helper:
        return Helper(data)

    def __repr__(self) -> str:
        return f"Helper(id={self.id!r})"

    def __str__(self) -> str:
        return f"Helper(id={self.id!r})"

    def is_valid(self) -> bool:
        return self.id != -1


class Helpers:
    def __init__(self, helpers: list[Helper]):
        self.helpers = helpers

    @staticmethod
    def init() -> Helpers:
        return Helpers([])

    @staticmethod
    def read(stream: core.Data) -> Helpers:
        total = stream.read_int()
        helpers: list[Helper] = []
        for _ in range(total):
            helpers.append(Helper.read(stream))
        return Helpers(helpers)

    def write(self, stream: core.Data):
        stream.write_int(len(self.helpers))
        for helper in self.helpers:
            helper.write(stream)

    def serialize(self) -> list[int]:
        return [helper.serialize() for helper in self.helpers]

    @staticmethod
    def deserialize(data: list[int]) -> Helpers:
        return Helpers([Helper.deserialize(helper) for helper in data])

    def __repr__(self) -> str:
        return f"Helpers(helpers={self.helpers!r})"

    def __str__(self) -> str:
        return f"Helpers(helpers={self.helpers!r})"


class Gamatoto:
    def __init__(
        self,
        remaining_seconds: float,
        return_flag: bool,
        xp: int,
        dest_id: int,
        recon_length: int,
        unknown: int,
        notif_value: int,
    ):
        self.remaining_seconds = remaining_seconds
        self.return_flag = return_flag
        self.xp = xp
        self.dest_id = dest_id
        self.recon_length = recon_length
        self.unknown = unknown
        self.notif_value = notif_value
        self.helpers = Helpers.init()
        self.is_ad_present = False
        self.skin = 0
        self.collab_flags: dict[int, bool] = {}
        self.collab_durations: dict[int, float] = {}

    @staticmethod
    def init() -> Gamatoto:
        return Gamatoto(
            0.0,
            False,
            0,
            0,
            0,
            0,
            0,
        )

    @staticmethod
    def read(stream: core.Data) -> Gamatoto:
        remaining_seconds = stream.read_double()
        return_flag = stream.read_bool()
        xp = stream.read_int()
        dest_id = stream.read_int()
        recon_length = stream.read_int()
        unknown = stream.read_int()
        notif_value = stream.read_int()
        return Gamatoto(
            remaining_seconds,
            return_flag,
            xp,
            dest_id,
            recon_length,
            unknown,
            notif_value,
        )

    def write(self, stream: core.Data):
        stream.write_double(self.remaining_seconds)
        stream.write_bool(self.return_flag)
        stream.write_int(self.xp)
        stream.write_int(self.dest_id)
        stream.write_int(self.recon_length)
        stream.write_int(self.unknown)
        stream.write_int(self.notif_value)

    def read_2(self, stream: core.Data):
        self.helpers = Helpers.read(stream)
        self.is_ad_present = stream.read_bool()

    def write_2(self, stream: core.Data):
        self.helpers.write(stream)
        stream.write_bool(self.is_ad_present)

    def read_skin(self, stream: core.Data):
        self.skin = stream.read_int()

    def write_skin(self, stream: core.Data):
        stream.write_int(self.skin)

    def read_collab_data(self, stream: core.Data):
        self.collab_flags: dict[int, bool] = stream.read_int_bool_dict()
        self.collab_durations: dict[int, float] = stream.read_int_double_dict()

    def write_collab_data(self, stream: core.Data):
        stream.write_int_bool_dict(self.collab_flags)
        stream.write_int_double_dict(self.collab_durations)

    def serialize(self) -> dict[str, Any]:
        return {
            "remaining_seconds": self.remaining_seconds,
            "return_flag": self.return_flag,
            "xp": self.xp,
            "dest_id": self.dest_id,
            "recon_length": self.recon_length,
            "unknown": self.unknown,
            "notif_value": self.notif_value,
            "helpers": self.helpers.serialize(),
            "is_ad_present": self.is_ad_present,
            "skin": self.skin,
            "collab_flags": self.collab_flags,
            "collab_durations": self.collab_durations,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> Gamatoto:
        gamatoto = Gamatoto(
            data.get("remaining_seconds", 0.0),
            data.get("return_flag", False),
            data.get("xp", 0),
            data.get("dest_id", 0),
            data.get("recon_length", 0),
            data.get("unknown", 0),
            data.get("notif_value", 0),
        )
        gamatoto.helpers = Helpers.deserialize(data.get("helpers", []))
        gamatoto.is_ad_present = data.get("is_ad_present", False)
        gamatoto.skin = data.get("skin", 0)
        gamatoto.collab_flags = data.get("collab_flags", {})
        gamatoto.collab_durations = data.get("collab_durations", {})
        return gamatoto

    def __repr__(self):
        return (
            f"Gamatoto(remaining_seconds={self.remaining_seconds!r}, "
            f"return_flag={self.return_flag!r}, xp={self.xp!r}, "
            f"dest_id={self.dest_id!r}, recon_length={self.recon_length!r}, "
            f"unknown={self.unknown!r}, notif_value={self.notif_value!r}, "
            f"helpers={self.helpers!r}, is_ad_present={self.is_ad_present!r}, "
            f"skin={self.skin!r}, collab_flags={self.collab_flags!r}, "
            f"collab_durations={self.collab_durations!r})"
        )

    def __str__(self):
        return self.__repr__()

    def edit_xp(self, save_file: core.SaveFile):
        gamatoto_levels = core.core_data.get_gamatoto_levels(save_file)
        current_level = gamatoto_levels.get_level_from_xp(self.xp)
        if current_level is None:
            return
        xp = self.xp

        color.ColoredText.localize(
            "gamatoto_level_current", level=current_level.level, xp=xp
        )
        choice = dialog_creator.ChoiceInput(
            ["enter_raw_gamatoto_xp", "enter_gamatoto_level"],
            ["enter_raw_gamatoto_xp", "enter_gamatoto_level"],
            [],
            {},
            "edit_gamatoto_level_q",
            single_choice=True,
        ).single_choice()
        if choice is None:
            return
        choice -= 1

        if choice == 0:
            xp = dialog_creator.SingleEditor(
                "gamatoto_xp", self.xp, None, localized_item=True
            ).edit()
            current_level = gamatoto_levels.get_level_from_xp(xp)
        elif choice == 1:
            value = dialog_creator.SingleEditor(
                "gamatoto_level",
                current_level.level,
                gamatoto_levels.get_max_level(),
                localized_item=True,
            ).edit()
            xp = gamatoto_levels.get_xp_from_level(value)
            current_level = gamatoto_levels.get_level(value)

        if xp is None:
            return

        self.xp = xp

        if current_level is None:
            return

        color.ColoredText.localize(
            "gamatoto_level_success", level=current_level.level, xp=xp
        )

    def edit_helpers(self, save_file: core.SaveFile):
        members_name = core.core_data.get_gamatoto_members_name(save_file)

        gamatoto_levels = core.core_data.get_gamatoto_levels(save_file)
        max_helpers = gamatoto_levels.get_total_helpers()

        members = members_name.get_members_from_helpers(self.helpers)
        color.ColoredText.localize("current_gamatoto_helpers")
        for member in members:
            if member is None:
                continue
            color.ColoredText.localize(
                "gamatoto_helper",
                name=member.name,
                rarity_name=member.rarity_name,
            )
        rarity_names = members_name.get_all_rarity_names()
        if rarity_names is None:
            return

        total_rarity_amounts: list[int] = [0] * len(rarity_names)
        for helper in self.helpers.helpers:
            if not helper.is_valid():
                continue
            member = members_name.get_member(helper.id)
            if member is None:
                continue
            total_rarity_amounts[member.rarity] += 1

        rarity_amounts = dialog_creator.MultiEditor.from_reduced(
            "gamatoto_helpers",
            rarity_names,
            total_rarity_amounts,
            max_helpers,
            group_name_localized=True,
            cumulative_max=True,
        ).edit()

        helpers: list[Helper] = []
        for i, rarity_amount in enumerate(rarity_amounts):
            rarity_members = members_name.get_all_rarity(i)
            if rarity_members is None:
                continue
            for _ in range(rarity_amount):
                member = rarity_members.pop(0)
                helpers.append(Helper(member.member_id))
        self.helpers = Helpers(helpers)

        members = members_name.get_members_from_helpers(self.helpers)
        color.ColoredText.localize("new_gamatoto_helpers")
        for member in members:
            if member is None:
                continue
            color.ColoredText.localize(
                "gamatoto_helper",
                name=member.name,
                rarity_name=member.rarity_name,
            )


def edit_xp(save_file: core.SaveFile):
    save_file.gamatoto.edit_xp(save_file)


def edit_helpers(save_file: core.SaveFile):
    save_file.gamatoto.edit_helpers(save_file)


# ============================================================
# FILE: ototo.py
# ============================================================
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from bcsfe import core
from bcsfe.cli import dialog_creator, color


@dataclass
class LevelPartRecipeUnlock:
    index: int
    cannon_id: int
    part_id: int
    unknown: int
    unknown2: int
    level: int


class CastleRecipeUnlock:
    def __init__(self, save_file: core.SaveFile):
        self.save_file = save_file
        self.level_part_recipe_unlocks = self.get_recipe_unlocks()

    def get_recipe_unlocks(self) -> list[LevelPartRecipeUnlock] | None:
        gdg = core.core_data.get_game_data_getter(self.save_file)
        data = gdg.download("DataLocal", "CastleRecipeUnlock.csv")
        if data is None:
            return None
        csv = core.CSV(data)
        level_part_recipe_unlocks: list[LevelPartRecipeUnlock] = []
        for i, line in enumerate(csv):
            level_part_recipe_unlocks.append(
                LevelPartRecipeUnlock(
                    index=i,
                    cannon_id=line[0].to_int(),
                    part_id=line[1].to_int(),
                    unknown=line[2].to_int(),
                    unknown2=line[3].to_int(),
                    level=line[4].to_int(),
                )
            )

        return level_part_recipe_unlocks

    def get_recipe_unlock(self, index: int) -> LevelPartRecipeUnlock | None:
        if self.level_part_recipe_unlocks is None:
            return None
        for recipe_unlock in self.level_part_recipe_unlocks:
            if recipe_unlock.index == index:
                return recipe_unlock

        return None

    def get_max_level(self, cannon_id: int, part_id: int) -> int | None:
        if self.level_part_recipe_unlocks is None:
            return None
        max_level = 0

        for recipe_unlock in self.level_part_recipe_unlocks:
            if (
                recipe_unlock.cannon_id == cannon_id
                and recipe_unlock.part_id == part_id
            ):
                if recipe_unlock.level > max_level:
                    max_level = recipe_unlock.level

        return max_level

    def get_max_part_level(self, part_id: int) -> int | None:
        if self.level_part_recipe_unlocks is None:
            return None
        max_level = 0
        for recipe_unlock in self.level_part_recipe_unlocks:
            if recipe_unlock.part_id == part_id:
                if recipe_unlock.level > max_level:
                    max_level = recipe_unlock.level

        return max_level


@dataclass
class CannonDescription:
    cannon_id: int
    build_name: str
    foundation_build_description: str
    style_build_description: str
    effect_build_description: str
    cannon_build_description: str
    cannon_name: str
    foundation_name: str
    style_name: str
    effect_description: str
    improve_foundation_description: str
    improve_style_description: str
    improved_foundation_name: str
    improved_style_name: str
    improved_effect1_description: str
    improved_effect2_description: str

    def get_part_names(self) -> list[str]:
        effect_name = self.effect_build_description.split("<br>")[0]
        if not effect_name:
            effect_name = self.build_name
        return [
            effect_name,
            self.improve_foundation_description.split("<br>")[0],
            self.improve_style_description.split("<br>")[0],
        ]

    def get_part_name(self, index: int) -> str:
        return self.get_part_names()[index]

    def get_longest_part_name(self) -> str:
        return max(self.get_part_names(), key=len)

    def get_cannon_name(self) -> str:
        return self.cannon_name


class CannonDescriptions:
    def __init__(self, save_file: core.SaveFile):
        self.save_file = save_file
        self.cannon_descriptions = self.get_cannon_descriptions()

    def get_cannon_descriptions(self) -> list[CannonDescription] | None:
        gdg = core.core_data.get_game_data_getter(self.save_file)
        data = gdg.download("resLocal", "CastleRecipeDescriptions.csv")
        if data is None:
            return None
        csv = core.CSV(
            data,
            delimiter=core.Delimeter.from_country_code_res(self.save_file.cc),
            remove_empty=False,
        )
        cannon_descriptions: list[CannonDescription] = []
        for line in csv:
            cannon_descriptions.append(
                CannonDescription(
                    cannon_id=line[0].to_int(),
                    build_name=line[1].to_str(),
                    foundation_build_description=line[2].to_str(),
                    style_build_description=line[3].to_str(),
                    effect_build_description=line[4].to_str(),
                    cannon_build_description=line[5].to_str(),
                    cannon_name=line[6].to_str(),
                    foundation_name=line[7].to_str(),
                    style_name=line[8].to_str(),
                    effect_description=line[9].to_str(),
                    improve_foundation_description=line[10].to_str(),
                    improve_style_description=line[11].to_str(),
                    improved_foundation_name=line[12].to_str(),
                    improved_style_name=line[13].to_str(),
                    improved_effect1_description=line[14].to_str(),
                    improved_effect2_description=line[15].to_str(),
                )
            )

        return cannon_descriptions

    def get_cannon_description(
        self, cannon_id: int
    ) -> CannonDescription | None:
        if self.cannon_descriptions is None:
            return None
        for cannon_description in self.cannon_descriptions:
            if cannon_description.cannon_id == cannon_id:
                return cannon_description

        return None

    def get_longest_longest_part_name(self) -> str | None:
        if self.cannon_descriptions is None:
            return None
        longest_part_name = ""
        for cannon_description in self.cannon_descriptions:
            l_name = cannon_description.get_longest_part_name()
            if len(l_name) > len(longest_part_name):
                longest_part_name = l_name

        return longest_part_name


class Cannon:
    def __init__(self, development: int, levels: list[int]):
        self.development = development
        self.levels = levels

    @staticmethod
    def init() -> Cannon:
        return Cannon(0, [])

    @staticmethod
    def read(stream: core.Data) -> Cannon:
        total = stream.read_int()
        levels: list[int] = []
        development = stream.read_int()
        for _ in range(total - 1):
            levels.append(stream.read_int())
        return Cannon(development, levels)

    def write(self, stream: core.Data):
        stream.write_int(len(self.levels) + 1)
        stream.write_int(self.development)
        for level in self.levels:
            stream.write_int(level)

    def serialize(self) -> list[int]:
        return [self.development] + self.levels

    @staticmethod
    def deserialize(data: list[int]) -> Cannon:
        return Cannon(data[0], data[1:])

    def __repr__(self):
        return f"Cannon({self.development}, {self.levels})"

    def __str__(self):
        return f"Cannon({self.development}, {self.levels})"


class Cannons:
    def __init__(
        self, cannons: dict[int, Cannon], selected_parts: list[list[int]]
    ):
        self.cannons = cannons
        self.selected_parts = selected_parts

    @staticmethod
    def init(gv: core.GameVersion) -> Cannons:
        cannnons = {}
        if gv < 80200:
            selected_parts = [[0, 0, 0]]
        else:
            if gv > 90699:
                total_selected_parts = 0
            else:
                total_selected_parts = 10

            selected_parts = [[0, 0, 0] for _ in range(total_selected_parts)]
        return Cannons(cannnons, selected_parts)

    @staticmethod
    def read(stream: core.Data, gv: core.GameVersion) -> Cannons:
        total = stream.read_int()
        cannons: dict[int, Cannon] = {}
        for _ in range(total):
            cannon_id = stream.read_int()
            cannon = Cannon.read(stream)
            cannons[cannon_id] = cannon
        if gv < 80200:
            selected_parts = [stream.read_int_list(length=3)]
        else:
            if gv > 90699:
                total_selected_parts = stream.read_byte()
            else:
                total_selected_parts = 10

            selected_parts: list[list[int]] = []
            for _ in range(total_selected_parts):
                selected_parts.append(stream.read_byte_list(length=3))

        return Cannons(cannons, selected_parts)

    def write(self, stream: core.Data, gv: core.GameVersion):
        stream.write_int(len(self.cannons))
        for cannon_id, cannon in self.cannons.items():
            stream.write_int(cannon_id)
            cannon.write(stream)
        if gv < 80200:
            stream.write_int_list(
                self.selected_parts[0], write_length=False, length=3
            )
        else:
            if gv > 90699:
                stream.write_byte(len(self.selected_parts))

            for part in self.selected_parts:
                stream.write_byte_list(part, write_length=False, length=3)

    def serialize(self) -> dict[str, Any]:
        return {
            "cannons": {
                cannon_id: cannon.serialize()
                for cannon_id, cannon in self.cannons.items()
            },
            "selected_parts": self.selected_parts,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> Cannons:
        return Cannons(
            {
                cannon_id: Cannon.deserialize(cannon)
                for cannon_id, cannon in data.get("cannons", {}).items()
            },
            data.get("selected_parts", []),
        )

    def __repr__(self):
        return f"Cannons({self.cannons}, {self.selected_parts})"

    def __str__(self):
        return f"Cannons({self.cannons}, {self.selected_parts})"


class Ototo:
    def __init__(
        self,
        base_materials: core.BaseMaterials,
        game_version: core.GameVersion | None = None,
    ):
        self.base_materials = base_materials
        self.remaining_seconds = 0.0
        self.return_flag = False
        self.improve_id = 0
        self.engineers = 0
        self.cannons = Cannons.init(game_version) if game_version else None

    @staticmethod
    def init(game_version: core.GameVersion) -> Ototo:
        return Ototo(core.BaseMaterials.init(), game_version)

    @staticmethod
    def read(stream: core.Data) -> Ototo:
        bm = core.BaseMaterials.read(stream)
        return Ototo(bm)

    def write(self, stream: core.Data):
        self.base_materials.write(stream)

    def read_2(self, stream: core.Data, gv: core.GameVersion):
        self.remaining_seconds = stream.read_double()
        self.return_flag = stream.read_bool()
        self.improve_id = stream.read_int()
        self.engineers = stream.read_int()
        self.cannons = Cannons.read(stream, gv)

    def write_2(self, stream: core.Data, gv: core.GameVersion):
        stream.write_double(self.remaining_seconds)
        stream.write_bool(self.return_flag)
        stream.write_int(self.improve_id)
        stream.write_int(self.engineers)
        if self.cannons is None:
            Cannons.init(gv).write(stream, gv)
        else:
            self.cannons.write(stream, gv)

    def serialize(self) -> dict[str, Any]:
        return {
            "base_materials": self.base_materials.serialize(),
            "remaining_seconds": self.remaining_seconds,
            "return_flag": self.return_flag,
            "improve_id": self.improve_id,
            "engineers": self.engineers,
            "cannons": self.cannons.serialize() if self.cannons else None,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> Ototo:
        ototo = Ototo(
            core.BaseMaterials.deserialize(data.get("base_materials", []))
        )
        ototo.remaining_seconds = data.get("remaining_seconds", 0.0)
        ototo.return_flag = data.get("return_flag", False)
        ototo.improve_id = data.get("improve_id", 0)
        ototo.engineers = data.get("engineers", 0)
        ototo.cannons = Cannons.deserialize(data.get("cannons", {}))
        return ototo

    def __repr__(self):
        return f"Ototo({self.base_materials}, {self.remaining_seconds}, {self.return_flag}, {self.improve_id}, {self.engineers}, {self.cannons})"

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def get_max_engineers(save_file: core.SaveFile) -> int:
        file = core.core_data.get_game_data_getter(save_file).download(
            "DataLocal", "CastleCustomLimit.csv"
        )
        if file is None:
            return 5
        csv = core.CSV(file)
        return csv.lines[0][0].to_int()

    def edit_engineers(self, save_file: core.SaveFile):
        name = core.core_data.get_gatya_item_names(save_file).get_name(92)
        if name is None:
            name = "engineers"
            localized_item = True
        else:
            localized_item = False
        self.engineers = dialog_creator.SingleEditor(
            name,
            self.engineers,
            Ototo.get_max_engineers(save_file),
            localized_item=localized_item,
        ).edit()

    def display_current_cannons(
        self, save_file: core.SaveFile
    ) -> list[str] | None:
        descriptions = CannonDescriptions(save_file)
        recipe_unlocks = CastleRecipeUnlock(save_file)

        color.ColoredText.localize("current_cannon_stats")

        if self.cannons is None:
            self.cannons = Cannons.init(save_file.game_version)

        names: list[str] = []
        longest_part_name = descriptions.get_longest_longest_part_name()
        if longest_part_name is None:
            return None
        longest_part_name = len(longest_part_name)

        for cannon_id, cannon in self.cannons.cannons.items():
            description = descriptions.get_cannon_description(cannon_id)
            if description is None:
                continue
            recipe_unlock = recipe_unlocks.get_recipe_unlock(cannon_id)
            if recipe_unlock is None:
                continue
            cannon_name = description.get_cannon_name()
            names.append(cannon_name)
            text = cannon_name
            if cannon_id != 0:
                cannon_name_length = len(cannon_name) - 10
                buffer = " " * (longest_part_name - cannon_name_length)
                text += core.core_data.local_manager.get_key(
                    "development",
                    development=Ototo.get_stage_name(cannon.development),
                    escape=False,
                    buffer=buffer,
                )

            for part_id, level in enumerate(cannon.levels):
                if part_id == 0:
                    level += 1

                text += "\n"
                text += "        "
                buffer = " " * (
                    longest_part_name
                    - len(description.get_part_name(part_id))
                    + 2
                )
                name = description.get_part_name(part_id)
                text += core.core_data.local_manager.get_key(
                    "cannon_part", name=name, level=level, buffer=buffer
                )

            text += "\n"

            color.ColoredText.localize("cannon_stats", parts=text, escape=False)

        return names

    def edit_cannon(self, save_file: core.SaveFile):
        if self.cannons is None:
            self.cannons = Cannons.init(save_file.game_version)

        names = self.display_current_cannons(save_file)
        if names is None:
            return

        cannon_ids, all_at_once = dialog_creator.ChoiceInput.from_reduced(
            names, dialog="select_cannon"
        ).multiple_choice()
        if cannon_ids is None:
            return

        if len(cannon_ids) > 1 and not all_at_once:
            choice = dialog_creator.ChoiceInput.from_reduced(
                ["individual", "edit_all_at_once"],
                dialog="cannon_edit_type",
                single_choice=True,
            ).single_choice()
            if choice is None:
                return
            choice -= 1
            if choice == 0:
                all_at_once = False
            else:
                all_at_once = True

        if len(cannon_ids) > 1 or (len(cannon_ids) == 1 and cannon_ids[0] != 0):
            choice = dialog_creator.ChoiceInput.from_reduced(
                ["development_o", "level_o"],
                dialog="cannon_dev_level_q",
                single_choice=True,
            ).single_choice()
            if choice is None:
                return
            choice -= 1
        else:
            choice = 1
        if choice == 0:
            self.edit_cannon_development(save_file, all_at_once, cannon_ids)
        elif choice == 1:
            self.edit_cannon_level(save_file, all_at_once, cannon_ids)

        color.ColoredText.localize("cannon_success")

        self.display_current_cannons(save_file)

    def select_development(self) -> int | None:
        return dialog_creator.ChoiceInput.from_reduced(
            ["none", "foundation", "style", "effect"],
            dialog="select_development",
            single_choice=True,
        ).single_choice()

    def edit_cannon_development(
        self, save_file: core.SaveFile, all_at_once: bool, cannon_ids: list[int]
    ):
        if self.cannons is None:
            self.cannons = Cannons.init(save_file.game_version)
        if all_at_once:
            development = self.select_development()
            if development is None:
                return
            for cannon_id in cannon_ids:
                if cannon_id == 0:
                    continue
                self.cannons.cannons[cannon_id].development = development - 1
        else:
            for cannon_id in cannon_ids:
                if cannon_id == 0:
                    continue
                cannon_description = CannonDescriptions(
                    save_file
                ).get_cannon_description(cannon_id)
                if cannon_description is None:
                    continue
                current_development = self.cannons.cannons[
                    cannon_id
                ].development

                color.ColoredText.localize(
                    "selected_cannon_stage",
                    name=cannon_description.get_cannon_name(),
                    stage=Ototo.get_stage_name(current_development),
                    escape=False,
                )
                development = self.select_development()
                if development is None:
                    return
                self.cannons.cannons[cannon_id].development = development - 1

    def edit_cannon_level(
        self, save_file: core.SaveFile, all_at_once: bool, cannon_ids: list[int]
    ):
        if self.cannons is None:
            self.cannons = Cannons.init(save_file.game_version)
        cannon_descriptions = CannonDescriptions(save_file)
        cannon_recipe = CastleRecipeUnlock(save_file)
        if all_at_once:
            max_part_level_0 = cannon_recipe.get_max_part_level(0)
            max_part_level_1 = cannon_recipe.get_max_part_level(1)
            max_part_level_2 = cannon_recipe.get_max_part_level(2)
            if (
                max_part_level_0 is None
                or max_part_level_1 is None
                or max_part_level_2 is None
            ):
                return
            levels = dialog_creator.MultiEditor.from_reduced(
                "cannon_level",
                ["effect", "improved_foundation", "improved_style"],
                None,
                max_values=[
                    max_part_level_0,
                    max_part_level_1,
                    max_part_level_2,
                ],
                group_name_localized=True,
                items_localized=True,
            ).edit()
            if not levels:
                return
            for cannon_id in cannon_ids:
                cannon = self.get_cannon(cannon_id)
                if cannon is None:
                    continue
                cannon.development = max(cannon.development, 3)

                for part_id, level in enumerate(levels):
                    if part_id == 0:
                        level -= 1
                    max_level = cannon_recipe.get_max_level(cannon_id, part_id)
                    if max_level is None:
                        continue
                    if part_id >= len(cannon.levels):
                        break
                    cannon.levels[part_id] = min(level, max_level)
        else:
            for cannon_id in cannon_ids:
                cannon = self.get_cannon(cannon_id)
                if cannon is None:
                    continue
                cannon.development = max(cannon.development, 3)

                cannon_desc = cannon_descriptions.get_cannon_description(
                    cannon_id
                )
                if cannon_desc is None:
                    continue
                levels = cannon.levels
                levels[0] += 1
                names = ["effect", "improved_foundation", "improved_style"]
                if cannon_id == 0:
                    names = ["effect"]
                max_part_level_0 = cannon_recipe.get_max_part_level(0)
                max_part_level_1 = cannon_recipe.get_max_part_level(1)
                max_part_level_2 = cannon_recipe.get_max_part_level(2)
                if (
                    max_part_level_0 is None
                    or max_part_level_1 is None
                    or max_part_level_2 is None
                ):
                    return

                levels = dialog_creator.MultiEditor.from_reduced(
                    cannon_desc.get_cannon_name(),
                    names,
                    levels,
                    max_values=[
                        max_part_level_0,
                        max_part_level_1,
                        max_part_level_2,
                    ],
                    items_localized=True,
                ).edit()
                for part_id, level in enumerate(levels):
                    if part_id == 0:
                        level -= 1
                    cannon.levels[part_id] = level

    def get_cannon(self, cannon_id: int) -> Cannon | None:
        if self.cannons is None:
            return None
        return self.cannons.cannons.get(cannon_id, None)

    @staticmethod
    def get_stage_name(development: int) -> str:
        if development == 0:
            return core.core_data.local_manager.get_key("none")
        if development == 1:
            return core.core_data.local_manager.get_key("foundation")
        if development == 2:
            return core.core_data.local_manager.get_key("style")
        if development == 3:
            return core.core_data.local_manager.get_key("effect")
        return core.core_data.local_manager.get_key(
            "unknown_stage", stage=development
        )


def edit_cannon(save_file: core.SaveFile):
    save_file.ototo.edit_cannon(save_file)

