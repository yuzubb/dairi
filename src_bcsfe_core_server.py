# === COMBINED FILE ===
# フォルダ: src_bcsfe_core_server
# 元ファイル(9件): __init__.py, client_info.py, event_data.py, game_data_getter.py, headers.py, managed_item.py, request.py, server_handler.py, updater.py

# ============================================================
# FILE: __init__.py
# ============================================================
from bcsfe.core.server import (
    managed_item,
    headers,
    client_info,
    server_handler,
    game_data_getter,
    request,
    updater,
    event_data,
)

__all__ = [
    "managed_item",
    "server_handler",
    "headers",
    "client_info",
    "game_data_getter",
    "request",
    "updater",
    "event_data"
]


# ============================================================
# FILE: client_info.py
# ============================================================
from __future__ import annotations
from typing import Any
from bcsfe import core


class ClientInfo:
    def __init__(self, cc: core.CountryCode, gv: core.GameVersion):
        self.cc = cc
        self.gv = gv

    @staticmethod
    def from_save_file(save_file: core.SaveFile):
        return ClientInfo(save_file.cc, save_file.game_version)

    def get_client_info(self) -> dict[str, Any]:
        cc = self.cc.get_client_info_code()

        data = {
            "clientInfo": {
                "client": {
                    "countryCode": cc,
                    "version": self.gv.game_version,
                },
                "device": {
                    "model": "SM-G955F",
                },
                "os": {
                    "type": "android",
                    "version": "9",
                },
            },
            "nonce": core.Random.get_hex_string(32),
        }
        return data


# ============================================================
# FILE: event_data.py
# ============================================================
from __future__ import annotations
from collections.abc import Callable
from typing import Type, TypeVar

from bcsfe import core


class FilterDate:
    def __init__(self, start_mmdd: int, start_hhmm: int, end_mmdd: int, end_hhmm: int):
        self.start_mmdd = start_mmdd
        self.start_hhmm = start_hhmm
        self.end_mmdd = end_mmdd
        self.end_hhmm = end_hhmm

    @staticmethod
    def from_csv_row(row: core.Row) -> FilterDate:
        return FilterDate(
            row.next_int(), row.next_int(), row.next_int(), row.next_int()
        )


class FilterItem:
    def __init__(
        self,
        filter_date: FilterDate | None,
        filter_day_flags: list[bool],  # 31 item array
        filter_week: int,
        filter_times_start_end_hhmm: list[tuple[int, int]],
    ):
        self.filter_date = filter_date
        self.filter_day_flags = filter_day_flags
        self.filter_week = filter_week
        self.filter_times_start_end_hhmm = filter_times_start_end_hhmm

    @staticmethod
    def from_csv_row(row: core.Row) -> FilterItem:
        filter_date_enabled = row.next_bool()

        filter_date = None
        if filter_date_enabled:
            filter_date = FilterDate.from_csv_row(row)

        filter_day_count = row.next_int()

        filter_day_flags: list[bool] = [False] * 31

        for _ in range(filter_day_count):
            day_ind = row.next_int() - 1
            if day_ind >= 0 and day_ind < len(filter_day_flags):
                filter_day_flags[day_ind] = True

        filter_week = row.next_int()
        filter_time_count = row.next_int()

        filter_times_start_end_hhmm: list[tuple[int, int]] = []

        for _ in range(filter_time_count):
            start_hhmm = row.next_int()
            end_hhmm = row.next_int()

            filter_times_start_end_hhmm.append((start_hhmm, end_hhmm))

        return FilterItem(
            filter_date, filter_day_flags, filter_week, filter_times_start_end_hhmm
        )


def split_yyyymmdd(yyyymmdd: int) -> tuple[int, int, int]:
    year = yyyymmdd // 10_000
    month = (yyyymmdd % 10_000) // 100
    day = yyyymmdd % 100

    return year, month, day


def split_hhmm(hhmm: int) -> tuple[int, int]:
    hour = hhmm // 100
    minute = hhmm % 100

    return hour, minute


class FilterData:
    def __init__(
        self,
        start_yyyymmdd: int,
        start_hhmm: int,
        end_yyyymmdd: int,
        end_hhmm: int,
        min_game_version: int,
        max_game_version: int,
        platform_flag: int,
        filter_items: list[FilterItem],
    ):
        self.start_yyyymmdd = start_yyyymmdd
        self.start_hhmm = start_hhmm
        self.end_yyyymmdd = end_yyyymmdd
        self.end_hhmm = end_hhmm
        self.min_game_version = min_game_version
        self.max_game_version = max_game_version
        self.platform_flag = platform_flag
        self.filter_items = filter_items

    @staticmethod
    def from_csv_row(row: core.Row) -> FilterData:
        start_yyyymmdd = row.next_int()
        start_hhmm = row.next_int()
        end_yyyymmdd = row.next_int()
        end_hhmm = row.next_int()
        min_game_version = row.next_int()
        max_game_version = row.next_int()
        platform_flag = row.next_int()
        total_items = row.next_int()

        filter_items: list[FilterItem] = []

        for _ in range(total_items):
            filter_items.append(FilterItem.from_csv_row(row))

        return FilterData(
            start_yyyymmdd,
            start_hhmm,
            end_yyyymmdd,
            end_hhmm,
            min_game_version,
            max_game_version,
            platform_flag,
            filter_items,
        )


class Localization:
    def __init__(self, lang: str, title: str, message: str):
        self.lang = lang
        self.title = title
        self.message = message

    @staticmethod
    def from_csv_row(row: core.Row) -> Localization:
        return Localization(row.next_str(), row.next_str(), row.next_str())


class RarityGatya:
    def __init__(self, prob: int, guaranteed: int):
        self.prob = prob
        self.guaranteed = guaranteed

    @staticmethod
    def from_csv_row(row: core.Row) -> RarityGatya:
        return RarityGatya(row.next_int(), row.next_int())


class ServerGatyaDataSet:
    def __init__(
        self,
        number: int,
        catfood: int,
        stage_progress: int,
        flags: int,
        rarity_info: list[RarityGatya],
        message: str,
        collab_message: tuple[str, str] | None,
    ):
        self.number = number
        self.catfood = catfood
        self.stage_progress = stage_progress
        self.flags = flags
        self.rarity_info = rarity_info
        self.message = message
        self.other_event_message = collab_message

    @staticmethod
    def from_csv_row(row: core.Row, flag: int) -> ServerGatyaDataSet:
        number = row.next_int()
        catfood = row.next_int()
        stage_progress = row.next_int()
        flags = row.next_int()
        rarity_info: list[RarityGatya] = []

        for _ in range(5):
            rarity_info.append(RarityGatya.from_csv_row(row))

        message = row.next_str()

        collab_message = None
        if flag == 4:
            collab_message = (row.next_str(), row.next_str())

        return ServerGatyaDataSet(
            number,
            catfood,
            stage_progress,
            flags,
            rarity_info,
            message,
            collab_message,
        )

    def is_visible_silhouette(self) -> bool:
        return (self.flags & 1) != 0

    def is_required_user_rank_1600(self) -> bool:
        return (self.flags & 2) != 0

    def has_stepup_gatya(self) -> bool:
        return (self.flags & 4) != 0


class ServerGatyaDataItem:
    def __init__(self, filter: FilterData, flags: int, sets: list[ServerGatyaDataSet]):
        self.filter = filter
        self.flags = flags
        self.sets = sets

    @staticmethod
    def from_csv_row(row: core.Row) -> ServerGatyaDataItem:
        filter = FilterData.from_csv_row(row)
        flag = row.next_int()
        count = row.next_int()

        sets: list[ServerGatyaDataSet] = []

        for _ in range(count):
            sets.append(ServerGatyaDataSet.from_csv_row(row, flag))

        return ServerGatyaDataItem(filter, flag, sets)

    def get_normal_flag(self) -> bool:
        return self.flags == 0

    def get_rare_flag(self) -> bool:
        return 1 <= self.flags <= 3

    def get_collab_flag(self) -> bool:
        return self.flags == 4

    def get_first_rare_flag(self) -> bool:
        return self.flags == 2

    def get_first_rare_10_flag(self) -> bool:
        return self.flags == 3


class ServerItemDataItem:
    def __init__(
        self,
        filter: FilterData,
        event_number: int,  # server item id
        item_number: int,
        item_unit: int,  # base quanity, not cat unit (e.g 2 XP+1000s)
        title: str,
        message: str,
        stage_progress: int,
        stage_progress_flag: int,
        flags: int,
        locales: list[Localization] | None,
    ):
        self.filter = filter
        self.event_number = event_number
        self.item_number = item_number
        self.item_unit = item_unit
        self.title = title
        self.message = message
        self.stage_progress = stage_progress
        self.stage_progress_flag = stage_progress_flag
        self.flags = flags
        self.locales = locales

    def is_every_day(self) -> bool:
        return (self.flags & 1) != 0

    def is_required_user_rank_1600(self) -> bool:
        return (self.flags & 2) != 0

    @staticmethod
    def from_csv_row(row: core.Row) -> ServerItemDataItem:
        filter = FilterData.from_csv_row(row)

        event_number = row.next_int()
        item_number = row.next_int()
        item_unit = row.next_int()
        title = row.next_str()
        message = row.next_str()
        stage_progress = row.next_int()
        stage_progress_flag = row.next_bool()
        flags = row.next_int()

        locales: list[Localization] | None = None

        if not row.done():
            locales = []
            total_locales = row.next_int()

            for _ in range(total_locales):
                locales.append(Localization.from_csv_row(row))

        return ServerItemDataItem(
            filter,
            event_number,
            item_number,
            item_unit,
            title,
            message,
            stage_progress,
            stage_progress_flag,
            flags,
            locales,
        )


Item = TypeVar("Item")
T = TypeVar("T")


def read_event_data(
    csv: core.CSV,
    read_func: Callable[[core.Row], Item],
    init_func: Callable[[list[Item]], T],
) -> T | None:
    start = csv.read_line()
    if start is None:
        return None

    if start.next_str() != "[start]":
        return None

    if not start.done():
        return None

    items: list[Item] = []

    while True:
        row = csv.read_line()
        if row is None:
            return None

        if len(row) == 0:
            return None

        if row[0].to_str() == "[end]":
            break

        item = read_func(row)

        items.append(item)

    return init_func(items)


class ServerItemData:
    def __init__(self, items: list[ServerItemDataItem]):
        self.items = items

    @staticmethod
    def from_csv(csv: core.CSV) -> ServerItemData | None:
        return read_event_data(csv, ServerItemDataItem.from_csv_row, ServerItemData)

    @staticmethod
    def from_data(data: core.Data) -> ServerItemData | None:
        csv = core.CSV(data, delimiter="\t", remove_comments=False, remove_empty=False)

        return ServerItemData.from_csv(csv)


class ServerGatyaData:
    def __init__(self, items: list[ServerGatyaDataItem]):
        self.items = items

    @staticmethod
    def from_csv(csv: core.CSV) -> ServerGatyaData | None:
        return read_event_data(csv, ServerGatyaDataItem.from_csv_row, ServerGatyaData)

    @staticmethod
    def from_data(data: core.Data) -> ServerGatyaData | None:
        csv = core.CSV(data, delimiter="\t", remove_comments=False, remove_empty=False)

        return ServerGatyaData.from_csv(csv)


# ============================================================
# FILE: game_data_getter.py
# ============================================================
from __future__ import annotations
from io import BytesIO
from typing import Any, Callable

from bcsfe.cli import color, dialog_creator

import tarfile

from bcsfe import core


class GameDataGetter:
    def __init__(
        self, cc: core.CountryCode, gv: core.GameVersion, do_print: bool = True
    ):
        self.repo_url = core.core_data.config.get_game_data_repo()
        self.print = do_print
        self.lang = core.core_data.config.get_str(core.ConfigKey.LOCALE)
        self.cc = cc.get_cc_lang()
        self.real_cc = cc
        self.gv = gv
        self.cc = self.cc if not self.cc.is_lang() else self.real_cc
        self.version, exact_match = self.find_gv(self.cc, gv)

        self.all_versions = None
        self.url = None
        self.filepath = None

        if exact_match:
            return

        self.metadata = self.get_metadata()
        if self.metadata is None:
            return
        self.all_versions = self.get_versions(self.metadata)
        self.url = self.metadata.get("base_url")
        if self.all_versions is not None:
            self.version, self.filepath = self.get_version(self.all_versions, self.cc)

    def find_gv(
        self, cc: core.CountryCode, gv: core.GameVersion
    ) -> tuple[str | None, bool]:
        versions = GameDataGetter.get_all_downloaded_versions().get(cc.get_code())
        if versions is None:
            return None, False

        versions_int = [
            core.GameVersion.from_string(version).game_version for version in versions
        ]

        versions_int.sort()

        for version in versions_int:
            if version >= gv.game_version:
                return core.GameVersion(version).to_string(), version == gv.game_version
        return None, False

    def does_save_version_match(self, save_file: core.SaveFile) -> bool:
        if self.version is None:
            return False

        return save_file.game_version == self.version

    def get_version(
        self, versions: dict[str, dict[str, str]], cc: core.CountryCode
    ) -> tuple[str | None, str | None]:
        cc_versions = versions.get(cc.get_code())
        if cc_versions is None:
            return None, None
        if not cc_versions:
            return None, None
        gv_string = self.gv.to_string()
        if gv_string not in cc_versions:
            cc_version_keys = list(cc_versions.keys())
            cc_version_keys.sort()
            for version in cc_version_keys:
                if (
                    core.GameVersion.from_string(version).game_version
                    >= self.gv.game_version
                ):
                    return version, cc_versions[version]
            return cc_version_keys[-1], cc_versions[cc_version_keys[-1]]
        return gv_string, cc_versions[gv_string]

    def get_metadata(self, show_alt: bool = True) -> dict[str, Any] | None:
        response = core.RequestHandler(self.repo_url).get()
        if response is None:
            if (
                self.repo_url
                == core.core_data.config.get_default(core.ConfigKey.GAME_DATA_REPO)
                and show_alt
            ):
                alt = "https://gitlab.com/fieryhenry/bcdata/-/raw/main/metadata.json"
                res = dialog_creator.YesNoInput().get_input_once(
                    "use_alternative_repo",
                    {
                        "repo": "https://gitlab.com/fieryhenry/bcdata/-/raw/main/metadata.json"
                    },
                )
                if res:
                    core.core_data.config.set(core.ConfigKey.GAME_DATA_REPO, alt)
                    self.repo_url = alt
                    return self.get_metadata(show_alt=False)

            return None
        try:
            data = response.json()
        except core.JSONDecodeError as e:
            print(e)
            return None
        return data

    def get_versions(self, metdata: dict[str, Any]) -> dict[str, dict[str, str]] | None:
        return metdata.get("versions")

    def get_packname(self, packname: str) -> str:
        if packname != "resLocal":
            return packname
        if self.cc != core.CountryCodeType.EN:
            return packname
        langs = core.CountryCode.get_langs()
        if self.lang in langs:
            return f"{packname}_{self.lang}"
        return packname

    @staticmethod
    def get_game_data_dir() -> core.Path:
        return core.Path.get_documents_folder().add("game_data")

    def get_file_path(self, pack_name: str, file_name: str) -> core.Path | None:
        pack_name = self.get_packname(pack_name)
        path = self.get_version_path()
        if path is None:
            return None
        return path.add(pack_name).generate_dirs().add(file_name)

    def download_version_data(self):
        if self.url is None or self.filepath is None or self.version is None:
            return None
        url = self.url + self.filepath

        if self.print:
            color.ColoredText.localize("downloading_compressed_data", url=url)

        downloaded_data = core.RequestHandler(url).get()
        if downloaded_data is None:
            if self.print:
                color.ColoredText.localize("no_internet")
            return None

        archive = tarfile.open(
            name=self.filepath, fileobj=BytesIO(downloaded_data.content)
        )

        outdir = (
            GameDataGetter.get_game_data_dir().add(self.cc.get_code()).add(self.version)
        ).generate_dirs()

        archive.extractall(outdir.path)

        outdir.add("downloaded").write(core.Data())

        return True

    def get_version_path(self) -> core.Path | None:
        if self.version is None:
            return None
        return (
            GameDataGetter.get_game_data_dir().add(self.cc.get_code()).add(self.version)
        ).generate_dirs()

    def has_downloaded(self) -> bool:
        path = self.get_version_path()
        if path is None:
            return False
        return path.add("downloaded").exists()

    def get_file(self, pack_name: str, file_name: str) -> core.Data | bool:
        path = self.get_file_path(pack_name, file_name)
        if path is None:
            return False

        if path.exists():
            return path.read()
        else:
            if self.has_downloaded():
                return True
            if self.download_version_data() is None:
                return False

            path = self.get_file_path(pack_name, file_name)
            if path is None:
                return False

            if path.exists():
                return path.read()
            return self.has_downloaded()

    def save_file(self, pack_name: str, file_name: str) -> core.Data | bool:
        pack_name = self.get_packname(pack_name)
        data = self.get_file(pack_name, file_name)
        if isinstance(data, bool):
            return data

        path = self.get_file_path(pack_name, file_name)
        if path is None:
            return False
        data.to_file(path)
        return data

    def save_file_data(
        self, pack_name: str, file_name: str, data: core.Data
    ) -> core.Data | None:
        pack_name = self.get_packname(pack_name)

        path = self.get_file_path(pack_name, file_name)
        if path is None:
            return None
        data.to_file(path)
        return data

    def is_downloaded(self, pack_name: str, file_name: str) -> bool:
        pack_name = self.get_packname(pack_name)
        path = self.get_file_path(pack_name, file_name)
        if path is None:
            return False
        return path.exists()

    def download_from_path(
        self, path: str, retries: int = 2, display_text: bool = True
    ) -> core.Data | None:
        pack_name, file_name = path.split("/")
        pack_name = self.get_packname(pack_name)
        return self.download(pack_name, file_name, retries, display_text)

    def download(
        self,
        pack_name: str,
        file_name: str,
        retries: int = 2,
        display_text: bool = True,
    ) -> core.Data | None:
        retries -= 1
        pack_name = self.get_packname(pack_name)

        if self.is_downloaded(pack_name, file_name):
            path = self.get_file_path(pack_name, file_name)
            if path is None:
                return None
            try:
                return path.read()
            except FileNotFoundError:
                return None

        if retries == 0:
            return None

        version = self.version

        if version is None:
            if display_text:
                self.print_no_file(pack_name, file_name)
            return None

        if display_text and not self.has_downloaded():
            color.ColoredText.localize(
                "downloading",
                file_name=file_name,
                pack_name=pack_name,
                country_code=self.cc.get_code(),
                version=version,
            )
        data = self.save_file(pack_name, file_name)
        if isinstance(data, bool):
            if not data and display_text:
                self.print_no_file(pack_name, file_name)
            return None

        data = self.download(pack_name, file_name, retries, display_text)
        if data is None:
            if display_text:
                self.print_no_file(pack_name, file_name)
            return None
        return data

    def download_all(
        self,
        pack_name: str,
        file_names: list[str],
        display_text: bool = True,
    ) -> list[tuple[str, core.Data] | None]:
        pack_name = self.get_packname(pack_name)

        callables: list[Callable[..., Any]] = []
        args: list[tuple[str, str, int, bool]] = []
        for file_name in file_names:
            callables.append(self.download)
            args.append((pack_name, file_name, 2, display_text))
        core.thread_run_many(callables, args)
        data_list: list[tuple[str, core.Data] | None] = []
        for file_name in file_names:
            path = self.get_file_path(pack_name, file_name)
            if path is None:
                data_list.append(None)
            elif not path.exists():
                data_list.append(None)
            else:
                data_list.append((file_name, path.read()))
        return data_list

    @staticmethod
    def get_all_downloaded_versions() -> dict[str, list[str]]:
        versions: dict[str, list[str]] = {}
        for cc in core.CountryCode.get_all_str():
            dir = GameDataGetter.get_game_data_dir().add(cc)
            if not dir.exists():
                continue
            for version in GameDataGetter.get_game_data_dir().add(cc).get_dirs():
                if not version.exists():
                    continue
                if not version.add("downloaded").exists():
                    continue
                if cc in versions:
                    versions[cc].append(version.basename())
                else:
                    versions[cc] = [version.basename()]

        return versions

    @staticmethod
    def delete_old_versions(to_keep: int) -> None:
        versions = GameDataGetter.get_all_downloaded_versions()
        for cc, cc_versions in versions.items():
            cc_versions.sort(reverse=True)
            to_keep = min(to_keep, len(cc_versions))
            for version in cc_versions[to_keep:]:
                path = GameDataGetter.get_game_data_dir().add(cc).add(version)
                path.remove()

    def print_no_file(self, packname: str, file_name: str) -> None:
        if self.version is None:
            color.ColoredText.localize("failed_to_get_game_versions")
        else:
            color.ColoredText.localize(
                "failed_to_download_game_data",
                file_name=file_name,
                pack_name=packname,
                country_code=self.cc.get_code(),
                version=self.version,
                url=self.url,
            )


# ============================================================
# FILE: headers.py
# ============================================================
from __future__ import annotations
import time
from bcsfe import core


class AccountHeaders:
    def __init__(self, save_file: core.SaveFile, data: str):
        self.save_file = save_file
        self.data = data

    def get_headers(self) -> dict[str, str]:
        return AccountHeaders.get_headers_static(
            self.save_file.inquiry_code, self.data
        )

    @staticmethod
    def get_headers_static(iq: str, data: str):
        return {
            "accept-enconding": "gzip",
            "connection": "keep-alive",
            "content-type": "application/json",
            "nyanko-signature": core.NyankoSignature(
                iq, data
            ).generate_signature(),
            "nyanko-timestamp": str(int(time.time())),
            "nyanko-signature-version": "1",
            "nyanko-signature-algorithm": "HMACSHA256",
            "user-agent": "Dalvik/2.1.0 (Linux; U; Android 9; SM-G955F Build/N2G48B)",
        }


# ============================================================
# FILE: managed_item.py
# ============================================================
from __future__ import annotations

"""ManagedItem class for bcsfe."""

from enum import Enum
from typing import Any
import uuid
import time
from bcsfe import core


class DetailType(Enum):
    """Enum for the different types of details."""

    GET = "get"
    USE = "use"


class ManagedItemType(Enum):
    """Enum for the different types of managed items."""

    CATFOOD = "catfood"
    RARE_TICKET = "rareTicket"
    PLATINUM_TICKET = "platinumTicket"
    LEGEND_TICKET = "legendTicket"


class ManagedItem:
    """Managed item for backupmetadata"""

    def __init__(
        self,
        amount: int,
        detail_type: DetailType,
        managed_item_type: ManagedItemType,
        detail_code: str = "",
        detail_created_at: int = 0,
    ):
        self.amount = amount
        self.detail_type = detail_type
        self.managed_item_type = managed_item_type
        if not detail_code:
            detail_code = str(uuid.uuid4())
        self.detail_code = detail_code
        if not detail_created_at:
            detail_created_at = int(time.time())
        self.detail_created_at = detail_created_at

    @staticmethod
    def from_change(
        change: int, managed_item_type: ManagedItemType
    ) -> ManagedItem:
        """Create a managed item from a change."""
        if change > 0:
            detail_type = DetailType.GET
        else:
            detail_type = DetailType.USE
        managed_item = ManagedItem(abs(change), detail_type, managed_item_type)
        return managed_item

    def to_dict(self) -> dict[str, Any]:
        """Convert the managed item to a dictionary."""

        data = {
            "amount": self.amount,
            "detailCode": self.detail_code,
            "detailCreatedAt": self.detail_created_at,
            "detailType": self.detail_type.value,
            "managedItemType": self.managed_item_type.value,
        }
        return data

    def to_short_form(self) -> str:
        """Convert the managed item to a short form."""

        return f"{self.amount}_{self.detail_created_at}_{self.managed_item_type.value}_{self.detail_type.value}"

    @staticmethod
    def from_short_form(short_form: str) -> ManagedItem:
        values = short_form.split("_")
        try:
            amount = int(values[0])
        except (IndexError, ValueError):
            amount = 0

        try:
            detail_created_at = int(values[1])
        except (IndexError, ValueError):
            detail_created_at = 0

        try:
            managed_item_type = values[2]
        except IndexError:
            managed_item_type = ManagedItemType.CATFOOD.value

        try:
            detail_type = values[3]
        except IndexError:
            detail_type = DetailType.GET.value

        return ManagedItem(
            amount,
            DetailType(detail_type),
            ManagedItemType(managed_item_type),
            detail_created_at=detail_created_at,
        )

    def __str__(self) -> str:
        return f"{self.amount} {self.managed_item_type.value} ({self.detail_type.value})"

    def __repr__(self) -> str:
        return f"{self.amount} {self.managed_item_type.value} ({self.detail_type.value})"


class BackupMetaData:
    def __init__(
        self,
        save_file: core.SaveFile,
    ):
        self.save_file = save_file
        self.identifier = "managed_items"

    def set_managed_items(self, managed_items: list[ManagedItem]):
        self.save_file.remove_strings(self.identifier)
        for managed_item in managed_items:
            string = managed_item.to_short_form()
            self.save_file.store_string(
                self.identifier, string, overwrite=False
            )

    def get_managed_items(self) -> list[ManagedItem]:
        managed_items: list[ManagedItem] = []
        managed_items_str = self.save_file.get_strings(self.identifier)
        for managed_item_str in managed_items_str:
            managed_item = ManagedItem.from_short_form(managed_item_str)
            if managed_item.amount == 0:
                continue
            managed_items.append(managed_item)
        return managed_items

    def add_managed_item(self, managed_item: ManagedItem):
        if managed_item.amount == 0:
            return
        managed_items = self.get_managed_items()
        managed_items.append(managed_item)
        self.set_managed_items(managed_items)

    def remove_managed_items(self) -> None:
        self.save_file.remove_strings(self.identifier)

    def create(
        self, save_key: str | None = None, add_managed_items: bool = True
    ) -> str:
        """Create the backup metadata."""

        return BackupMetaData.create_static(
            self.save_file.inquiry_code,
            self.save_file.officer_pass.play_time,
            self.save_file.calculate_user_rank(),
            self.get_managed_items(),
            save_key,
            add_managed_items,
        )

    @staticmethod
    def create_static(
        iq: str,
        playtime: int,
        userrank: int,
        items: list[ManagedItem],
        save_key: str | None = None,
        add_managed_items: bool = True,
    ):
        managed_items: list[dict[str, Any]] = []
        if add_managed_items:
            for managed_item in items:
                if managed_item.amount == 0:
                    continue
                managed_items.append(managed_item.to_dict())

        managed_items_json = core.JsonFile.from_object(managed_items)
        managed_items_str = (
            managed_items_json.to_data(indent=None).to_str().replace(" ", "")
        )

        backup_metadata: dict[str, Any] = {
            "managedItemDetails": managed_items,
            "nonce": core.Random.get_hex_string(32),
            "playTime": playtime,
            "rank": userrank,
            "receiptLogIds": [],
            "signature_v1": core.NyankoSignature(
                iq, managed_items_str
            ).generate_signature_v1(),
        }
        if save_key is not None:
            backup_metadata["saveKey"] = save_key
        return (
            core.JsonFile.from_object(backup_metadata)
            .to_data(indent=None)
            .to_str()
            .replace(" ", "")
        )


# ============================================================
# FILE: request.py
# ============================================================
from __future__ import annotations

import requests

from bcsfe import core


class MultiPartFile:
    def __init__(self, content: bytes, content_type: str, filename: str | None = None):
        self.content = content
        self.content_type = content_type
        self.filename = filename


class MultipartForm:
    def __init__(self):
        self.data: dict[str, MultiPartFile] = {}

    def into_files(
        self,
    ) -> dict[str, tuple[str | None, bytes, str]]:
        out = {}
        for name, data in self.data.items():
            out[name] = (data.filename, data.content, data.content_type)

        return out

    def add_key(
        self, key: str, content: bytes, content_type: str, filename: str | None = None
    ):
        self.data[key] = MultiPartFile(content, content_type, filename)

    def get_all_type(self, content_type: str) -> str:
        data = ""
        for key, file in self.data.items():
            if file.content_type == content_type:
                content = file.content.decode("utf-8", errors="ignore")
                data += f"key: {key}, data: {content}\n"

        return data


class RequestHandler:
    """Handles HTTP requests."""

    def __init__(
        self,
        url: str,
        headers: dict[str, str] | None = None,
        data: core.Data | None = None,
        form: MultipartForm | None = None,
    ):
        """Initializes a new instance of the RequestHandler class.

        Args:
            url (str): URL to request.
            headers (dict[str, str] | None, optional): Headers to send with the request. Defaults to None.
            data (core.Data | None, optional): Data to send with the request. Defaults to None.
        """
        if data is None:
            data = core.Data()
        self.url = url
        self.headers = headers
        self.data = data
        self.form = form

    def get(
        self,
        stream: bool = False,
        no_timeout: bool = False,
    ) -> requests.Response | None:
        """Sends a GET request.

        Returns:
            requests.Response: Response from the server.
        """
        try:
            return requests.get(
                self.url,
                headers=self.headers,
                timeout=(
                    None
                    if no_timeout
                    else core.core_data.config.get_int(
                        core.ConfigKey.MAX_REQUEST_TIMEOUT
                    )
                ),
                stream=stream,
                files=None if self.form is None else self.form.into_files(),
            )
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return None

    def post(self, no_timeout: bool = False) -> requests.Response | None:
        """Sends a POST request.

        Returns:
            requests.Response: Response from the server.
        """
        try:
            return requests.post(
                self.url,
                headers=self.headers,
                data=self.data.data,
                timeout=(
                    None
                    if no_timeout
                    else core.core_data.config.get_int(
                        core.ConfigKey.MAX_REQUEST_TIMEOUT
                    )
                ),
                files=None if self.form is None else self.form.into_files(),
            )
        except requests.exceptions.ConnectionError:
            return None


# ============================================================
# FILE: server_handler.py
# ============================================================
from __future__ import annotations
import base64
import time
from typing import Any

from bcsfe import core
import jwt

from bcsfe.cli import color


class RequestResult:
    def __init__(
        self,
        url: str,
        response: core.Response | None,
        headers: dict[str, str],
        data: str,
        payload: dict[str, Any] | None = None,
        timestamp: str | None = None,
    ):
        self.url = url
        self.response = response
        self.headers = headers
        self.data = data
        self.payload = payload
        self.timestamp = timestamp


class ServerHandler:
    auth_url = "https://nyanko-auth.ponosgames.com"
    save_url = "https://nyanko-save.ponosgames.com"
    backups_url = "https://nyanko-backups.ponosgames.com"
    aws_url = "https://nyanko-service-data-prd.s3.amazonaws.com"
    managed_item_url = "https://nyanko-managed-item.ponosgames.com"
    events_url = "https://nyanko-events.ponosgames.com"

    def __init__(self, save_file: core.SaveFile, print: bool = True):
        self.save_file = save_file
        self.print = print
        self.counter = 0

    @staticmethod
    def get_password_key() -> str:
        return "password"

    @staticmethod
    def get_auth_token_key() -> str:
        return "auth_token"

    @staticmethod
    def get_save_key_key() -> str:
        return "save_key"

    def save_password(self, password: str):
        self.save_file.store_string(ServerHandler.get_password_key(), password)

    def get_stored_password(self) -> str | None:
        return self.save_file.get_string(ServerHandler.get_password_key())

    def remove_stored_password(self):
        self.save_file.remove_string(ServerHandler.get_password_key())

    def save_save_key_data(self, save_key: dict[str, Any]):
        self.save_file.store_dict(ServerHandler.get_save_key_key(), save_key)

    def get_stored_save_key_data(self) -> dict[str, Any] | None:
        save_key_data = self.save_file.get_dict(ServerHandler.get_save_key_key())
        if save_key_data is None:
            return None
        if not self.validate_save_key_data(save_key_data):
            self.remove_stored_save_key_data()
            return None
        return save_key_data

    def validate_save_key_data(self, save_key_data: dict[str, Any]) -> bool:
        key = save_key_data.get("key")
        if key is None:
            return False
        if key.split("/")[2] != self.save_file.inquiry_code:
            return False
        policy = save_key_data.get("policy")
        if policy is None:
            return False
        policy = base64.b64decode(policy)
        json_policy = core.JsonFile.from_data(core.Data(policy)).to_object()
        expiration = json_policy.get("expiration")
        if expiration is None:
            return False
        expiration = int(
            time.mktime(time.strptime(expiration, "%Y-%m-%dT%H:%M:%S.%fZ"))
        )
        if expiration < time.time():
            return False
        return True

    def remove_stored_save_key_data(self):
        self.save_file.remove_dict(ServerHandler.get_save_key_key())

    def save_auth_token(self, auth_token: str):
        self.save_file.store_string(ServerHandler.get_auth_token_key(), auth_token)

    def get_stored_auth_token(self) -> str | None:
        token = self.save_file.get_string(ServerHandler.get_auth_token_key())
        return token

    def remove_stored_auth_token(self):
        self.save_file.remove_string(ServerHandler.get_auth_token_key())

    def get_password_new(self) -> str | None:
        self.print_key("getting_password")

        url = f"{self.auth_url}/v1/users"
        data = {
            "accountCode": self.save_file.inquiry_code,
            "accountCreatedAt": int(self.save_file.energy_penalty_timestamp),
            "nonce": core.Random.get_hex_string(32),
        }
        password = self.do_password_request(url, data)
        return password

    @staticmethod
    def log_error(key: str, result: RequestResult):
        if "EXPECT_THIS_TO_FAIL" in result.data:
            return
        if result.response is None:
            log_text = "Failed to make request. Check your internet connection."
            core.core_data.logger.log_error(log_text)
            return
        log_text = (
            f"Error: {key}\n"
            f"URL: {result.url}\n"
            f"Response Headers: {result.response.headers}\n"
            f"Response Body: {result.response.content.decode('utf-8')}\n"
            f"Status Code: {result.response.status_code}\n"
            f"Reason: {result.response.reason}\n"
            f"Request Headers: {result.headers}\n"
            f"Request Body: {result.data}\n"
        )
        core.core_data.logger.log_error(log_text)

    def do_password_request(self, url: str, dict_data: dict[str, Any]) -> str | None:
        result = self.do_request(url, dict_data)
        if result.payload is None:
            ServerHandler.log_error("password_fail", result)
            return None
        payload = result.payload
        password = payload.get("password", None)
        if password is None:
            ServerHandler.log_error("password_fail", result)
            self.remove_stored_password()
            return None
        password_refresh_token = payload.get("passwordRefreshToken", None)
        if password_refresh_token is None:
            ServerHandler.log_error("password_fail", result)
            self.remove_stored_password()
            return None
        account_code = payload.get("accountCode", None)
        timestamp = result.timestamp

        self.save_file.password_refresh_token = password_refresh_token
        self.save_password(password)
        if account_code:
            self.save_file.inquiry_code = account_code
            self.remove_stored_auth_token()
            self.remove_stored_save_key_data()

            if timestamp is not None:
                self.save_file.energy_penalty_timestamp = int(timestamp)
            if not self.update_managed_items():
                return None

        return password

    def do_request(self, url: str, dict_data: dict[str, Any]) -> RequestResult:
        data = (
            core.JsonFile.from_object(dict_data)
            .to_data(indent=None)
            .to_str()
            .replace(" ", "")
        )
        headers = core.AccountHeaders(self.save_file, data).get_headers()
        response = core.RequestHandler(url, headers, core.Data(data)).post()
        if response is None:
            self.log_no_internet(RequestResult(url, None, headers, data))
            return RequestResult(url, response, headers, data)
        json: dict[str, Any] = response.json()
        status_code = json.get("statusCode", 0)
        if status_code != 1:
            return RequestResult(url, response, headers, data)

        timestamp = json.get("timestamp", None)

        payload = json.get("payload", {})
        return RequestResult(url, response, headers, data, payload, timestamp)

    def refresh_password(self) -> str | None:
        self.print_key("refreshing_password")

        url = f"{self.auth_url}/v1/user/password"
        data = {
            "accountCode": self.save_file.inquiry_code,
            "passwordRefreshToken": self.save_file.password_refresh_token,
            "nonce": core.Random.get_hex_string(32),
        }
        return self.do_password_request(url, data)

    def get_auth_token_new(self, password: str) -> str | None:
        self.print_key("getting_auth_token")

        url = f"{self.auth_url}/v1/tokens"
        data = core.ClientInfo.from_save_file(self.save_file).get_client_info()
        data["password"] = password
        data["accountCode"] = self.save_file.inquiry_code

        result = self.do_request(url, data)
        if result.payload is None:
            ServerHandler.log_error("auth_token_fail", result)
            self.remove_stored_auth_token()
            self.remove_stored_password()
            return None
        payload = result.payload
        auth_token = payload.get("token", None)
        if auth_token is None:
            ServerHandler.log_error("auth_token_fail", result)
            self.remove_stored_auth_token()
            self.remove_stored_password()
            return None
        self.save_auth_token(auth_token)
        return auth_token

    def get_password(self, tries: int = 0) -> str | None:
        password = self.get_stored_password()
        if password is not None:
            return password
        password = self.refresh_password()
        if password is not None:
            return password
        password = self.get_password_new()
        if password is not None:
            return password
        self.create_new_account()
        if tries >= 1:
            return None
        return self.get_password(tries + 1)

    def validate_auth_token(self, auth_token: str) -> bool:
        token = jwt.decode(  # type: ignore
            auth_token,
            algorithms=["HS256"],
            options={"verify_signature": False},
        )
        if not token:
            return False
        if token.get("exp", 0) < time.time():
            return False
        if token.get("accountCode", None) != self.save_file.inquiry_code:
            return False

        return True

    def get_auth_token(self, tries: int = 1) -> str | None:
        auth_token = self.get_stored_auth_token()
        if auth_token is not None:
            if self.validate_auth_token(auth_token):
                return auth_token
            self.remove_stored_auth_token()
        password = self.get_password()
        if password is None:
            return None
        auth_token = self.get_stored_auth_token()
        if auth_token is not None:
            return auth_token
        auth_token = self.get_auth_token_new(password)
        if auth_token is not None:
            return auth_token

        if tries > 0:
            self.print_key("retry_auth_token")
            return self.get_auth_token(tries - 1)

        return None

    def log_no_internet(self, result: RequestResult):
        ServerHandler.log_error("no_internet", result)
        if self.print:
            core.print_no_internet()

    def get_save_key_new(self, auth_token: str) -> dict[str, Any] | None:
        self.print_key("getting_save_key")

        nonce = core.Random.get_hex_string(32)
        url = f"{self.save_url}/v2/save/key?nonce={nonce}"
        headers = {
            "accept-encoding": "gzip",
            "connection": "keep-alive",
            "authorization": "Bearer " + auth_token,
            "nyanko-timestamp": str(int(time.time())),
            "user-agent": "Dalvik/2.1.0 (Linux; U; Android 9; SM-G955F Build/N2G48B)",
        }
        response = core.RequestHandler(url, headers).get()
        if response is None:
            self.log_no_internet(RequestResult(url, None, headers, ""))
            return None
        json: dict[str, Any] = response.json()
        status_code = json.get("statusCode", 0)
        if status_code != 1:
            ServerHandler.log_error(
                "save_key_fail", RequestResult(url, response, headers, "")
            )
            self.remove_stored_auth_token()
            return None
        payload = json.get("payload", {})
        self.save_save_key_data(payload)
        return payload

    def get_save_key(self) -> dict[str, Any] | None:
        # save_key = self.get_stored_save_key_data()
        # if save_key and save_key.get("key", None):
        #    return save_key
        auth_token = self.get_auth_token()
        if auth_token is None:
            return None
        # save_key = self.get_stored_save_key_data()
        # if save_key:
        #    return save_key
        save_key = self.get_save_key_new(auth_token)
        if save_key is not None:
            return save_key

        return None

    def get_upload_request_form(
        self,
        save_key: dict[str, str],
    ) -> core.MultipartForm:
        save_data = self.save_file.to_data()
        form_data = core.MultipartForm()
        for key, value in save_key.items():
            if key == "url":
                continue
            form_data.add_key(key, value.encode(), "text/plain")

        form_data.add_key(
            "file", save_data.to_bytes(), "application/octet-stream", "file.sav"
        )
        return form_data

    def upload_save_data(self, save_key: dict[str, Any]) -> bool:
        self.print_key("uploading_save_file")

        form = self.get_upload_request_form(save_key)
        if form is None:
            self.remove_stored_save_key_data()
            return False
        url = save_key.get("url")
        if url is None:
            url = f"{self.aws_url}/"
        headers = {
            "accept-encoding": "gzip",
            "connection": "keep-alive",
            "user-agent": "Dalvik/2.1.0 (Linux; U; Android 9; SM-G955F Build/N2G48B)",
        }
        response = core.RequestHandler(url, headers, form=form).post(no_timeout=True)
        if response is None:
            self.log_no_internet(RequestResult(url, None, headers, ""))
            return False
        if response.status_code != 204:
            ServerHandler.log_error(
                "upload_fail_aws",
                RequestResult(
                    url,
                    response,
                    headers,
                    form.get_all_type("text-plain"),
                ),
            )

            self.remove_stored_save_key_data()
            return False
        return True

    def print_key(self, key: str, **kwargs: Any):
        if self.print:
            color.ColoredText.localize(key, **kwargs)

    def get_codes(self, upload_managed_items: bool = True) -> tuple[str, str] | None:
        self.save_file.show_ban_message = False

        auth_token = self.get_auth_token()
        if auth_token is None:
            return None

        save_key = self.get_save_key()

        if save_key is None:
            self.remove_stored_save_key_data()
            return None

        if not self.upload_save_data(save_key):
            return None

        self.print_key("getting_codes")

        bmd = core.BackupMetaData(self.save_file)
        meta_data = bmd.create(save_key["key"], upload_managed_items)

        url = f"{self.save_url}/v2/transfers"
        headers = core.AccountHeaders(self.save_file, meta_data).get_headers()
        headers["authorization"] = "Bearer " + auth_token

        response = core.RequestHandler(url, headers, core.Data(meta_data)).post()
        if response is None:
            self.log_no_internet(RequestResult(url, None, headers, meta_data))
            return None
        json: dict[str, Any] = response.json()
        status_code = json.get("statusCode", 0)
        if status_code != 1:
            ServerHandler.log_error(
                "upload_fail_transfers",
                RequestResult(url, response, headers, meta_data),
            )
            self.remove_stored_auth_token()
            return None
        payload = json.get("payload", {})
        transfer_code = payload.get("transferCode", None)
        confirmation_code = payload.get("pin", None)
        if transfer_code is None or confirmation_code is None:
            ServerHandler.log_error(
                "upload_fail_transfers",
                RequestResult(url, response, headers, ""),
            )
            self.remove_stored_auth_token()
            return None
        bmd.remove_managed_items()
        if self.print:
            print()
        return (transfer_code, confirmation_code)

    def has_managed_items(self) -> bool:
        bmd = core.BackupMetaData(self.save_file)
        managed_items = bmd.get_managed_items()
        if len(managed_items) == 0:
            return False
        return True

    def upload_meta_data(self) -> bool:
        auth_token = self.get_auth_token()
        if auth_token is None:
            return False

        save_key = self.get_save_key()
        if save_key is None:
            self.remove_stored_save_key_data()
            return False

        if not self.upload_save_data(save_key):
            return False

        bmd = core.BackupMetaData(self.save_file)
        meta_data = bmd.create(save_key["key"])

        url = f"{self.save_url}/v2/backups"
        headers = core.AccountHeaders(self.save_file, meta_data).get_headers()
        headers["authorization"] = "Bearer " + auth_token

        response = core.RequestHandler(url, headers, core.Data(meta_data)).post()
        if response is None:
            self.log_no_internet(RequestResult(url, None, headers, meta_data))
            return False
        json: dict[str, Any] = response.json()
        status_code = json.get("statusCode", 0)
        if status_code != 1:
            self.remove_stored_auth_token()
            return False
        bmd.remove_managed_items()
        return True

    def get_new_inquiry_code(self) -> str | None:
        url = f"{self.backups_url}/?action=createAccount&referenceId="

        response = core.RequestHandler(url).get()
        if response is None:
            self.log_no_internet(RequestResult(url, None, {}, ""))
            return None
        data = response.json()
        iq = data["accountId"]
        return iq

    def create_new_account(self) -> bool:
        new_iq = self.get_new_inquiry_code()
        if new_iq is None:
            return False
        self.save_file.inquiry_code = new_iq
        self.remove_stored_auth_token()
        self.remove_stored_save_key_data()
        self.remove_stored_password()
        fail_text = "EXPECT_THIS_TO_FAIL"
        start_count = (40 - len(fail_text)) // 2
        end_count = 40 - len(fail_text) - start_count
        self.save_file.password_refresh_token = (
            "_" * start_count + fail_text + "_" * end_count
        )
        password = self.get_password()
        auth_token = self.get_auth_token()
        save_key_data = self.get_save_key()
        self.update_managed_items()
        self.save_file.show_ban_message = False
        if password is None or auth_token is None or save_key_data is None:
            return False
        return True

    @staticmethod
    def from_codes(
        transfer_code: str,
        confirmation_code: str,
        cc: core.CountryCode,
        gv: core.GameVersion,
        print: bool = True,
        save_backup: bool = True,
    ) -> tuple[ServerHandler | None, RequestResult | None]:
        url = f"{ServerHandler.save_url}/v2/transfers/{transfer_code}/reception"
        data = core.ClientInfo(cc, gv).get_client_info()
        data["pin"] = confirmation_code
        data_str = (
            core.JsonFile.from_object(data)
            .to_data(indent=None)
            .to_str()
            .replace(" ", "")
        )

        headers = {
            "content-type": "application/json",
            "accept-encoding": "gzip",
            "connection": "keep-alive",
            "user-agent": "Dalvik/2.1.0 (Linux; U; Android 9; SM-G955F Build/N2G48B)",
        }
        response = core.RequestHandler(url, headers, core.Data(data_str)).post()
        if response is None:
            if print:
                core.print_no_internet()
            return None, None
        resp_headers = response.headers
        content_type = resp_headers.get("content-type", "")
        if content_type != "application/octet-stream":
            return None, RequestResult(url, response, headers, data_str)

        save_data = response.content

        if save_backup:
            temp_path = (
                core.Path.get_documents_folder()
                .add("saves")
                .generate_dirs()
                .add("transfer_backup")
            )
            try:
                temp_path.write(core.Data(save_data))
            except Exception as e:
                color.ColoredText.localize(
                    "transfer_backup_fail", path=str(temp_path), error=e
                )
            else:
                if print:
                    color.ColoredText.localize("transfer_backup", path=str(temp_path))

        save_file = core.SaveFile(core.Data(save_data), cc=cc)

        password_refresh_token = resp_headers.get("Nyanko-Password-Refresh-Token")
        if password_refresh_token is not None:
            save_file.password_refresh_token = password_refresh_token

        server_handler = ServerHandler(save_file)
        password = resp_headers.get("Nyanko-Password")
        if password is not None:
            server_handler.save_password(password)

        return server_handler, RequestResult(url, response, headers, data_str)

    def update_managed_items(self) -> bool:
        auth_token = self.get_auth_token()
        if auth_token is None:
            return False
        data = {
            "catfoodAmount": self.save_file.catfood,
            "isPaid": True,
            "legendTicketAmount": self.save_file.legend_tickets,
            "nonce": core.Random.get_hex_string(32),
            "platinumTicketAmount": self.save_file.platinum_tickets,
            "rareTicketAmount": self.save_file.rare_tickets,
        }
        data_str = (
            core.JsonFile.from_object(data)
            .to_data(indent=None)
            .to_str()
            .replace(" ", "")
        )
        url = f"{self.managed_item_url}/v1/managed-items"
        headers = core.AccountHeaders(self.save_file, data_str).get_headers()
        headers["authorization"] = "Bearer " + auth_token
        response = core.RequestHandler(url, headers, core.Data(data_str)).post()
        if response is None:
            self.log_no_internet(RequestResult(url, None, headers, data_str))
            return False
        json: dict[str, Any] = response.json()
        status_code = json.get("statusCode", 0)
        if status_code != 1:
            self.remove_stored_auth_token()
            return False

        core.BackupMetaData(self.save_file).remove_managed_items()
        return True

    def download_event_data(self, filename: str) -> core.Data | None:
        url = (
            self.events_url
            + f"/battlecats{self.save_file.cc.get_patching_code()}_production/{filename}"
        )

        auth_token = self.get_auth_token()

        if auth_token is None:
            return None

        url += f"?jwt={auth_token}"

        headers = {
            "accept-encoding": "gzip",
            "connection": "keep-alive",
            "user-agent": "Dalvik/2.1.0 (Linux; U; Android 9; Pixel 2 Build/PQ3A.190801.002)",
        }

        resp = core.RequestHandler(url, headers).get()

        if resp is None:
            return None

        return core.Data(resp.content)

    def download_gatya_data(self) -> core.Data | None:
        return self.download_event_data("gatya.tsv")

    def download_item_data(self) -> core.Data | None:
        return self.download_event_data("item.tsv")

    def download_sale_data(self) -> core.Data | None:
        return self.download_event_data("sale.tsv")


# ============================================================
# FILE: updater.py
# ============================================================
from __future__ import annotations
import sys
from typing import Any
from bcsfe import core
import bcsfe


class Updater:
    package_name = "bcsfe"

    def __init__(self):
        pass

    def get_local_version(self) -> str:
        return bcsfe.__version__

    def get_pypi_json(self) -> dict[str, Any] | None:
        url = f"https://pypi.org/pypi/{self.package_name}/json"
        # add a User-Agent since pypi started to block the default requests user-agent
        # this probably won't be needed in the future as i assume this block is temporary
        response = core.RequestHandler(
            url, headers={"User-Agent": "BCSFE-Updater"}
        ).get()
        if response is None:
            return None
        try:
            return response.json()
        except core.JSONDecodeError:
            return None

    def get_releases(self) -> list[str] | None:
        pypi_json = self.get_pypi_json()
        if pypi_json is None:
            return None
        releases = pypi_json.get("releases")
        if releases is None:
            return None
        return list(releases.keys())

    def get_latest_version(self, prereleases: bool = False) -> str | None:
        releases = self.get_releases()
        if releases is None:
            return None

        releases.reverse()
        if prereleases:
            return releases[0]
        else:
            for release in releases:
                if "b" not in release:
                    return release
            return releases[0]

    def get_latest_version_info(
        self, prereleases: bool = False
    ) -> dict[str, Any] | None:
        pypi_json = self.get_pypi_json()
        if pypi_json is None:
            return None
        releases = pypi_json.get("releases")
        if releases is None:
            return None
        return releases.get(self.get_latest_version(prereleases))

    def update(self, target_version: str) -> bool:
        binary = sys.orig_argv[0]
        python_aliases = [binary, "py", "python", "python3"]
        for python_alias in python_aliases:
            cmd = f"{python_alias} -m pip install --upgrade {self.package_name}=={target_version}"
            result = core.Path().run(cmd)
            if result.exit_code == 0:
                break
        else:
            pip_aliases = ["pip", "pip3"]
            for pip_alias in pip_aliases:
                cmd = f"{pip_alias} install --upgrade {self.package_name}=={target_version}"
                result = core.Path().run(cmd)
                if result.exit_code == 0:
                    break
            else:
                return False
        return True

    def has_enabled_pre_release(self) -> bool:
        return core.core_data.config.get_bool(core.ConfigKey.UPDATE_TO_BETA)

