# === COMBINED FILE ===
# フォルダ: src_bcsfe_core_game_battle
# 元ファイル(5件): __init__.py, battle_items.py, cleared_slots.py, enemy.py, slots.py

# ============================================================
# FILE: __init__.py
# ============================================================
from bcsfe.core.game.battle import slots, battle_items, cleared_slots

__all__ = ["slots", "battle_items", "cleared_slots"]


# ============================================================
# FILE: battle_items.py
# ============================================================
from __future__ import annotations

import datetime
from math import inf, isnan
import math
from typing import Any
from bcsfe import core
from bcsfe.cli import dialog_creator, color


class EndlessItem:
    def __init__(
        self, active: bool, unknown: bool, amount: int, start: float, end: float
    ):
        self.active = active
        self.unknown = unknown
        self.amount = amount
        self.start = start
        self.end = end

    @staticmethod
    def init() -> EndlessItem:
        return EndlessItem(False, False, 0, 0, 0)

    @staticmethod
    def read(stream: core.Data) -> EndlessItem:
        return EndlessItem(
            stream.read_bool(),
            stream.read_bool(),
            stream.read_byte(),
            stream.read_double(),
            stream.read_double(),
        )

    def write(self, stream: core.Data):
        stream.write_bool(self.active)
        stream.write_bool(self.unknown)
        stream.write_byte(self.amount)
        stream.write_double(self.start)
        stream.write_double(self.end)

    def serialize(self) -> dict[str, Any]:
        return {
            "active": self.active,
            "unknown": self.unknown,
            "amount": self.amount,
            "start": self.start,
            "end": self.end,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> EndlessItem:
        return EndlessItem(
            data.get("active", False),
            data.get("unknown", False),
            data.get("amount", 0),
            data.get("start", 0.0),
            data.get("end", 0.0),
        )

    def get_endless_duration(self) -> datetime.timedelta | None:
        if not self.active:
            return datetime.timedelta()

        if self.end == inf:
            return None
        if math.isnan(self.end) or math.isnan(self.start):
            return None

        return datetime.timedelta(
            seconds=self.end - self.start + (self.amount * 3 * 60 * 60)
        )

    def get_endless_duration_formatted(self) -> str:
        duration = self.get_endless_duration()

        if duration is None:
            return core.localize("infinity_duration")

        days = duration.days
        hours, rem = divmod(duration.seconds, 3600)
        minutes, seconds = divmod(rem, 60)

        return core.localize(
            "duration", days=days, hours=hours, minutes=minutes, seconds=seconds
        )

    def set_duration_mins(self, mins: float, amount: int):
        self.active = True
        self.unknown = True
        self.amount = amount
        self.start = datetime.datetime.now(datetime.timezone.utc).timestamp()
        self.end = self.start + mins * 60


class BattleItem:
    def __init__(self, amount: int):
        self.amount = amount
        self.locked = False

        self.endless_item = EndlessItem.init()

    @staticmethod
    def init() -> BattleItem:
        return BattleItem(0)

    @staticmethod
    def read_amount(stream: core.Data) -> BattleItem:
        return BattleItem(stream.read_int())

    def write_amount(self, stream: core.Data):
        stream.write_int(self.amount)

    def read_locked(self, stream: core.Data):
        self.locked = stream.read_bool()

    def write_locked(self, stream: core.Data):
        stream.write_bool(self.locked)

    def read_endless_items(self, stream: core.Data):
        self.endless_item = EndlessItem.read(stream)

    def write_endless_items(self, stream: core.Data):
        self.endless_item.write(stream)

    def serialize(self) -> dict[str, Any]:
        return {
            "amount": self.amount,
            "locked": self.locked,
            "endless": self.endless_item.serialize(),
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> BattleItem:
        battle_item = BattleItem(data.get("amount", 0))
        battle_item.locked = data.get("locked", False)
        battle_item.endless_item = EndlessItem.deserialize(data.get("endless", {}))
        return battle_item

    def __repr__(self):
        try:
            return f"BattleItem({self.amount}, {self.locked}, {self.endless_item})"
        except AttributeError:
            return f"BattleItem({self.amount}, {self.endless_item})"

    def __str__(self):
        return self.__repr__()


class BattleItems:
    def __init__(self, items: list[BattleItem]):
        self.items = items
        self.lock_item = False

    @staticmethod
    def init() -> BattleItems:
        return BattleItems([BattleItem.init() for _ in range(6)])

    @staticmethod
    def read_items(stream: core.Data) -> BattleItems:
        total_items = 6
        items = [BattleItem.read_amount(stream) for _ in range(total_items)]
        return BattleItems(items)

    def write_items(self, stream: core.Data):
        for item in self.items:
            item.write_amount(stream)

    def read_locked_items(self, stream: core.Data):
        self.lock_item = stream.read_bool()
        for item in self.items:
            item.read_locked(stream)

    def write_locked_items(self, stream: core.Data):
        stream.write_bool(self.lock_item)
        for item in self.items:
            item.write_locked(stream)

    def read_endless_items(self, stream: core.Data):
        for i in range(6):
            if i >= len(self.items):
                _ = EndlessItem.read(stream)  # ensure we still read 6 items
            else:
                item = self.items[i]
                item.read_endless_items(stream)

    def write_endless_items(self, stream: core.Data):
        for i in range(6):
            if i >= len(self.items):
                EndlessItem.init().write(stream)  # ensure we still write 6 items
            else:
                item = self.items[i]
                item.write_endless_items(stream)

    def serialize(self) -> dict[str, Any]:
        return {
            "items": [item.serialize() for item in self.items],
            "lock_item": self.lock_item,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> BattleItems:
        battle_items = BattleItems(
            [BattleItem.deserialize(item) for item in data.get("items", [])]
        )
        battle_items.lock_item = data.get("lock_item", False)
        return battle_items

    def __repr__(self):
        return f"BattleItems({self.items})"

    def __str__(self):
        return f"BattleItems({self.items})"

    def get_names(self, save_file: core.SaveFile) -> list[str] | None:
        names = core.core_data.get_gatya_item_names(save_file).names
        if names is None:
            return None
        items = core.core_data.get_gatya_item_buy(save_file).get_by_category(3)
        if items is None:
            return None

        names = [names[item.id] for item in items]
        return names

    def edit(self, save_file: core.SaveFile):
        group_name = save_file.get_localizable().get("shop_category1")
        if group_name is None:
            group_name = core.core_data.local_manager.get_key("battle_items")
        item_names = self.get_names(save_file)
        if item_names is None:
            return
        current_values = [item.amount for item in self.items]
        values = dialog_creator.MultiEditor.from_reduced(
            group_name,
            item_names,
            current_values,
            core.core_data.max_value_manager.get("battle_items"),
        ).edit()
        for i, value in enumerate(values):
            self.items[i].amount = value

    def edit_endless_items(self, save_file: core.SaveFile):
        item_names = self.get_names(save_file)
        if item_names is None:
            return

        current_values = [
            item.endless_item.get_endless_duration_formatted() for item in self.items
        ]

        (options, all_at_once) = dialog_creator.ChoiceInput.from_reduced(
            [core.localize("endless_item_item", item=item) for item in item_names],
            current_values,
            localize_options=False,
            dialog="select_option",
        ).multiple_choice(False)

        if options is None:
            return

        infinity_str = core.localize("infinity")

        if all_at_once:
            val = dialog_creator.StringInput().get_input_locale_while(
                "enter_duration_minutes", {}
            )
            if val is None:
                return

            if val.lower() == infinity_str.lower():
                val = inf
            else:
                try:
                    val = float(val)
                except ValueError:
                    return

            for item in self.items:
                item.endless_item.set_duration_mins(val, 0)
        else:
            for opt in options:
                val = dialog_creator.StringInput().get_input_locale_while(
                    "enter_duration_minutes_item", {"item": item_names[opt]}
                )
                if val is None:
                    return

                if val.lower() == infinity_str.lower():
                    val = inf
                else:
                    try:
                        val = float(val)
                    except ValueError:
                        color.ColoredText.localize("invalid_minute_count")
                        continue

                self.items[opt].endless_item.set_duration_mins(val, 0)

        color.ColoredText.localize("endless_items_success")


# ============================================================
# FILE: cleared_slots.py
# ============================================================
from __future__ import annotations
from bcsfe import core
from typing import Any


class CatSlot:
    def __init__(self, cat_id: int, form: int):
        self.cat_id = cat_id
        self.form = form

    @staticmethod
    def init() -> CatSlot:
        return CatSlot(0, 0)

    @staticmethod
    def read(stream: core.Data) -> CatSlot:
        cat_id = stream.read_short()
        form = stream.read_byte()
        return CatSlot(cat_id, form)

    def write(self, stream: core.Data):
        stream.write_short(self.cat_id)
        stream.write_byte(self.form)

    def serialize(self) -> dict[str, Any]:
        return {
            "cat_id": self.cat_id,
            "form": self.form,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> CatSlot:
        return CatSlot(data.get("cat_id", 0), data.get("form", 0))

    def __repr__(self):
        return f"CatSlot({self.cat_id}, {self.form})"

    def __str__(self):
        return self.__repr__()


class LineupCat:
    def __init__(
        self,
        index: int,
        cats: list[CatSlot],
        u1: int,
        u2: int,
        u3: int,
    ):
        self.index = index
        self.cats = cats
        self.u1 = u1
        self.u2 = u2
        self.u3 = u3

    @staticmethod
    def init() -> LineupCat:
        cats = [CatSlot.init() for _ in range(10)]
        return LineupCat(0, cats, 0, 0, 0)

    @staticmethod
    def read(stream: core.Data) -> LineupCat:
        index = stream.read_short()
        length = 10

        cats = [CatSlot.read(stream) for _ in range(length)]
        u1 = stream.read_byte()
        u2 = stream.read_byte()
        u3 = stream.read_byte()
        return LineupCat(index, cats, u1, u2, u3)

    def write(self, stream: core.Data):
        stream.write_short(self.index)
        for cat in self.cats:
            cat.write(stream)
        stream.write_byte(self.u1)
        stream.write_byte(self.u2)
        stream.write_byte(self.u3)

    def serialize(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "cats": [cat.serialize() for cat in self.cats],
            "u1": self.u1,
            "u2": self.u2,
            "u3": self.u3,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> LineupCat:
        return LineupCat(
            data.get("index", 0),
            [CatSlot.deserialize(cat) for cat in data.get("cats", [])],
            data.get("u1", 0),
            data.get("u2", 0),
            data.get("u3", 0),
        )

    def __repr__(self):
        return f"LineupCat({self.index}, {self.cats}, {self.u1}, {self.u2}, {self.u3})"

    def __str__(self):
        return self.__repr__()


class ClearedSlotsCat:
    def __init__(self, lineups: list[LineupCat]):
        self.lineups = lineups

    @staticmethod
    def init() -> ClearedSlotsCat:
        return ClearedSlotsCat([])

    @staticmethod
    def read(stream: core.Data) -> ClearedSlotsCat:
        total = stream.read_short()
        lineups = [LineupCat.read(stream) for _ in range(total)]
        return ClearedSlotsCat(lineups)

    def write(self, stream: core.Data):
        stream.write_short(len(self.lineups))
        for lineup in self.lineups:
            lineup.write(stream)

    def serialize(self) -> list[dict[str, Any]]:
        return [lineup.serialize() for lineup in self.lineups]

    @staticmethod
    def deserialize(data: list[dict[str, Any]]) -> ClearedSlotsCat:
        return ClearedSlotsCat(
            [LineupCat.deserialize(lineup) for lineup in data],
        )

    def __repr__(self):
        return f"ClearedSlotsCat({self.lineups})"

    def __str__(self):
        return self.__repr__()


class StageSlot:
    def __init__(self, stage_id: int):
        self.stage_id = stage_id

    @staticmethod
    def init() -> StageSlot:
        return StageSlot(0)

    @staticmethod
    def read(stream: core.Data) -> StageSlot:
        stage_id = stream.read_int()
        return StageSlot(stage_id)

    def write(self, stream: core.Data):
        stream.write_int(self.stage_id)

    def serialize(self) -> int:
        return self.stage_id

    @staticmethod
    def deserialize(data: int) -> StageSlot:
        return StageSlot(data)

    def __repr__(self):
        return f"StageSlot({self.stage_id})"

    def __str__(self):
        return self.__repr__()


class StageLineups:
    def __init__(self, index: int, slots: list[StageSlot]):
        self.index = index
        self.slots = slots

    @staticmethod
    def init() -> StageLineups:
        return StageLineups(0, [])

    @staticmethod
    def read(stream: core.Data) -> StageLineups:
        index = stream.read_short()
        total = stream.read_short()
        slots = [StageSlot.read(stream) for _ in range(total)]
        return StageLineups(index, slots)

    def write(self, stream: core.Data):
        stream.write_short(self.index)
        stream.write_short(len(self.slots))
        for slot in self.slots:
            slot.write(stream)

    def serialize(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "slots": [slot.serialize() for slot in self.slots],
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> StageLineups:
        return StageLineups(
            data.get("index", 0),
            [StageSlot.deserialize(slot) for slot in data.get("slots", [])],
        )

    def __repr__(self):
        return f"StageLineups({self.index}, {self.slots})"

    def __str__(self):
        return self.__repr__()


class ClearedStageSlots:
    def __init__(self, lineups: list[StageLineups]):
        self.lineups = lineups

    @staticmethod
    def init() -> ClearedStageSlots:
        return ClearedStageSlots([])

    @staticmethod
    def read(stream: core.Data) -> ClearedStageSlots:
        total = stream.read_short()
        lineups = [StageLineups.read(stream) for _ in range(total)]
        return ClearedStageSlots(lineups)

    def write(self, stream: core.Data):
        stream.write_short(len(self.lineups))
        for lineup in self.lineups:
            lineup.write(stream)

    def serialize(self) -> dict[str, Any]:
        return {
            "lineups": [lineup.serialize() for lineup in self.lineups],
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> ClearedStageSlots:
        return ClearedStageSlots(
            [
                StageLineups.deserialize(lineup)
                for lineup in data.get("lineups", [])
            ],
        )

    def __repr__(self):
        return f"ClearedStageSlots({self.lineups})"

    def __str__(self):
        return self.__repr__()


class ClearedSlots:
    def __init__(
        self,
        cleared_slots: ClearedSlotsCat,
        cleared_stage_slots: ClearedStageSlots,
        unknown: dict[int, bool],
    ):
        self.cleared_slots = cleared_slots
        self.cleared_stage_slots = cleared_stage_slots
        self.unknown = unknown

    @staticmethod
    def init() -> ClearedSlots:
        return ClearedSlots(
            ClearedSlotsCat.init(),
            ClearedStageSlots.init(),
            {},
        )

    @staticmethod
    def read(stream: core.Data) -> ClearedSlots:
        cleared_slots = ClearedSlotsCat.read(stream)
        cleared_stage_slots = ClearedStageSlots.read(stream)
        length = stream.read_short()
        unknown = stream.read_short_bool_dict(length)
        return ClearedSlots(cleared_slots, cleared_stage_slots, unknown)

    def write(self, stream: core.Data):
        self.cleared_slots.write(stream)
        self.cleared_stage_slots.write(stream)
        stream.write_short(len(self.unknown))
        stream.write_short_bool_dict(self.unknown, write_length=False)

    def serialize(self) -> dict[str, Any]:
        return {
            "cleared_slots": self.cleared_slots.serialize(),
            "cleared_stage_slots": self.cleared_stage_slots.serialize(),
            "unknown": self.unknown,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> ClearedSlots:
        return ClearedSlots(
            ClearedSlotsCat.deserialize(data.get("cleared_slots", [])),
            ClearedStageSlots.deserialize(data.get("cleared_stage_slots", {})),
            data.get("unknown", {}),
        )

    def __repr__(self):
        return f"ClearedSlots({self.cleared_slots}, {self.cleared_stage_slots}, {self.unknown})"

    def __str__(self):
        return self.__repr__()


# ============================================================
# FILE: enemy.py
# ============================================================
from __future__ import annotations
from bcsfe import core


class Enemy:
    def __init__(self, id: int):
        self.id = id

    def unlock_enemy_guide(self, save_file: core.SaveFile):
        save_file.enemy_guide[self.id] = 1

    def reset_enemy_guide(self, save_file: core.SaveFile):
        save_file.enemy_guide[self.id] = 0

    def get_name(self, save_file: core.SaveFile) -> str | None:
        return core.core_data.get_enemy_names(save_file).get_name(self.id)


class EnemyDictionaryItem:
    def __init__(self, enemy_id: int, scale: int, first_seen: int | None):
        self.enemy_id = enemy_id
        self.scale = scale
        self.first_seen = first_seen


class EnemyDictionary:
    def __init__(self, save_file: core.SaveFile):
        self.save_file = save_file
        self.dictionary = self.__get_dictionary()

    def __get_dictionary(self) -> list[EnemyDictionaryItem] | None:
        gdg = core.core_data.get_game_data_getter(self.save_file)
        csv_data = gdg.download("DataLocal", "enemy_dictionary_list.csv")
        if csv_data is None:
            return None

        csv = core.CSV(csv_data)
        data: list[EnemyDictionaryItem] = []

        for row in csv:
            first_seen = None
            if len(row) >= 3:
                first_seen = row[2].to_int()
            data.append(
                EnemyDictionaryItem(row[0].to_int(), row[1].to_int(), first_seen)
            )

        return data

    def get_valid_enemies(self) -> list[int] | None:
        if self.dictionary is None:
            return None

        return [enemy.enemy_id for enemy in self.dictionary]

    def get_invalid_enemies(self, total_enemies: int) -> list[int] | None:
        valid_enemies = self.get_valid_enemies()
        if valid_enemies is None:
            return None

        valid_enemies = set(valid_enemies)

        return list(filter(lambda i: i not in valid_enemies, range(total_enemies)))


class EnemyDescription:
    def __init__(self, trait_str: str, description: list[str] | None):
        self.trait_str = trait_str
        self.description = description


class EnemyDescriptions:
    def __init__(self, save_file: core.SaveFile):
        self.save_file = save_file
        self.descriptions = self.__get_descriptions()

    def __get_descriptions(self) -> list[EnemyDescription] | None:
        gdg = core.core_data.get_game_data_getter(self.save_file)
        data = gdg.download(
            "resLocal",
            f"EnemyPictureBook_{core.core_data.get_lang(self.save_file)}.csv",
        )
        if data is None:
            return None

        csv = core.CSV(data, core.Delimeter.from_country_code_res(self.save_file.cc))
        descriptions: list[EnemyDescription] = []

        for i, row in enumerate(csv):
            if len(row) == 1:
                descriptions.append(EnemyDescription(row[0].to_str(), None))
            else:
                descriptions.append(
                    EnemyDescription(row[0].to_str(), row[1:].to_str_list())
                )

        return descriptions


class EnemyNames:
    def __init__(self, save_file: core.SaveFile):
        self.save_file = save_file
        self.names = self.get_names()

    def get_names(self) -> list[str] | None:
        gdg = core.core_data.get_game_data_getter(self.save_file)
        data = gdg.download("resLocal", "Enemyname.tsv")
        if data is None:
            return None
        csv = core.CSV(
            data,
            "\t",
            remove_empty=False,
        )
        names: list[str] = []
        for row in csv:
            names.append(row[0].to_str())

        return names

    def get_name(self, id: int) -> str | None:
        if self.names is None:
            return None
        try:
            name = self.names[id]
            if not name:
                return core.core_data.local_manager.get_key(
                    "enemy_not_in_name_list", id=id
                )
        except IndexError:
            return core.core_data.local_manager.get_key("enemy_unknown_name", id=id)
        return name


# ============================================================
# FILE: slots.py
# ============================================================
from __future__ import annotations
from typing import Any
from bcsfe import core
from bcsfe.cli import dialog_creator


class EquipSlot:
    def __init__(self, cat_id: int):
        self.cat_id = cat_id

    @staticmethod
    def read(stream: core.Data) -> EquipSlot:
        return EquipSlot(stream.read_int())

    def write(self, stream: core.Data):
        stream.write_int(self.cat_id)

    def serialize(self) -> int:
        return self.cat_id

    @staticmethod
    def deserialize(data: int) -> EquipSlot:
        return EquipSlot(data)

    def __repr__(self):
        return f"EquipSlot({self.cat_id})"

    def __str__(self):
        return f"EquipSlot({self.cat_id})"


class EquipSlots:
    def __init__(self, slots: list[EquipSlot]):
        self.slots = slots
        self.name = ""

    @staticmethod
    def read(stream: core.Data) -> EquipSlots:
        length = 10
        slots = [EquipSlot.read(stream) for _ in range(length)]
        return EquipSlots(slots)

    @staticmethod
    def init() -> EquipSlots:
        length = 10
        slots = [EquipSlot(-1) for _ in range(length)]
        return EquipSlots(slots)

    def write(self, stream: core.Data):
        for slot in self.slots:
            slot.write(stream)

    def read_name(self, stream: core.Data):
        length = stream.read_int()
        try:
            self.name = stream.read_string(length)
        except UnicodeDecodeError:
            stream.pos -= length
            self.name = stream.read_utf8_string_by_char_length(length)

    def write_name(self, stream: core.Data):
        stream.write_string(self.name)

    def serialize(self) -> dict[str, Any]:
        return {
            "slots": [slot.serialize() for slot in self.slots],
            "name": self.name,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> EquipSlots:
        slots = EquipSlots(
            [EquipSlot.deserialize(slot) for slot in data.get("slots", [])]
        )
        slots.name = data.get("name")
        return slots

    def __repr__(self):
        return f"EquipSlots({self.slots}, {self.name})"

    def __str__(self):
        return self.__repr__()


class LineUps:
    def __init__(self, slots: list[EquipSlots], total_slots: int = 15):
        self.slots = slots
        self.selected_slot = 0
        self.unlocked_slots = 0
        self.slot_names_length = total_slots

    @staticmethod
    def init(gv: core.GameVersion) -> LineUps:
        if gv < 90700:
            length = 10
        else:
            length = 15
        slots = [EquipSlots.init() for _ in range(length)]
        return LineUps(slots, length)

    @staticmethod
    def read(stream: core.Data, gv: core.GameVersion) -> LineUps:
        if gv < 90700:
            length = 10
        else:
            length = stream.read_byte()
        slots = [EquipSlots.read(stream) for _ in range(length)]
        return LineUps(slots)

    def write(self, stream: core.Data, gv: core.GameVersion):
        if gv >= 90700:
            stream.write_byte(len(self.slots))
            length = len(self.slots)
        else:
            length = 10
        if length > len(self.slots):
            self.slots += [EquipSlots.init() for _ in range(length)]
        else:
            self.slots = self.slots[:length]
        for slot in self.slots:
            slot.write(stream)

    def read_2(self, stream: core.Data, gv: core.GameVersion):
        self.selected_slot = stream.read_int()
        if gv < 90700:
            unlocked_slots_l = stream.read_bool_list(10)
            unlocked_slots = sum(unlocked_slots_l)
        else:
            unlocked_slots = stream.read_byte()
        self.unlocked_slots = unlocked_slots

    def write_2(self, stream: core.Data, gv: core.GameVersion):
        stream.write_int(self.selected_slot)
        if gv < 90700:
            unlocked_slots_l = [False] * 10
            unlocked_slots = min(self.unlocked_slots, 10)
            for i in range(unlocked_slots):
                unlocked_slots_l[i] = True
            stream.write_bool_list(unlocked_slots_l, write_length=False)
        else:
            stream.write_byte(self.unlocked_slots)

    def read_slot_names(self, stream: core.Data, gv: core.GameVersion):
        if gv >= 110600:
            total_slots = stream.read_byte()
        else:
            total_slots = 15
        for i in range(total_slots):
            try:
                self.slots[i].read_name(stream)
            except IndexError:
                slot = EquipSlots.init()
                slot.read_name(stream)
                self.slots.append(slot)

        self.slot_names_length = total_slots

    def write_slot_names(self, stream: core.Data, gv: core.GameVersion):
        if gv >= 110600:
            stream.write_byte(self.slot_names_length)
        for i in range(self.slot_names_length):
            try:
                self.slots[i].write_name(stream)
            except IndexError:
                slot = EquipSlots.init()
                slot.write_name(stream)
                self.slots.append(slot)

    def serialize(self) -> dict[str, Any]:
        return {
            "slots": [slot.serialize() for slot in self.slots],
            "selected_slot": self.selected_slot,
            "unlocked_slots": self.unlocked_slots,
            "slot_names_length": self.slot_names_length,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> LineUps:
        line_ups = LineUps(
            [EquipSlots.deserialize(slot) for slot in data.get("slots", [])]
        )
        line_ups.selected_slot = data.get("selected_slot", 0)
        line_ups.unlocked_slots = data.get("unlocked_slots", 0)
        line_ups.slot_names_length = data.get("slot_names_length", 0)
        return line_ups

    def __repr__(self):
        return f"LineUps({self.slots}, {self.selected_slot}, {self.unlocked_slots})"

    def __str__(self):
        return self.__repr__()

    def edit_unlocked_slots(self):
        self.unlocked_slots = dialog_creator.SingleEditor(
            "unlocked_slots",
            self.unlocked_slots,
            self.slot_names_length,
            localized_item=True,
            remove_alias=True,
        ).edit()

