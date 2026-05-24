# === COMBINED FILE ===
# フォルダ: src_bcsfe_cli_edits
# 元ファイル(12件): __init__.py, aku_realm.py, basic_items.py, cat_editor.py, clear_tutorial.py, enemy_editor.py, event_tickets.py, fixes.py, map.py, max_all.py, rare_ticket_trade.py, storage.py

# ============================================================
# FILE: __init__.py
# ============================================================
from bcsfe.cli.edits import (
    basic_items,
    cat_editor,
    clear_tutorial,
    rare_ticket_trade,
    fixes,
    enemy_editor,
    aku_realm,
    map,
    event_tickets,
    max_all,
    storage,
)

__all__ = [
    "basic_items",
    "cat_editor",
    "clear_tutorial",
    "rare_ticket_trade",
    "fixes",
    "enemy_editor",
    "aku_realm",
    "map",
    "event_tickets",
    "max_all",
    "storage",
]


# ============================================================
# FILE: aku_realm.py
# ============================================================
from __future__ import annotations
from bcsfe import core
from bcsfe.cli import color


def unlock_aku_realm(save_file: core.SaveFile):
    stage_ids = [255, 256, 257, 258, 265, 266, 268]
    for stage_id in stage_ids:
        save_file.event_stages.clear_map(1, stage_id, 0, False)

    color.ColoredText.localize("aku_realm_unlocked")


# ============================================================
# FILE: basic_items.py
# ============================================================
from __future__ import annotations
import random
from bcsfe import core
from bcsfe.cli import dialog_creator, color, edits
from bcsfe.core.game.catbase.gatya_item import GatyaItemCategory


class BasicItems:
    @staticmethod
    def get_name(name: str | None, key: str) -> str:
        if name is None:
            return core.core_data.local_manager.get_key(key)
        return name.strip()

    @staticmethod
    def reset_golden_cat_cpus(save_file: core.SaveFile):
        save_file.golden_cpu_count = 0

        color.ColoredText.localize("reset_golden_cat_cpus_success")

    @staticmethod
    def edit_catfood(save_file: core.SaveFile):
        should_exit = not dialog_creator.YesNoInput().get_input_once("catfood_warning")
        if should_exit:
            return

        name = core.core_data.get_gatya_item_names(save_file).get_name(22)
        original_amount = save_file.catfood
        save_file.catfood = dialog_creator.SingleEditor(
            BasicItems.get_name(name, "catfood"),
            save_file.catfood,
            core.core_data.max_value_manager.get("catfood"),
        ).edit()
        change = save_file.catfood - original_amount
        core.BackupMetaData(save_file).add_managed_item(
            core.ManagedItem.from_change(change, core.ManagedItemType.CATFOOD)
        )

    @staticmethod
    def edit_xp(save_file: core.SaveFile):
        name = core.core_data.get_gatya_item_names(save_file).get_name(6)
        save_file.xp = dialog_creator.SingleEditor(
            BasicItems.get_name(name, "xp"),
            save_file.xp,
            core.core_data.max_value_manager.get("xp"),
        ).edit()

    @staticmethod
    def edit_normal_tickets(save_file: core.SaveFile):
        name = core.core_data.get_gatya_item_names(save_file).get_name(20)
        save_file.normal_tickets = dialog_creator.SingleEditor(
            BasicItems.get_name(name, "normal_tickets"),
            save_file.normal_tickets,
            core.core_data.max_value_manager.get("normal_tickets"),
        ).edit()

    @staticmethod
    def edit_100_million_ticket(save_file: core.SaveFile):
        color.ColoredText.localize("100_million_warn")
        name = core.core_data.get_gatya_item_names(save_file).get_name(212)
        save_file.hundred_million_ticket = dialog_creator.SingleEditor(
            BasicItems.get_name(name, "100_million_tickets"),
            save_file.hundred_million_ticket,
            core.core_data.max_value_manager.get("100_million_tickets"),
        ).edit()

    @staticmethod
    def get_bannable_feature_options(feature_name: str, safe_feature_name: str) -> int:
        feature_name = core.core_data.local_manager.get_key(feature_name)
        safe_feature_name = core.core_data.local_manager.get_key(safe_feature_name)

        options = [
            core.core_data.local_manager.get_key(
                "continue_editing", feature_name=feature_name
            ),
            core.core_data.local_manager.get_key(
                "go_to_safe_feature", safer_feature_name=safe_feature_name
            ),
            core.core_data.local_manager.get_key(
                "cancel_editing", feature_name=feature_name
            ),
        ]
        option = dialog_creator.ChoiceInput(
            options,
            options,
            [],
            {"feature_name": feature_name},
            "select_an_option_to_continue",
        ).single_choice()
        if option is None:
            return 2
        option -= 1
        return option

    @staticmethod
    def edit_rare_tickets(save_file: core.SaveFile):
        color.ColoredText.localize("rare_ticket_warning")
        name = core.core_data.get_gatya_item_names(save_file).get_name(21)
        option = BasicItems.get_bannable_feature_options(
            "rare_tickets_l", "rare_ticket_trade_l"
        )
        if option == 2:
            return
        if option == 1:
            return edits.rare_ticket_trade.RareTicketTrade.rare_ticket_trade(save_file)

        original_amount = save_file.rare_tickets
        save_file.rare_tickets = dialog_creator.SingleEditor(
            BasicItems.get_name(name, "rare_tickets"),
            save_file.rare_tickets,
            core.core_data.max_value_manager.get("rare_tickets"),
        ).edit()
        change = save_file.rare_tickets - original_amount
        core.BackupMetaData(save_file).add_managed_item(
            core.ManagedItem.from_change(change, core.ManagedItemType.RARE_TICKET)
        )

    @staticmethod
    def edit_platinum_tickets(save_file: core.SaveFile):
        color.ColoredText.localize("platinum_ticket_warning")
        name = core.core_data.get_gatya_item_names(save_file).get_name(29)
        option = BasicItems.get_bannable_feature_options(
            "platinum_tickets_l", "platinum_shards_l"
        )
        if option == 2:
            return
        if option == 1:
            return edits.basic_items.BasicItems.edit_platinum_shards(save_file)

        original_amount = save_file.platinum_tickets
        save_file.platinum_tickets = dialog_creator.SingleEditor(
            BasicItems.get_name(name, "platinum_tickets"),
            save_file.platinum_tickets,
            core.core_data.max_value_manager.get("platinum_tickets"),
        ).edit()
        change = save_file.platinum_tickets - original_amount
        core.BackupMetaData(save_file).add_managed_item(
            core.ManagedItem.from_change(change, core.ManagedItemType.PLATINUM_TICKET)
        )

    @staticmethod
    def edit_legend_tickets(save_file: core.SaveFile):
        should_exit = not dialog_creator.YesNoInput().get_input_once(
            "legend_ticket_warning"
        )
        if should_exit:
            return
        name = core.core_data.get_gatya_item_names(save_file).get_name(145)
        original_amount = save_file.legend_tickets
        save_file.legend_tickets = dialog_creator.SingleEditor(
            BasicItems.get_name(name, "legend_tickets"),
            save_file.legend_tickets,
            core.core_data.max_value_manager.get("legend_tickets"),
        ).edit()
        change = save_file.legend_tickets - original_amount
        core.BackupMetaData(save_file).add_managed_item(
            core.ManagedItem.from_change(change, core.ManagedItemType.LEGEND_TICKET)
        )

    @staticmethod
    def edit_platinum_shards(save_file: core.SaveFile):
        name = core.core_data.get_gatya_item_names(save_file).get_name(157)
        platinum_ticket_amount = save_file.platinum_tickets
        max_value = (
            core.core_data.max_value_manager.get("platinum_tickets")
            - platinum_ticket_amount
        ) * 10 + 9

        max_value = max(0, max_value)
        save_file.platinum_shards = dialog_creator.SingleEditor(
            BasicItems.get_name(name, "platinum_shards"),
            save_file.platinum_shards,
            max_value,
        ).edit()

    @staticmethod
    def edit_np(save_file: core.SaveFile):
        name = core.core_data.get_gatya_item_names(save_file).get_name(7)
        save_file.np = dialog_creator.SingleEditor(
            BasicItems.get_name(name, "np"),
            save_file.np,
            core.core_data.max_value_manager.get("np"),
        ).edit()

    @staticmethod
    def edit_leadership(save_file: core.SaveFile):
        name = core.core_data.get_gatya_item_names(save_file).get_name(105)
        save_file.leadership = dialog_creator.SingleEditor(
            BasicItems.get_name(name, "leadership"),
            save_file.leadership,
            core.core_data.max_value_manager.get("leadership"),
        ).edit()

    @staticmethod
    def edit_battle_items(save_file: core.SaveFile):
        save_file.battle_items.edit(save_file)

    @staticmethod
    def edit_battle_items_endless(save_file: core.SaveFile):
        save_file.battle_items.edit_endless_items(save_file)

    @staticmethod
    def edit_catamins(save_file: core.SaveFile):
        names_o = core.core_data.get_gatya_item_names(save_file)
        items = core.core_data.get_gatya_item_buy(save_file).get_by_category(6)
        if items is None:
            return
        names: list[str] = []
        for item in items:
            name = names_o.get_name(item.id)
            if name is None:
                name = core.core_data.local_manager.get_key(
                    "unknown_catamin_name", id=item.id
                )
            names.append(name)
        values = dialog_creator.MultiEditor.from_reduced(
            "catamins",
            names,
            save_file.catamins,
            core.core_data.max_value_manager.get("catamins"),
            group_name_localized=True,
        ).edit()
        save_file.catamins = values

    @staticmethod
    def edit_catseyes(save_file: core.SaveFile):
        names_o = core.core_data.get_gatya_item_names(save_file)
        items = core.core_data.get_gatya_item_buy(save_file).get_by_category(5)
        if items is None:
            return
        names: list[str] = []
        for item in items:
            name = names_o.get_name(item.id)
            if name is None:
                name = core.core_data.local_manager.get_key(
                    "unknown_catseye_name", id=item.id
                )
            names.append(name)

        values = dialog_creator.MultiEditor.from_reduced(
            "catseyes",
            names,
            save_file.catseyes,
            core.core_data.max_value_manager.get("catseyes"),
            group_name_localized=True,
        ).edit()
        save_file.catseyes = values

    @staticmethod
    def edit_treasure_chests(save_file: core.SaveFile):
        names_o = core.core_data.get_gatya_item_names(save_file)
        items = core.core_data.get_gatya_item_buy(save_file).get_by_category(
            GatyaItemCategory.TREASURE_CHESTS
        )
        if items is None:
            return
        names: list[str] = []
        for item in items[: len(save_file.treasure_chests)]:
            name = names_o.get_name(item.id)
            if name is None:
                name = core.core_data.local_manager.get_key(
                    "unknown_treasure_chest_name", id=item.id
                )
            names.append(name)

        values = dialog_creator.MultiEditor.from_reduced(
            "treasure_chests",
            names,
            save_file.treasure_chests,
            core.core_data.max_value_manager.get("treasure_chests"),
            group_name_localized=True,
        ).edit()
        save_file.treasure_chests = values

    @staticmethod
    def edit_catfruit(save_file: core.SaveFile):
        names = core.Matatabi(save_file).get_names()
        if names is None:
            return
        new_names: list[str] = []
        for i, name in enumerate(names):
            if name is None:
                name = core.core_data.local_manager.get_key(
                    "unknown_catfruit_name", id=i
                )
            new_names.append(name)
        names = new_names

        extra = len(save_file.catfruit) - len(names)
        if extra > 0:
            for i in range(extra):
                names.append(
                    core.core_data.local_manager.get_key(
                        "unknown_catfruit_name", id=i + len(names)
                    )
                )

        if save_file.game_version < 110400:
            max_value = core.core_data.max_value_manager.get_old("catfruit")
            cumulative_max = True
        else:
            max_value = core.core_data.max_value_manager.get_new("catfruit")
            cumulative_max = False

        names = names[: len(save_file.catfruit)]

        values = dialog_creator.MultiEditor.from_reduced(
            "catfruit",
            names,
            save_file.catfruit,
            max_value,
            group_name_localized=True,
            cumulative_max=cumulative_max,
        ).edit()
        save_file.catfruit = values

    @staticmethod
    def set_restart_pack(save_file: core.SaveFile):
        save_file.restart_pack = 1
        name = core.core_data.get_gatya_item_names(save_file).get_name(123)
        color.ColoredText.localize("value_gave", name=name)

    @staticmethod
    def edit_inquiry_code(save_file: core.SaveFile):
        should_exit = not dialog_creator.YesNoInput().get_input_once(
            "inquiry_code_warning"
        )
        if should_exit:
            return
        item_name = save_file.get_localizable().get("autoSave_txt5")
        save_file.inquiry_code = dialog_creator.StringEditor(
            BasicItems.get_name(item_name, "inquiry_code"),
            save_file.inquiry_code,
        ).edit()

    @staticmethod
    def edit_password_refresh_token(save_file: core.SaveFile):
        should_exit = not dialog_creator.YesNoInput().get_input_once(
            "password_refresh_token_warning"
        )
        if should_exit:
            return
        save_file.password_refresh_token = dialog_creator.StringEditor(
            "password_refresh_token",
            save_file.password_refresh_token,
            item_localized=True,
        ).edit()

    @staticmethod
    def edit_scheme_items(save_file: core.SaveFile):
        save_file.scheme_items.edit(save_file)

    @staticmethod
    def edit_engineers(save_file: core.SaveFile):
        save_file.ototo.edit_engineers(save_file)

    @staticmethod
    def edit_base_materials(save_file: core.SaveFile):
        save_file.ototo.base_materials.edit_base_materials(save_file)

    @staticmethod
    def edit_rare_gatya_seed(save_file: core.SaveFile):
        save_file.gatya.edit_rare_gatya_seed()

    @staticmethod
    def edit_normal_gatya_seed(save_file: core.SaveFile):
        save_file.gatya.edit_normal_gatya_seed()

    @staticmethod
    def edit_event_gatya_seed(save_file: core.SaveFile):
        save_file.gatya.edit_event_gatya_seed()

    @staticmethod
    def edit_unlocked_slots(save_file: core.SaveFile):
        save_file.lineups.edit_unlocked_slots()

    @staticmethod
    def edit_labyrinth_medals(save_file: core.SaveFile):
        names_o = core.core_data.get_gatya_item_names(save_file)
        items = core.core_data.get_gatya_item_buy(save_file).get_by_category(11)
        if items is None:
            return
        names: list[str] = []
        for item in items:
            name = names_o.get_name(item.id)
            if name is None:
                name = core.core_data.local_manager.get_key(
                    "unknown_labyrinth_medal_name", id=item.id
                )
            names.append(name)

        values = dialog_creator.MultiEditor.from_reduced(
            "labyrinth_medals",
            names,
            save_file.labyrinth_medals,
            core.core_data.max_value_manager.get("labyrinth_medals"),
            group_name_localized=True,
        ).edit()
        save_file.labyrinth_medals = values

    @staticmethod
    def edit_special_skills(save_file: core.SaveFile):
        save_file.special_skills.edit(save_file)

    @staticmethod
    def unlock_equip_menu(save_file: core.SaveFile):
        save_file.unlock_equip_menu()
        color.ColoredText.localize("equip_menu_unlocked")

    @staticmethod
    def allow_filibuster_stage_reclearing(save_file: core.SaveFile):
        save_file.filibuster_stage_enabled = True
        save_file.filibuster_stage_id = random.randint(0, 47)
        color.ColoredText.localize("filibuster_stage_reclearing_allowed")


# ============================================================
# FILE: cat_editor.py
# ============================================================
from __future__ import annotations
import enum
from typing import Any, Callable

from bcsfe import core
from bcsfe.cli import color, dialog_creator


class SelectMode(enum.Enum):
    AND = 0
    OR = 1
    REPLACE = 2


class CatEditor:
    def __init__(self, save_file: core.SaveFile):
        self.save_file = save_file

    def get_current_cats(self):
        return self.save_file.cats.get_unlocked_cats()

    def get_non_unlocked_cats(self):
        return self.save_file.cats.get_non_unlocked_cats()

    def get_non_gacha_cats(self):
        return self.save_file.cats.get_non_gacha_cats(self.save_file)

    def filter_cats(self, cats: list[core.Cat]) -> list[core.Cat]:
        unlocked_cats = self.get_current_cats()
        return [cat for cat in cats if cat in unlocked_cats]

    def get_cats_rarity(self, rarity: int) -> list[core.Cat]:
        return self.save_file.cats.get_cats_rarity(self.save_file, rarity)

    def get_cats_name(self, name: str) -> list[core.Cat]:
        return self.save_file.cats.get_cats_name(self.save_file, name)

    def get_cats_obtainable(self) -> list[core.Cat] | None:
        return self.save_file.cats.get_cats_obtainable(self.save_file)

    def get_cats_unobtainable(self) -> list[core.Cat] | None:
        return self.save_file.cats.get_cats_non_obtainable(self.save_file)

    def get_cats_gatya_banner(self, gatya_id: int) -> list[core.Cat] | None:
        return self.save_file.cats.get_cats_gatya_banner(self.save_file, gatya_id)

    def print_selected_cats(self, current_cats: list[core.Cat]):
        if len(current_cats) > 50:
            color.ColoredText.localize("total_selected_cats", total=len(current_cats))
        else:
            for cat in current_cats:
                names = cat.get_names_cls(self.save_file)
                if not names:
                    names = [str(cat.id)]
                color.ColoredText.localize("selected_cat", id=cat.id, name=names[0])

    def select(
        self, current_cats: list[core.Cat] | None = None, finish_option: bool = True
    ) -> tuple[list[core.Cat], bool]:
        if current_cats is None:
            current_cats = []
        options: dict[str, Callable[[], Any]] = {
            "select_cats_all": self.save_file.cats.get_all_cats,
            "select_cats_current": self.get_current_cats,
            "select_cats_obtainable": self.get_cats_obtainable,
            "select_cats_id": self.select_id,
            "select_cats_name": self.select_name,
            "select_cats_rarity": self.select_rarity,
            "select_cats_gatya_banner": self.select_gatya_banner,
            "select_cats_not_unlocked": self.get_non_unlocked_cats,
            "select_cats_not_obtainable": self.get_cats_unobtainable,
            "select_cats_non_gatya": self.get_non_gacha_cats,
            "select_cats_game_version": self.select_cats_game_version,
        }
        if finish_option:
            options["finish"] = lambda: None
        option_id = dialog_creator.ChoiceInput(
            list(options), list(options), [], {}, "select_cats", True
        ).single_choice()
        if option_id is None:
            return current_cats, False
        option_id -= 1

        if option_id == len(options) - 1 and finish_option:
            return current_cats, True

        func = options[list(options)[option_id]]
        new_cats = func()

        if new_cats is None:
            return current_cats, False

        if current_cats:
            mode_id = dialog_creator.IntInput().get_basic_input_locale("and_mode_q", {})
            if mode_id is None:
                mode = SelectMode.OR
            elif mode_id == 1:
                mode = SelectMode.AND
            elif mode_id == 2:
                mode = SelectMode.OR
            elif mode_id == 3:
                mode = SelectMode.REPLACE
            else:
                mode = SelectMode.OR
        else:
            mode = SelectMode.OR

        if mode == SelectMode.AND:
            return list(set(current_cats) & set(new_cats)), False
        if mode == SelectMode.OR:
            return list(set(current_cats) | set(new_cats)), False
        if mode == SelectMode.REPLACE:
            return new_cats, False
        return new_cats, False

    def select_id(self) -> list[core.Cat] | None:
        cat_ids = dialog_creator.RangeInput(
            len(self.save_file.cats.cats) - 1
        ).get_input_locale("enter_cat_ids", {})
        if cat_ids is None:
            return None
        return self.save_file.cats.get_cats_by_ids(cat_ids)

    def select_cats_game_version(self) -> list[core.Cat] | None:
        unitbuy = core.UnitBuy(self.save_file)
        if unitbuy.unit_buy is None:
            return None

        versions_set: set[int] = set()
        for cat in unitbuy.unit_buy:
            if cat.game_version == -1:
                continue
            versions_set.add(cat.game_version)

        if not versions_set:
            return None

        versions = list(versions_set)
        versions.sort()

        color.ColoredText.localize("possible_gvs")

        cur_major_v = -1
        for version in versions:
            gv = core.GameVersion(version)
            major_v = gv.get_parts()[0]
            if major_v != cur_major_v:
                if cur_major_v != -1:
                    print()
                cur_major_v = major_v
            else:
                color.ColoredText(", ", end="")
            color.ColoredText(f"<@t>{gv.format()}</>", end="")

        print()

        usr_input = dialog_creator.StringInput().get_input_locale("select_gv")
        if usr_input is None:
            return None
        chunks = usr_input.split(" ")

        versions_selected: list[int] = []
        for chunk in chunks:
            parts = chunk.split("-")
            if len(parts) == 2:
                min = parts[0]
                max = parts[1]

                v1 = core.GameVersion.from_string(min)
                v2 = core.GameVersion.from_string(max)

                for v in range(v1.game_version, v2.game_version + 1):
                    versions_selected.append(v)
            else:
                v = core.GameVersion.from_string(chunk)
                versions_selected.append(v.game_version)

        valid_versions: set[int] = set()
        for version in versions_selected:
            if version in versions_set:
                valid_versions.add(version)

        if not valid_versions:
            color.ColoredText.localize("no_valid_gvs_entered")

        cats: list[core.Cat] = []
        for cat in self.save_file.cats.cats:
            row = unitbuy.get_unit_buy(cat.id)
            if row is None:
                continue
            if row.game_version in valid_versions:
                cats.append(cat)

        return cats

    def select_rarity(self) -> list[core.Cat] | None:
        rarity_names = self.save_file.cats.get_rarity_names(self.save_file)
        rarity_ids, _ = dialog_creator.ChoiceInput(
            rarity_names, rarity_names, [], {}, "select_rarity"
        ).multiple_choice()
        if rarity_ids is None:
            return None
        cats: list[core.Cat] = []
        for rarity_id in rarity_ids:
            rarity_cats = self.get_cats_rarity(rarity_id)
            cats = list(set(cats + rarity_cats))
        return cats

    def select_name(self) -> list[core.Cat] | None:
        usr_name = dialog_creator.StringInput().get_input_locale("enter_name", {})
        if usr_name is None:
            return []
        cats = self.get_cats_name(usr_name)
        if not cats:
            color.ColoredText.localize("no_cats_found_name", name=usr_name)
            return None
        cat_names: list[str] = []
        cat_list: list[core.Cat] = []
        for cat in cats:
            names = cat.get_names_cls(self.save_file)
            if not names:
                names = [str(cat.id)]
            for name in names:
                if usr_name.lower() in name.lower():
                    cat_names.append(name)
                    cat_list.append(cat)
                    break
        if len(cat_names) == 1:
            color.ColoredText(f"<@t>{cat_names[0]}</>")
        cat_option_ids, _ = dialog_creator.ChoiceInput(
            cat_names, cat_names, [], {}, "select_name"
        ).multiple_choice()
        if cat_option_ids is None:
            return None
        cats_selected: list[core.Cat] = []
        for cat_option_id in cat_option_ids:
            cats_selected.append(cat_list[cat_option_id])
        return cats_selected

    def select_obtainable(self) -> list[core.Cat] | None:
        return self.get_cats_obtainable()

    def select_gatya_banner_name(self) -> list[int] | None:

        filter_down = dialog_creator.YesNoInput().get_input_once("filter_down_q_gatya")
        if filter_down is None:
            return None

        all_names = core.GatyaInfos(self.save_file).get_all_names()
        ids = list(all_names.keys())
        ids.sort()
        names: list[str] = []
        for id in ids:
            names.append(all_names[id])
        new_names: list[str] = []
        new_ids: list[int] = []

        unknown_name = core.core_data.local_manager.get_key("unknown_banner")

        if filter_down:
            ids.reverse()
            for id in ids:
                name = all_names[id]
                if name in new_names or name == unknown_name:
                    continue
                new_names.append(name)
                new_ids.append(id)
            new_ids.reverse()
            new_names.reverse()
        else:
            new_names = names
            new_ids = ids

        ids = new_ids

        formatted_names: list[str] = []

        for name in new_names:
            formatted_name = core.core_data.local_manager.get_key(
                "banner_txt", name=name
            )
            formatted_names.append(formatted_name)
        gatya_option_ids, _ = dialog_creator.ChoiceInput.from_reduced(
            formatted_names,
            ints=ids,
            dialog="select_gatya_banner",
            start_index=0,
        ).multiple_choice(False)
        if gatya_option_ids is None:
            return None
        gatya_ids: list[int] = []
        for gatya_option_id in gatya_option_ids:
            gatya_ids.append(ids[gatya_option_id])

        return gatya_ids

    def select_gatya_banner(self) -> list[core.Cat] | None:
        gset = self.save_file.gatya.read_gatya_data_set(self.save_file).gatya_data_set
        if gset is None:
            return None

        by_id = dialog_creator.ChoiceInput.from_reduced(
            ["by_id", "by_name"], dialog="gatya_by_id_q"
        ).single_choice()
        if by_id is None:
            return None

        if by_id == 1:
            gatya_ids = dialog_creator.RangeInput(len(gset) - 1).get_input_locale(
                "select_gatya_banner", {}
            )
        else:
            gatya_ids = self.select_gatya_banner_name()
        if gatya_ids is None:
            return None
        cats: list[core.Cat] = []
        for gatya_id in gatya_ids:
            gatya_cats = self.get_cats_gatya_banner(gatya_id)
            if gatya_cats is None:
                continue
            cats = list(set(cats + gatya_cats))
        return cats

    def unlock_cats(self, cats: list[core.Cat]):
        cats = self.get_save_cats(cats)
        for cat in cats:
            cat.unlock(self.save_file)
        color.ColoredText.localize("unlock_success")

    def remove_cats(self, cats: list[core.Cat]):
        reset = core.core_data.config.get_bool(core.ConfigKey.RESET_CAT_DATA)
        cats = self.get_save_cats(cats)
        for cat in cats:
            cat.remove(reset=reset, save_file=self.save_file)
        color.ColoredText.localize("remove_success")

    def get_save_cats(self, cats: list[core.Cat]):
        ct_cats: list[core.Cat] = []
        for cat in cats:
            ct = self.save_file.cats.get_cat_by_id(cat.id)
            if ct is None:
                continue
            ct_cats.append(ct)
        return ct_cats

    def true_form_cats(self, cats: list[core.Cat], force: bool = False):
        cats = self.get_save_cats(cats)
        set_current_forms = core.core_data.config.get_bool(
            core.ConfigKey.SET_CAT_CURRENT_FORMS
        )
        self.save_file.cats.true_form_cats(
            self.save_file, cats, force, set_current_forms
        )
        color.ColoredText.localize("true_form_success")

    def fourth_form_cats(self, cats: list[core.Cat], force: bool = False):
        cats = self.get_save_cats(cats)
        set_current_forms = core.core_data.config.get_bool(
            core.ConfigKey.SET_CAT_CURRENT_FORMS
        )
        self.save_file.cats.fourth_form_cats(
            self.save_file, cats, force, set_current_forms
        )
        color.ColoredText.localize("fourth_form_success")

    def remove_true_form_cats(self, cats: list[core.Cat]):
        cats = self.get_save_cats(cats)
        for cat in cats:
            cat.remove_true_form()
        color.ColoredText.localize("remove_true_form_success")

    def remove_fourth_form_cats(self, cats: list[core.Cat]):
        cats = self.get_save_cats(cats)
        for cat in cats:
            cat.remove_fourth_form()
        color.ColoredText.localize("remove_fourth_form_success")

    def upgrade_cats(self, cats: list[core.Cat]):
        cats = self.get_save_cats(cats)
        if not cats:
            return
        if len(cats) == 1:
            option_id = 0
        else:
            options: list[str] = [
                "upgrade_individual",
                "upgrade_all",
            ]
            option_id = dialog_creator.ChoiceInput(
                options, options, [], {}, "upgrade_cats_select_mod", True
            ).single_choice()
            if option_id is None:
                return
            option_id -= 1
        success = False
        if option_id == 0:
            for cat in cats:
                names = cat.get_names_cls(self.save_file)
                if not names:
                    names = [str(cat.id)]
                color.ColoredText.localize(
                    "selected_cat_upgrades",
                    name=names[0],
                    id=cat.id,
                    base_level=cat.upgrade.base + 1,
                    plus_level=cat.upgrade.plus,
                )
                power_up = core.PowerUpHelper(cat, self.save_file)
                upgrade, should_exit = core.Upgrade.get_user_upgrade(
                    power_up.get_max_possible_base() - 1,
                    power_up.get_max_possible_plus(),
                )
                if should_exit:
                    return
                if upgrade is not None:
                    power_up.reset_upgrade()
                    power_up.upgrade_by(upgrade.base)
                    cat.set_upgrade(self.save_file, upgrade, True)
                    color.ColoredText.localize(
                        "selected_cat_upgraded",
                        name=names[0],
                        id=cat.id,
                        base_level=cat.upgrade.base + 1,
                        plus_level=cat.upgrade.plus,
                    )
                    success = True
        else:
            power_up = core.PowerUpHelper(cats[0], self.save_file)
            upgrade, should_exit = core.Upgrade.get_user_upgrade(
                power_up.get_max_max_base_upgrade_level() - 1,
                power_up.get_max_max_plus_upgrade_level(),
            )
            if upgrade is None or should_exit:
                return
            success = True
            for cat in cats:
                power_up = core.PowerUpHelper(cat, self.save_file)
                power_up.reset_upgrade()
                power_up.upgrade_by(upgrade.base)
                cat.set_upgrade(self.save_file, upgrade, True)
        if success:
            color.ColoredText.localize("upgrade_success")

    def remove_talents_cats(self, cats: list[core.Cat]):
        for cat in cats:
            if cat.talents is None:
                continue
            for talent in cat.talents:
                talent.level = 0
        color.ColoredText.localize("talents_remove_success")

    def unlock_cat_guide(self, cats: list[core.Cat]):
        for cat in cats:
            if core.core_data.config.get_bool(core.ConfigKey.UNLOCK_CAT_ON_EDIT):
                cat.unlock(self.save_file)
            cat.catguide_collected = True
        color.ColoredText.localize("unlock_cat_guide_success")

    def remove_cat_guide(self, cats: list[core.Cat]):
        for cat in cats:
            cat.catguide_collected = False
        color.ColoredText.localize("remove_cat_guide_success")

    def upgrade_talents_cats(self, cats: list[core.Cat]):
        cats = self.get_save_cats(cats)
        if not cats:
            return
        gdg = core.core_data.get_game_data_getter(self.save_file)
        is_good_version = gdg.does_save_version_match(self.save_file)
        if not is_good_version:
            data_version = gdg.version
            if data_version is None:
                color.ColoredText.localize("no_data_version")
                return
            color.ColoredText.localize(
                "talents_version_warning",
                save_version=self.save_file.game_version.to_string(),
                data_version=data_version,
            )
            should_stay = dialog_creator.YesNoInput().get_input_once("continue_q")
            if not should_stay:
                return

        if len(cats) == 1:
            option_id = 0
        else:
            options: list[str] = [
                "talents_individual",
                "talents_all",
            ]
            option_id = dialog_creator.ChoiceInput(
                options, options, [], {}, "upgrade_talents_select_mod", True
            ).single_choice()
            if option_id is None:
                return
            option_id -= 1

        talent_data = self.save_file.cats.read_talent_data(self.save_file)
        if talent_data is None:
            return
        if option_id == 0:
            for cat in cats:
                if cat.talents is None:
                    continue
                names = cat.get_names_cls(self.save_file)
                if not names:
                    names = [str(cat.id)]
                color.ColoredText.localize(
                    "selected_cat",
                    name=names[0],
                    id=cat.id,
                )
                data = talent_data.get_cat_talents(cat)
                if data is None:
                    color.ColoredText.localize("no_talent_data", id=cat.id)
                    continue
                if core.core_data.config.get_bool(core.ConfigKey.UNLOCK_CAT_ON_EDIT):
                    cat.unlock(self.save_file)
                talent_names, max_levels, current_levels, ids = data
                values = dialog_creator.MultiEditor.from_reduced(
                    "talents",
                    talent_names,
                    current_levels,
                    max_levels,
                    group_name_localized=True,
                ).edit()
                current_levels = values
                for i, id in enumerate(ids):
                    talent = cat.get_talent_from_id(id)
                    if talent is None:
                        continue
                    talent.level = current_levels[i]
        else:
            for cat in cats:
                if cat.talents is None:
                    continue
                data = talent_data.get_cat_talents(cat)
                if data is None:
                    continue
                if core.core_data.config.get_bool(core.ConfigKey.UNLOCK_CAT_ON_EDIT):
                    cat.unlock(self.save_file)
                talent_names, max_levels, current_levels, ids = data
                for i, id in enumerate(ids):
                    talent = cat.get_talent_from_id(id)
                    if talent is None:
                        continue
                    talent.level = max_levels[i]
        color.ColoredText.localize("talents_success")

    @staticmethod
    def edit_cats(save_file: core.SaveFile):
        cat_editor, current_cats = CatEditor.from_save_file(save_file)
        if cat_editor is None:
            return
        while True:
            should_exit, current_cats = cat_editor.run_edit_cats(current_cats)
            if should_exit:
                break

    @staticmethod
    def unlock_remove_cats_run(
        save_file: core.SaveFile,
        current_cats: list[core.Cat] | None = None,
        cat_editor: CatEditor | None = None,
    ):
        if cat_editor is None or current_cats is None:
            cat_editor, current_cats = CatEditor.from_save_file(save_file)
        if cat_editor is None:
            return
        choice = dialog_creator.ChoiceInput(
            ["unlock_cats", "remove_cats"],
            ["unlock_cats", "remove_cats"],
            [],
            {},
            "unlock_remove_q",
            True,
            remove_alias=True,
        ).single_choice()
        if choice is None:
            return
        choice -= 1
        if choice == 0:
            cat_editor.unlock_cats(current_cats)
        elif choice == 1:
            cat_editor.remove_cats(current_cats)
        CatEditor.set_rank_up_sale(save_file)

    @staticmethod
    def true_form_remove_form_cats_run(
        save_file: core.SaveFile,
        current_cats: list[core.Cat] | None = None,
        cat_editor: CatEditor | None = None,
    ):
        if cat_editor is None or current_cats is None:
            cat_editor, current_cats = CatEditor.from_save_file(save_file)
        if cat_editor is None:
            return
        choice = dialog_creator.ChoiceInput.from_reduced(
            ["true_form_cats", "remove_true_form_cats"],
            dialog="true_form_remove_form_q",
            single_choice=True,
        ).single_choice()
        if choice is None:
            return
        choice -= 1
        if choice == 0:
            cat_editor.true_form_cats(current_cats)
        elif choice == 1:
            cat_editor.remove_true_form_cats(current_cats)

    @staticmethod
    def fourth_form_remove_form_cats_run(
        save_file: core.SaveFile,
        current_cats: list[core.Cat] | None = None,
        cat_editor: CatEditor | None = None,
    ):
        if cat_editor is None or current_cats is None:
            cat_editor, current_cats = CatEditor.from_save_file(save_file)
        if cat_editor is None:
            return
        choice = dialog_creator.ChoiceInput.from_reduced(
            ["fourth_form_cats", "remove_fourth_form_cats"],
            dialog="fourth_form_remove_form_q",
            single_choice=True,
        ).single_choice()
        if choice is None:
            return
        choice -= 1
        if choice == 0:
            cat_editor.fourth_form_cats(current_cats)
        elif choice == 1:
            cat_editor.remove_fourth_form_cats(current_cats)

    @staticmethod
    def force_true_form_cats_run(save_file: core.SaveFile):
        color.ColoredText.localize("force_true_form_cats_warning")
        cat_editor, current_cats = CatEditor.from_save_file(save_file)
        if cat_editor is None:
            return
        cat_editor.true_form_cats(current_cats, force=True)

    @staticmethod
    def force_fourth_form_cats_run(save_file: core.SaveFile):
        color.ColoredText.localize("force_fourth_form_cats_warning")
        cat_editor, current_cats = CatEditor.from_save_file(save_file)
        if cat_editor is None:
            return
        cat_editor.fourth_form_cats(current_cats, force=True)

    @staticmethod
    def upgrade_cats_run(save_file: core.SaveFile):
        cat_editor, current_cats = CatEditor.from_save_file(save_file)
        if cat_editor is None:
            return
        cat_editor.upgrade_cats(current_cats)
        CatEditor.set_rank_up_sale(save_file)

    @staticmethod
    def upgrade_talents_remove_talents_cats_run(
        save_file: core.SaveFile,
        current_cats: list[core.Cat] | None = None,
        cat_editor: CatEditor | None = None,
    ):
        if cat_editor is None or current_cats is None:
            cat_editor, current_cats = CatEditor.from_save_file(save_file)
        if cat_editor is None:
            return
        choice = dialog_creator.ChoiceInput(
            ["upgrade_talents_cats", "remove_talents_cats"],
            ["upgrade_talents_cats", "remove_talents_cats"],
            [],
            {},
            "upgrade_talents_remove_talents_q",
            True,
        ).single_choice()
        if choice is None:
            return
        choice -= 1
        if choice == 0:
            cat_editor.upgrade_talents_cats(current_cats)
        elif choice == 1:
            cat_editor.remove_talents_cats(current_cats)

    @staticmethod
    def unlock_cat_guide_remove_guide_run(
        save_file: core.SaveFile,
        current_cats: list[core.Cat] | None = None,
        cat_editor: CatEditor | None = None,
    ):
        if cat_editor is None or current_cats is None:
            cat_editor, current_cats = CatEditor.from_save_file(save_file)
        if cat_editor is None:
            return
        choice = dialog_creator.ChoiceInput(
            ["unlock_cat_guide", "remove_cat_guide"],
            ["unlock_cat_guide", "remove_cat_guide"],
            [],
            {},
            "unlock_cat_guide_remove_guide_q",
            True,
        ).single_choice()
        if choice is None:
            return
        choice -= 1
        if choice == 0:
            cat_editor.unlock_cat_guide(current_cats)
        elif choice == 1:
            cat_editor.remove_cat_guide(current_cats)

    @staticmethod
    def from_save_file(
        save_file: core.SaveFile,
    ) -> tuple[CatEditor | None, list[core.Cat]]:
        cat_editor = CatEditor(save_file)
        stop = False
        cats = []
        while not stop:
            current_cats, finished = cat_editor.select(cats)
            cats = current_cats
            cat_editor.print_selected_cats(cats)
            if finished:
                stop = True
                continue
            finished = dialog_creator.YesNoInput().get_input_once(
                "finished_cats_selection"
            )
            if finished is None:
                return None, []
            stop = finished
        return cat_editor, cats

    def run_edit_cats(
        self,
        cats: list[core.Cat],
    ) -> tuple[bool, list[core.Cat]]:
        self.print_selected_cats(cats)
        options: list[str] = [
            "select_cats_again",
            "unlock_remove_cats",
            "upgrade_cats",
            "true_form_remove_form_cats",
            "force_true_form_cats",
            "fourth_form_remove_form_cats",
            "force_fourth_form_cats",
            "upgrade_talents_remove_talents_cats",
            "unlock_remove_cat_guide",
            "finish_edit_cats",
        ]
        option_id = dialog_creator.ChoiceInput(
            options,
            options,
            [],
            {},
            "select_edit_cats_option",
            True,
            remove_alias=True,
        ).single_choice()
        if option_id is None:
            return False, cats
        option_id -= 1
        if option_id == 0:
            cats_, _ = self.select(cats, False)
            cats = cats_
        elif option_id == 1:
            self.unlock_remove_cats_run(self.save_file, cats, self)
        elif option_id == 2:
            self.upgrade_cats(cats)
        elif option_id == 3:
            self.true_form_remove_form_cats_run(self.save_file, cats, self)
        elif option_id == 4:
            color.ColoredText.localize("force_true_form_cats_warning")
            self.true_form_cats(cats, force=True)
        elif option_id == 5:
            self.fourth_form_remove_form_cats_run(self.save_file, cats, self)
        elif option_id == 6:
            color.ColoredText.localize("force_fourth_form_cats_warning")
            self.fourth_form_cats(cats, force=True)
        elif option_id == 7:
            self.upgrade_talents_remove_talents_cats_run(self.save_file, cats, self)
        elif option_id == 8:
            self.unlock_cat_guide_remove_guide_run(self.save_file, cats, self)
        CatEditor.set_rank_up_sale(self.save_file)
        if option_id == 9:
            return True, cats
        return False, cats

    @staticmethod
    def set_rank_up_sale(save_file: core.SaveFile):
        save_file.rank_up_sale_value = 0x7FFFFFFF


# ============================================================
# FILE: clear_tutorial.py
# ============================================================
from __future__ import annotations
from bcsfe import core
from bcsfe.cli import color


def clear_tutorial(
    save_file: core.SaveFile, display_already_cleared: bool = True
):
    core.StoryChapters.clear_tutorial(save_file)
    if display_already_cleared:
        color.ColoredText.localize("tutorial_cleared")


# ============================================================
# FILE: enemy_editor.py
# ============================================================
from __future__ import annotations
from typing import Any
from bcsfe import core
from bcsfe.cli import color, dialog_creator
from bcsfe.cli.edits.cat_editor import SelectMode
from bcsfe.core.game.battle.enemy import EnemyNames


class EnemyEditor:
    def __init__(self, save_file: core.SaveFile) -> None:
        self.save_file = save_file

    def unlock_enemy_guide(self, enemies: list[core.Enemy]):
        for enemy in enemies:
            enemy.unlock_enemy_guide(self.save_file)

        color.ColoredText.localize("unlock_enemy_guide_success")

    def remove_enemy_guide(self, enemies: list[core.Enemy]):
        for enemy in enemies:
            enemy.reset_enemy_guide(self.save_file)

        color.ColoredText.localize("remove_enemy_guide_success")

    def print_selected_enemies(self, enemies: list[core.Enemy]):
        if not enemies:
            return
        if len(enemies) > 50:
            color.ColoredText.localize("total_selected_enemies", total=len(enemies))
        else:
            for enemy in enemies:
                color.ColoredText.localize(
                    "selected_enemy",
                    id=enemy.id,
                    name=enemy.get_name(self.save_file),
                )

    def select(self, current_enemies: list[core.Enemy] | None):
        if current_enemies is None:
            current_enemies = []
        self.print_selected_enemies(current_enemies)

        options: dict[str, Any] = {
            "select_enemies_valid": self.get_all_valid_enemies,
            "select_enemies_all": self.get_all_enemies,
            "select_enemies_id": self.select_id,
            "select_enemies_name": self.select_name,
            "select_enemies_invalid": self.get_all_invalid_enemies,
        }
        option_id = dialog_creator.ChoiceInput.from_reduced(
            list(options), dialog="select_enemies", single_choice=True
        ).single_choice()
        if option_id is None:
            return current_enemies
        option_id -= 1

        func = options[list(options)[option_id]]
        new_enemies = func()
        if new_enemies is None:
            return None

        if current_enemies:
            mode_id = dialog_creator.IntInput().get_basic_input_locale("and_mode_q", {})
            if mode_id is None:
                mode = SelectMode.OR
            elif mode_id == 1:
                mode = SelectMode.AND
            elif mode_id == 2:
                mode = SelectMode.OR
            elif mode_id == 3:
                mode = SelectMode.REPLACE
            else:
                mode = SelectMode.OR
        else:
            mode = SelectMode.OR

        if mode == SelectMode.AND:
            return [enemy for enemy in new_enemies if enemy in current_enemies]
        if mode == SelectMode.OR:
            return list(set(current_enemies + new_enemies))
        if mode == SelectMode.REPLACE:
            return new_enemies
        return new_enemies

    def get_all_enemies(self) -> list[core.Enemy]:
        enemies: list[core.Enemy] = []
        for i in range(len(self.save_file.enemy_guide)):
            enemies.append(core.Enemy(i))
        return enemies

    def get_all_valid_enemies(self) -> list[core.Enemy] | None:
        valid_ids = core.EnemyDictionary(self.save_file).get_valid_enemies()
        if valid_ids is None:
            return None

        return [core.Enemy(id) for id in valid_ids]

    def get_all_invalid_enemies(self) -> list[core.Enemy] | None:
        invalid_ids = core.EnemyDictionary(self.save_file).get_invalid_enemies(
            len(self.save_file.enemy_guide)
        )
        if invalid_ids is None:
            return None

        return [core.Enemy(id) for id in invalid_ids]

    def select_id(self) -> list[core.Enemy] | None:
        enemy_ids = dialog_creator.RangeInput(
            len(self.save_file.enemy_guide) - 1
        ).get_input_locale("enter_enemy_ids", {})
        if enemy_ids is None:
            return None
        enemy_ids = [enemy_id - 2 for enemy_id in enemy_ids]
        return self.get_enemies_by_id(enemy_ids)

    def get_enemies_by_id(self, ids: list[int]) -> list[core.Enemy]:
        enemies: list[core.Enemy] = []
        for enemy in self.get_all_enemies():
            if enemy.id in ids:
                enemies.append(enemy)
        return enemies

    def select_name(self) -> list[core.Enemy] | None:
        usr_name = dialog_creator.StringInput().get_input_locale("enter_enemy_name", {})
        if usr_name is None:
            return None
        enemies = self.get_enemies_by_name(usr_name)
        if not enemies:
            color.ColoredText.localize("enemy_not_found_name", name=usr_name)
            return None

        enemy_names = [enemy.get_name(self.save_file) for enemy in enemies]
        new_enemy_names: list[str] = []
        for enemy_name in enemy_names:
            if enemy_name is None:
                return None

            new_enemy_names.append(enemy_name)

        enemy_option_ids, _ = dialog_creator.ChoiceInput.from_reduced(
            new_enemy_names, dialog="select_enemies", single_choice=False
        ).multiple_choice()
        if enemy_option_ids is None:
            return None
        enemies_selected: list[core.Enemy] = []
        for enemy_option_id in enemy_option_ids:
            enemies_selected.append(enemies[enemy_option_id])
        return enemies_selected

    def get_enemies_by_name(self, name: str) -> list[core.Enemy]:
        enemies: list[core.Enemy] = []
        for enemy in self.get_all_enemies():
            enemy_name = enemy.get_name(self.save_file)
            if enemy_name is None:
                continue
            if name.lower() in enemy_name.lower():
                enemies.append(enemy)
        return enemies

    @staticmethod
    def from_save_file(
        save_file: core.SaveFile,
    ) -> tuple[EnemyEditor | None, list[core.Enemy]]:
        enemy_editor = EnemyEditor(save_file)
        current_enemies = enemy_editor.select([])
        if current_enemies is None:
            return None, []
        return enemy_editor, current_enemies

    @staticmethod
    def edit_enemy_guide(
        save_file: core.SaveFile,
        current_enemies: list[core.Enemy] | None = None,
        enemy_editor: EnemyEditor | None = None,
    ):
        if enemy_editor is None or current_enemies is None:
            enemy_editor, current_enemies = EnemyEditor.from_save_file(save_file)
        if enemy_editor is None or not current_enemies:
            return

        choice = dialog_creator.ChoiceInput.from_reduced(
            ["unlock_enemy_guide", "remove_enemy_guide"],
            dialog="edit_enemy_guide",
            single_choice=True,
        ).single_choice()
        if choice is None:
            return
        choice -= 1
        if choice == 0:
            enemy_editor.unlock_enemy_guide(current_enemies)
        elif choice == 1:
            enemy_editor.remove_enemy_guide(current_enemies)


# ============================================================
# FILE: event_tickets.py
# ============================================================
from __future__ import annotations
from bcsfe import cli, core
from bcsfe.core.game.catbase.gatya import GatyaEventType
from bcsfe.core.server.event_data import split_hhmm, split_yyyymmdd


class EventTickets:
    def __init__(self, save_file: core.SaveFile):
        self.save_file = save_file
        self.gatya_item_buy = core.core_data.get_gatya_item_buy(self.save_file)
        self.gatya_item_names = core.core_data.get_gatya_item_names(self.save_file)
        self.gatya_option_n = core.GatyaDataOption.read(
            self.save_file, GatyaEventType.NORMAL
        )
        self.gatya_option_r = core.GatyaDataOption.read(
            self.save_file, GatyaEventType.RARE
        )
        self.gatya_option_e = core.GatyaDataOption.read(
            self.save_file, GatyaEventType.EVENT
        )

        cli.color.ColoredText.localize("downloading_gatya_data")
        temp_save_file = core.SaveFile(cc=save_file.cc, gv=save_file.game_version)
        gatya_event_data = core.ServerHandler(temp_save_file).download_gatya_data()

        if gatya_event_data is None:
            cli.color.ColoredText.localize("download_gatya_data_fail")
            self.gatya_event_data = None
        else:
            cli.color.ColoredText.localize("download_gatya_data_success")
            self.gatya_event_data = core.ServerGatyaData.from_data(gatya_event_data)

    @staticmethod
    def edit(save_file: core.SaveFile):
        event_tickets = EventTickets(save_file)

        if event_tickets.gatya_event_data is None:
            return

        event_ticket_items: list[
            tuple[
                core.ServerGatyaDataItem, core.ServerGatyaDataSet, core.GatyaItemBuyItem
            ]
        ] = []

        if (
            event_tickets.gatya_option_n is None
            or event_tickets.gatya_option_r is None
            or event_tickets.gatya_option_e is None
        ):
            return

        for item in event_tickets.gatya_event_data.items:
            for gset in item.sets:
                if gset.number == -1:
                    continue

                gset_opt = None

                if item.get_normal_flag():
                    gset_opt = event_tickets.gatya_option_n.get(gset.number)
                elif item.get_rare_flag():
                    gset_opt = event_tickets.gatya_option_r.get(gset.number)
                elif item.get_collab_flag():
                    gset_opt = event_tickets.gatya_option_e.get(gset.number)

                if gset_opt is None:
                    continue

                gatya_item = event_tickets.gatya_item_buy.get(gset_opt.ticket_item_id)
                if gatya_item is None:
                    continue

                category = gatya_item.category
                if category in [
                    core.GatyaItemCategory.EVENT_TICKETS.value,
                    core.GatyaItemCategory.LUCKY_TICKETS_1.value,
                    core.GatyaItemCategory.LUCKY_TICKETS_2.value,
                ]:
                    event_ticket_items.append((item, gset, gatya_item))

        event_names: list[str] = []
        values: list[int] = []

        for event_item, gset, gatya_item in event_ticket_items:
            start_y, start_m, start_d = split_yyyymmdd(event_item.filter.start_yyyymmdd)
            start_h, start_min = split_hhmm(event_item.filter.start_hhmm)
            end_y, end_m, end_d = split_yyyymmdd(event_item.filter.end_yyyymmdd)
            end_h, end_min = split_hhmm(event_item.filter.end_hhmm)
            time_str = f"{start_y}-{start_m:02}-{start_d:02} {start_h:02}:{start_min:02} -> {end_y}-{end_m:02}-{end_d:02} {end_h:02}:{end_min:02}"
            event_message = gset.message.replace("<br>", "\n")

            base_msg = f"{time_str}"
            item_name = event_tickets.gatya_item_names.get_name(gatya_item.id)
            if item_name is not None:
                base_msg += f" - {item_name}"

            if event_message:
                base_msg += f" - {event_message}"

            current_amount = event_tickets.get_ticket(gatya_item.id)

            if current_amount is not None:
                event_names.append(base_msg)
                values.append(current_amount)

        values = cli.dialog_creator.MultiEditor.from_reduced(
            "event_tickets",
            event_names,
            ints=values,
            max_values=core.core_data.max_value_manager.get("event_tickets"),
            group_name_localized=True,
        ).edit()

        for (event_item, gset, gatya_item), value in zip(event_ticket_items, values):
            event_tickets.edit_ticket(gatya_item.id, value)

    def get_ticket(self, item_id: int) -> int | None:
        item = self.gatya_item_buy.get(item_id)
        if item is None:
            return

        if item.category == core.GatyaItemCategory.EVENT_TICKETS.value:
            if item.index < len(self.save_file.event_capsules):
                return self.save_file.event_capsules[item.index]
        if item.category == core.GatyaItemCategory.LUCKY_TICKETS_1.value:
            if item.index < len(self.save_file.lucky_tickets):
                return self.save_file.lucky_tickets[item.index]
        if item.category == core.GatyaItemCategory.LUCKY_TICKETS_2.value:
            if item.index < len(self.save_file.event_capsules_2):
                return self.save_file.event_capsules_2[item.index]

        return None

    def edit_ticket(self, item_id: int, amount: int):
        item = self.gatya_item_buy.get(item_id)
        if item is None:
            return

        if item.category == core.GatyaItemCategory.EVENT_TICKETS.value:
            if item.index < len(self.save_file.event_capsules):
                self.save_file.event_capsules[item.index] = amount
        if item.category == core.GatyaItemCategory.LUCKY_TICKETS_1.value:
            if item.index < len(self.save_file.lucky_tickets):
                self.save_file.lucky_tickets[item.index] = amount
        if item.category == core.GatyaItemCategory.LUCKY_TICKETS_2.value:
            if item.index < len(self.save_file.event_capsules_2):
                self.save_file.event_capsules_2[item.index] = amount


# ============================================================
# FILE: fixes.py
# ============================================================
from __future__ import annotations
from bcsfe import core
from bcsfe.cli import color
import datetime


class Fixes:
    @staticmethod
    def fix_gamatoto_crash(save_file: core.SaveFile):
        save_file.gamatoto.skin = 2

        color.ColoredText.localize("fix_gamatoto_crash_success")

    @staticmethod
    def fix_ototo_crash(save_file: core.SaveFile):
        save_file.ototo.cannons = core.game.gamoto.ototo.Cannons.init(
            save_file.game_version
        )
        color.ColoredText.localize("fix_ototo_crash_success")

    @staticmethod
    def fix_time_errors(save_file: core.SaveFile):
        save_file.date_3 = datetime.datetime.now()
        save_file.timestamp = datetime.datetime.now().timestamp()
        save_file.energy_penalty_timestamp = datetime.datetime.now().timestamp()

        color.ColoredText.localize("fix_time_errors_success")

        # 10 = 62 / hgt1 = ahead by too much
        # 11 = 63 / hgt0 = behind by too much
        # 12 = 61 / hgt2 = ahead by too much

        # date_3 - controls gacha errors (hgt2)
        # can't be ahead of the device time

        # timestamp - controls gacha errors (hgt1, hgt0)
        # can't be ahead by more than 10 minutes to device time
        # can't be behind by more than 1.5 days to device time

        # penalty_timestamp - controls energy / gamatoto errors
        # can't by ahead of device time
        # can't be ahead by more than 1 day to device time
        # can't be behind by more than 1 day to device time


# ============================================================
# FILE: map.py
# ============================================================
from __future__ import annotations
from bcsfe import core
from bcsfe.cli import color, dialog_creator
from typing import Union

ChaptersType = Union[
    "core.EventChapters",
    "core.GauntletChapters",
    "core.LegendQuestChapters",
    "core.ZeroLegendsChapters",
    "core.Chapters",
]


def get_total_maps(chapters: ChaptersType) -> int:
    if isinstance(chapters, core.EventChapters):
        return chapters.get_lengths()[1]
    return len(chapters.chapters)


def unclear_stage(
    chapters: ChaptersType,
    map: int,
    star: int,
    stage: int,
    type: int | None = None,
) -> bool:
    if isinstance(chapters, core.EventChapters):
        if type is None:
            raise ValueError("Type must be specified for EventChapters!")
        return chapters.unclear_stage(type, map, star, stage)
    else:
        return chapters.unclear_stage(map, star, stage)


def clear_stage(
    chapters: ChaptersType,
    map: int,
    star: int,
    stage: int,
    clear_amount: int = 1,
    overwrite_clear_progress: bool = False,
    type: int | None = None,
    ensure_cleared_only: bool = False,
) -> bool:
    if isinstance(chapters, core.EventChapters):
        if type is None:
            raise ValueError("Type must be specified for EventChapters!")

        return chapters.clear_stage(
            type, map, star, stage, clear_amount, overwrite_clear_progress
        )
    else:
        return chapters.clear_stage(
            map,
            star,
            stage,
            clear_amount,
            overwrite_clear_progress,
            ensure_cleared_only=ensure_cleared_only,
        )


def unclear_rest(
    chapters: ChaptersType,
    stages: list[int],
    stars: int,
    id: int,
    type: int | None = None,
):
    if isinstance(chapters, core.EventChapters):
        if type is None:
            raise ValueError("Type must be specified for EventChapters!")
        chapters.unclear_rest(stages, stars, id, type)
    else:
        chapters.unclear_rest(stages, stars, id)


def get_total_stars(
    map_option: core.MapOption,
    base_index: int,
    chapters: ChaptersType,
    id: int,
    type: int | None = None,
) -> int:

    max_stars = get_max_stars(chapters, id, type)

    map_option_stars = map_option.get_map(base_index + id)
    if map_option_stars is not None:
        return min(max_stars, map_option_stars.crown_count)
    return max_stars


def get_max_max_stars(
    map_option: core.MapOption,
    base_index: int,
    ids: list[int],
    chapters: ChaptersType,
    type: int | None = None,
) -> int:
    m = 0
    for id in ids:
        val = get_total_stars(map_option, base_index, chapters, id, type)
        if val > m:
            m = val

    return m


def get_max_stars(
    chapters: ChaptersType,
    id: int,
    type: int | None = None,
) -> int:

    if isinstance(chapters, core.EventChapters):
        if type is None:
            raise ValueError("Type must be specified for EventChapters!")
        max_stars = chapters.get_total_stars(type, id)
    else:
        max_stars = chapters.get_total_stars(id)

    return max_stars


def get_total_stages(
    chapters: ChaptersType, id: int, star: int, type: int | None = None
):
    if isinstance(chapters, core.EventChapters):
        if type is None:
            raise ValueError("Type must be specified for EventChapters!")
        total_stars = chapters.get_total_stages(type, id, star)
    else:
        total_stars = chapters.get_total_stages(id, star)

    return total_stars


def select_maps(
    save_file: core.SaveFile,
    chapters: ChaptersType,
    letter_code: str,
    base_index: int,
    no_r_prefix: bool = False,
) -> list[int] | None:
    map_names = core.MapNames(
        save_file, letter_code, no_r_prefix=no_r_prefix, base_index=base_index
    )
    names: dict[int, str | None] = {}
    for id, name in map_names.map_names.items():
        if id >= get_total_maps(chapters):
            continue
        names[id] = name

    return core.EventChapters.select_map_names(names)


def select_maps_stars(
    save_file: core.SaveFile,
    map_option: core.MapOption,
    chapters: ChaptersType,
    letter_code: str,
    base_index: int,
    type: int | None = None,
    no_r_prefix: bool = False,
) -> list[tuple[int, int]] | None:
    map_names = core.MapNames(
        save_file, letter_code, no_r_prefix=no_r_prefix, base_index=base_index
    )
    names: dict[int, str | None] = {}
    for id, name in map_names.map_names.items():
        if id >= get_total_maps(chapters):
            continue

        for star in range(get_total_stars(map_option, base_index, chapters, id, type)):
            names[id * 10 + star] = core.localize(
                "map_name_star", name=name, star=star + 1
            )

    ids = core.EventChapters.select_map_names(names)
    if ids is None:
        return None

    new_ids: list[tuple[int, int]] = []

    for id in ids:
        map_id = id // 10
        star_index = id % 10

        new_ids.append((map_id, star_index))

    return new_ids


def edit_chapters2_clear_count(
    save_file: core.SaveFile,
    chapters: ChaptersType,
    letter_code: str,
    base_index: int,
    type: int | None = None,
    no_r_prefix: bool = False,
):

    map_names = core.MapNames(
        save_file, letter_code, no_r_prefix=no_r_prefix, base_index=base_index
    )

    map_option = core.MapOption.from_save(save_file)
    if map_option is None:
        return None

    map_choices = select_maps_stars(
        save_file, map_option, chapters, letter_code, base_index, type, no_r_prefix
    )
    if map_choices is None:
        return None

    clear_all = edit_all_or_handle_ind(len(map_choices))
    if clear_all is None:
        return None

    if clear_all == 0:
        clear_count = core.EventChapters.ask_clear_amount()
        if clear_count is None:
            return None

        for local_map_id, star in map_choices:
            total_stages = get_total_stages(chapters, local_map_id, star, type)
            for stage in range(total_stages):
                clear_stage(chapters, local_map_id, star, stage, clear_count, type=type)
    else:
        for local_map_id, star in map_choices:
            print()
            core.EventChapters.print_current_chapter(
                core.localize(
                    "map_name_star",
                    star=star,
                    name=map_names.map_names.get(local_map_id),
                ),
                local_map_id,
            )
            clear_whole = dialog_creator.ChoiceInput.from_reduced(
                ["edit_whole_chapter", "edit_specific_stages"], dialog="edit_chapter_q"
            ).single_choice()
            if clear_whole is None:
                return None

            clear_whole -= 1

            if clear_whole == 0:
                clear_count = core.EventChapters.ask_clear_amount()
                if clear_count is None:
                    return None

                for stage in range(
                    get_total_stages(chapters, local_map_id, star, type)
                ):
                    clear_stage(
                        chapters, local_map_id, star, stage, clear_count, type=type
                    )
            else:
                stage_ids = core.EventChapters.ask_stages(map_names, local_map_id)

                if stage_ids is None:
                    return None

                all_selected_stages = dialog_creator.ChoiceInput.from_reduced(
                    ["each_stage_individually", "stage_all_at_once"],
                    dialog="set_clear_count_stage_q",
                ).single_choice()
                if all_selected_stages is None:
                    return None

                all_selected_stages -= 1

                stage_names = core.EventChapters.get_stage_names(
                    map_names, local_map_id
                )
                if stage_names is None:
                    stage_names = []
                if all_selected_stages == 0:
                    for stage in stage_ids:
                        print()
                        if stage < len(stage_names):
                            stage_name = stage_names[stage]
                        else:
                            stage_name = None
                        core.EventChapters.print_current_stage(stage_name, stage)
                        clear_count = core.EventChapters.ask_clear_amount()
                        if clear_count is None:
                            return None
                        clear_stage(
                            chapters, local_map_id, star, stage, clear_count, type=type
                        )
                else:
                    clear_count = core.EventChapters.ask_clear_amount()
                    if clear_count is None:
                        return None
                    for stage in stage_ids:
                        clear_stage(
                            chapters, local_map_id, star, stage, clear_count, type=type
                        )


def clear_all_or_handle_ind(map_choices_len: int) -> int | None:
    if map_choices_len <= 1:
        clear_all = 1
    else:
        clear_all = dialog_creator.ChoiceInput.from_reduced(
            ["clear_all", "handle_individually"], dialog="clear_chapters_q"
        ).single_choice()
        if clear_all is None:
            return None

        clear_all -= 1

    return clear_all


def unclear_all_or_handle_ind(map_choices_len: int) -> int | None:
    if map_choices_len <= 1:
        clear_all = 1
    else:
        clear_all = dialog_creator.ChoiceInput.from_reduced(
            ["unclear_all", "handle_individually"], dialog="unclear_chapters_q"
        ).single_choice()
        if clear_all is None:
            return None

        clear_all -= 1

    return clear_all


def edit_all_or_handle_ind(map_choices_len: int) -> int | None:
    if map_choices_len <= 1:
        clear_all = 1
    else:
        clear_all = dialog_creator.ChoiceInput.from_reduced(
            ["edit_map_all", "handle_individually"], dialog="edit_chapters_q_all"
        ).single_choice()
        if clear_all is None:
            return None

        clear_all -= 1

    return clear_all


def edit_chapters2_progress(
    save_file: core.SaveFile,
    chapters: ChaptersType,
    letter_code: str,
    base_index: int,
    type: int | None = None,
    no_r_prefix: bool = False,
    allow_unclear: bool = False,
):
    map_names = core.MapNames(
        save_file, letter_code, no_r_prefix=no_r_prefix, base_index=base_index
    )

    map_choices = select_maps(save_file, chapters, letter_code, base_index, no_r_prefix)
    if map_choices is None:
        return None

    clear_all = clear_all_or_handle_ind(len(map_choices))
    if clear_all is None:
        return None

    map_option = core.MapOption.from_save(save_file)
    if map_option is None:
        return None

    if clear_all == 0:
        max_stars = get_max_max_stars(
            map_option, base_index, map_choices, chapters, type
        )
        if allow_unclear:
            stars = core.EventChapters.ask_stars_unclear(max_stars, "max_stars")
        else:
            stars = core.EventChapters.ask_stars(max_stars, "max_stars")
        if stars is None:
            return None
        for local_map_id in map_choices:
            unclear_rest(
                chapters,
                [0],
                max(0, stars - 1),
                local_map_id,
                type,
            )
            for star in range(stars):
                total_stages = get_total_stages(chapters, local_map_id, star, type)
                for stage in range(total_stages):
                    clear_stage(
                        chapters,
                        local_map_id,
                        star,
                        stage,
                        type=type,
                        ensure_cleared_only=True,
                    )

        return map_choices

    for local_map_id in map_choices:
        name = map_names.map_names.get(local_map_id)
        core.EventChapters.print_current_chapter(name, local_map_id)
        clear_whole = dialog_creator.ChoiceInput.from_reduced(
            ["clear_whole_chapter", "clear_to_specific_stage"], dialog="clear_whole_q"
        ).single_choice()
        if clear_whole is None:
            return None

        clear_whole -= 1

        if clear_whole == 0:
            max_stars = get_total_stars(
                map_option, base_index, chapters, local_map_id, type
            )
            if allow_unclear:
                stars = core.EventChapters.ask_stars_unclear(max_stars)
            else:
                stars = core.EventChapters.ask_stars(max_stars)
            if stars is None:
                return None

            unclear_rest(
                chapters,
                [0],
                max(stars - 1, 0),
                local_map_id,
                type,
            )

            for star in range(stars):
                total_stages = get_total_stages(chapters, local_map_id, star, type)
                for stage in range(total_stages):
                    clear_stage(
                        chapters,
                        local_map_id,
                        star,
                        stage,
                        type=type,
                        ensure_cleared_only=True,
                    )

        else:
            stage_names = map_names.stage_names.get(local_map_id)
            stage_names = [
                stage_name
                for stage_name in stage_names or []
                if stage_name and stage_name != "＠"
            ]
            stage_id = core.EventChapters.ask_stages_stage_names_one(stage_names)
            if stage_id is None:
                return None

            max_stars = get_total_stars(
                map_option, base_index, chapters, local_map_id, type
            )

            if allow_unclear:
                stars = core.EventChapters.ask_stars_unclear(max_stars)
            else:
                stars = core.EventChapters.ask_stars(max_stars)
            if stars is None:
                return None

            unclear_rest(
                chapters, list(range(stage_id)), max(stars - 1, 0), local_map_id, type
            )

            for star in range(stars - 1):
                total_stages = get_total_stages(chapters, local_map_id, star, type)
                for stage in range(total_stages):
                    clear_stage(
                        chapters,
                        local_map_id,
                        star,
                        stage,
                        type=type,
                        ensure_cleared_only=True,
                    )

            for stage in range(stage_id + 1):
                clear_stage(
                    chapters,
                    local_map_id,
                    stars - 1,
                    stage,
                    type=type,
                    ensure_cleared_only=True,
                )


def edit_chapters(
    save_file: core.SaveFile,
    chapters: ChaptersType,
    letter_code: str,
    base_index: int,
    type: int | None = None,
    no_r_prefix: bool = False,
) -> dict[int, bool] | None:
    while True:
        choice = dialog_creator.ChoiceInput.from_reduced(
            [
                "edit_progress_clear",
                "edit_progress_unclear",
                "edit_clear_counts",
                "finish",
            ],
            dialog="edit_chapters_q",
        ).single_choice()
        if choice is None:
            return None
        choice -= 1

        if choice == 0:
            edit_chapters2_progress(
                save_file, chapters, letter_code, base_index, type, no_r_prefix
            )
        elif choice == 1:
            edit_chapters2_progress(
                save_file,
                chapters,
                letter_code,
                base_index,
                type,
                no_r_prefix,
                allow_unclear=True,
            )
        elif choice == 2:
            edit_chapters2_clear_count(
                save_file, chapters, letter_code, base_index, type, no_r_prefix
            )
        else:
            break
        color.ColoredText.localize("map_chapters_edited")
    color.ColoredText.localize("map_chapters_edited")

    return None


# ============================================================
# FILE: max_all.py
# ============================================================
from __future__ import annotations

from collections.abc import Callable
from bcsfe import core


def max_catfood(save_file: core.SaveFile):
    orig = save_file.catfood
    save_file.catfood = core.core_data.max_value_manager.get(core.MaxValueType.CATFOOD)
    core.BackupMetaData(save_file).add_managed_item(
        core.ManagedItem.from_change(
            save_file.catfood - orig, core.ManagedItemType.CATFOOD
        )
    )


def max_rare_tickets(save_file: core.SaveFile):
    orig = save_file.rare_tickets
    save_file.rare_tickets = core.core_data.max_value_manager.get(
        core.MaxValueType.RARE_TICKETS
    )
    core.BackupMetaData(save_file).add_managed_item(
        core.ManagedItem.from_change(
            save_file.rare_tickets - orig, core.ManagedItemType.RARE_TICKET
        )
    )


def max_plat_tickets(save_file: core.SaveFile):
    orig = save_file.platinum_tickets
    save_file.platinum_tickets = core.core_data.max_value_manager.get(
        core.MaxValueType.PLATINUM_TICKETS
    )
    core.BackupMetaData(save_file).add_managed_item(
        core.ManagedItem.from_change(
            save_file.platinum_tickets - orig, core.ManagedItemType.PLATINUM_TICKET
        )
    )


def max_plat_shards(save_file: core.SaveFile):
    save_file.platinum_shards = 10 * core.core_data.max_value_manager.get(
        core.MaxValueType.PLATINUM_TICKETS
    )


def max_legend_tickets(save_file: core.SaveFile):
    orig = save_file.legend_tickets
    save_file.legend_tickets = core.core_data.max_value_manager.get(
        core.MaxValueType.LEGEND_TICKETS
    )
    core.BackupMetaData(save_file).add_managed_item(
        core.ManagedItem.from_change(
            save_file.legend_tickets - orig, core.ManagedItemType.LEGEND_TICKET
        )
    )


def max_xp(save_file: core.SaveFile):
    save_file.xp = core.core_data.max_value_manager.get(core.MaxValueType.XP)


def max_np(save_file: core.SaveFile):
    save_file.np = core.core_data.max_value_manager.get(core.MaxValueType.NP)


def max_100_million_ticket(save_file: core.SaveFile):
    save_file.hundred_million_ticket = core.core_data.max_value_manager.get(
        core.MaxValueType.HUNDRED_MILLION_TICKETS
    )


def max_leadership(save_file: core.SaveFile):
    save_file.leadership = core.core_data.max_value_manager.get(
        core.MaxValueType.LEADERSHIP
    )


def max_battle_items(save_file: core.SaveFile):
    for item in save_file.battle_items.items:
        item.amount = core.core_data.max_value_manager.get(
            core.MaxValueType.BATTLE_ITEMS
        )


def max_catseyes(save_file: core.SaveFile):
    for id in range(len(save_file.catseyes)):
        save_file.catseyes[id] = core.core_data.max_value_manager.get(
            core.MaxValueType.CATSEYES
        )


def max_treasure_chests(save_file: core.SaveFile):
    for id in range(len(save_file.treasure_chests)):
        save_file.treasure_chests[id] = core.core_data.max_value_manager.get(
            core.MaxValueType.TREASURE_CHESTS
        )


def max_catamins(save_file: core.SaveFile):
    for id in range(len(save_file.catseyes)):
        save_file.catamins[id] = core.core_data.max_value_manager.get(
            core.MaxValueType.CATAMINS
        )


def max_labyrinth_medals(save_file: core.SaveFile):
    for id in range(len(save_file.labyrinth_medals)):
        save_file.labyrinth_medals[id] = core.core_data.max_value_manager.get(
            core.MaxValueType.LABYRINTH_MEDALS
        )


# def max_catfruit(save_file: core.SaveFile):
#     for id in range(len(save_file.catfruit)):
#         save_file.catfruit[id] = core.core_data.max_value_manager.get_new(
#             core.MaxValueType.CATFRUIT
#         )


def max_normal_tickets(save_file: core.SaveFile):
    save_file.normal_tickets = core.core_data.max_value_manager.get(
        core.MaxValueType.NORMAL_TICKETS
    )


def max_all(save_file: core.SaveFile):
    maxes = core.core_data.max_value_manager
    features: dict[str, Callable[[core.SaveFile], None]] = {
        "catfood": max_catfood,
        "xp": max_xp,
        "normal_tickets": max_normal_tickets,
        "rare_tickets": max_rare_tickets,
        "platinum_tickets": max_plat_tickets,
        "legend_tickets": max_legend_tickets,
        "platinum_shards": max_plat_shards,
        "np": max_np,
        "leadership": max_leadership,
        "battle_items": max_battle_items,
        "catseyes": max_catseyes,
        "catamins": max_catamins,
        "labyrinth_medals": max_labyrinth_medals,
        "100_million_ticket": max_100_million_ticket,
        "treasure_chests": max_treasure_chests,
    }
    # TODO: finish


# ============================================================
# FILE: rare_ticket_trade.py
# ============================================================
from __future__ import annotations
from bcsfe import core

from bcsfe.cli import color, dialog_creator


class RareTicketTrade:
    @staticmethod
    def rare_ticket_trade(save_file: core.SaveFile):
        current_amount = save_file.rare_tickets
        max_amount = max(
            core.core_data.max_value_manager.get("rare_tickets")
            - current_amount,
            0,
        )
        if max_amount == 0:
            color.ColoredText.localize("rare_ticket_trade_maxed")
            return
        to_add = dialog_creator.IntInput(max_amount, 0).get_input_locale_while(
            "rare_ticket_trade_enter",
            {"max": max_amount, "current": current_amount},
        )
        if to_add is None:
            return

        space = False
        for storage_item in save_file.cats.storage_items:
            if storage_item.item_type == 0 or (
                storage_item.item_id == 1 and storage_item.item_type == 2
            ):
                storage_item.item_id = 1
                storage_item.item_type = 2
                space = True
                break

        if not space:
            color.ColoredText.localize("rare_ticket_trade_storage_full")
            return

        amount = to_add * 5
        save_file.gatya.trade_progress = amount

        color.ColoredText.localize(
            "rare_ticket_successfully_traded", rare_ticket_count=to_add
        )


# ============================================================
# FILE: storage.py
# ============================================================
from __future__ import annotations
from bcsfe import core
from bcsfe.cli import color, dialog_creator
from bcsfe.cli.edits import cat_editor


def display_storage(save_file: core.SaveFile, storage: list[core.StorageItem]):
    color.ColoredText.localize("current_storage_items")
    index = 0
    for item in storage:
        if item.item_type == 0:
            continue

        index += 1
        color.ColoredText(f"{index}. ", end="")
        display_item(item, save_file)

    if index == 0:
        color.ColoredText.localize("storage_is_empty")

    available_slots = len(storage) - index

    color.ColoredText.localize("available_storage", slots=available_slots)


def display_item(item: core.StorageItem, save_file: core.SaveFile):
    color.ColoredText(get_item_str(item, save_file))


def get_item_str(item: core.StorageItem, save_file: core.SaveFile) -> str:
    if item.item_type == 1:
        cat_id = item.item_id
        names = core.Cat.get_names(cat_id, save_file)

        if not names:
            names = [str(cat_id)]

        return core.localize("cat", name=names[0], id=cat_id)
    elif item.item_type == 2:
        skill_id = item.item_id

        skill_names = (
            core.core_data.get_gatya_item_buy(save_file).get_names_by_category(
                core.GatyaItemCategory.SPECIAL_SKILLS
            )
            or []
        )

        if skill_id >= len(skill_names) or skill_id < 0:
            name = str(skill_id)
        else:
            name = skill_names[skill_id][1]

        return core.localize("special_skill", name=name, id=skill_id)
    elif item.item_type == 3:
        item_id = item.item_id

        name = core.core_data.get_gatya_item_names(save_file).get_name(item_id)
        if name is None:
            name = str(item_id)

        return core.localize("item", name=name, id=item_id)
    else:
        return core.localize(
            "unrecognised_storage_item", item_type=item.item_type, id=item.item_id
        )


def clear_storage(storage: list[core.StorageItem]):
    for item in storage:
        item.item_id = 0
        item.item_type = 0


def add_item(storage: list[core.StorageItem], item: core.StorageItem) -> bool:
    for citem in storage:
        if citem.item_type == 0:
            citem.item_type = item.item_type
            citem.item_id = item.item_id
            return True
    return False


def get_storage_space(storage: list[core.StorageItem]) -> int:
    space = 0

    for item in storage:
        if item.item_type == 0:
            space += 1
    return space


def edit_storage(save_file: core.SaveFile):
    display_storage(save_file, save_file.cats.storage_items)
    exit = False
    while not exit:
        exit = edit_loop(save_file)

    color.ColoredText.localize("storage_success")


def edit_loop(save_file: core.SaveFile) -> bool:
    storage = save_file.cats.storage_items

    options = [
        "display_storage",
        "clear_storage",
        "add_cats",
        "add_special_skills",
        "remove_items",
        "finish",
    ]

    choice = dialog_creator.ChoiceInput.from_reduced(
        options, dialog="select_option"
    ).single_choice()
    if choice is None:
        return False

    choice -= 1

    if choice == 0:
        display_storage(save_file, storage)
    if choice == 1:
        clear_storage(storage)
    elif choice == 2:
        editor, cats = cat_editor.CatEditor.from_save_file(save_file)
        if editor is None:
            return False

        space = get_storage_space(storage)
        if len(cats) > len(storage):
            color.ColoredText.localize(
                "too_many_cats_selected", max=len(storage), current=len(cats)
            )
            return False

        needs = len(cats) - space
        if needs > 0:
            color.ColoredText.localize("need_x_more_space", needs=needs)
            return False

        color.ColoredText.localize("added_cats")
        for cat in cats:
            item = core.StorageItem.from_cat(cat.id)
            add_item(storage, item)
            display_item(item, save_file)
    elif choice == 3:

        skill_names: list[str] = list(
            map(
                lambda sk: sk[1] or str(sk[0].id),
                core.core_data.get_gatya_item_buy(save_file).get_names_by_category(
                    core.GatyaItemCategory.SPECIAL_SKILLS
                )
                or [],
            )
        )

        options, _ = dialog_creator.ChoiceInput.from_reduced(
            skill_names, localize_options=False, dialog="select_special_skills"
        ).multiple_choice(False)

        if options is None:
            return False

        space = get_storage_space(storage)
        if len(options) > len(storage):
            color.ColoredText.localize(
                "too_many_skills_selected", max=len(storage), current=len(options)
            )
            return False

        needs = len(options) - space
        if needs > 0:
            color.ColoredText.localize("need_x_more_space", needs=needs)
            return False

        color.ColoredText.localize("added_special_skills")
        for choice in options:
            item = core.StorageItem.from_special_skill(choice)
            add_item(storage, item)
            display_item(item, save_file)

    elif choice == 4:
        options2: list[str] = []
        for item in storage:
            if item.item_type == 0:
                continue
            options2.append(get_item_str(item, save_file))

        choices, _ = dialog_creator.ChoiceInput.from_reduced(
            options2, localize_options=False
        ).multiple_choice(False)
        if choices is None:
            return False

        color.ColoredText.localize("removed_items")
        index = 0
        for item in storage:
            if item.item_type == 0:
                continue

            if index in choices:
                display_item(item, save_file)
                item.item_type = 0
                item.item_id = 0

            index += 1

    elif choice == 5:
        return True

    return False

