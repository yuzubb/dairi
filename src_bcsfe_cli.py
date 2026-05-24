# === COMBINED FILE ===
# フォルダ: src_bcsfe_cli
# 元ファイル(9件): __init__.py, color.py, dialog_creator.py, feature_handler.py, file_dialog.py, main.py, recent_saves.py, save_management.py, server_cli.py

# ============================================================
# FILE: __init__.py
# ============================================================
from bcsfe.cli import (
    color,
    dialog_creator,
    main,
    file_dialog,
    feature_handler,
    save_management,
    server_cli,
    edits,
    recent_saves,
)

__all__ = [
    "color",
    "dialog_creator",
    "main",
    "file_dialog",
    "feature_handler",
    "save_management",
    "server_cli",
    "edits",
    "recent_saves",
]


# ============================================================
# FILE: color.py
# ============================================================
from __future__ import annotations
from typing import Any
from aenum import NamedConstant  # type: ignore
import colored  # type: ignore
from bcsfe import core


class ColorHex(NamedConstant):
    GREEN = "#008000"
    G = GREEN
    RED = "#FF0000"
    R = RED
    DARK_YELLOW = "#D7C32A"
    DY = DARK_YELLOW
    BLACK = "#000000"
    BL = BLACK
    WHITE = "#FFFFFF"
    W = WHITE
    CYAN = "#00FFFF"
    C = CYAN
    DARK_GREY = "#A9A9A9"
    DG = DARK_GREY
    BLUE = "#0000FF"
    B = BLUE
    YELLOW = "#FFFF00"
    Y = YELLOW
    MAGENTA = "#FF00FF"
    M = MAGENTA
    DARK_BLUE = "#00008B"
    DB = DARK_BLUE
    DARK_CYAN = "#008B8B"
    DC = DARK_CYAN
    DARK_MAGENTA = "#8B008B"
    DM = DARK_MAGENTA
    DARK_RED = "#8B0000"
    DR = DARK_RED
    DARK_GREEN = "#006400"
    DGN = DARK_GREEN
    LIGHT_GREY = "#D3D3D3"
    LG = LIGHT_GREY
    ORANGE = "#FFA500"
    O = ORANGE

    @staticmethod
    def from_name(name: str) -> str:
        if name == "":
            return ""
        return getattr(ColorHex, name.upper())


class ColorHelper:
    def __init__(self):
        self.theme_handler = core.core_data.theme_manager

    def get_color(self, color_name: str) -> str:
        try:
            first_char = color_name[0]
        except IndexError:
            return ""
        if first_char == "#":
            return color_name
        if first_char == "@":
            try:
                second_char = color_name[1]
            except IndexError:
                return ""
            try:
                third_char = color_name[2]
            except IndexError:
                third_char = ""
            if second_char == "p":
                return self.theme_handler.get_primary_color()
            if second_char == "s" and third_char != "u":
                return self.theme_handler.get_secondary_color()
            if second_char == "t":
                return self.theme_handler.get_tertiary_color()
            if second_char == "q":
                return self.theme_handler.get_quaternary_color()
            if second_char == "e":
                return self.theme_handler.get_error_color()
            if second_char == "w":
                return self.theme_handler.get_warning_color()
            if second_char == "s" and third_char == "u":
                return self.theme_handler.get_success_color()
            return self.theme_handler.get_theme_color(color_name[1:])
        try:
            return ColorHex.from_name(color_name)
        except AttributeError:
            return ""


class ColoredText:
    def __init__(self, string: str, end: str = "\n") -> None:
        string = string.replace("\\n", "\n")
        self.string = string
        self.end = end
        self.color_helper = ColorHelper()
        self.display(string)

    def display(self, string: str) -> None:
        text_data = self.parse(string)
        for i, (text, color) in enumerate(text_data):
            if i == len(text_data) - 1:
                text += self.end
            if color == "":
                print(text, end="")
            else:
                try:
                    fg = colored.fg(color)  # type: ignore
                except Exception:
                    print(text, end="")
                    continue
                print(colored.stylize(text, fg), end="")  # type: ignore

    @staticmethod
    def localize(string: str, escape: bool = True, **kwargs: Any) -> ColoredText:
        return ColoredText(
            core.core_data.local_manager.get_key(string, escape=escape, **kwargs)
        )

    def parse(self, txt: str) -> list[tuple[str, str]]:
        txt = "<@p>" + txt + "</>"
        output: list[tuple[str, str]] = []
        i = 0
        tags: list[str] = []
        inside_tag = False
        in_closing_tag = False
        tag_text = ""
        text = ""
        special_chars = core.LocalManager.get_special_chars()
        while i < len(txt):
            char = txt[i]
            if char == "\\" and i + 1 < len(txt) and txt[i + 1] in special_chars:
                i += 1
                char = txt[i]
                text += char
                i += 1
                continue
            if tags:
                tag = tags[-1]
            else:
                tag = ""
            if char == ">" and inside_tag:
                inside_tag = False
                if not in_closing_tag:
                    tags.append(tag_text)
                if in_closing_tag:
                    in_closing_tag = False
                tag_text = ""
            if char == "<" and not inside_tag:
                inside_tag = True
                if text:
                    color = self.color_helper.get_color(tag)
                    output.append((text, color))
                    text = ""
                    tag_text = ""
            if char == "/" and inside_tag:
                in_closing_tag = True
                if tags:
                    tags.pop()
            if not inside_tag and char != ">" and char != "<":
                text += char
            if inside_tag and char != "<" and char != ">":
                tag_text += char
            i += 1
        return output


class ColoredInput:
    def __init__(self, end: str = "") -> None:
        self.end = end

    def get(self, display_string: str) -> str:
        ColoredText(display_string, end=self.end)
        return input()

    def localize(self, string: str, escape: bool = True, **kwargs: Any) -> str:
        text = core.core_data.local_manager.get_key(string, escape=escape, **kwargs)
        return self.get(text)


# ============================================================
# FILE: dialog_creator.py
# ============================================================
from __future__ import annotations
from typing import Any
from bcsfe import core
from bcsfe.cli import color


class RangeInput:
    def __init__(self, max: int | None = None, min: int = 0):
        self.max = max
        self.min = min

    def clamp_value(self, value: int) -> int:
        if self.max is None:
            return max(value, self.min)
        return max(min(value, self.max), self.min)

    def get_input_locale(
        self,
        dialog: str,
        perameters: dict[str, int | str],
        escape: bool = True,
    ) -> list[int] | None:
        user_input = color.ColoredInput(end="").localize(
            dialog, escape=escape, **perameters
        )
        return self.parse(user_input)

    def parse(self, user_input: str) -> list[int] | None:
        if user_input == "":
            return []
        if user_input == core.core_data.local_manager.get_key("quit_key"):
            return None
        parts = user_input.split(" ")
        ids: list[int] = []
        all_text = core.core_data.local_manager.get_key("all")
        for part in parts:
            if "-" in part and len(part.split("-")) == 2:
                lower, upper = part.split("-")
                try:
                    lower = int(lower)
                    upper = int(upper)
                except ValueError:
                    continue
                if lower > upper:
                    lower, upper = upper, lower
                if self.max is not None:
                    lower = max(lower, self.min)
                    upper = min(upper, self.max)
                else:
                    lower = max(lower, self.min)
                ids.extend(range(lower, upper + 1))
            elif part.lower() == all_text.lower() and self.max is not None:
                ids.extend(range(self.min, self.max + 1))
            else:
                try:
                    part = int(part)
                except ValueError:
                    continue
                if self.max is not None:
                    part = max(part, self.min)
                    part = min(part, self.max)
                else:
                    part = max(part, self.min)
                ids.append(part)
        return ids


class IntInput:
    def __init__(
        self,
        max: int | None = None,
        min: int = 0,
        default: int | None = None,
        signed: bool = True,
        bit_count: int = 32,
        ensure_max: bool = False,
    ):
        self.signed = signed
        self.bit_count = bit_count
        self.max = self.get_max_value(max, signed, bit_count, ensure_max)
        self.min = min
        self.default = default

    @staticmethod
    def get_max_value(
        max: int | None,
        signed: bool = True,
        bit_count: int = 32,
        ensure_max: bool = False,
    ) -> int:
        disable_maxes = (
            core.core_data.config.get_bool(core.ConfigKey.DISABLE_MAXES)
            and not ensure_max
        )
        if signed:
            bit_count -= 1
        max_int = (2**bit_count) - 1
        if disable_maxes or max is None:
            return max_int
        return min(max, max_int)

    def clamp_value(self, value: int) -> int:
        return max(min(value, self.max), self.min)

    def get_input(
        self,
        localization_key: str,
        perameters: dict[str, int | str],
        escape: bool = True,
    ) -> tuple[int | None, str]:
        user_input = color.ColoredInput(end="").localize(
            localization_key, escape=escape, **perameters
        )
        if user_input == "" and self.default is not None:
            return self.default, user_input
        try:
            user_input_i = int(user_input)
        except ValueError:
            return None, user_input

        return self.clamp_value(user_input_i), user_input

    def get_input_locale_while(
        self, dialog: str, perameters: dict[str, int | str], escape: bool = True
    ) -> int | None:
        while True:
            int_val, user_input = self.get_input(dialog, perameters, escape=escape)
            if int_val is not None:
                return int_val
            if user_input == core.core_data.local_manager.get_key("quit_key"):
                return None

    def get_input_locale(
        self, localization_key: str | None, perameters: dict[str, int | str]
    ) -> tuple[int | None, str]:
        if localization_key is None:
            if self.default is not None:
                perameters = {
                    "min": self.min,
                    "max": self.max,
                    "default": self.default,
                }
                localization_key = "input_int_default"
            else:
                perameters = {"min": self.min, "max": self.max}
                localization_key = "input_int"
        return self.get_input(localization_key, perameters)

    def get_basic_input_locale(self, localization_key: str, perameters: dict[str, Any]):
        try:
            user_input = int(
                color.ColoredInput(end="").localize(localization_key, **perameters)
            )
        except ValueError:
            return None
        return user_input


class ListOutput:
    def __init__(
        self,
        strings: list[str],
        ints: list[int] | list[str],
        dialog: str | None = None,
        perameters: dict[str, Any] | None = None,
        start_index: int = 1,
        localize_elements: bool = True,
    ):
        self.strings = strings
        self.ints = ints
        self.dialog = dialog
        if perameters is None:
            perameters = {}
        self.perameters = perameters
        self.start_index = start_index
        self.localize_elements = localize_elements

    def get_output(self, dialog: str | None, strings: list[str]) -> str:
        end_string = ""
        if dialog is not None:
            end_string = core.core_data.local_manager.get_key(dialog, **self.perameters)
        end_string += "\n"
        for i, string in enumerate(strings):
            try:
                int_string = str(self.ints[i])
            except IndexError:
                int_string = ""

            string = string.replace("{int}", int_string)
            end_string += f" <@s>{i + self.start_index}.</> <@t>{string}</>\n"
        end_string = end_string.strip("\n")
        return end_string

    def display(self, dialog: str | None, strings: list[str]) -> None:
        output = self.get_output(dialog, strings)
        color.ColoredText(output)

    def display_locale(self, remove_alias: bool = False) -> None:
        dialog = ""
        if self.dialog is not None:
            dialog = core.core_data.local_manager.get_key(self.dialog)
        new_strings: list[str] = []
        for string in self.strings:
            if self.localize_elements:
                string_ = core.core_data.local_manager.get_key(string)
            else:
                string_ = string
            if remove_alias:
                string_ = core.core_data.local_manager.get_all_aliases(string_)[0]
            new_strings.append(string_)

        self.display(dialog, new_strings)

    def display_non_locale(self) -> None:
        self.display(self.dialog, self.strings)


class ChoiceInput:
    def __init__(
        self,
        items: list[str],
        strings: list[str],
        ints: list[int] | list[str],
        perameters: dict[str, int | str],
        dialog: str,
        single_choice: bool = False,
        remove_alias: bool = False,
        display_all_at_once: bool = True,
        start_index: int = 1,
        localize_options: bool = True,
    ):
        self.items = items
        self.strings = strings
        self.ints = ints
        self.perameters = perameters
        self.dialog = dialog
        self.is_single_choice = single_choice
        self.remove_alias = remove_alias
        self.display_all_at_once = display_all_at_once
        self.start_index = start_index
        self.localize_options = localize_options

    @staticmethod
    def from_reduced(
        items: list[str],
        ints: list[int] | list[str] | None = None,
        perameters: dict[str, int | str] | None = None,
        dialog: str | None = None,
        single_choice: bool = False,
        remove_alias: bool = False,
        display_all_at_once: bool = True,
        start_index: int = 1,
        localize_options: bool = True,
    ) -> ChoiceInput:
        if perameters is None:
            perameters = {}
        if ints is None:
            ints = []
        if dialog is None:
            dialog = ""
        return ChoiceInput(
            items.copy(),
            items.copy(),
            ints.copy(),
            perameters.copy(),
            dialog,
            single_choice,
            remove_alias,
            display_all_at_once,
            start_index,
            localize_options,
        )

    def get_input(self) -> tuple[int | None, str]:
        if len(self.strings) == 0:
            return None, ""
        if len(self.strings) == 1:
            return self.get_min_value(), ""
        ListOutput(
            self.strings,
            self.ints,
            start_index=self.start_index,
            localize_elements=self.localize_options,
        ).display_locale(self.remove_alias)
        return IntInput(
            self.get_max_value(), self.get_min_value(), ensure_max=True
        ).get_input_locale(self.dialog, self.perameters)

    def get_input_while(self) -> int | None:
        if len(self.strings) == 0:
            return None
        while True:
            int_val, user_input = self.get_input()
            if int_val is not None:
                return int_val
            if user_input == core.core_data.local_manager.get_key("quit_key"):
                return None
            for i, string in enumerate(self.strings):
                if self.localize_options:
                    string = core.core_data.local_manager.get_key(string)
                if string.lower().strip() == user_input.lower().strip():
                    return i + self.start_index

    def get_max_value(self) -> int:
        return len(self.strings) + self.start_index - 1

    def get_min_value(self) -> int:
        return self.start_index

    def get_input_locale(self, localized: bool = True) -> tuple[list[int] | None, bool]:
        if len(self.strings) == 0:
            return [], False
        if len(self.strings) == 1:
            return [self.get_min_value()], False
        if not self.is_single_choice and self.display_all_at_once:
            if localized:
                self.strings.append("all_at_once")
            else:
                self.strings.append(core.core_data.local_manager.get_key("all_at_once"))
        if localized:
            ListOutput(
                self.strings,
                self.ints,
                start_index=self.start_index,
                localize_elements=self.localize_options,
            ).display_locale()
        else:
            ListOutput(
                self.strings,
                self.ints,
                start_index=self.start_index,
                localize_elements=self.localize_options,
            ).display_non_locale()
        key = "input_many"
        if self.is_single_choice:
            key = "input_single"
        dialog = core.core_data.local_manager.get_key(key).format(
            min=self.get_min_value(), max=self.get_max_value()
        )
        usr_input = color.ColoredInput().get(dialog).strip().split(" ")
        int_vals: list[int] = []
        for inp in usr_input:
            try:
                value = int(inp)
                if value > self.get_max_value() or value < self.get_min_value():
                    raise ValueError
                int_vals.append(value)
            except ValueError:
                if inp == core.core_data.local_manager.get_key("quit_key"):
                    return None, False

                cont = False
                for i, string in enumerate(self.strings):
                    if self.localize_options:
                        string = core.core_data.local_manager.get_key(string)
                    if string.lower().strip() == inp.lower().strip():
                        int_vals.append(i + self.start_index)
                        cont = True
                        break

                if cont:
                    continue

                color.ColoredText.localize(
                    "invalid_input_int",
                    min=self.get_min_value(),
                    max=self.get_max_value(),
                )
        if (
            self.get_max_value() in int_vals
            and not self.is_single_choice
            and self.display_all_at_once
        ):
            return list(range(self.get_min_value(), self.get_max_value())), True

        if self.is_single_choice and len(int_vals) > 1:
            int_vals = [int_vals[0]]

        return int_vals, False

    def get_input_locale_while(self) -> list[int] | None:
        if len(self.strings) == 0:
            return []
        if len(self.strings) == 1:
            return [self.get_min_value()]
        while True:
            int_vals, all_at_once = self.get_input_locale()
            if int_vals is None:
                return None
            if all_at_once:
                return int_vals
            if len(int_vals) == 0:
                continue
            if len(int_vals) == 1 and int_vals[0] == 0:
                return []
            return int_vals

    def multiple_choice(
        self, localized_options: bool = True
    ) -> tuple[list[int] | None, bool]:
        color.ColoredText.localize(self.dialog, True, **self.perameters)
        user_input, all_at_once = self.get_input_locale(localized_options)
        if user_input is None:
            return None, all_at_once
        return [i - self.start_index for i in user_input], all_at_once

    def single_choice(self) -> int | None:
        return self.get_input_while()

    def get(self) -> tuple[int | None | list[int], bool]:
        if self.is_single_choice:
            return self.single_choice(), False
        return self.multiple_choice()


class MultiEditor:
    def __init__(
        self,
        group_name: str,
        items: list[str],
        strings: list[str],
        ints: list[int] | None,
        max_values: list[int] | int | None,
        perameters: dict[str, int | str] | None,
        dialog: str,
        single_choice: bool = False,
        signed: bool = True,
        group_name_localized: bool = False,
        cumulative_max: bool = False,
        bit_count: int = 32,
    ):
        self.items = items
        self.strings = strings
        self.ints = ints
        self.bit_count = bit_count
        if self.ints is not None:
            total_ints = len(self.ints)
        else:
            total_ints = len(self.strings)
        if max_values is None:
            max_values_ = [None] * total_ints
        elif isinstance(max_values, int):
            max_values_ = [max_values] * total_ints
        else:
            max_values_ = max_values
        self.max_values = max_values_
        if perameters is None:
            perameters = {}
        self.perameters = perameters
        if group_name_localized:
            self.perameters["group_name"] = core.core_data.local_manager.get_key(
                group_name
            )
        else:
            self.perameters["group_name"] = group_name
        self.dialog = dialog
        self.is_single_choice = single_choice
        self.signed = signed
        self.cumulative_max = cumulative_max

    @staticmethod
    def from_reduced(
        group_name: str,
        items: list[str],
        ints: list[int] | None,
        max_values: list[int] | int | None,
        group_name_localized: bool = False,
        dialog: str = "input",
        cumulative_max: bool = False,
        items_localized: bool = False,
    ):
        if items_localized:
            for i, item in enumerate(items):
                items[i] = core.core_data.local_manager.get_key(item)
        text: list[str] = []
        for item_name in items:
            if ints is not None:
                text.append(f"{item_name} <@q>: {{int}}</>")
            else:
                text.append(f"{item_name}")
        return MultiEditor(
            group_name,
            items,
            text,
            ints,
            max_values,
            None,
            dialog,
            group_name_localized=group_name_localized,
            cumulative_max=cumulative_max,
        )

    def edit(self) -> list[int]:
        choices, all_at_once = ChoiceInput(
            self.items,
            self.strings,
            self.ints or [],  # type: ignore
            self.perameters,
            "select_edit",
        ).get()
        if choices is None:
            return self.ints or []
        if isinstance(choices, int):
            choices = [choices]
        if all_at_once:
            return self.edit_all(choices)
        return self.edit_one(choices)

    def edit_all(self, choices: list[int]) -> list[int]:
        max_max_value = 0
        for choice in choices:
            if choice >= len(self.max_values):
                max_value = None
            else:
                max_value = self.max_values[choice]
            if max_value is None:
                max_value = IntInput.get_max_value(
                    max_value, self.signed, self.bit_count
                )
            max_max_value = max(max_max_value, max_value)
        if self.cumulative_max:
            max_max_value = max_max_value // len(choices)
        usr_input = IntInput(max_max_value, default=None).get_input_locale_while(
            self.dialog + "_all",
            {
                "name": self.perameters["group_name"],
                "max": max_max_value,
            },
        )
        if usr_input is None:
            return self.ints or []
        ints = self.ints or [0] * len(self.strings)

        for choice in choices:
            if choice >= len(self.max_values):
                max_value = None
            else:
                max_value = self.max_values[choice]
            max_value = IntInput.get_max_value(max_value, self.signed, self.bit_count)
            value = min(usr_input, max_value)
            ints[choice] = value
            if self.ints is not None:
                color.ColoredText.localize(
                    "value_changed",
                    name=self.items[choice],
                    value=value,
                )

        return ints

    def edit_one(self, choices: list[int]) -> list[int]:
        ints = self.ints or [0] * len(self.strings)

        for choice in choices:
            if choice >= len(self.max_values):
                max_value = None
            else:
                max_value = self.max_values[choice]
            if max_value is None:
                max_value = IntInput.get_max_value(
                    max_value, self.signed, self.bit_count
                )

            if self.cumulative_max:
                max_value -= sum(ints) - ints[choice]
                max_value = max(max_value, 0)

            item = self.items[choice]
            usr_input = IntInput(
                max_value, default=ints[choice]
            ).get_input_locale_while(
                self.dialog,
                {"name": item, "value": ints[choice], "max": max_value},
                escape=False,
            )
            if usr_input is None:
                continue
            ints[choice] = usr_input
            color.ColoredText.localize(
                "value_changed", name=item, value=ints[choice], escape=False
            )
        return ints


class SingleEditor:
    def __init__(
        self,
        item: str,
        value: int,
        max_value: int | None = None,
        min_value: int = 0,
        signed: bool = True,
        localized_item: bool = False,
        remove_alias: bool = False,
        bit_count: int = 32,
    ):
        if localized_item:
            item = core.core_data.local_manager.get_key(item)
        if remove_alias:
            item = core.core_data.local_manager.get_all_aliases(item)[0]
        self.item = item
        self.value = value
        self.max_value = max_value
        self.min_value = min_value
        self.signed = signed
        self.bit_count = bit_count

    def edit(self, escape_text: bool = True) -> int:
        max_value = IntInput.get_max_value(self.max_value, self.signed, self.bit_count)
        if self.max_value is None:
            dialog = "input_non_max"
        elif self.min_value != 0:
            dialog = "input_min"
        else:
            dialog = "input"
        usr_input = IntInput(
            max_value,
            self.min_value,
            default=self.value,
            signed=self.signed,
            bit_count=self.bit_count,
        ).get_input_locale_while(
            dialog,
            {
                "name": self.item,
                "value": self.value,
                "max": max_value,
                "min": self.min_value,
            },
            escape=escape_text,
        )
        if usr_input is None:
            return self.value
        print()
        color.ColoredText.localize(
            "value_changed", name=self.item, value=usr_input, escape=escape_text
        )
        return usr_input


class StringInput:
    def __init__(self, default: str = ""):
        self.default = default

    def get_input_locale_while(
        self, key: str, perameters: dict[str, Any]
    ) -> str | None:
        while True:
            usr_input = self.get_input_locale(key, perameters)
            if usr_input is None:
                return None
            if usr_input == "":
                return self.default
            if usr_input == " ":
                continue
            return usr_input

    def get_input_locale(
        self,
        key: str,
        perameters: dict[str, Any] | None = None,
        escape: bool = True,
    ) -> str | None:
        if perameters is None:
            perameters = {}
        usr_input = color.ColoredInput().localize(key, escape, **perameters)
        quit_key = core.core_data.local_manager.get_key("quit_key")
        if usr_input == "" or usr_input == quit_key:
            return None
        if usr_input == f"\\{quit_key}":
            return quit_key
        return usr_input


class StringEditor:
    def __init__(self, item: str, value: str, item_localized: bool = False):
        if item_localized:
            item = core.core_data.local_manager.get_key(item)
        self.item = item
        self.value = value

    def edit(self) -> str:
        usr_input = StringInput(default=self.value).get_input_locale_while(
            "input_non_max",
            {"name": self.item, "value": self.value},
        )
        if usr_input is None:
            return self.value
        color.ColoredText.localize(
            "value_changed",
            name=self.item,
            value=usr_input,
        )
        return usr_input


class YesNoInput:
    def __init__(self, default: bool = False):
        self.default = default

    def get_input_once(
        self, key: str, perameters: dict[str, Any] | None = None
    ) -> bool | None:
        if perameters is None:
            perameters = {}
        usr_input = color.ColoredInput().localize(key, **perameters)
        if usr_input == "":
            return self.default

        if usr_input == core.core_data.local_manager.get_key("quit_key"):
            return None
        return (
            usr_input == core.core_data.local_manager.get_key("yes_key")
            or usr_input.lower().strip()
            == core.core_data.local_manager.get_key("yes").lower().strip()
        )


class DialogBuilder:
    def __init__(self, dialog_structure: dict[Any, Any]):
        self.dialog_structure = dialog_structure


# ============================================================
# FILE: feature_handler.py
# ============================================================
from __future__ import annotations
from typing import Any, Callable
from bcsfe import core
from bcsfe.cli import dialog_creator, color, edits, save_management, main


class FeatureHandler:
    def __init__(self, save_file: core.SaveFile):
        self.save_file = save_file

    def get_features(self):
        cat_features = {"cats": edits.cat_editor.CatEditor.edit_cats}
        if core.core_data.config.get_bool(core.ConfigKey.SEPARATE_CAT_EDIT_OPTIONS):
            cat_features = {
                "unlock_remove_cats": edits.cat_editor.CatEditor.unlock_remove_cats_run,
                "upgrade_cats": edits.cat_editor.CatEditor.upgrade_cats_run,
                "true_form_remove_form_cats": edits.cat_editor.CatEditor.true_form_remove_form_cats_run,
                "force_true_form_cats": edits.cat_editor.CatEditor.force_true_form_cats_run,
                "fourth_form_remove_form_cats": edits.cat_editor.CatEditor.fourth_form_remove_form_cats_run,
                "force_fourth_form_cats": edits.cat_editor.CatEditor.force_fourth_form_cats_run,
                "upgrade_talents_remove_talents_cats": edits.cat_editor.CatEditor.upgrade_talents_remove_talents_cats_run,
                "unlock_remove_cat_guide": edits.cat_editor.CatEditor.unlock_cat_guide_remove_guide_run,
            }

        cat_features["special_skills"] = (
            edits.basic_items.BasicItems.edit_special_skills
        )

        cat_features["cat_storage"] = edits.storage.edit_storage

        features: dict[str, Any] = {
            "save_management": {
                "save_save": save_management.SaveManagement.save_save,
                "save_upload": save_management.SaveManagement.save_upload,
                "save_save_file": save_management.SaveManagement.save_save_dialog,
                "save_save_documents": save_management.SaveManagement.save_save_documents,
                "waydroid_push": save_management.SaveManagement.waydroid_push,
                "waydroid_push_rerun": save_management.SaveManagement.waydroid_push_rerun,
                "adb_push": save_management.SaveManagement.adb_push,
                "adb_push_rerun": save_management.SaveManagement.adb_push_rerun,
                "root_push": save_management.SaveManagement.root_push,
                "root_push_rerun": save_management.SaveManagement.root_push_rerun,
                "export_save": save_management.SaveManagement.export_save,
                "load_save": save_management.SaveManagement.load_save,
                # "init_save": save_management.SaveManagement.init_save,
                "convert_region": save_management.SaveManagement.convert_save_cc,
                "convert_version": save_management.SaveManagement.convert_save_gv,
            },
            "items": {
                "catfood": edits.basic_items.BasicItems.edit_catfood,
                "xp": edits.basic_items.BasicItems.edit_xp,
                "normal_tickets": edits.basic_items.BasicItems.edit_normal_tickets,
                "rare_tickets": edits.basic_items.BasicItems.edit_rare_tickets,
                "rare_ticket_trade_feature_name": edits.rare_ticket_trade.RareTicketTrade.rare_ticket_trade,
                "platinum_tickets": edits.basic_items.BasicItems.edit_platinum_tickets,
                "legend_tickets": edits.basic_items.BasicItems.edit_legend_tickets,
                "platinum_shards": edits.basic_items.BasicItems.edit_platinum_shards,
                "np": edits.basic_items.BasicItems.edit_np,
                "leadership": edits.basic_items.BasicItems.edit_leadership,
                "battle_items": edits.basic_items.BasicItems.edit_battle_items,
                "battle_items_endless": edits.basic_items.BasicItems.edit_battle_items_endless,
                "catseyes": edits.basic_items.BasicItems.edit_catseyes,
                "catfruit": edits.basic_items.BasicItems.edit_catfruit,
                "talent_orbs": core.game.catbase.talent_orbs.SaveOrbs.edit_talent_orbs,
                "catamins": edits.basic_items.BasicItems.edit_catamins,
                "scheme_items": edits.basic_items.BasicItems.edit_scheme_items,
                "labyrinth_medals": edits.basic_items.BasicItems.edit_labyrinth_medals,
                "100_million_tickets": edits.basic_items.BasicItems.edit_100_million_ticket,
                "event_tickets": edits.event_tickets.EventTickets.edit,
                "treasure_chests": edits.basic_items.BasicItems.edit_treasure_chests,
                "reset_golden_cat_cpus": edits.basic_items.BasicItems.reset_golden_cat_cpus,
            },
            "cats_special_skills": cat_features,
            "levels": {
                "clear_tutorial": edits.clear_tutorial.clear_tutorial,
                "clear_story": core.game.map.story.StoryChapters.clear_story,
                "challenge_score": core.game.map.challenge.edit_challenge_score,
                "dojo_score": core.game.map.dojo.edit_dojo_score,
                "add_enigma_stages": core.game.map.enigma.edit_enigma,
                "clear_enigma_stages": core.game.map.gauntlets.GauntletChapters.edit_enigma_stages,
                "unlock_aku_realm": edits.aku_realm.unlock_aku_realm,
                "story_treasures": core.game.map.story.StoryChapters.edit_treasures,
                "outbreaks": core.game.map.outbreaks.Outbreaks.edit_outbreaks,
                "aku_chapters": core.game.map.aku.AkuChapters.edit_aku_chapters,
                "itf_timed_scores": core.game.map.story.StoryChapters.edit_itf_timed_scores,
                "filibuster_reclearing": edits.basic_items.BasicItems.allow_filibuster_stage_reclearing,
                "sol": core.game.map.event.EventChapters.edit_sol_chapters,
                "event": core.game.map.event.EventChapters.edit_event_chapters,
                "collab": core.game.map.event.EventChapters.edit_collab_chapters,
                "gauntlets": core.game.map.gauntlets.GauntletChapters.edit_gauntlets,
                "collab_gauntlets": core.game.map.gauntlets.GauntletChapters.edit_collab_gauntlets,
                "uncanny": core.game.map.uncanny.UncannyChapters.edit_uncanny,
                "catamin_stages": core.game.map.uncanny.UncannyChapters.edit_catamin_stages,
                "behemoth_culling": core.game.map.gauntlets.GauntletChapters.edit_behemoth_culling,
                "legend_quest": core.game.map.legend_quest.LegendQuestChapters.edit_legend_quest,
                "towers": core.game.map.tower.TowerChapters.edit_towers,
                "zero_legends": core.game.map.zero_legends.ZeroLegendsChapters.edit_zero_legends,
                "dojo_catclaw_championships": core.game.map.zero_legends.ZeroLegendsChapters.edit_catclaw_championships,
            },
            "gamototo": {
                "engineers": edits.basic_items.BasicItems.edit_engineers,
                "base_materials": edits.basic_items.BasicItems.edit_base_materials,
                "gamatoto_xp_level": core.game.gamoto.gamatoto.edit_xp,
                "gamatoto_helpers": core.game.gamoto.gamatoto.edit_helpers,
                "ototo_cat_cannon": core.game.gamoto.ototo.edit_cannon,
                "cat_shrine": core.game.gamoto.cat_shrine.CatShrine.edit_catshrine,
            },
            "account": {
                "unban_account": save_management.SaveManagement.unban_account,
                "upload_items": save_management.SaveManagement.upload_items,
                "inquiry_code": edits.basic_items.BasicItems.edit_inquiry_code,
                "password_refresh_token": edits.basic_items.BasicItems.edit_password_refresh_token,
            },
            "gatya": {
                "rare_gatya_seed": edits.basic_items.BasicItems.edit_rare_gatya_seed,
                "normal_gatya_seed": edits.basic_items.BasicItems.edit_normal_gatya_seed,
                "event_gatya_seed": edits.basic_items.BasicItems.edit_event_gatya_seed,
            },
            "fixes": {
                "fix_gamatoto_crash": edits.fixes.Fixes.fix_gamatoto_crash,
                "fix_ototo_crash": edits.fixes.Fixes.fix_ototo_crash,
                "fix_time_errors": edits.fixes.Fixes.fix_time_errors,
                "unlock_equip_menu": edits.basic_items.BasicItems.unlock_equip_menu,
                "fix_officer_pass_crash": core.OfficerPass.fix_crash,
            },
            "other": {
                "unlocked_slots": edits.basic_items.BasicItems.edit_unlocked_slots,
                "reset_gambling_events": core.GamblingEvent.reset_events,
                "restart_pack": edits.basic_items.BasicItems.set_restart_pack,
                "special_skills": edits.basic_items.BasicItems.edit_special_skills,
                "playtime": core.game.catbase.playtime.edit,
                "enemy_guide": edits.enemy_editor.EnemyEditor.edit_enemy_guide,
                "user_rank_rewards": core.game.catbase.user_rank_rewards.edit_user_rank_rewards,
                "unlock_equip_menu": edits.basic_items.BasicItems.unlock_equip_menu,
                "gold_pass": core.game.catbase.nyanko_club.NyankoClub.edit_gold_pass,
                "medals": core.game.catbase.medals.Medals.edit_medals,
                "missions": core.game.catbase.mission.Missions.edit_missions,
            },
            "config": core.core_data.config.edit_config,
            "update_external": core.update_external_content,
            "exit": main.Main.exit_editor,
        }
        return features

    def get_feature(self, feature_name: str):
        feature_path = feature_name.split(".")
        feature_dict = self.get_features()
        feature = feature_dict
        for path in feature_path:
            feature = feature[path]

        return feature

    def search_features(
        self,
        name: str,
        parent_path: str = "",
        features: dict[str, Any] | None = None,
        found_features: dict[str, int] | None = None,
    ) -> dict[str, int]:
        name = name.lower()
        if features is None:
            features = self.get_features()
        if found_features is None:
            found_features = {}

        for feature_name_key, feature in features.items():
            feature_name = core.core_data.local_manager.get_key(feature_name_key)
            path = (
                f"{parent_path}.{feature_name_key}" if parent_path else feature_name_key
            )
            if isinstance(feature, dict):
                found_features.update(
                    self.search_features(
                        name,
                        path,
                        feature,  # type: ignore
                        found_features,
                    )
                )
            for alias in core.LocalManager.get_all_aliases(feature_name):
                if not name:
                    found_features[path] = 100
                    break
                alias = alias.lower()

                name = name.replace(" ", "")
                alias = alias.replace(" ", "")
                if alias in name or name in alias:
                    found_features[path] = 100
                break

        return found_features

    def display_features(self, features: list[str]):
        feature_names: list[str] = []
        for feature_name in features:
            feature_names.append(feature_name.split(".")[-1])
        print()
        dialog_creator.ListOutput(feature_names, [], "features", {}).display_locale(
            remove_alias=True
        )

    def select_features(self, features: list[str], parent_path: str = "") -> list[str]:
        if features != list(self.get_features().keys()):
            features.insert(0, "go_back")
        self.display_features(features)
        print()
        usr_input = color.ColoredInput().localize("select_features").strip()
        selected_features: list[str] = []
        if usr_input.isdigit():
            usr_input = int(usr_input)
            if usr_input > len(features):
                color.ColoredText.localize("invalid_input")
            elif usr_input < 1:
                color.ColoredText.localize("invalid_input")
            else:
                feature_name_top = features[usr_input - 1]
                if feature_name_top == "go_back":
                    return list(self.get_features().keys())
                feature = self.get_feature(feature_name_top)
                if isinstance(feature, dict):
                    for feature_name in feature.keys():  # type: ignore
                        feature_path = (
                            f"{parent_path}.{feature_name_top}.{feature_name}"
                            if parent_path
                            else f"{feature_name_top}.{feature_name}"
                        )
                        selected_features.append(feature_path)

                else:
                    feature_path = (
                        f"{parent_path}.{feature_name_top}"
                        if parent_path
                        else feature_name_top
                    )
                    selected_features.append(feature_path)

        else:
            feats = self.search_features(usr_input)
            if not feats:
                color.ColoredText.localize("no_feature_with_name", name=usr_input)
            kv_map = list(feats.items())
            kv_map.sort(key=lambda v: v[1], reverse=True)
            selected_features = [v[0] for v in kv_map]

        return selected_features

    def select_features_run(self):
        features = self.get_features()
        features = list(features.keys())
        self.save_file.to_file_thread(self.save_file.get_temp_path())
        edits.clear_tutorial.clear_tutorial(self.save_file, False)
        self.save_file.show_ban_message = False

        while True:
            features = self.select_features(features)

            new_features: list[str] = []
            found_strs: list[str] = []
            for feature_ in features:
                if feature_.split(".")[-1] in found_strs:
                    continue
                found_strs.append(feature_.split(".")[-1])
                new_features.append(feature_)

            features = new_features
            feature = None
            if len(features) == 1:
                feature = features[0]
            if len(features) == 2 and features[0] == "go_back":
                feature = features[1]

            if not feature:
                continue

            feature = self.get_feature(feature)

            if isinstance(feature, Callable):
                self.do_save_actions()

                feature(self.save_file)

                self.save_file.to_file_thread(self.save_file.get_temp_path())

                features = self.get_features()
                features = list(features.keys())

                core.core_data.game_data_getter = None  # reset game data getter so that if an old version is removed, it will download the new version

    def do_save_actions(self):
        if core.core_data.config.get_bool(core.ConfigKey.CLEAR_TUTORIAL_ON_LOAD):
            edits.clear_tutorial.clear_tutorial(self.save_file, False)
        if core.core_data.config.get_bool(core.ConfigKey.REMOVE_BAN_MESSAGE_ON_LOAD):
            self.save_file.show_ban_message = False


# ============================================================
# FILE: file_dialog.py
# ============================================================
from __future__ import annotations
from bcsfe import core
from bcsfe.cli import color, dialog_creator


class FileDialog:
    def load_tk(self):
        try:
            import tkinter as tk
            from tkinter import filedialog

            self.tk = tk
            self.filedialog = filedialog
        except ImportError:
            self.tk = None
            self.filedialog = None

    def __init__(self):
        self.load_tk()
        if self.tk is not None:
            try:
                self.root = self.tk.Tk()
            except self.tk.TclError:
                self.tk = None
                self.filedialog = None
                return

            self.root.withdraw()
            self.root.wm_attributes("-topmost", 1)  # type: ignore

    def select_files_in_dir(
        self, path: core.Path, ignore_json: bool
    ) -> str | None:
        """Print current files in directory.

        Args:
            path (core.Path): Path to directory.
        """
        color.ColoredText.localize("current_files_dir", dir=path)
        path.generate_dirs()
        files = path.get_files()
        if not files:
            color.ColoredText.localize("no_files_dir")

        files.sort(key=lambda file: file.basename())

        # remove files with .json extension
        if ignore_json:
            files = [file for file in files if file.get_extension() != "json"]

        files_str_ls = [file.basename() for file in files]
        options = files_str_ls + [core.localize("other_dir"), core.localize("another_path")]

        choice = dialog_creator.ChoiceInput.from_reduced(
            options,
            dialog="select_files_dir",
            single_choice=True,
            localize_options=False,
        ).single_choice()
        if choice is None:
            return

        choice -= 1
        if choice == len(files):
            path_input = color.ColoredInput().localize("enter_path_dir")
            path_obj = core.Path(path_input)
            if path_obj.is_relative():
                path_obj = path.add(path_obj)
            if not path_obj.exists():
                color.ColoredText.localize("path_not_exists", path=path_obj)
                return self.select_files_in_dir(path, ignore_json)
            return self.select_files_in_dir(path_obj, ignore_json)
        if choice == len(files) + 1:
            path_input = color.ColoredInput().localize("enter_path")
            return path_input or None
        return files[choice].to_str()

    def use_tk(self) -> bool:
        return (
            self.tk is not None
            and self.filedialog is not None
            and core.core_data.config.get_bool(core.ConfigKey.USE_FILE_DIALOG)
        )

    def get_file(
        self,
        title: str,
        initialdir: str,
        initialfile: str,
        filetypes: list[tuple[str, str]] | None = None,
        ignore_json: bool = False,
    ) -> str | None:
        if filetypes is None:
            filetypes = []
        title = core.core_data.local_manager.get_key(title)
        color.ColoredText.localize(title)
        if not self.use_tk():
            curr_path = core.Path(initialdir).add(initialfile)
            file = self.select_files_in_dir(curr_path.parent(), ignore_json)
            if file is None:
                return None
            path_obj = core.Path(file)
            if path_obj.exists():
                return file
            color.ColoredText.localize("path_not_exists", path=path_obj)
            return None

        return (
            self.filedialog.askopenfilename(  # type: ignore
                title=title,
                filetypes=filetypes,
                initialdir=initialdir,
                initialfile=initialfile,
            )
            or None
        )

    def save_file(
        self,
        title: str,
        initialdir: str,
        initialfile: str,
        filetypes: list[tuple[str, str]] | None = None,
    ) -> str | None:
        """Save file dialog

        Args:
            title (str): Title of dialog.
            filetypes (list[tuple[str, str]] | None, optional): File types. Defaults to None.
            initialdir (str, optional): Initial directory. Defaults to "".
            initialfile (str, optional): Initial file. Defaults to "".

        Returns:
            str | None: Path to file.
        """
        if filetypes is None:
            filetypes = []
        title = core.core_data.local_manager.get_key(title)
        color.ColoredText.localize(title)
        if not self.use_tk():
            def_path = core.Path(initialdir).add(initialfile).to_str()
            path = color.ColoredInput().localize(
                "enter_path_default", default=def_path
            )
            return path.strip().strip("'").strip('"') if path else def_path
        return (
            self.filedialog.asksaveasfilename(  # type: ignore
                title=title,
                filetypes=filetypes,
                initialdir=initialdir,
                initialfile=initialfile,
            )
            or None
        )


# ============================================================
# FILE: main.py
# ============================================================
from __future__ import annotations

"""Main class for the CLI."""

import sys
import traceback
from typing import Any, NoReturn
from bcsfe.cli import (
    file_dialog,
    color,
    feature_handler,
    save_management,
    dialog_creator,
)
from bcsfe import core


class Main:
    """Main class for the CLI."""

    def __init__(self):
        self.save_file = None
        self.exit = False
        self.save_path = None
        self.fh = None

    def wipe_temp_save(self):
        """Wipe the temp save."""
        core.SaveFile.get_temp_path().remove()

    def main(self, input_path: str | None = None):
        """Main function for the CLI."""
        self.wipe_temp_save()
        core.GameDataGetter.delete_old_versions(5)
        self.check_update()
        print()
        self.print_start_text()
        while not self.exit:
            stop = self.load_save_options(input_path)
            if stop:
                break

    def check_update(self):
        """Check for updates."""

        updater = core.Updater()
        has_pre_release = updater.has_enabled_pre_release()
        local_version = updater.get_local_version()
        latest_version = updater.get_latest_version(has_pre_release)

        if latest_version is None:
            color.ColoredText.localize("update_check_fail")
            return

        color.ColoredText.localize(
            "version_line",
            local_version=local_version,
            latest_version=latest_version,
        )

        is_local_beta = "b" in local_version
        is_latest_beta = "b" in latest_version

        local_no_beta = local_version.split("b")[0]
        latest_no_beta = latest_version.split("b")[0]

        if latest_no_beta > local_no_beta:
            update_needed = True
        elif latest_no_beta < local_no_beta:
            update_needed = False
        else:
            if latest_version == local_version:
                update_needed = False
            else:
                if is_local_beta and is_latest_beta:
                    update_needed = latest_version > local_version
                elif is_local_beta:
                    update_needed = True
                else:
                    update_needed = False

        show_message = core.core_data.config.get(core.ConfigKey.SHOW_UPDATE_MESSAGE)
        if not show_message:
            update_needed = False

        if update_needed:
            update = dialog_creator.YesNoInput(True).get_input_once(
                "update_available", {"latest_version": latest_version}
            )
            if update is None:
                return

            if update:
                if updater.update(latest_version):
                    color.ColoredText.localize("update_success")
                else:
                    color.ColoredText.localize("update_fail")
                sys.exit()
            else:
                disable_message = dialog_creator.YesNoInput(False).get_input_once(
                    "disable_update_message"
                )
                if disable_message is None:
                    return

                core.core_data.config.set(
                    core.ConfigKey.SHOW_UPDATE_MESSAGE, not disable_message
                )

    def print_start_text(self):
        external_theme = core.ExternalThemeManager.get_external_theme_config()
        external_locale = core.ExternalLocaleManager.get_external_locale_config()
        if external_theme is None:
            theme_text = core.core_data.local_manager.get_key(
                "theme_text",
                theme_path=core.ThemeHandler.get_theme_path(
                    core.core_data.theme_manager.theme_code
                ),
                theme_version=core.core_data.theme_manager.get_version(),
                theme_author=core.core_data.theme_manager.get_author(),
                theme_name=core.core_data.theme_manager.get_name(),
                escape=False,
            )
        else:
            theme_text = core.core_data.local_manager.get_key(
                "theme_text",
                theme_name=external_theme.name,
                theme_version=external_theme.version,
                theme_author=external_theme.author,
                theme_path=core.ThemeHandler.get_theme_path(
                    external_theme.get_full_name()
                ),
                escape=False,
            )
        if external_locale is None:
            authors = core.core_data.local_manager.authors
            locale_text = core.core_data.local_manager.get_key(
                "default_locale_text_authors",
                path=core.core_data.local_manager.path,
                authors=", ".join(authors),
                name=core.core_data.local_manager.name,
                escape=False,
            )
        else:
            locale_text = core.core_data.local_manager.get_key(
                "locale_text",
                locale_name=external_locale.name,
                locale_version=external_locale.version,
                locale_author=external_locale.author,
                locale_path=core.LocalManager.get_locale_folder(
                    external_locale.get_full_name()
                ),
                escape=False,
            )
        color.ColoredText.localize(
            "welcome",
            config_path=core.core_data.config.get_config_path(),
            locale_text=locale_text,
            theme_text=theme_text,
            escape=False,
        )
        print()

    def load_save_options(self, input_path: str | None = None):
        """Load save options."""
        save_file, stop = save_management.SaveManagement.select_save(True, input_path)
        if save_file is None:
            return stop
        self.save_file = save_file

        color.ColoredText.localize(
            "current_save",
            inquiry_code=save_file.inquiry_code[:4]
            + "***"
            + save_file.inquiry_code[-2:],
            gv=save_file.game_version,
            cc=save_file.cc,
        )

        self.feature_handler()
        return False

    def feature_handler(self):
        """Run the feature handler."""
        if self.save_file is None:
            return
        self.fh = feature_handler.FeatureHandler(self.save_file)
        self.fh.select_features_run()

    @staticmethod
    def save_save_dialog(save_file: core.SaveFile) -> core.Path | None:
        """Save save file dialog.

        Args:
            save_file (core.SaveFile): Save file to save.

        Returns:
            core.Path: Path to save file.
        """
        path = file_dialog.FileDialog().save_file(
            "save_save_dialog",
            initialdir=core.SaveFile.get_saves_path().to_str(),
            initialfile="SAVE_DATA",
        )
        if path is None:
            return None
        path = core.Path(path)
        path.parent().generate_dirs()
        save_file.save_path = path
        return path

    @staticmethod
    def save_json_dialog(json_data: dict[str, Any]) -> core.Path | None:
        """Save json file dialog.

        Args:
            json_data (dict): Json data to save.

        Returns:
            core.Path: Path to save file.
        """
        path = file_dialog.FileDialog().save_file(
            "save_json_dialog",
            initialfile="SAVE_DATA.json",
            initialdir=core.SaveFile.get_saves_path().to_str(),
        )
        if path is None:
            return None
        path = core.Path(path)
        path.parent().generate_dirs()
        core.JsonFile.from_object(json_data).to_data().to_file(path)
        return path

    @staticmethod
    def load_save_file() -> core.Path | None:
        """Load save file from file dialog.

        Returns:
            core.Path: Path to save file.
        """
        path = file_dialog.FileDialog().get_file(
            "select_save_file",
            initialdir=core.SaveFile.get_saves_path().to_str(),
            initialfile="SAVE_DATA",
            ignore_json=True,
        )
        if path is None:
            return None
        path = core.Path(path)
        return path

    @staticmethod
    def load_save_data_json() -> tuple[core.Path, core.CountryCode] | None:
        """Load save data from json file.

        Returns:
            core.Path: Path to save file.
        """
        path = file_dialog.FileDialog().get_file(
            "load_save_data_json",
            initialfile="SAVE_DATA.json",
            initialdir=core.SaveFile.get_saves_path().to_str(),
        )
        if path is None:
            return None
        path = core.Path(path)
        if not path.exists():
            return None
        try:
            json_data = core.JsonFile.from_data(path.read()).to_object()
        except core.JSONDecodeError:
            color.ColoredText.localize(
                "load_json_fail", error=core.core_data.logger.get_traceback()
            )
            return None
        try:
            save_file = core.SaveFile.from_dict(json_data)
        except core.SaveError:
            color.ColoredText.localize(
                "load_json_fail", error=core.core_data.logger.get_traceback()
            )
            return None
        path = Main.save_save_dialog(save_file)
        if path is None:
            return None
        save_file.to_file(path)
        return path, save_file.cc

    @staticmethod
    def exit_editor(
        save_file: core.SaveFile | None = None, check_temp: bool = True
    ) -> NoReturn:
        """Exit the editor."""
        save_file_temp = None
        if check_temp:
            temp_path = core.SaveFile.get_temp_path()
            if temp_path.exists():
                try:
                    save_file_temp = core.SaveFile(temp_path.read())
                except core.SaveError as e:
                    tb = traceback.format_exc()
                    color.ColoredText.localize(
                        "save_temp_fail", error=str(e), traceback=tb
                    )
                    Main.leave()

        if save_file is None:
            save_file = save_file_temp
        if save_file is None:
            if check_temp:
                color.ColoredText.localize("save_temp_not_found")
            Main.leave()
        if save_file_temp is None:
            save_file_temp = save_file

        try:
            print()
            color.ColoredText.localize("checking_for_changes")
            if save_file.save_path is None:
                same = False
            else:
                same = save_file.save_path.read() == save_file.to_data()
        except core.SaveError:
            same = False

        if not same:
            color.ColoredText.localize("changes_found")
            print()
            save = color.ColoredInput().localize("save_before_exit") == "y"
            if save:
                save_management.SaveManagement.save_save(save_file)
        else:
            color.ColoredText.localize("no_changes")

        Main.leave()

    @staticmethod
    def leave() -> NoReturn:
        """Leave the editor."""
        color.ColoredText.localize("leave")
        sys.exit()


# ============================================================
# FILE: recent_saves.py
# ============================================================
from __future__ import annotations
from typing import Any

from bcsfe import core
import datetime
import json
from bcsfe.cli import color, dialog_creator


class RecentSave:
    def __init__(
        self,
        path: core.Path,
        cc: core.CountryCode,
        gv: core.GameVersion,
        inquiry: str,
        time: datetime.datetime,
        name: core.Path,
    ):
        self.path = path
        self.cc = cc
        self.gv = gv
        self.inquiry = inquiry
        self.time = time
        self.name = name

    @staticmethod
    def from_dict(data: dict[str, Any]) -> RecentSave | None:
        path = data.get("path")
        cc = data.get("cc")
        gv = data.get("gv")
        inquiry = data.get("inquiry")
        time_stamp = data.get("timestamp")
        name = data.get("name")
        if (
            path is None
            or cc is None
            or gv is None
            or inquiry is None
            or time_stamp is None
            or name is None
        ):
            return None

        return RecentSave(
            core.Path(path),
            core.CountryCode(cc),
            core.GameVersion.from_string(gv),
            inquiry,
            datetime.datetime.fromtimestamp(time_stamp),
            core.Path(name),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path.to_str(),
            "cc": self.cc.get_code(),
            "gv": self.gv.to_string(),
            "inquiry": self.inquiry,
            "timestamp": self.time.timestamp(),
            "name": self.name.to_str(),
        }


class RecentSaves:
    def __init__(self, saves: list[RecentSave]):
        self.saves = saves

    @staticmethod
    def from_json(data: list[dict[str, Any]]) -> RecentSaves:
        res: list[RecentSave] = []

        for item in data:
            save = RecentSave.from_dict(item)
            if save is not None:
                res.append(save)

        return RecentSaves(res)

    def to_json(self) -> list[dict[str, Any]]:
        return [save.to_dict() for save in self.saves][-10:]  # only store 10

    @staticmethod
    def from_path(path: core.Path) -> RecentSaves | None:
        json_data = json.loads(path.read().to_str())

        return RecentSaves.from_json(json_data)

    def to_path(self, path: core.Path):
        data = json.dumps(self.to_json(), indent=4)

        path.write(core.Data(data))

    @staticmethod
    def read_default() -> RecentSaves:
        path = RecentSaves.get_path()
        if path.exists():
            return RecentSaves.from_path(path) or RecentSaves([])
        return RecentSaves([])

    @staticmethod
    def get_path() -> core.Path:
        return core.Path.get_documents_folder().add("recent_saves.json")

    def save_default(self):
        path = RecentSaves.get_path()
        self.to_path(path)

    def select(self) -> RecentSave | None:
        if not self.saves:
            color.ColoredText.localize("no_recent_saves")
            return None
        items: list[str] = []
        for save in self.saves:
            items.append(
                core.localize(
                    "recent_save",
                    path=save.path,
                    cc=save.cc,
                    gv=save.gv,
                    inquiry_code=save.inquiry,
                    year=save.time.year,
                    month=str(save.time.month).zfill(2),
                    day=str(save.time.day).zfill(2),
                    hour=str(save.time.hour).zfill(2),
                    minute=str(save.time.minute).zfill(2),
                    second=str(save.time.second).zfill(2),
                    name=save.name,
                )
            )
        items.reverse()

        resp = dialog_creator.ChoiceInput.from_reduced(
            items, localize_options=False, dialog="select_recent"
        ).single_choice()
        if resp is None:
            return None

        resp = len(self.saves) - resp

        return self.saves[resp]


# ============================================================
# FILE: save_management.py
# ============================================================
from __future__ import annotations
import datetime
from bcsfe import core
import bcsfe
from bcsfe.core import io
from bcsfe.cli import main, color, dialog_creator, server_cli, recent_saves
from bcsfe.core.country_code import CountryCode
from bcsfe.core.io.config import ConfigKey


class SaveManagement:
    def __init__(self):
        pass

    @staticmethod
    def save_save(save_file: core.SaveFile, check_strict: bool = True):
        """Save the save file without a dialog.

        Args:
            save_file (core.SaveFile): The save file to save.
        """
        SaveManagement.upload_items_checker(save_file, check_strict)

        if save_file.save_path is None:
            save_file.save_path = main.Main.save_save_dialog(save_file)

        if save_file.save_path is None:
            return

        save_file.to_file(save_file.save_path)

        color.ColoredText.localize("save_success", path=save_file.save_path)

    @staticmethod
    def save_save_dialog(save_file: core.SaveFile):
        """Save the save file with a dialog.

        Args:
            save_file (core.SaveFile): The save file to save.
        """
        SaveManagement.upload_items_checker(save_file)
        save_file.save_path = main.Main.save_save_dialog(save_file)
        if save_file.save_path is None:
            return

        save_file.to_file(save_file.save_path)

        color.ColoredText.localize("save_success", path=save_file.save_path)

    @staticmethod
    def save_save_documents(save_file: core.SaveFile):
        """Save the save file to the documents folder.

        Args:
            save_file (core.SaveFile): The save file to save.
        """
        SaveManagement.upload_items_checker(save_file)
        save_file.save_path = core.SaveFile.get_saves_path().add("SAVE_DATA")
        save_file.to_file(save_file.save_path)
        color.ColoredText.localize("save_success", path=save_file.save_path)

    @staticmethod
    def save_upload(save_file: core.SaveFile):
        """Save the save file and upload it to the server.

        Args:
            save_file (core.SaveFile): The save file to save.
        """
        if core.core_data.config.get_bool(core.ConfigKey.STRICT_BAN_PREVENTION):
            color.ColoredText.localize("strict_ban_prevention_enabled")
            SaveManagement.create_new_account(save_file)

        result = core.ServerHandler(save_file).get_codes()
        if result is not None:
            SaveManagement.save_save(save_file, check_strict=False)
            transfer_code, confirmation_code = result
            color.ColoredText.localize(
                "upload_result",
                transfer_code=transfer_code,
                confirmation_code=confirmation_code,
            )
        else:
            color.ColoredText.localize("upload_fail")
            SaveManagement.save_save(save_file, check_strict=False)

    @staticmethod
    def unban_account(save_file: core.SaveFile):
        """Unban the account.

        Args:
            save_file (core.SaveFile): The save file to unban.
        """
        server_handler = core.ServerHandler(save_file)
        success = server_handler.create_new_account()
        if success:
            color.ColoredText.localize("unban_success")
        else:
            color.ColoredText.localize("unban_fail")

    @staticmethod
    def create_new_account(save_file: core.SaveFile):
        """Create a new account.

        Args:
            save_file (core.SaveFile): The save file to create a new account.
        """
        server_handler = core.ServerHandler(save_file)
        success = server_handler.create_new_account()
        if success:
            color.ColoredText.localize("create_new_account_success")
        else:
            color.ColoredText.localize("create_new_account_fail")

    @staticmethod
    def waydroid_push(save_file: core.SaveFile) -> core.WayDroidHandler | None:
        SaveManagement.save_save(save_file)
        try:
            waydroid_handler = core.WayDroidHandler()
        except core.AdbNotInstalled as e:
            core.AdbHandler.display_no_adb_error(e)
            return None
        except core.io.waydroid.WayDroidNotInstalledError as e:
            core.WayDroidHandler.display_waydroid_not_installed(e)
            return None

        if not waydroid_handler.adb_handler.select_device():
            return None

        if save_file.used_storage and save_file.package_name is not None:
            waydroid_handler.set_package_name(save_file.package_name)
        else:
            packages = waydroid_handler.get_battlecats_packages()
            package_name = SaveManagement.select_package_name(packages)
            if package_name is None:
                color.ColoredText.localize("no_package_name_error")
                return waydroid_handler
            waydroid_handler.set_package_name(package_name)

        if save_file.save_path is None:
            return waydroid_handler

        result = waydroid_handler.load_battlecats_save(save_file.save_path)
        if result.success:
            color.ColoredText.localize("waydroid_push_success")
        else:
            color.ColoredText.localize("waydroid_push_fail", error=result.result)

        return waydroid_handler

    @staticmethod
    def waydroid_push_rerun(save_file: core.SaveFile) -> core.AdbHandler | None:
        waydroid_handler = SaveManagement.waydroid_push(save_file)
        if not waydroid_handler:
            return
        if waydroid_handler.package_name is None:
            return
        result = waydroid_handler.rerun_game()
        if result.success:
            color.ColoredText.localize("waydroid_rerun_success")
        else:
            color.ColoredText.localize("waydroid_rerun_fail", error=result.result)

    @staticmethod
    def adb_push(save_file: core.SaveFile) -> core.AdbHandler | None:
        """Push the save file to the device.

        Args:
            save_file (core.SaveFile): The save file to push.

        Returns:
            core.AdbHandler: The AdbHandler instance.
        """
        SaveManagement.save_save(save_file)
        try:
            adb_handler = core.AdbHandler()
        except core.AdbNotInstalled as e:
            core.AdbHandler.display_no_adb_error(e)
            return None
        success = adb_handler.select_device()
        if not success:
            return adb_handler
        if save_file.used_storage and save_file.package_name is not None:
            adb_handler.set_package_name(save_file.package_name)
        else:
            packages = adb_handler.get_battlecats_packages()
            package_name = SaveManagement.select_package_name(packages)
            if package_name is None:
                color.ColoredText.localize("no_package_name_error")
                return adb_handler
            adb_handler.set_package_name(package_name)
        if save_file.save_path is None:
            return adb_handler
        result = adb_handler.load_battlecats_save(save_file.save_path)
        if result.success:
            color.ColoredText.localize("adb_push_success")
        else:
            color.ColoredText.localize("adb_push_fail", error=result.result)

        return adb_handler

    @staticmethod
    def root_push(save_file: core.SaveFile) -> core.RootHandler | None:
        """Push the save file to the device.

        Args:
            save_file (core.SaveFile): The save file to push.

        Returns:
            core.AdbHandler: The AdbHandler instance.
        """
        SaveManagement.save_save(save_file)
        root_handler = core.RootHandler()
        if not root_handler.is_android():
            color.ColoredText.localize("root_push_not_android_error")
            return None
        if not root_handler.is_rooted():
            color.ColoredText.localize("not_rooted_error")
            return None
        if save_file.used_storage and save_file.package_name is not None:
            root_handler.set_package_name(save_file.package_name)
        else:
            packages = root_handler.get_battlecats_packages()
            package_name = SaveManagement.select_package_name(packages)
            if package_name is None:
                color.ColoredText.localize("no_package_name_error")
                return root_handler
            root_handler.set_package_name(package_name)
        if save_file.save_path is None:
            return root_handler
        result = root_handler.load_battlecats_save(save_file.save_path)
        if result.success:
            color.ColoredText.localize("root_push_success")
        else:
            color.ColoredText.localize("root_push_fail", error=result.result)

        return root_handler

    @staticmethod
    def adb_push_rerun(save_file: core.SaveFile):
        """Push the save file to the device and rerun the game.

        Args:
            save_file (core.SaveFile): The save file to push.
        """
        adb_handler = SaveManagement.adb_push(save_file)
        if not adb_handler:
            return
        if adb_handler.package_name is None:
            return
        result = adb_handler.rerun_game()
        if result.success:
            color.ColoredText.localize("adb_rerun_success")
        else:
            color.ColoredText.localize("adb_rerun_fail", error=result.result)

    @staticmethod
    def root_push_rerun(save_file: core.SaveFile):
        """Push the save file to the device and rerun the game.

        Args:
            save_file (core.SaveFile): The save file to push.
        """
        root_handler = SaveManagement.root_push(save_file)
        if not root_handler:
            return
        if root_handler.package_name is None:
            return
        result = root_handler.rerun_game()
        if result.success:
            color.ColoredText.localize("root_rerun_success")
        else:
            color.ColoredText.localize("root_rerun_fail", error=result.result)

    @staticmethod
    def export_save(save_file: core.SaveFile):
        """Export the save file to a json file.

        Args:
            save_file (core.SaveFile): The save file to export.
        """
        data = save_file.to_dict()
        path = main.Main.save_json_dialog(data)
        if path is None:
            return
        data = core.JsonFile.from_object(data).to_data()
        data.to_file(path)
        color.ColoredText.localize("export_success", path=path)

    @staticmethod
    def init_save(save_file: core.SaveFile):
        """Initialize the save file to a new save file.

        Args:
            save_file (core.SaveFile): The save file to initialize.
        """
        confirm = dialog_creator.YesNoInput().get_input_once("init_save_confirm")
        if not confirm:
            return
        save_file.init_save(save_file.game_version)
        color.ColoredText.localize("init_save_success")

    @staticmethod
    def upload_items(save_file: core.SaveFile, check_strict: bool = True):
        """Upload the items to the server.

        Args:
            save_file (core.SaveFile): The save file to upload.
        """
        if (
            core.core_data.config.get_bool(core.ConfigKey.STRICT_BAN_PREVENTION)
            and check_strict
        ):
            color.ColoredText.localize("strict_ban_prevention_enabled")
            SaveManagement.create_new_account(save_file)

        server_handler = core.ServerHandler(save_file)
        success = server_handler.upload_meta_data()
        if success:
            color.ColoredText.localize("upload_items_success")
        else:
            color.ColoredText.localize("upload_items_fail")

    @staticmethod
    def upload_items_checker(save_file: core.SaveFile, check_strict: bool = True):
        managed_items = core.BackupMetaData(save_file).get_managed_items()
        if not managed_items:
            return
        should_upload = dialog_creator.YesNoInput().get_input_once(
            "upload_items_checker_confirm"
        )
        if not should_upload:
            return
        SaveManagement.upload_items(save_file, check_strict)

    @staticmethod
    def select_save(
        starting_options: bool = False, input_file: str | None = None
    ) -> tuple[core.SaveFile | None, bool]:
        """Select a new save file.

        Args:
            starting_options (bool, optional): Whether to add the starting specific options. Defaults to False.


        Returns:
            core.SaveFile | None: The save file.
        """
        if input_file is not None:
            file = SaveManagement.load_save_file_path(
                core.Path(input_file), None, False, None
            )
            if file is None:
                return (None, True)
            return (file[0], False)

        options = [
            "download_save",
            "select_save_file",
            "load_from_documents",
            "adb_pull_save",
            "load_save_data_json",
            "load_recent_saves",
            # "create_new_save",
        ]
        if starting_options:
            options.append("edit_config")
            options.append("update_external")
            options.append("exit")

        use_waydroid = core.core_data.config.get_bool(ConfigKey.USE_WAYDROID)
        if use_waydroid:
            options[3] = "waydroid_pull_save"

        root_handler = io.root_handler.RootHandler()

        if root_handler.is_android():
            options[3] = "root_storage_pull_save"

        choice = dialog_creator.ChoiceInput(
            options, options, [], {}, "save_load_option", True
        ).get_input_locale_while()
        if choice is None:
            return None, False
        choice = choice[0] - 1

        save_path = None
        cc: core.CountryCode | None = None
        used_storage = False
        package_name = None

        if choice == 0:
            data = server_cli.ServerCLI().download_save()
            if data is not None:
                save_path, cc = data
            else:
                save_path = None
        elif choice == 1:
            save_path = main.Main.load_save_file()
        elif choice == 2:
            save_path = core.SaveFile.get_saves_path().add("SAVE_DATA")
            if not save_path.exists():
                color.ColoredText.localize("save_file_not_found")
                return None, False
        elif choice == 3:
            handler = root_handler
            if not root_handler.is_android():
                if use_waydroid:
                    try:
                        handler = core.WayDroidHandler()
                    except core.AdbNotInstalled as e:
                        core.AdbHandler.display_no_adb_error(e)
                        return None, False
                    except core.io.waydroid.WayDroidNotInstalledError as e:
                        core.WayDroidHandler.display_waydroid_not_installed(e)
                        return None, False
                    if not handler.adb_handler.select_device():
                        return None, False
                else:
                    try:
                        handler = core.AdbHandler()
                    except core.AdbNotInstalled as e:
                        core.AdbHandler.display_no_adb_error(e)
                        return None, False
                    if not handler.select_device():
                        return None, False

            elif not root_handler.is_rooted():
                color.ColoredText.localize("not_rooted_error")
                return None, False

            package_names = handler.get_battlecats_packages()

            package_name = SaveManagement.select_package_name(package_names)
            if package_name is None:
                color.ColoredText.localize("no_package_name_error")
                return None, False
            handler.set_package_name(package_name)
            if root_handler.is_android():
                key = "storage_pulling"
            else:
                if use_waydroid:
                    key = "waydroid_pulling"
                else:
                    key = "adb_pulling"
            color.ColoredText.localize(key, package_name=package_name)
            save_path, result = handler.save_locally()
            if save_path is None:
                if root_handler.is_android():
                    key = "storage_pull_fail"
                else:
                    if use_waydroid:
                        key = "waydroid_pull_fail"
                    else:
                        key = "adb_pull_fail"
                color.ColoredText.localize(
                    key,
                    package_name=package_name,
                    error=result.result,
                )
            else:
                used_storage = True
        elif choice == 4:
            data = main.Main.load_save_data_json()
            if data is not None:
                save_path, cc = data
            else:
                save_path = None
        elif choice == 5:
            recent_save = recent_saves.RecentSaves.read_default().select()
            if recent_save is None:
                save_path = None
            else:
                save_path = recent_save.path
                cc = recent_save.cc

        # elif choice == 5:
        #     color.ColoredText.localize("create_new_save_warning")
        #     cc = core.CountryCode.select()
        #     if cc is None:
        #         return None, False
        #     try:
        #         gv = core.GameVersion.from_string(
        #             color.ColoredInput().localize(
        #                 "game_version_dialog",
        #             )
        #         )
        #     except ValueError:
        #         color.ColoredText.localize("invalid_game_version")
        #         return None, False
        #     save = core.SaveFile(cc=cc, gv=gv, load=False)
        #     save_path = main.Main.save_save_dialog(save)
        #     if save_path is None:
        #         return None, False
        #     save.to_file(save_path)
        #     color.ColoredText.localize("create_new_save_success")

        elif choice == 6 and starting_options:
            core.core_data.config.edit_config()
        elif choice == 7 and starting_options:
            core.update_external_content()
        elif choice == 8 and starting_options:
            main.Main.exit_editor(check_temp=False)

        if save_path is None or not save_path.exists():
            return None, False

        save = SaveManagement.load_save_file_path(
            save_path, cc, used_storage, package_name
        )

        if save is None:
            return (None, False)

        save, backup_path = save

        if choice != 5:
            recent_s = recent_saves.RecentSaves.read_default()
            recent_s.saves.append(
                recent_saves.RecentSave(
                    backup_path,
                    save.cc,
                    save.game_version,
                    save.inquiry_code,
                    datetime.datetime.now(),
                    save_path,
                )
            )
            recent_s.save_default()
        return (
            save,
            False,
        )

    @staticmethod
    def load_save_file_path(
        save_path: core.Path,
        cc: CountryCode | None,
        used_storage: bool,
        package_name: str | None = None,
    ) -> tuple[core.SaveFile, core.Path] | None:
        color.ColoredText.localize("save_file_found", path=save_path)

        data = save_path.read()
        try:
            save_file = core.SaveFile(data, cc, package_name=package_name)
        except core.CantDetectSaveCCError:
            color.ColoredText.localize("cant_detect_cc")
            cc = core.CountryCode.select()
            if cc is None:
                return None
            try:
                save_file = core.SaveFile(data, cc)
            except Exception:
                tb = core.core_data.logger.get_traceback()
                data.reset_pos()
                color.ColoredText.localize(
                    "parse_save_error",
                    error=tb,
                    version=bcsfe.__version__,
                    game_version=data.read_int(),
                    country_code=cc.get_code(),
                )
                return None

        except Exception:
            tb = core.core_data.logger.get_traceback()
            save_file2 = core.SaveFile(data, cc, load=False)
            data.reset_pos()
            color.ColoredText.localize(
                "parse_save_error",
                error=tb,
                version=bcsfe.__version__,
                game_version=data.read_int(),
                country_code=save_file2.cc,
            )
            return None

        save_file.save_path = save_path
        backup_path = save_file.get_default_path()
        save_file.save_path.copy_thread(backup_path)
        save_file.used_storage = used_storage

        return save_file, backup_path

    @staticmethod
    def select_package_name(package_names: list[str]) -> str | None:
        choice = dialog_creator.ChoiceInput.from_reduced(
            package_names,
            dialog="select_package_name",
            single_choice=True,
            localize_options=False,
        ).single_choice()
        if choice is None:
            return None
        return package_names[choice - 1]

    @staticmethod
    def load_save(save_file: core.SaveFile):
        """Load a new save file.

        Args:
            save_file (core.SaveFile): The current save file.
        """
        SaveManagement.upload_items_checker(save_file)
        new_save_file, stop = SaveManagement.select_save()
        if new_save_file is None:
            return stop
        save_file.load_save_file(new_save_file)
        core.core_data.init_data()
        color.ColoredText.localize("load_save_success")
        return False

    @staticmethod
    def convert_save_cc(save_file: core.SaveFile):
        color.ColoredText.localize("cc_warning", current=save_file.cc)
        ccs_to_select = core.CountryCode.get_all()
        cc = core.CountryCode.select_from_ccs(ccs_to_select)
        if cc is None:
            return
        save_file.set_cc(cc)
        core.ServerHandler(save_file).create_new_account()
        core.core_data.init_data()
        color.ColoredText.localize("country_code_set", cc=cc)

    @staticmethod
    def convert_save_gv(save_file: core.SaveFile):
        color.ColoredText.localize(
            "gv_warning", current=save_file.game_version.to_string()
        )
        try:
            gv = core.GameVersion.from_string(
                color.ColoredInput().localize("game_version_dialog").strip()
            )
        except ValueError:
            color.ColoredText.localize("invalid_game_version")
            return
        save_file.set_gv(gv)
        core.core_data.init_data()
        color.ColoredText.localize("game_version_set", version=gv.to_string())


# ============================================================
# FILE: server_cli.py
# ============================================================
from __future__ import annotations
from bcsfe.cli import dialog_creator, main, color, file_dialog
from bcsfe import core


class ServerCLI:
    def __init__(self):
        pass

    def download_save(
        self,
    ) -> tuple[core.Path, core.CountryCode] | None:
        transfer_code = dialog_creator.StringInput().get_input_locale_while(
            "enter_transfer_code", {}
        )
        if transfer_code is None:
            return None
        confirmation_code = dialog_creator.StringInput().get_input_locale_while(
            "enter_confirmation_code", {}
        )
        if confirmation_code is None:
            return None
        cc = core.CountryCode.select()
        if cc is None:
            return None
        gv = core.GameVersion(120200)  # not important

        color.ColoredText.localize(
            "downloading_save_file",
            transfer_code=transfer_code,
            confirmation_code=confirmation_code,
            country_code=cc,
        )

        server_handler, result = core.ServerHandler.from_codes(
            transfer_code,
            confirmation_code,
            cc,
            gv,
        )
        if server_handler is None and result is not None:
            color.ColoredText.localize("invalid_codes_error")
            if dialog_creator.YesNoInput().get_input_once(
                "display_response_debug_info_q"
            ):
                if result.response is not None:
                    color.ColoredText.localize(
                        "response_text_display",
                        url=result.url,
                        request_headers=result.headers,
                        request_body=result.data,
                        response_headers=result.response.headers,
                        response_body=result.response.text,
                    )
            return
        if server_handler is None:
            return

        save_file = server_handler.save_file
        if file_dialog.FileDialog().filedialog is None:
            path = core.SaveFile.get_saves_path().add("SAVE_DATA")
        else:
            path = main.Main().save_save_dialog(save_file)
        if path is None:
            return None

        save_file.to_file(path)

        color.ColoredText.localize("save_downloaded", path=path.to_str())

        return path, cc

