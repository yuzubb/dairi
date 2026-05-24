# === COMBINED FILE ===
# フォルダ: src_bcsfe_core_game_map
# 元ファイル(20件): __init__.py, aku.py, challenge.py, chapters.py, dojo.py, enigma.py, event.py, ex_stage.py, gauntlets.py, item_reward_stage.py, legend_quest.py, map_names.py, map_option.py, map_reset.py, outbreaks.py, story.py, timed_score.py, tower.py, uncanny.py, zero_legends.py

# ============================================================
# FILE: __init__.py
# ============================================================
from bcsfe.core.game.map import (
    story,
    event,
    item_reward_stage,
    timed_score,
    ex_stage,
    dojo,
    outbreaks,
    tower,
    challenge,
    map_reset,
    uncanny,
    legend_quest,
    gauntlets,
    enigma,
    aku,
    zero_legends,
    chapters,
    map_names,
    map_option,
)

__all__ = [
    "story",
    "event",
    "item_reward_stage",
    "timed_score",
    "ex_stage",
    "dojo",
    "outbreaks",
    "tower",
    "challenge",
    "map_reset",
    "uncanny",
    "legend_quest",
    "gauntlets",
    "enigma",
    "aku",
    "zero_legends",
    "chapters",
    "map_names",
    "map_option",
]


# ============================================================
# FILE: aku.py
# ============================================================
from __future__ import annotations
from typing import Any
from bcsfe import core
from bcsfe.cli import color


class Stage:
    def __init__(self, clear_times: int):
        self.clear_times = clear_times

    @staticmethod
    def init() -> Stage:
        return Stage(0)

    @staticmethod
    def read(data: core.Data) -> Stage:
        clear_times = data.read_short()
        return Stage(clear_times)

    def write(self, data: core.Data):
        data.write_short(self.clear_times)

    def serialize(self) -> int:
        return self.clear_times

    @staticmethod
    def deserialize(data: int) -> Stage:
        return Stage(
            data,
        )

    def __repr__(self):
        return f"Stage({self.clear_times})"

    def __str__(self):
        return self.__repr__()

    def clear_stage(self, clear_count: int = 1):
        self.clear_times = clear_count


class Chapter:
    def __init__(self, current_stage: int, total_stages: int = 0):
        self.current_stage = current_stage
        self.stages: list[Stage] = [Stage.init() for _ in range(total_stages)]

    @staticmethod
    def init(total_stages: int) -> Chapter:
        return Chapter(0, total_stages)

    @staticmethod
    def read_current_stage(data: core.Data):
        current_stage = data.read_byte()
        return Chapter(current_stage)

    def write_current_stage(self, data: core.Data):
        data.write_byte(self.current_stage)

    def read_stages(self, data: core.Data, total_stages: int):
        self.stages = [Stage.read(data) for _ in range(total_stages)]

    def write_stages(self, data: core.Data):
        for stage in self.stages:
            stage.write(data)

    def serialize(self) -> dict[str, Any]:
        return {
            "current_stage": self.current_stage,
            "stages": [stage.serialize() for stage in self.stages],
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> Chapter:
        chapter = Chapter(data.get("current_stage", 0))
        chapter.stages = [
            Stage.deserialize(stage) for stage in data.get("stages", [])
        ]
        return chapter

    def __repr__(self):
        return f"Chapter({self.current_stage}, {self.stages})"

    def __str__(self):
        return self.__repr__()


class ChaptersStars:
    def __init__(self, chapters: list[Chapter]):
        self.chapters = chapters

    @staticmethod
    def init(total_stages: int, total_stars: int) -> ChaptersStars:
        return ChaptersStars(
            [Chapter.init(total_stages) for _ in range(total_stars)]
        )

    @staticmethod
    def read_current_stage(data: core.Data, total_stars: int):
        chapters = [
            Chapter.read_current_stage(data) for _ in range(total_stars)
        ]
        return ChaptersStars(chapters)

    def write_current_stage(self, data: core.Data):
        for chapter in self.chapters:
            chapter.write_current_stage(data)

    def read_stages(self, data: core.Data, total_stages: int):
        for chapter in self.chapters:
            chapter.read_stages(data, total_stages)

    def write_stages(self, data: core.Data):
        for chapter in self.chapters:
            chapter.write_stages(data)

    def serialize(self) -> list[dict[str, Any]]:
        return [chapter.serialize() for chapter in self.chapters]

    @staticmethod
    def deserialize(data: list[dict[str, Any]]) -> ChaptersStars:
        chapters = [Chapter.deserialize(chapter) for chapter in data]
        return ChaptersStars(chapters)

    def __repr__(self):
        return f"ChaptersStars({self.chapters})"

    def __str__(self):
        return self.__repr__()


class AkuChapters:
    def __init__(self, chapters: list[ChaptersStars]):
        self.chapters = chapters

    @staticmethod
    def init() -> AkuChapters:
        return AkuChapters([])

    @staticmethod
    def read(data: core.Data) -> AkuChapters:
        total_chapters = data.read_short()
        total_stages = data.read_byte()
        total_stars = data.read_byte()

        chapters = [
            ChaptersStars.read_current_stage(data, total_stars)
            for _ in range(total_chapters)
        ]

        for chapter in chapters:
            chapter.read_stages(data, total_stages)

        return AkuChapters(chapters)

    def write(self, data: core.Data):
        data.write_short(len(self.chapters))
        try:
            data.write_byte(len(self.chapters[0].chapters[0].stages))
        except IndexError:
            data.write_byte(0)
        try:
            data.write_byte(len(self.chapters[0].chapters))
        except IndexError:
            data.write_byte(0)

        for chapter in self.chapters:
            chapter.write_current_stage(data)

        for chapter in self.chapters:
            chapter.write_stages(data)

    def serialize(self) -> list[list[dict[str, Any]]]:
        return [chapter.serialize() for chapter in self.chapters]

    @staticmethod
    def deserialize(data: list[list[dict[str, Any]]]) -> AkuChapters:
        chapters = [ChaptersStars.deserialize(chapter) for chapter in data]
        return AkuChapters(chapters)

    def __repr__(self):
        return f"Chapters({self.chapters})"

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def edit_aku_chapters(save_file: core.SaveFile):
        aku = save_file.aku
        chapter = aku.chapters[0].chapters[0]

        clear_progress = core.StoryChapters.get_selected_chapter_progress(
            max_stages=len(chapter.stages)
        )
        if clear_progress is None:
            return

        if clear_progress > 1:
            individual_clear_count = (
                core.StoryChapters.ask_if_individual_clear_counts()
            )
            if individual_clear_count is None:
                return
        else:
            individual_clear_count = True

        if individual_clear_count:
            stage_names = core.StageNames(save_file, "DM", 49).stage_names
            if stage_names is None:
                return
            for i, stage in enumerate(chapter.stages[:clear_progress]):
                stage_name = stage_names[i]
                color.ColoredText.localize(
                    "aku_current_stage", name=stage_name, id=i
                )
                clear_count = core.StoryChapters.ask_clear_count()
                if clear_count is None:
                    return
                stage.clear_stage(clear_count)
        else:
            clear_count = core.StoryChapters.ask_clear_count()
            if clear_count is None:
                return
            for stage in chapter.stages[:clear_progress]:
                stage.clear_stage(clear_count)

        for i in range(clear_progress, len(chapter.stages)):
            chapter.stages[i].clear_stage(clear_count=0)

        color.ColoredText.localize("aku_clear_success")


# ============================================================
# FILE: challenge.py
# ============================================================
from __future__ import annotations
from typing import Any
from bcsfe import core
from bcsfe.cli import dialog_creator


class ChallengeChapters:
    def __init__(self, chapters: core.Chapters):
        self.chapters = chapters
        self.scores: list[int] = []
        self.shown_popup: bool = False

    @staticmethod
    def init() -> ChallengeChapters:
        return ChallengeChapters(core.Chapters.init())

    @staticmethod
    def read(data: core.Data) -> ChallengeChapters:
        ch = core.Chapters.read(data)
        return ChallengeChapters(ch)

    def write(self, data: core.Data):
        self.chapters.write(data)

    def read_scores(self, data: core.Data):
        total_scores = data.read_int()
        self.scores = [data.read_int() for _ in range(total_scores)]

    def write_scores(self, data: core.Data):
        data.write_int(len(self.scores))
        for score in self.scores:
            data.write_int(score)

    def read_popup(self, data: core.Data):
        self.shown_popup = data.read_bool()

    def write_popup(self, data: core.Data):
        data.write_bool(self.shown_popup)

    def serialize(self) -> dict[str, Any]:
        return {
            "chapters": self.chapters.serialize(),
            "scores": self.scores,
            "shown_popup": self.shown_popup,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> ChallengeChapters:
        challenge = ChallengeChapters(
            core.Chapters.deserialize(data.get("chapters", {})),
        )
        challenge.scores = data.get("scores", [])
        challenge.shown_popup = data.get("shown_popup", False)
        return challenge

    def __repr__(self):
        return f"Challenge({self.chapters})"

    def __str__(self):
        return self.__repr__()

    def edit_score(self):
        if not self.scores:
            self.scores = [0]
        self.scores[0] = dialog_creator.SingleEditor(
            "challenge_score", self.scores[0], None, localized_item=True
        ).edit()
        self.shown_popup = True
        self.chapters.clear_stage(0, 0, 0, False)


def edit_challenge_score(save_file: core.SaveFile):
    save_file.challenge.edit_score()


# ============================================================
# FILE: chapters.py
# ============================================================
from __future__ import annotations
from typing import Any
from bcsfe import core
from bcsfe.cli import edits


class Stage:
    def __init__(self, clear_times: int):
        self.clear_times = clear_times

    @staticmethod
    def init() -> Stage:
        return Stage(0)

    @staticmethod
    def read(data: core.Data) -> Stage:
        clear_times = data.read_int()
        return Stage(clear_times)

    def write(self, data: core.Data):
        data.write_int(self.clear_times)

    def serialize(self) -> int:
        return self.clear_times

    @staticmethod
    def deserialize(data: int) -> Stage:
        return Stage(
            data,
        )

    def __repr__(self):
        return f"Stage({self.clear_times})"

    def __str__(self):
        return self.__repr__()

    def clear_stage(self, clear_amount: int = 1, ensure_cleared_only: bool = False):
        if ensure_cleared_only:
            self.clear_times = self.clear_times or clear_amount
        else:
            self.clear_times = clear_amount

    def unclear_stage(self):
        self.clear_times = 0


class Chapter:
    def __init__(self, selected_stage: int, total_stages: int = 0):
        self.selected_stage = selected_stage
        self.clear_progress = 0
        self.stages: list[Stage] = [Stage.init() for _ in range(total_stages)]
        self.chapter_unlock_state = 0

        self.total_stages = 0

    def clear_stage(
        self,
        index: int,
        clear_amount: int = 1,
        overwrite_clear_progress: bool = False,
        ensure_cleared_only: bool = False,
    ) -> bool:
        if overwrite_clear_progress:
            self.clear_progress = index + 1
        else:
            self.clear_progress = max(self.clear_progress, index + 1)
        self.chapter_unlock_state = 3
        self.stages[index].clear_stage(clear_amount, ensure_cleared_only)
        if index == self.total_stages - 1:
            return True
        return False

    def unclear_stage(self, index: int):
        self.clear_progress = min(self.clear_progress, index)
        self.stages[index].unclear_stage()
        return True

    @staticmethod
    def init(total_stages: int) -> Chapter:
        return Chapter(0, total_stages)

    @staticmethod
    def read_selected_stage(data: core.Data) -> Chapter:
        selected_stage = data.read_int()
        return Chapter(selected_stage)

    def write_selected_stage(self, data: core.Data):
        data.write_int(self.selected_stage)

    def read_clear_progress(self, data: core.Data):
        self.clear_progress = data.read_int()

    def write_clear_progress(self, data: core.Data):
        data.write_int(self.clear_progress)

    def read_stages(self, data: core.Data, total_stages: int):
        self.stages = [Stage.read(data) for _ in range(total_stages)]

    def write_stages(self, data: core.Data):
        for stage in self.stages:
            stage.write(data)

    def read_chapter_unlock_state(self, data: core.Data):
        self.chapter_unlock_state = data.read_int()

    def write_chapter_unlock_state(self, data: core.Data):
        data.write_int(self.chapter_unlock_state)

    def serialize(self) -> dict[str, Any]:
        return {
            "selected_stage": self.selected_stage,
            "clear_progress": self.clear_progress,
            "stages": [stage.serialize() for stage in self.stages],
            "chapter_unlock_state": self.chapter_unlock_state,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> Chapter:
        chapter = Chapter(data.get("selected_stage", 0))
        chapter.clear_progress = data.get("clear_progress", 0)
        chapter.stages = [Stage.deserialize(stage) for stage in data.get("stages", [])]
        chapter.chapter_unlock_state = data.get("chapter_unlock_state", 0)
        return chapter

    def __repr__(self):
        return f"Chapter({self.selected_stage}, {self.clear_progress}, {self.stages}, {self.chapter_unlock_state})"

    def __str__(self):
        return self.__repr__()


class ChaptersStars:
    def __init__(self, chapters: list[Chapter]):
        self.chapters = chapters

    def clear_stage(
        self,
        star: int,
        stage: int,
        clear_amount: int = 1,
        overwrite_clear_progress: bool = False,
        ensure_cleared_only: bool = False,
    ) -> bool:
        finished = self.chapters[star].clear_stage(
            stage, clear_amount, overwrite_clear_progress, ensure_cleared_only
        )
        if finished:
            if star + 1 < len(self.chapters):
                self.chapters[star + 1].chapter_unlock_state = 1
        return finished

    def unclear_stage(self, star: int, stage: int):
        finished = self.chapters[star].unclear_stage(stage)
        if finished and star + 1 < len(self.chapters):
            for chapter in self.chapters[star + 1 :]:
                chapter.chapter_unlock_state = 0
        return finished

    @staticmethod
    def init(total_stages: int, total_stars: int) -> ChaptersStars:
        chapters = [Chapter.init(total_stages) for _ in range(total_stars)]
        return ChaptersStars(chapters)

    @staticmethod
    def read_selected_stage(data: core.Data, total_stars: int) -> ChaptersStars:
        chapters = [Chapter.read_selected_stage(data) for _ in range(total_stars)]
        return ChaptersStars(chapters)

    def write_selected_stage(self, data: core.Data):
        for chapter in self.chapters:
            chapter.write_selected_stage(data)

    def read_clear_progress(self, data: core.Data):
        for chapter in self.chapters:
            chapter.read_clear_progress(data)

    def write_clear_progress(self, data: core.Data):
        for chapter in self.chapters:
            chapter.write_clear_progress(data)

    def read_stages(self, data: core.Data, total_stages: int):
        for _ in range(total_stages):
            for chapter in self.chapters:
                chapter.stages.append(Stage.read(data))

    def write_stages(self, data: core.Data):
        for i in range(len(self.chapters[0].stages)):
            for chapter in self.chapters:
                chapter.stages[i].write(data)

    def read_chapter_unlock_state(self, data: core.Data):
        for chapter in self.chapters:
            chapter.read_chapter_unlock_state(data)

    def write_chapter_unlock_state(self, data: core.Data):
        for chapter in self.chapters:
            chapter.write_chapter_unlock_state(data)

    def serialize(self) -> list[dict[str, Any]]:
        return [chapter.serialize() for chapter in self.chapters]

    @staticmethod
    def deserialize(data: list[dict[str, Any]]) -> ChaptersStars:
        chapters = [Chapter.deserialize(chapter) for chapter in data]
        return ChaptersStars(chapters)

    def __repr__(self):
        return f"ChaptersStars({self.chapters})"

    def __str__(self):
        return self.__repr__()


class Chapters:
    def __init__(self, chapters: list[ChaptersStars]):
        self.chapters = chapters

    def get_total_stars(self, map: int) -> int:
        return len(self.chapters[map].chapters)

    def get_total_stages(self, map: int, star: int) -> int:
        return len(self.chapters[map].chapters[star].stages)

    def clear_stage(
        self,
        map: int,
        star: int,
        stage: int,
        clear_amount: int = 1,
        overwrite_clear_progress: bool = False,
        ensure_cleared_only: bool = False,
    ) -> bool:
        finished = self.chapters[map].clear_stage(
            star, stage, clear_amount, overwrite_clear_progress, ensure_cleared_only
        )
        if finished and map + 1 < len(self.chapters):
            self.chapters[map + 1].chapters[0].chapter_unlock_state = 1

        return finished

    def unclear_stage(self, map: int, star: int, stage: int) -> bool:
        finished = self.chapters[map].unclear_stage(star, stage)
        if finished and map + 1 < len(self.chapters) and star == 0:
            for chapter in self.chapters[map + 1].chapters:
                chapter.chapter_unlock_state = 0

        return finished

    @staticmethod
    def init() -> Chapters:
        return Chapters([])

    @staticmethod
    def read(data: core.Data, read_every_time: bool = True) -> Chapters:
        total_stages = 0
        total_chapters = 0
        total_stars = 0
        if read_every_time:
            total_chapters = data.read_int()
            total_stars = data.read_int()
        else:
            total_chapters = data.read_int()
            total_stages = data.read_int()
            total_stars = data.read_int()

        chapters = [
            ChaptersStars.read_selected_stage(data, total_stars)
            for _ in range(total_chapters)
        ]

        if read_every_time:
            total_chapters = data.read_int()
            total_stars = data.read_int()

        for chapter in chapters:
            chapter.read_clear_progress(data)

        if read_every_time:
            total_chapters = data.read_int()
            total_stages = data.read_int()
            total_stars = data.read_int()

        for chapter in chapters:
            chapter.read_stages(data, total_stages)

        if read_every_time:
            total_chapters = data.read_int()
            total_stars = data.read_int()

        for chapter in chapters:
            chapter.read_chapter_unlock_state(data)

        return Chapters(chapters)

    def get_lengths(self) -> tuple[int, int, int]:
        total_chapters = len(self.chapters)
        try:
            total_stages = len(self.chapters[0].chapters[0].stages)
        except IndexError:
            total_stages = 0

        try:
            total_stars = len(self.chapters[0].chapters)
        except IndexError:
            total_stars = 0
        return (total_chapters, total_stages, total_stars)

    def write(self, data: core.Data, write_every_time: bool = True):
        total_chapters, total_stages, total_stars = self.get_lengths()
        if write_every_time:
            data.write_int(total_chapters)
            data.write_int(total_stars)
        else:
            data.write_int(total_chapters)
            data.write_int(total_stages)
            data.write_int(total_stars)
        for chapter in self.chapters:
            chapter.write_selected_stage(data)

        if write_every_time:
            data.write_int(total_chapters)
            data.write_int(total_stars)
        for chapter in self.chapters:
            chapter.write_clear_progress(data)

        if write_every_time:
            data.write_int(total_chapters)
            data.write_int(total_stages)
            data.write_int(total_stars)
        for chapter in self.chapters:
            chapter.write_stages(data)

        if write_every_time:
            data.write_int(total_chapters)
            data.write_int(total_stars)
        for chapter in self.chapters:
            chapter.write_chapter_unlock_state(data)

    def serialize(self) -> list[list[dict[str, Any]]]:
        return [chapter.serialize() for chapter in self.chapters]

    @staticmethod
    def deserialize(data: list[list[dict[str, Any]]]) -> Chapters:
        chapters = [ChaptersStars.deserialize(chapter) for chapter in data]
        tower_chapters = Chapters(chapters)
        return tower_chapters

    def __repr__(self):
        return f"Chapters({self.chapters})"

    def __str__(self):
        return self.__repr__()

    def unclear_rest(self, stages: list[int], stars: int, id: int):
        if not stages:
            return
        for star in range(stars, self.get_total_stars(id)):
            for stage in range(max(stages), self.get_total_stages(id, star)):
                self.chapters[id].chapters[star].stages[stage].clear_times = 0
                self.chapters[id].chapters[star].clear_progress = 0

    def edit_chapters(
        self, save_file: core.SaveFile, letter_code: str, base_index: int
    ) -> dict[int, bool] | None:
        return edits.map.edit_chapters(
            save_file, self, letter_code, base_index=base_index
        )

    def set_total_stages(self, map: int, total_stages: int):
        for chapter in self.chapters[map].chapters:
            chapter.total_stages = total_stages


# ============================================================
# FILE: dojo.py
# ============================================================
from __future__ import annotations
from typing import Any
from bcsfe import core
from bcsfe.cli import dialog_creator


class Stage:
    def __init__(self, score: int):
        self.score = score

    @staticmethod
    def init() -> Stage:
        return Stage(0)

    @staticmethod
    def read(stream: core.Data) -> Stage:
        score = stream.read_int()
        return Stage(score)

    def write(self, stream: core.Data):
        stream.write_int(self.score)

    def serialize(self) -> int:
        return self.score

    @staticmethod
    def deserialize(data: int) -> Stage:
        return Stage(data)

    def __repr__(self) -> str:
        return f"Stage(score={self.score!r})"

    def __str__(self) -> str:
        return f"Stage(score={self.score!r})"


class Chapter:
    def __init__(self, stages: dict[int, Stage]):
        self.stages = stages

    def get_stage(self, stage_id: int) -> Stage:
        if stage_id not in self.stages:
            self.stages[stage_id] = Stage.init()
        return self.stages[stage_id]

    @staticmethod
    def init() -> Chapter:
        return Chapter({})

    @staticmethod
    def read(stream: core.Data) -> Chapter:
        total = stream.read_int()
        stages: dict[int, Stage] = {}
        for _ in range(total):
            stage_id = stream.read_int()
            stage = Stage.read(stream)
            stages[stage_id] = stage

        return Chapter(stages)

    def write(self, stream: core.Data):
        stream.write_int(len(self.stages))
        for stage_id, stage in self.stages.items():
            stream.write_int(stage_id)
            stage.write(stream)

    def serialize(self) -> dict[int, Any]:
        return {stage_id: stage.serialize() for stage_id, stage in self.stages.items()}

    @staticmethod
    def deserialize(data: dict[int, Any]) -> Chapter:
        return Chapter(
            {stage_id: Stage.deserialize(stage) for stage_id, stage in data.items()}
        )

    def __repr__(self) -> str:
        return f"Chapter(stages={self.stages!r})"

    def __str__(self) -> str:
        return f"Chapter(stages={self.stages!r})"


class Chapters:
    def __init__(self, chapters: dict[int, Chapter]):
        self.chapters = chapters

    def get_stage(self, chapter_id: int, stage_id: int) -> Stage:
        if chapter_id not in self.chapters:
            self.chapters[chapter_id] = Chapter.init()
        return self.chapters[chapter_id].get_stage(stage_id)

    @staticmethod
    def init() -> Chapters:
        return Chapters({})

    @staticmethod
    def read(stream: core.Data) -> Chapters:
        total = stream.read_int()
        chapters: dict[int, Chapter] = {}
        for _ in range(total):
            chapter_id = stream.read_int()
            chapter = Chapter.read(stream)
            chapters[chapter_id] = chapter

        return Chapters(chapters)

    def write(self, stream: core.Data):
        stream.write_int(len(self.chapters))
        for chapter_id, chapter in self.chapters.items():
            stream.write_int(chapter_id)
            chapter.write(stream)

    def serialize(self) -> dict[int, Any]:
        return {
            chapter_id: chapter.serialize()
            for chapter_id, chapter in self.chapters.items()
        }

    @staticmethod
    def deserialize(data: dict[int, Any]) -> Chapters:
        return Chapters(
            {
                chapter_id: Chapter.deserialize(chapter)
                for chapter_id, chapter in data.items()
            }
        )

    def __repr__(self) -> str:
        return f"Chapters(chapters={self.chapters!r})"

    def __str__(self) -> str:
        return f"Chapters(chapters={self.chapters!r})"


class Ranking:
    def __init__(
        self,
        score: int,
        ranking: int,
        has_submitted: bool,
        has_completed: bool,
        has_seen_results: bool,
        start_date: int,
        end_date: int,
        event_number: int,
        should_show_rank_description: bool,
        should_show_start_message: bool,
        submit_error_flag: bool,
        other: str | None,
    ):
        self.score = score
        self.ranking = ranking
        self.has_submitted = has_submitted
        self.has_completed = has_completed
        self.has_seen_results = has_seen_results
        self.start_date = start_date
        self.end_date = end_date
        self.event_number = event_number
        self.should_show_rank_description = should_show_rank_description
        self.should_show_start_message = should_show_start_message
        self.submit_error_flag = submit_error_flag
        self.did_win_rewards = False
        self.other = other

    @staticmethod
    def init() -> Ranking:
        return Ranking(
            0,
            0,
            False,
            False,
            False,
            0,
            0,
            0,
            False,
            False,
            False,
            None,
        )

    @staticmethod
    def read(stream: core.Data, game_version: core.GameVersion) -> Ranking:
        score = stream.read_int()
        ranking = stream.read_int()
        has_submitted = stream.read_bool()
        has_completed = stream.read_bool()
        has_seen_results = stream.read_bool()
        start_date = stream.read_int()
        end_date = stream.read_int()
        event_number = stream.read_int()
        should_show_rank_description = stream.read_bool()
        should_show_start_message = stream.read_bool()
        submit_error_flag = stream.read_bool()

        if game_version >= 140500:
            # game seems to do more that just this, may break in the future
            other = stream.read_string()
        else:
            other = None
        return Ranking(
            score,
            ranking,
            has_submitted,
            has_completed,
            has_seen_results,
            start_date,
            end_date,
            event_number,
            should_show_rank_description,
            should_show_start_message,
            submit_error_flag,
            other,
        )

    def write(self, stream: core.Data, game_version: core.GameVersion):
        stream.write_int(self.score)
        stream.write_int(self.ranking)
        stream.write_bool(self.has_submitted)
        stream.write_bool(self.has_completed)
        stream.write_bool(self.has_seen_results)
        stream.write_int(self.start_date)
        stream.write_int(self.end_date)
        stream.write_int(self.event_number)
        stream.write_bool(self.should_show_rank_description)
        stream.write_bool(self.should_show_start_message)
        stream.write_bool(self.submit_error_flag)
        if game_version >= 140500:
            # game seems to do more that just this, may break in the future
            stream.write_string(self.other or "")

    def read_did_win_rewards(self, stream: core.Data):
        self.did_win_rewards = stream.read_bool()

    def write_did_win_rewards(self, stream: core.Data):
        stream.write_bool(self.did_win_rewards)

    def serialize(self) -> dict[str, Any]:
        return {
            "score": self.score,
            "ranking": self.ranking,
            "has_submitted": self.has_submitted,
            "has_completed": self.has_completed,
            "has_seen_results": self.has_seen_results,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "event_number": self.event_number,
            "should_show_rank_description": self.should_show_rank_description,
            "should_show_start_message": self.should_show_start_message,
            "submit_error_flag": self.submit_error_flag,
            "did_win_rewards": self.did_win_rewards,
            "other": self.other,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> Ranking:
        ranking = Ranking(
            data.get("score", 0),
            data.get("ranking", 0),
            data.get("has_submitted", False),
            data.get("has_completed", False),
            data.get("has_seen_results", False),
            data.get("start_date", 0),
            data.get("end_date", 0),
            data.get("event_number", 0),
            data.get("should_show_rank_description", False),
            data.get("should_show_start_message", False),
            data.get("submit_error_flag", False),
            data.get("other", None),
        )
        ranking.did_win_rewards = data.get("did_win_rewards", False)
        return ranking

    def __repr__(self) -> str:
        return (
            f"Ranking(score={self.score!r}, ranking={self.ranking!r}, "
            f"has_submitted={self.has_submitted!r}, has_completed={self.has_completed!r}, "
            f"has_seen_results={self.has_seen_results!r}, start_date={self.start_date!r}, "
            f"end_date={self.end_date!r}, event_number={self.event_number!r}, "
            f"should_show_rank_description={self.should_show_rank_description!r}, "
            f"should_show_start_message={self.should_show_start_message!r}, "
            f"submit_error_flag={self.submit_error_flag!r},"
            f"did_win_rewards={self.did_win_rewards!r}),"
            f"other={self.other!r})"
        )

    def __str__(self) -> str:
        return self.__repr__()


class Dojo:
    def __init__(self, chapters: Chapters):
        self.chapters = chapters
        self.item_lock_flags = False
        self.item_locks = [False] * 6
        self.ranking = Ranking.init()

    @staticmethod
    def init() -> Dojo:
        return Dojo(Chapters.init())

    @staticmethod
    def read_chapters(stream: core.Data) -> Dojo:
        chapters = Chapters.read(stream)
        return Dojo(chapters)

    def write_chapters(self, stream: core.Data):
        self.chapters.write(stream)

    def read_item_locks(self, stream: core.Data):
        self.item_lock_flags = stream.read_bool()
        self.item_locks = stream.read_bool_list(6)

    def write_item_locks(self, stream: core.Data):
        stream.write_bool(self.item_lock_flags)
        stream.write_bool_list(self.item_locks, write_length=False, length=6)

    def read_ranking(self, stream: core.Data, game_version: core.GameVersion):
        self.ranking = Ranking.read(stream, game_version)

    def write_ranking(self, stream: core.Data, game_version: core.GameVersion):
        self.ranking.write(stream, game_version)

    def serialize(self) -> dict[str, Any]:
        return {
            "chapters": self.chapters.serialize(),
            "item_locks": self.item_locks,
            "item_lock_flags": self.item_lock_flags,
            "ranking": self.ranking.serialize(),
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> Dojo:
        chapters = Chapters.deserialize(data.get("chapters", {}))
        item_locks = data.get("item_locks", [])
        item_lock_flags = data.get("item_lock_flags", False)
        dojo = Dojo(chapters)
        dojo.item_locks = item_locks
        dojo.item_lock_flags = item_lock_flags
        dojo.ranking = Ranking.deserialize(data.get("ranking", {}))
        return dojo

    def __repr__(self) -> str:
        return f"Dojo(chapters={self.chapters!r}, item_locks={self.item_locks!r}, item_lock_flags={self.item_lock_flags!r}, ranking={self.ranking!r})"

    def __str__(self) -> str:
        return self.__repr__()

    def edit_score(self):
        stage = self.chapters.get_stage(0, 0)
        stage.score = dialog_creator.SingleEditor(
            "dojo_score",
            stage.score,
            None,
            localized_item=True,
        ).edit()


def edit_dojo_score(save_file: core.SaveFile):
    save_file.dojo.edit_score()


# ============================================================
# FILE: enigma.py
# ============================================================
from __future__ import annotations
import time
from typing import Any
from bcsfe import core
from bcsfe.cli import dialog_creator, color


class Stage:
    def __init__(
        self,
        level: int,
        stage_id: int,
        decoding_satus: int,
        start_time: float,
    ):
        self.level = level
        self.stage_id = stage_id
        self.decoding_satus = decoding_satus
        self.start_time = start_time

    @staticmethod
    def init() -> Stage:
        return Stage(0, 0, 0, 0.0)

    @staticmethod
    def read(data: core.Data) -> Stage:
        level = data.read_int()
        stage_id = data.read_int()
        decoding_satus = data.read_byte()
        start_time = data.read_double()

        return Stage(level, stage_id, decoding_satus, start_time)

    def write(self, data: core.Data):
        data.write_int(self.level)
        data.write_int(self.stage_id)
        data.write_byte(self.decoding_satus)
        data.write_double(self.start_time)

    def serialize(self) -> dict[str, Any]:
        return {
            "level": self.level,
            "stage_id": self.stage_id,
            "decoding_satus": self.decoding_satus,
            "start_time": self.start_time,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> Stage:
        return Stage(
            data.get("level", 0),
            data.get("stage_id", 0),
            data.get("decoding_satus", 0),
            data.get("start_time", 0.0),
        )

    def __repr__(self):
        return f"Stage({self.level}, {self.stage_id}, {self.decoding_satus}, {self.start_time})"

    def __str__(self):
        return self.__repr__()


class Enigma:
    def __init__(
        self,
        energy_since_1: int,
        energy_since_2: int,
        enigma_level: int,
        unknown_1: int,
        unknown_2: bool,
        stages: list[Stage],
        extra: tuple[int, int, int, float] | None,
    ):
        self.energy_since_1 = energy_since_1
        self.energy_since_2 = energy_since_2
        self.enigma_level = enigma_level
        self.unknown_1 = unknown_1
        self.unknown_2 = unknown_2
        self.stages = stages
        self.extra = extra

    @staticmethod
    def init() -> Enigma:
        return Enigma(0, 0, 0, 0, False, [], None)

    @staticmethod
    def read(data: core.Data, game_version: core.GameVersion) -> Enigma:
        energy_since_1 = data.read_int()
        energy_since_2 = data.read_int()
        enigma_level = data.read_byte()
        unknown_1 = data.read_byte()
        unknown_2 = data.read_bool()

        total_stages = data.read_byte()

        stages = [Stage.read(data) for _ in range(total_stages)]

        extra_data = None

        if game_version >= 140500:
            has_extra = data.read_bool()
            if has_extra:
                extra_data = (
                    data.read_int(),
                    data.read_int(),
                    data.read_byte(),
                    data.read_double(),
                )
        return Enigma(
            energy_since_1,
            energy_since_2,
            enigma_level,
            unknown_1,
            unknown_2,
            stages,
            extra_data,
        )

    def write(self, data: core.Data, game_version: core.GameVersion):
        data.write_int(self.energy_since_1)
        data.write_int(self.energy_since_2)
        data.write_byte(self.enigma_level)
        data.write_byte(self.unknown_1)
        data.write_bool(self.unknown_2)
        data.write_byte(len(self.stages))
        for stage in self.stages:
            stage.write(data)

        if game_version >= 140500:
            data.write_bool(self.extra is not None)
            if self.extra is not None:
                data.write_int(self.extra[0])
                data.write_int(self.extra[1])
                data.write_byte(self.extra[2])
                data.write_double(self.extra[3])

    def serialize(self) -> dict[str, Any]:
        return {
            "energy_since_1": self.energy_since_1,
            "energy_since_2": self.energy_since_2,
            "enigma_level": self.enigma_level,
            "unknown_1": self.unknown_1,
            "unknown_2": self.unknown_2,
            "stages": [stage.serialize() for stage in self.stages],
            "extra": self.extra,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> Enigma:
        return Enigma(
            data.get("energy_since_1", 0),
            data.get("energy_since_2", 0),
            data.get("enigma_level", 0),
            data.get("unknown_1", 0),
            data.get("unknown_2", False),
            [Stage.deserialize(stage) for stage in data.get("stages", [])],
            data.get("extra", None),
        )

    def __repr__(self):
        return f"Enigma({self.energy_since_1}, {self.energy_since_2}, {self.enigma_level}, {self.unknown_1}, {self.unknown_2}, {self.stages}, {self.extra})"

    def __str__(self):
        return self.__repr__()

    def edit_enigma(self, save_file: core.SaveFile):
        names = core.MapNames(save_file, "H", base_index=25000).map_names
        names_list: list[str] = []
        keys = list(names.keys())
        keys.sort()
        for id in keys:
            name = names[id]
            if name is None:
                name = core.core_data.local_manager.get_key(
                    "unknown_enigma_name", id=id
                )
            names_list.append(name)

        base_level = 25000

        color.ColoredText.localize("current_enigma_stages")
        for stage in self.stages:
            name = names[stage.stage_id - base_level]
            if name is None:
                name = core.core_data.local_manager.get_key(
                    "unknown_enigma_name", id=stage.stage_id
                )
            color.ColoredText.localize(
                "enigma_stage", name=name, id=stage.stage_id - base_level
            )

        if self.stages:
            wipe = dialog_creator.YesNoInput().get_input_once("wipe_enigma")
            if wipe is None:
                return
            if wipe:
                for stage in self.stages:
                    id = stage.stage_id
                    save_file.event_stages.chapter_completion_count[id] = 0
                self.stages = []

        ids, _ = dialog_creator.ChoiceInput(
            names_list,
            names_list,
            [],
            {},
            "enigma_select",
        ).multiple_choice()
        if ids is None:
            return

        for enigma_id in ids:
            abs_id = enigma_id + base_level
            save_file.event_stages.chapter_completion_count[abs_id] = 0
            # TODO: level? they can go much higher than 3... not sure it really matters though
            stage = Stage(3, abs_id, 2, int(time.time()))
            self.stages.append(stage)

        color.ColoredText.localize("enigma_success")


def edit_enigma(save_file: core.SaveFile):
    save_file.enigma.edit_enigma(save_file)


# ============================================================
# FILE: event.py
# ============================================================
from __future__ import annotations
from typing import Any
from bcsfe import core
from bcsfe.cli import color, dialog_creator, edits


class EventStage:
    def __init__(self, clear_amount: int):
        self.clear_amount = clear_amount

    @staticmethod
    def init() -> EventStage:
        return EventStage(0)

    @staticmethod
    def read(data: core.Data, is_int: bool) -> EventStage:
        if is_int:
            clear_amount = data.read_int()
        else:
            clear_amount = data.read_short()
        return EventStage(clear_amount)

    def write(self, data: core.Data, is_int: bool):
        if is_int:
            data.write_int(self.clear_amount)
        else:
            data.write_short(self.clear_amount)

    def serialize(self) -> int:
        return self.clear_amount

    @staticmethod
    def deserialize(data: int) -> EventStage:
        return EventStage(
            clear_amount=data,
        )

    def __repr__(self) -> str:
        return f"<EventStage clear_amount={self.clear_amount}>"

    def __str__(self) -> str:
        return self.__repr__()

    def clear_stage(self, clear_amount: int = 1, ensure_cleared_only: bool = False):
        if ensure_cleared_only:
            self.clear_amount = self.clear_amount or clear_amount
        else:
            self.clear_amount = clear_amount

    def unclear_stage(self):
        self.clear_amount = 0


class EventSubChapter:
    def __init__(self, selected_stage: int, total_stages: int = 0):
        self.selected_stage = selected_stage
        self.clear_progress = 0
        self.stages = [EventStage.init() for _ in range(total_stages)]
        self.chapter_unlock_state = 0

    def clear_stage(
        self,
        index: int,
        clear_amount: int = 1,
        overwrite_clear_progress: bool = False,
        ensure_cleared_only: bool = False,
    ) -> bool:
        if overwrite_clear_progress:
            self.clear_progress = index + 1
        else:
            self.clear_progress = max(self.clear_progress, index + 1)
        self.stages[index].clear_stage(clear_amount, ensure_cleared_only)
        self.chapter_unlock_state = 3
        if index == len(self.stages) - 1:
            return True
        return False

    def unclear_stage(self, index: int) -> bool:
        self.clear_progress = min(self.clear_progress, index)
        self.stages[index].unclear_stage()

        return True

    def clear_map(self, increment: bool = True) -> bool:
        self.clear_progress = len(self.stages)
        self.chapter_unlock_state = 3
        for stage in self.stages:
            if increment:
                clear_amount = stage.clear_amount + 1
            else:
                clear_amount = stage.clear_amount or 1
            stage.clear_stage(clear_amount)
        return True

    @staticmethod
    def init(total_stages: int) -> EventSubChapter:
        return EventSubChapter(0, total_stages)

    @staticmethod
    def read_selected_stage(data: core.Data, is_int: bool) -> EventSubChapter:
        if is_int:
            selected_stage = data.read_int()
        else:
            selected_stage = data.read_byte()
        return EventSubChapter(selected_stage)

    def write_selected_stage(self, data: core.Data, is_int: bool):
        if is_int:
            data.write_int(self.selected_stage)
        else:
            data.write_byte(self.selected_stage)

    def read_clear_progress(self, data: core.Data, is_int: bool):
        if is_int:
            self.clear_progress = data.read_int()
        else:
            self.clear_progress = data.read_byte()

    def write_clear_progress(self, data: core.Data, is_int: bool):
        if is_int:
            data.write_int(self.clear_progress)
        else:
            data.write_byte(self.clear_progress)

    def read_stages(self, data: core.Data, total_stages: int, is_int: bool):
        self.stages = [EventStage.read(data, is_int) for _ in range(total_stages)]

    def write_stages(self, data: core.Data, is_int: bool):
        for stage in self.stages:
            stage.write(data, is_int)

    def read_chapter_unlock_state(self, data: core.Data, is_int: bool):
        if is_int:
            self.chapter_unlock_state = data.read_int()
        else:
            self.chapter_unlock_state = data.read_byte()

    def write_chapter_unlock_state(self, data: core.Data, is_int: bool):
        if is_int:
            data.write_int(self.chapter_unlock_state)
        else:
            data.write_byte(self.chapter_unlock_state)

    def serialize(self) -> dict[str, Any]:
        return {
            "selected_stage": self.selected_stage,
            "clear_progress": self.clear_progress,
            "stages": [stage.serialize() for stage in self.stages],
            "chapter_unlock_state": self.chapter_unlock_state,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> EventSubChapter:
        sub_chapter = EventSubChapter(
            selected_stage=data.get("selected_stage", 0),
        )
        sub_chapter.clear_progress = data.get("clear_progress", 0)
        sub_chapter.stages = [
            EventStage.deserialize(stage) for stage in data.get("stages", [])
        ]
        sub_chapter.chapter_unlock_state = data.get("chapter_unlock_state", 0)
        return sub_chapter

    def __repr__(self) -> str:
        return f"<EventSubChapter selected_stage={self.selected_stage}, clear_progress={self.clear_progress}, stages={self.stages}, chapter_unlock_state={self.chapter_unlock_state}>"

    def __str__(self) -> str:
        return self.__repr__()


class EventSubChapterStars:
    def __init__(self, chapters: list[EventSubChapter]):
        self.chapters = chapters
        self.legend_restriction = 0

    def clear_stage(
        self,
        star: int,
        stage: int,
        clear_amount: int = 1,
        overwrite_clear_progress: bool = False,
        ensure_cleared_only: bool = False,
    ) -> bool:
        finished = self.chapters[star].clear_stage(
            stage, clear_amount, overwrite_clear_progress, ensure_cleared_only
        )
        if finished:
            if star + 1 < len(self.chapters):
                self.chapters[star + 1].chapter_unlock_state = 1
        return finished

    def unclear_stage(self, star: int, stage: int):
        finished = self.chapters[star].unclear_stage(stage)
        if finished and star + 1 < len(self.chapters):
            for chapter in self.chapters[star + 1 :]:
                chapter.chapter_unlock_state = 0
        return finished

    def clear_map(self, star: int, increment: bool = True) -> bool:
        finished = self.chapters[star].clear_map(increment)
        if finished:
            if star + 1 < len(self.chapters):
                self.chapters[star + 1].chapter_unlock_state = 1
        return finished

    def clear_chapter(self, increment: bool = True) -> bool:
        for chapter in self.chapters:
            chapter.clear_map(increment)
        return True

    @staticmethod
    def init(total_stars: int) -> EventSubChapterStars:
        return EventSubChapterStars(
            [EventSubChapter.init(0) for _ in range(total_stars)]
        )

    @staticmethod
    def read_selected_stage(
        data: core.Data, total_stars: int, is_int: bool
    ) -> EventSubChapterStars:
        chapters = [
            EventSubChapter.read_selected_stage(data, is_int)
            for _ in range(total_stars)
        ]
        return EventSubChapterStars(chapters)

    def write_selected_stage(self, data: core.Data, is_int: bool):
        for chapter in self.chapters:
            chapter.write_selected_stage(data, is_int)

    def read_clear_progress(self, data: core.Data, is_int: bool):
        for chapter in self.chapters:
            chapter.read_clear_progress(data, is_int)

    def write_clear_progress(self, data: core.Data, is_int: bool):
        for chapter in self.chapters:
            chapter.write_clear_progress(data, is_int)

    def read_stages(self, data: core.Data, total_stages: int, is_int: bool):
        for _ in range(total_stages):
            for chapter in self.chapters:
                chapter.stages.append(EventStage.read(data, is_int))
                # chapter.read_stages(data, total_stages, is_int)

    def write_stages(self, data: core.Data, is_int: bool):
        for i in range(len(self.chapters[0].stages)):
            for chapter in self.chapters:
                chapter.stages[i].write(data, is_int)
                # chapter.write_stages(data, is_int)

    def read_chapter_unlock_state(self, data: core.Data, is_int: bool):
        for chapter in self.chapters:
            chapter.read_chapter_unlock_state(data, is_int)

    def write_chapter_unlock_state(self, data: core.Data, is_int: bool):
        for chapter in self.chapters:
            chapter.write_chapter_unlock_state(data, is_int)

    def read_legend_restrictions(self, data: core.Data):
        self.legend_restriction = data.read_int()

    def write_legend_restrictions(self, data: core.Data):
        data.write_int(self.legend_restriction)

    def serialize(self) -> dict[str, Any]:
        return {
            "chapters": [chapter.serialize() for chapter in self.chapters],
            "legend_restriction": self.legend_restriction,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> EventSubChapterStars:
        chapters = [
            EventSubChapter.deserialize(chapter) for chapter in data.get("chapters", [])
        ]
        chapter = EventSubChapterStars(chapters)
        chapter.legend_restriction = data.get("legend_restriction", 0)
        return chapter

    def __repr__(self) -> str:
        return f"<EventSubChapterStars chapters={self.chapters}, legend_restriction={self.legend_restriction}>"

    def __str__(self) -> str:
        return self.__repr__()


class EventChapterGroup:
    def __init__(self, chapters: list[EventSubChapterStars]):
        self.chapters = chapters

    def clear_stage(
        self,
        map: int,
        star: int,
        stage: int,
        clear_amount: int = 1,
        overwrite_clear_progress: bool = False,
        ensure_cleared_only: bool = False,
    ) -> bool:
        finished = self.chapters[map].clear_stage(
            star,
            stage,
            clear_amount,
            overwrite_clear_progress,
            ensure_cleared_only,
        )
        if finished and map + 1 < len(self.chapters):
            self.chapters[map + 1].chapters[0].chapter_unlock_state = 1

        return finished

    def unclear_stage(self, map: int, star: int, stage: int) -> bool:
        finished = self.chapters[map].unclear_stage(star, stage)
        if finished and map + 1 < len(self.chapters) and star == 0:
            for chapter in self.chapters[map + 1].chapters:
                chapter.chapter_unlock_state = 0

        return finished

    def clear_map(self, map: int, star: int, increment: bool = True):
        finished = self.chapters[map].clear_map(star, increment)
        if finished and map + 1 < len(self.chapters):
            self.chapters[map + 1].chapters[0].chapter_unlock_state = 1

    def clear_chapter(self, map: int, increment: bool = True):
        finished = self.chapters[map].clear_chapter(increment)
        if finished and map + 1 < len(self.chapters):
            self.chapters[map + 1].chapters[0].chapter_unlock_state = 1

    def clear_group(self, increment: bool = True):
        for chapter in self.chapters:
            chapter.clear_chapter(increment)

    @staticmethod
    def init(total_subchapters: int, total_stars: int) -> EventChapterGroup:
        return EventChapterGroup(
            [EventSubChapterStars.init(total_stars) for _ in range(total_subchapters)]
        )

    @staticmethod
    def read_selected_stage(
        data: core.Data, total_subchapters: int, total_stars: int, is_int: bool
    ) -> EventChapterGroup:
        chapters = [
            EventSubChapterStars.read_selected_stage(data, total_stars, is_int)
            for _ in range(total_subchapters)
        ]
        return EventChapterGroup(chapters)

    def write_selected_stage(self, data: core.Data, is_int: bool):
        for chapter in self.chapters:
            chapter.write_selected_stage(data, is_int)

    def read_clear_progress(self, data: core.Data, is_int: bool):
        for chapter in self.chapters:
            chapter.read_clear_progress(data, is_int)

    def write_clear_progress(self, data: core.Data, is_int: bool):
        for chapter in self.chapters:
            chapter.write_clear_progress(data, is_int)

    def read_stages(self, data: core.Data, total_stages: int, is_int: bool):
        for chapter in self.chapters:
            chapter.read_stages(data, total_stages, is_int)

    def write_stages(self, data: core.Data, is_int: bool):
        for chapter in self.chapters:
            chapter.write_stages(data, is_int)

    def read_chapter_unlock_state(self, data: core.Data, is_int: bool):
        for chapter in self.chapters:
            chapter.read_chapter_unlock_state(data, is_int)

    def write_chapter_unlock_state(self, data: core.Data, is_int: bool):
        for chapter in self.chapters:
            chapter.write_chapter_unlock_state(data, is_int)

    def read_legend_restrictions(self, data: core.Data):
        for chapter in self.chapters:
            chapter.read_legend_restrictions(data)

    def write_legend_restrictions(self, data: core.Data):
        for chapter in self.chapters:
            chapter.write_legend_restrictions(data)

    def serialize(self) -> list[dict[str, Any]]:
        return [chapter.serialize() for chapter in self.chapters]

    @staticmethod
    def deserialize(data: list[dict[str, Any]]) -> EventChapterGroup:
        chapters = [EventSubChapterStars.deserialize(chapter) for chapter in data]
        return EventChapterGroup(chapters)

    def __repr__(self) -> str:
        return f"<EventChapterGroup chapters={self.chapters}>"

    def __str__(self) -> str:
        return self.__repr__()


class EventChapters:
    def __init__(self, chapters: list[EventChapterGroup]):
        self.chapters = chapters
        self.chapter_completion_count: dict[int, int] = {}
        self.displayed_cleared_limit_text: dict[int, bool] = {}
        self.event_start_dates: dict[int, int] = {}
        self.stages_reward_claimed: list[int] = []

    def clear_stage(
        self,
        type: int,
        map: int,
        star: int,
        stage: int,
        clear_amount: int = 1,
        overwrite_clear_progress: bool = False,
        ensure_cleared_only: bool = False,
    ) -> bool:
        return self.chapters[type].clear_stage(
            map,
            star,
            stage,
            clear_amount,
            overwrite_clear_progress,
            ensure_cleared_only,
        )

    def unclear_stage(self, type: int, map: int, star: int, stage: int) -> bool:
        return self.chapters[type].unclear_stage(map, star, stage)

    def clear_map(self, type: int, map: int, star: int, increment: bool = True):
        self.chapters[type].clear_map(map, star, increment)

    def clear_chapter(self, type: int, map: int, increment: bool = True):
        self.chapters[type].clear_chapter(map, increment)

    def clear_group(self, type: int, increment: bool = True):
        self.chapters[type].clear_group(increment)

    @staticmethod
    def init(gv: core.GameVersion) -> EventChapters:
        if gv < 20:
            return EventChapters([])
        if gv <= 32:
            total_map_types = 3
            total_subchapters = 150
            stars_per_subchapter = 3
        elif gv <= 34:
            total_map_types = 4
            total_subchapters = 150
            stars_per_subchapter = 3
        else:
            total_map_types = 0
            total_subchapters = 0
            stars_per_subchapter = 0

        return EventChapters(
            [
                EventChapterGroup.init(total_subchapters, stars_per_subchapter)
                for _ in range(total_map_types)
            ]
        )

    @staticmethod
    def read(data: core.Data, gv: core.GameVersion) -> EventChapters:
        if gv < 20:
            return EventChapters([])
        stages_per_subchapter = 0
        if 80099 < gv:
            total_map_types = data.read_byte()
            total_subchapters = data.read_short()
            stars_per_subchapter = data.read_byte()
            stages_per_subchapter = data.read_byte()
            is_int = False
        elif gv <= 32:
            total_map_types = 3
            total_subchapters = 150
            stars_per_subchapter = 3
            is_int = True
        elif gv <= 34:
            total_map_types = 4
            total_subchapters = 150
            stars_per_subchapter = 3
            is_int = True
        else:
            total_map_types = data.read_int()
            total_subchapters = data.read_int()
            stars_per_subchapter = data.read_int()
            is_int = True
        chapters = [
            EventChapterGroup.read_selected_stage(
                data, total_subchapters, stars_per_subchapter, is_int
            )
            for _ in range(total_map_types)
        ]
        if 80099 < gv:
            is_int = False
        elif gv <= 32:
            total_map_types = 3
            total_subchapters = 150
            stars_per_subchapter = 3
            is_int = True
        elif gv <= 34:
            total_map_types = 4
            total_subchapters = 150
            stars_per_subchapter = 3
            is_int = True
        else:
            total_map_types = data.read_int()
            total_subchapters = data.read_int()
            stars_per_subchapter = data.read_int()
            is_int = True

        for chapter in chapters:
            chapter.read_clear_progress(data, is_int)

        if 80099 < gv:
            is_int = False
        elif gv <= 32:
            total_map_types = 3
            total_subchapters = 150
            stars_per_subchapter = 3
            stages_per_subchapter = 12
            is_int = True
        elif gv <= 34:
            total_map_types = 4
            total_subchapters = 150
            stars_per_subchapter = 3
            stages_per_subchapter = 12
            is_int = True
        else:
            total_map_types = data.read_int()
            total_subchapters = data.read_int()
            stages_per_subchapter = data.read_int()
            stars_per_subchapter = data.read_int()
            is_int = True

        for chapter in chapters:
            chapter.read_stages(data, stages_per_subchapter, is_int)

        if 80099 < gv:
            is_int = False
        elif gv <= 32:
            total_map_types = 3
            total_subchapters = 150
            stars_per_subchapter = 3
            is_int = True
        elif gv <= 34:
            total_map_types = 4
            total_subchapters = 150
            stars_per_subchapter = 3
            is_int = True
        else:
            total_map_types = data.read_int()
            total_subchapters = data.read_int()
            stars_per_subchapter = data.read_int()
            is_int = True

        for chapter in chapters:
            chapter.read_chapter_unlock_state(data, is_int)

        return EventChapters(chapters)

    def get_lengths(self) -> tuple[int, int, int, int]:
        total_map_types = len(self.chapters)
        try:
            total_subchapters = len(self.chapters[0].chapters)
        except IndexError:
            total_subchapters = 0

        try:
            stars_per_subchapter = len(self.chapters[0].chapters[0].chapters)
        except IndexError:
            stars_per_subchapter = 0

        try:
            stages_per_subchapter = len(self.chapters[0].chapters[0].chapters[0].stages)
        except IndexError:
            stages_per_subchapter = 0
        return (
            total_map_types,
            total_subchapters,
            stars_per_subchapter,
            stages_per_subchapter,
        )

    def write(self, data: core.Data, gv: core.GameVersion):
        (
            total_map_types,
            total_subchapters,
            stars_per_subchapter,
            stages_per_subchapter,
        ) = self.get_lengths()
        if gv <= 34:
            is_int = True
        else:
            if 80099 < gv:
                data.write_byte(total_map_types)
                data.write_short(total_subchapters)
                data.write_byte(stars_per_subchapter)
                data.write_byte(stages_per_subchapter)
                is_int = False
            else:
                data.write_int(total_map_types)
                data.write_int(total_subchapters)
                data.write_int(stars_per_subchapter)
                is_int = True

        for chapter in self.chapters:
            chapter.write_selected_stage(data, is_int)

        if gv <= 34:
            is_int = True
        else:
            if 80099 < gv:
                is_int = False
            else:
                data.write_int(total_map_types)
                data.write_int(total_subchapters)
                data.write_int(stars_per_subchapter)
                is_int = True

        for chapter in self.chapters:
            chapter.write_clear_progress(data, is_int)

        if gv <= 34:
            is_int = True
        else:
            if 80099 < gv:
                is_int = False
            else:
                data.write_int(total_map_types)
                data.write_int(total_subchapters)
                data.write_int(stages_per_subchapter)
                data.write_int(stars_per_subchapter)
                is_int = True

        for chapter in self.chapters:
            chapter.write_stages(data, is_int)

        if gv <= 34:
            is_int = True
        else:
            if 80099 < gv:
                is_int = False
            else:
                data.write_int(total_map_types)
                data.write_int(total_subchapters)
                data.write_int(stars_per_subchapter)
                is_int = True

        for chapter in self.chapters:
            chapter.write_chapter_unlock_state(data, is_int)

    def read_legend_restrictions(self, data: core.Data, gv: core.GameVersion):
        if gv < 20:
            return
        if gv < 33:
            total_map_types = 3  # type: ignore
            total_subchapters = 150  # type: ignore
        elif gv < 41:
            total_map_types = 4  # type: ignore
            total_subchapters = 150  # type: ignore
        else:
            total_map_types = data.read_int()  # type: ignore
            total_subchapters = data.read_int()  # type: ignore

        for chapter in self.chapters:
            chapter.read_legend_restrictions(data)

    def write_legend_restrictions(self, data: core.Data, gv: core.GameVersion):
        if gv < 20:
            return
        if gv >= 41:
            data.write_int(len(self.chapters))
            try:
                data.write_int(len(self.chapters[0].chapters))
            except IndexError:
                data.write_int(0)

        for chapter in self.chapters:
            chapter.write_legend_restrictions(data)

    def read_dicts(self, data: core.Data):
        self.chapter_completion_count = data.read_int_int_dict()
        self.displayed_cleared_limit_text = data.read_int_bool_dict()
        self.event_start_dates = data.read_int_int_dict()
        self.stages_reward_claimed = data.read_int_list()

    def write_dicts(self, data: core.Data):
        data.write_int_int_dict(self.chapter_completion_count)
        data.write_int_bool_dict(self.displayed_cleared_limit_text)
        data.write_int_int_dict(self.event_start_dates)
        data.write_int_list(self.stages_reward_claimed)

    def serialize(self) -> dict[str, Any]:
        return {
            "chapters": [chapter.serialize() for chapter in self.chapters],
            "chapter_completion_count": self.chapter_completion_count,
            "displayed_cleared_limit_text": self.displayed_cleared_limit_text,
            "event_start_dates": self.event_start_dates,
            "stages_reward_claimed": self.stages_reward_claimed,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> EventChapters:
        chapters = [
            EventChapterGroup.deserialize(chapter)
            for chapter in data.get("chapters", [])
        ]
        ch = EventChapters(chapters)
        ch.chapter_completion_count = data.get("chapter_completion_count", {})
        ch.displayed_cleared_limit_text = data.get("displayed_cleared_limit_text", {})
        ch.event_start_dates = data.get("event_start_dates", {})
        ch.stages_reward_claimed = data.get("stages_reward_claimed", [])
        return ch

    def __repr__(self) -> str:
        return f"EventChapters({self.chapters}, {self.chapter_completion_count}, {self.displayed_cleared_limit_text}, {self.event_start_dates}, {self.stages_reward_claimed})"

    def __str__(self) -> str:
        return self.__repr__()

    def get_total_stars(self, type: int, map: int) -> int:
        try:
            return len(self.chapters[type].chapters[map].chapters)
        except IndexError:
            return len(self.chapters[0].chapters[0].chapters)

    def get_total_stages(self, type: int, map: int, star: int) -> int:
        try:
            return len(self.chapters[type].chapters[map].chapters[star].stages)
        except IndexError:
            return len(self.chapters[0].chapters[0].chapters[0].stages)

    @staticmethod
    def ask_stars(
        max_stars: int, prompt: str = "custom_star_count_per_chapter"
    ) -> int | None:
        if max_stars <= 1:
            return max_stars
        stars = dialog_creator.IntInput(min=1, max=max_stars).get_input_locale(
            prompt, {"max": max_stars}
        )[0]
        if stars is None:
            return None
        return stars

    @staticmethod
    def ask_stars_unclear(
        max_stars: int, prompt: str = "custom_star_count_per_chapter"
    ) -> int | None:
        stars = dialog_creator.IntInput(min=0, max=max_stars).get_input_locale(
            prompt, {"max": max_stars}
        )[0]
        if stars is None:
            return None
        return stars

    @staticmethod
    def get_stage_names(map_names: core.MapNames, chapter_id: int) -> list[str] | None:
        stage_names = map_names.stage_names.get(chapter_id)
        if stage_names is None:
            return None
        new_stage_names: list[str] = []
        for stage in stage_names:
            if stage == "＠":
                continue
            new_stage_names.append(stage)
        return new_stage_names

    @staticmethod
    def ask_stages(map_names: core.MapNames, chapter_id: int) -> list[int] | None:
        stage_names = EventChapters.get_stage_names(map_names, chapter_id)
        if stage_names is None:
            return None

        dialog_creator.ListOutput(
            stage_names, ints=[], dialog="select_stage", localize_elements=False
        ).display_locale()

        choices = dialog_creator.RangeInput(len(stage_names), 1).get_input_locale(
            "stages_select", {}
        )
        if choices is None:
            return None
        return [c - 1 for c in choices]

    @staticmethod
    def ask_stages_stage_names(stage_names: list[str]) -> list[int] | None:
        val = EventChapters.ask_stages_stage_names_one(stage_names)
        if val is None:
            return None
        return list(range(val + 1))

    @staticmethod
    def ask_stages_stage_names_one(stage_names: list[str]) -> int | None:
        new_stage_names: list[str] = []
        for stage in stage_names:
            if stage == "＠":
                continue
            new_stage_names.append(stage)
        stage_names = new_stage_names
        choice = dialog_creator.ChoiceInput.from_reduced(
            stage_names, dialog="select_stage_progress", single_choice=True
        ).single_choice()
        if choice is None:
            return None
        return choice - 1

    @staticmethod
    def ask_clear_amount() -> int | None:
        val = dialog_creator.IntInput(
            max=core.core_data.max_value_manager.get("stage_clear_count"), bit_count=16
        ).get_input_locale("clear_amount_enter", {})[0]

        return val

    @staticmethod
    def edit_sol_chapters(save_file: core.SaveFile):
        EventChapters.edit_chapters(save_file, 0, "N", 0)

    @staticmethod
    def edit_event_chapters(save_file: core.SaveFile):
        EventChapters.edit_chapters(save_file, 1, "S", 1000)

    @staticmethod
    def edit_collab_chapters(save_file: core.SaveFile):
        EventChapters.edit_chapters(save_file, 2, "C", 2000)

    @staticmethod
    def select_map_names(names_dict: dict[int, str | None]) -> list[int] | None:
        map_ids: list[int] = []
        names_list: list[str] = []
        names_dict = dict(sorted(names_dict.items()))
        ids = list(names_dict.keys())
        for id, map_name in names_dict.items():
            if map_name is None:
                map_name = core.core_data.local_manager.get_key(
                    "unknown_map_name", id=id
                )
            else:
                map_name = core.core_data.local_manager.get_key(
                    "map_name", name=map_name, id=id, escape=False
                )
            names_list.append(map_name)

        while True:
            dialog_creator.ListOutput(
                names_list, [], "select_map", localize_elements=False
            ).display_locale()
            if names_list:
                example_name = names_list[0]
            else:
                example_name = ""
            usr_input = (
                color.ColoredInput()
                .localize("select_map_dialog", example=example_name, escape=False)
                .lower()
                .strip()
            )
            if usr_input == "q":
                return None
            usr_ids = dialog_creator.RangeInput(max=len(names_list), min=1).parse(
                usr_input
            )
            if not usr_ids:
                found_names: list[tuple[int, str]] = []
                for i, name in enumerate(names_list):
                    if usr_input.replace(" ", "_") in name.lower().strip().replace(
                        " ", "_"
                    ):
                        true_id = ids[i]
                        found_names.append((i, name))

                if len(found_names) == 0:
                    color.ColoredText.localize("no_map_found", name=usr_input)
                elif len(found_names) == 1:
                    id = found_names[0][0]
                    true_id = ids[id]
                    if true_id not in map_ids:
                        map_ids.append(true_id)
                else:
                    selected_ids, _ = dialog_creator.ChoiceInput.from_reduced(
                        [name for _, name in found_names],
                        dialog="select_map_from_names",
                    ).multiple_choice(False)
                    if selected_ids is None:
                        continue
                    for i in selected_ids:
                        id = found_names[i][0]
                        true_id = ids[id]
                        if true_id not in map_ids:
                            map_ids.append(true_id)
            else:
                for id in usr_ids:
                    id -= 1
                    true_id = ids[id]
                    if true_id not in map_ids:
                        map_ids.append(true_id)

            color.ColoredText.localize("current_maps", maps=map_ids)

            for id in map_ids:
                name = names_dict[id]
                EventChapters.print_current_chapter(name, id)

            option = dialog_creator.ChoiceInput.from_reduced(
                ["keep_selecting", "remove_selection", "finish_selection"],
                dialog="map_selection_q",
            ).single_choice()
            if option is None:
                return None

            option -= 1
            if option == 0:
                continue
            if option == 1:
                map_ids.clear()
            else:
                break
        return map_ids

    @staticmethod
    def print_current_chapter(name: str | None, id: int):
        if name is None:
            name = core.core_data.local_manager.get_key("unknown_map_name", id=id)
        color.ColoredText.localize(
            "current_sol_chapter", escape=False, name=name, id=id
        )

    @staticmethod
    def print_current_stage(name: str | None, index: int):
        if name is None:
            name = core.core_data.local_manager.get_key(
                "unknown_stage_name", index=index
            )
        color.ColoredText.localize("current_stage_map", name=name, index=index)

    @staticmethod
    def edit_chapters(
        save_file: core.SaveFile, type: int, letter_code: str, base_index: int
    ):
        edits.map.edit_chapters(
            save_file,
            save_file.event_stages,
            letter_code,
            type=type,
            base_index=base_index,
        )

    def unclear_rest(
        self,
        stages: list[int],
        stars: int,
        id: int,
        type: int,
    ):
        if not stages:
            return
        for star in range(stars, self.get_total_stars(type, id)):
            for stage in range(max(stages), self.get_total_stages(type, id, star)):
                self.chapters[type].chapters[id].chapters[star].stages[
                    stage
                ].clear_amount = 0
                self.chapters[type].chapters[id].chapters[star].clear_progress = 0


# ============================================================
# FILE: ex_stage.py
# ============================================================
from __future__ import annotations
from bcsfe import core


class Stage:
    def __init__(self, clear_amount: int):
        self.clear_amount = clear_amount

    @staticmethod
    def init() -> Stage:
        return Stage(0)

    @staticmethod
    def read(stream: core.Data) -> Stage:
        clear_amount = stream.read_int()
        return Stage(clear_amount)

    def write(self, stream: core.Data):
        stream.write_int(self.clear_amount)

    def serialize(self) -> int:
        return self.clear_amount

    @staticmethod
    def deserialize(data: int) -> Stage:
        return Stage(data)

    def __repr__(self) -> str:
        return f"Stage(clear_amount={self.clear_amount!r})"

    def __str__(self) -> str:
        return f"Stage(clear_amount={self.clear_amount!r})"


class Chapter:
    def __init__(self, stages: list[Stage]):
        self.stages = stages

    @staticmethod
    def init() -> Chapter:
        return Chapter([Stage.init() for _ in range(12)])

    @staticmethod
    def read(stream: core.Data) -> Chapter:
        total = 12
        stages: list[Stage] = []
        for _ in range(total):
            stages.append(Stage.read(stream))
        return Chapter(stages)

    def write(self, stream: core.Data):
        for stage in self.stages:
            stage.write(stream)

    def serialize(self) -> list[int]:
        return [stage.serialize() for stage in self.stages]

    @staticmethod
    def deserialize(data: list[int]) -> Chapter:
        return Chapter([Stage.deserialize(stage) for stage in data])

    def __repr__(self) -> str:
        return f"Chapter(stages={self.stages!r})"

    def __str__(self) -> str:
        return f"Chapter(stages={self.stages!r})"


class ExChapters:
    def __init__(self, chapters: list[Chapter]):
        self.chapters = chapters

    @staticmethod
    def init() -> ExChapters:
        return ExChapters([])

    @staticmethod
    def read(stream: core.Data) -> ExChapters:
        total = stream.read_int()
        chapters: list[Chapter] = []
        for _ in range(total):
            chapters.append(Chapter.read(stream))

        return ExChapters(chapters)

    def write(self, stream: core.Data):
        stream.write_int(len(self.chapters))
        for chapter in self.chapters:
            chapter.write(stream)

    def serialize(self) -> list[list[int]]:
        return [chapter.serialize() for chapter in self.chapters]

    @staticmethod
    def deserialize(data: list[list[int]]) -> ExChapters:
        return ExChapters([Chapter.deserialize(chapter) for chapter in data])

    def __repr__(self) -> str:
        return f"Chapters(chapters={self.chapters!r})"

    def __str__(self) -> str:
        return f"Chapters(chapters={self.chapters!r})"


# ============================================================
# FILE: gauntlets.py
# ============================================================
from __future__ import annotations
from typing import Any
from bcsfe import core
from bcsfe.cli import edits


class Stage:
    def __init__(self, clear_times: int):
        self.clear_times = clear_times

    @staticmethod
    def init() -> Stage:
        return Stage(0)

    @staticmethod
    def read(data: core.Data) -> Stage:
        clear_times = data.read_short()
        return Stage(clear_times)

    def write(self, data: core.Data):
        data.write_short(self.clear_times)

    def serialize(self) -> int:
        return self.clear_times

    @staticmethod
    def deserialize(data: int) -> Stage:
        return Stage(
            data,
        )

    def __repr__(self):
        return f"Stage({self.clear_times})"

    def __str__(self):
        return self.__repr__()

    def clear_stage(self, clear_amount: int = 1, ensure_cleared_only: bool = False):
        if ensure_cleared_only:
            self.clear_times = self.clear_times or clear_amount
        else:
            self.clear_times = clear_amount

    def unclear_stage(self):
        self.clear_times = 0


class Chapter:
    def __init__(self, selected_stage: int, total_stages: int = 0):
        self.selected_stage = selected_stage
        self.clear_progress = 0
        self.stages: list[Stage] = [Stage.init() for _ in range(total_stages)]
        self.chapter_unlock_state = 0
        self.total_stages = 0

    def clear_stage(
        self,
        index: int,
        clear_amount: int = 1,
        overwrite_clear_progress: bool = False,
        ensure_cleared_only: bool = False,
    ) -> bool:
        if overwrite_clear_progress:
            self.clear_progress = index + 1
        else:
            self.clear_progress = max(self.clear_progress, index + 1)
        self.stages[index].clear_stage(clear_amount, ensure_cleared_only)
        self.chapter_unlock_state = 3
        if index == self.total_stages - 1:
            return True
        return False

    def unclear_stage(self, index: int):
        self.clear_progress = min(self.clear_progress, index)
        self.stages[index].unclear_stage()
        return True

    @staticmethod
    def init(total_stages: int) -> Chapter:
        return Chapter(0, total_stages)

    @staticmethod
    def read_selected_stage(data: core.Data) -> Chapter:
        selected_stage = data.read_byte()
        return Chapter(selected_stage)

    def write_selected_stage(self, data: core.Data):
        data.write_byte(self.selected_stage)

    def read_clear_progress(self, data: core.Data):
        self.clear_progress = data.read_byte()

    def write_clear_progress(self, data: core.Data):
        data.write_byte(self.clear_progress)

    def read_stages(self, data: core.Data, total_stages: int):
        self.stages = [Stage.read(data) for _ in range(total_stages)]

    def write_stages(self, data: core.Data):
        for stage in self.stages:
            stage.write(data)

    def read_chapter_unlock_state(self, data: core.Data):
        self.chapter_unlock_state = data.read_byte()

    def write_chapter_unlock_state(self, data: core.Data):
        data.write_byte(self.chapter_unlock_state)

    def serialize(self) -> dict[str, Any]:
        return {
            "selected_stage": self.selected_stage,
            "clear_progress": self.clear_progress,
            "stages": [stage.serialize() for stage in self.stages],
            "chapter_unlock_state": self.chapter_unlock_state,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> Chapter:
        chapter = Chapter(data.get("selected_stage", 0))
        chapter.clear_progress = data.get("clear_progress", 0)
        chapter.stages = [Stage.deserialize(stage) for stage in data.get("stages", [])]
        chapter.chapter_unlock_state = data.get("chapter_unlock_state", 0)
        return chapter

    def __repr__(self):
        return f"Chapter({self.selected_stage}, {self.clear_progress}, {self.stages}, {self.chapter_unlock_state})"

    def __str__(self):
        return self.__repr__()


class ChaptersStars:
    def __init__(self, chapters: list[Chapter]):
        self.chapters = chapters

    def clear_stage(
        self,
        star: int,
        stage: int,
        clear_amount: int = 1,
        overwrite_clear_progress: bool = False,
        ensure_cleared_only: bool = False,
    ) -> bool:
        finished = self.chapters[star].clear_stage(
            stage, clear_amount, overwrite_clear_progress, ensure_cleared_only
        )
        if finished:
            if star + 1 < len(self.chapters):
                self.chapters[star + 1].chapter_unlock_state = 1
        return finished

    def unclear_stage(self, star: int, stage: int):
        finished = self.chapters[star].unclear_stage(stage)
        if finished and star + 1 < len(self.chapters):
            for chapter in self.chapters[star + 1 :]:
                chapter.chapter_unlock_state = 0
        return finished

    @staticmethod
    def init(total_stages: int, total_stars: int) -> ChaptersStars:
        chapters = [Chapter.init(total_stages) for _ in range(total_stars)]
        return ChaptersStars(chapters)

    @staticmethod
    def read_selected_stage(data: core.Data, total_stars: int) -> ChaptersStars:
        chapters = [Chapter.read_selected_stage(data) for _ in range(total_stars)]
        return ChaptersStars(chapters)

    def write_selected_stage(self, data: core.Data):
        for chapter in self.chapters:
            chapter.write_selected_stage(data)

    def read_clear_progress(self, data: core.Data):
        for chapter in self.chapters:
            chapter.read_clear_progress(data)

    def write_clear_progress(self, data: core.Data):
        for chapter in self.chapters:
            chapter.write_clear_progress(data)

    def read_stages(self, data: core.Data, total_stages: int):
        for _ in range(total_stages):
            for chapter in self.chapters:
                chapter.stages.append(Stage.read(data))

    def write_stages(self, data: core.Data):
        for i in range(len(self.chapters[0].stages)):
            for chapter in self.chapters:
                chapter.stages[i].write(data)

    def read_chapter_unlock_state(self, data: core.Data):
        for chapter in self.chapters:
            chapter.read_chapter_unlock_state(data)

    def write_chapter_unlock_state(self, data: core.Data):
        for chapter in self.chapters:
            chapter.write_chapter_unlock_state(data)

    def serialize(self) -> list[dict[str, Any]]:
        return [chapter.serialize() for chapter in self.chapters]

    @staticmethod
    def deserialize(data: list[dict[str, Any]]) -> ChaptersStars:
        chapters = [Chapter.deserialize(chapter) for chapter in data]
        return ChaptersStars(chapters)

    def __repr__(self):
        return f"ChaptersStars({self.chapters})"

    def __str__(self):
        return self.__repr__()


class GauntletChapters:
    def __init__(self, chapters: list[ChaptersStars], unknown: list[int]):
        self.chapters = chapters
        self.unknown = unknown

    def clear_stage(
        self,
        map: int,
        star: int,
        stage: int,
        clear_amount: int = 1,
        overwrite_clear_progress: bool = False,
        ensure_cleared_only: bool = False,
    ) -> bool:
        finished = self.chapters[map].clear_stage(
            star, stage, clear_amount, overwrite_clear_progress, ensure_cleared_only
        )
        if finished and map + 1 < len(self.chapters):
            self.chapters[map + 1].chapters[0].chapter_unlock_state = 1

        return finished

    def unclear_stage(self, map: int, star: int, stage: int) -> bool:
        finished = self.chapters[map].unclear_stage(star, stage)
        if finished and map + 1 < len(self.chapters) and star == 0:
            for chapter in self.chapters[map + 1].chapters:
                chapter.chapter_unlock_state = 0

        return finished

    @staticmethod
    def init() -> GauntletChapters:
        return GauntletChapters([], [])

    @staticmethod
    def read(data: core.Data) -> GauntletChapters:
        total_chapters = data.read_short()
        total_stages = data.read_byte()
        total_stars = data.read_byte()

        chapters = [
            ChaptersStars.read_selected_stage(data, total_stars)
            for _ in range(total_chapters)
        ]

        for chapter in chapters:
            chapter.read_clear_progress(data)

        for chapter in chapters:
            chapter.read_stages(data, total_stages)

        for chapter in chapters:
            chapter.read_chapter_unlock_state(data)

        unknown = [data.read_byte() for _ in range(total_chapters)]

        return GauntletChapters(chapters, unknown)

    def write(self, data: core.Data):
        data.write_short(len(self.chapters))
        try:
            data.write_byte(len(self.chapters[0].chapters[0].stages))
        except IndexError:
            data.write_byte(0)
        try:
            data.write_byte(len(self.chapters[0].chapters))
        except IndexError:
            data.write_byte(0)
        for chapter in self.chapters:
            chapter.write_selected_stage(data)

        for chapter in self.chapters:
            chapter.write_clear_progress(data)

        for chapter in self.chapters:
            chapter.write_stages(data)

        for chapter in self.chapters:
            chapter.write_chapter_unlock_state(data)

        for unknown in self.unknown:
            data.write_byte(unknown)

    def serialize(self) -> dict[str, Any]:
        return {
            "chapters": [chapter.serialize() for chapter in self.chapters],
            "unknown": self.unknown,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> GauntletChapters:
        chapters = [
            ChaptersStars.deserialize(chapter) for chapter in data.get("chapters", [])
        ]
        return GauntletChapters(chapters, data.get("unknown", []))

    def __repr__(self):
        return f"Chapters({self.chapters}, {self.unknown})"

    def __str__(self):
        return self.__repr__()

    def get_total_stars(self, map: int) -> int:
        try:
            return len(self.chapters[map].chapters)
        except IndexError:
            return 0

    def get_total_stages(self, map: int, star: int) -> int:
        try:
            return len(self.chapters[map].chapters[star].stages)
        except IndexError:
            return 0

    @staticmethod
    def edit_gauntlets(save_file: core.SaveFile):
        gauntlets = save_file.gauntlets
        gauntlets.edit_chapters(save_file, "A", 24000)

    @staticmethod
    def edit_collab_gauntlets(save_file: core.SaveFile):
        gauntlets = save_file.collab_gauntlets
        gauntlets.edit_chapters(save_file, "CA", 27000)

    @staticmethod
    def edit_behemoth_culling(save_file: core.SaveFile):
        gauntlets = save_file.behemoth_culling
        gauntlets.edit_chapters(save_file, "Q", 31000)

    @staticmethod
    def edit_enigma_stages(save_file: core.SaveFile):
        save_file.enigma_clears.edit_chapters(save_file, "H", 25000)

    def edit_chapters(
        self, save_file: core.SaveFile, letter_code: str, base_index: int
    ):
        edits.map.edit_chapters(save_file, self, letter_code, base_index=base_index)

    def unclear_rest(self, stages: list[int], stars: int, id: int):
        if not stages:
            return
        for star in range(stars, self.get_total_stars(id)):
            for stage in range(max(stages), self.get_total_stages(id, star)):
                self.chapters[id].chapters[star].stages[stage].clear_times = 0
                self.chapters[id].chapters[star].clear_progress = 0

    def set_total_stages(self, map: int, total_stages: int):
        for chapter in self.chapters[map].chapters:
            chapter.total_stages = total_stages


# ============================================================
# FILE: item_reward_stage.py
# ============================================================
from __future__ import annotations
from typing import Any
from bcsfe import core


class Stage:
    def __init__(self, claimed: bool):
        self.claimed = claimed

    @staticmethod
    def init() -> Stage:
        return Stage(False)

    @staticmethod
    def read(stream: core.Data) -> Stage:
        return Stage(stream.read_bool())

    def write(self, stream: core.Data):
        stream.write_bool(self.claimed)

    def serialize(self) -> bool:
        return self.claimed

    @staticmethod
    def deserialize(data: bool) -> Stage:
        return Stage(data)

    def __repr__(self) -> str:
        return f"Stage(claimed={self.claimed})"

    def __str__(self) -> str:
        return self.__repr__()


class SubChapter:
    def __init__(self, stages: list[Stage]):
        self.stages = stages

    @staticmethod
    def init(total_stages: int) -> SubChapter:
        stages = [Stage.init() for _ in range(total_stages)]
        return SubChapter(stages)

    @staticmethod
    def read(stream: core.Data, total_stages: int) -> SubChapter:
        stages: list[Stage] = []
        for _ in range(total_stages):
            stages.append(Stage.read(stream))
        return SubChapter(stages)

    def write(self, stream: core.Data):
        for stage in self.stages:
            stage.write(stream)

    def serialize(self) -> list[bool]:
        return [stage.serialize() for stage in self.stages]

    @staticmethod
    def deserialize(data: list[bool]) -> SubChapter:
        return SubChapter([Stage.deserialize(stage) for stage in data])

    def __repr__(self) -> str:
        return f"SubChapter(stages={self.stages})"

    def __str__(self) -> str:
        return self.__repr__()


class SubChapterStars:
    def __init__(self, sub_chapters: list[SubChapter]):
        self.sub_chapters = sub_chapters

    @staticmethod
    def init(total_stages: int, total_stars: int) -> SubChapterStars:
        sub_chapters = [
            SubChapter.init(total_stages) for _ in range(total_stars)
        ]
        return SubChapterStars(sub_chapters)

    @staticmethod
    def read(
        stream: core.Data, total_stages: int, total_stars: int
    ) -> SubChapterStars:
        sub_chapters: list[SubChapter] = []
        for _ in range(total_stars):
            sub_chapters.append(SubChapter.read(stream, total_stages))
        return SubChapterStars(sub_chapters)

    def write(self, stream: core.Data):
        for sub_chapter in self.sub_chapters:
            sub_chapter.write(stream)

    def serialize(self) -> list[list[bool]]:
        return [sub_chapter.serialize() for sub_chapter in self.sub_chapters]

    @staticmethod
    def deserialize(data: list[list[bool]]) -> SubChapterStars:
        return SubChapterStars(
            [SubChapter.deserialize(sub_chapter) for sub_chapter in data]
        )

    def __repr__(self) -> str:
        return f"SubChapterStars(sub_chapters={self.sub_chapters})"

    def __str__(self) -> str:
        return self.__repr__()


class ItemObtain:
    def __init__(self, flag: bool):
        self.flag = flag

    @staticmethod
    def init() -> ItemObtain:
        return ItemObtain(False)

    @staticmethod
    def read(stream: core.Data) -> ItemObtain:
        return ItemObtain(stream.read_bool())

    def write(self, stream: core.Data):
        stream.write_bool(self.flag)

    def serialize(self) -> bool:
        return self.flag

    @staticmethod
    def deserialize(data: bool) -> ItemObtain:
        return ItemObtain(data)

    def __repr__(self) -> str:
        return f"ItemObtain(flag={self.flag})"

    def __str__(self) -> str:
        return self.__repr__()


class ItemObtainSet:
    def __init__(self, item_obtains: dict[int, ItemObtain]):
        self.item_obtains = item_obtains

    @staticmethod
    def init() -> ItemObtainSet:
        return ItemObtainSet({})

    @staticmethod
    def read(stream: core.Data) -> ItemObtainSet:
        item_obtains: dict[int, ItemObtain] = {}
        for _ in range(stream.read_int()):
            key = stream.read_int()
            item_obtains[key] = ItemObtain.read(stream)
        return ItemObtainSet(item_obtains)

    def write(self, stream: core.Data):
        stream.write_int(len(self.item_obtains))
        for item_id, item_obtain in self.item_obtains.items():
            stream.write_int(item_id)
            item_obtain.write(stream)

    def serialize(self) -> dict[str, Any]:
        return {
            "item_obtains": {
                item_id: item_obtain.serialize()
                for item_id, item_obtain in self.item_obtains.items()
            }
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> ItemObtainSet:
        return ItemObtainSet(
            {
                int(item_id): ItemObtain.deserialize(item_obtain)
                for item_id, item_obtain in data.get("item_obtains", {}).items()
            }
        )

    def __repr__(self) -> str:
        return f"ItemObtainSet(item_obtains={self.item_obtains})"

    def __str__(self) -> str:
        return self.__repr__()


class ItemObtainSets:
    def __init__(self, item_obtain_sets: dict[int, ItemObtainSet]):
        self.item_obtain_sets = item_obtain_sets

    @staticmethod
    def init() -> ItemObtainSets:
        return ItemObtainSets({})

    @staticmethod
    def read(stream: core.Data) -> ItemObtainSets:
        item_obtain_sets: dict[int, ItemObtainSet] = {}
        for _ in range(stream.read_int()):
            key = stream.read_int()
            item_obtain_sets[key] = ItemObtainSet.read(stream)
        return ItemObtainSets(item_obtain_sets)

    def write(self, stream: core.Data):
        stream.write_int(len(self.item_obtain_sets))
        for item_id, item_obtain_set in self.item_obtain_sets.items():
            stream.write_int(item_id)
            item_obtain_set.write(stream)

    def serialize(self) -> dict[int, Any]:
        return {
            item_id: item_obtain_set.serialize()
            for item_id, item_obtain_set in self.item_obtain_sets.items()
        }

    @staticmethod
    def deserialize(data: dict[int, Any]) -> ItemObtainSets:
        return ItemObtainSets(
            {
                int(item_id): ItemObtainSet.deserialize(item_obtain_set)
                for item_id, item_obtain_set in data.items()
            }
        )

    def __repr__(self) -> str:
        return f"ItemObtainSets(item_obtain_sets={self.item_obtain_sets})"

    def __str__(self) -> str:
        return self.__repr__()


class UnobtainedItem:
    def __init__(self, unobtained: bool):
        self.unobtained = unobtained

    @staticmethod
    def init() -> UnobtainedItem:
        return UnobtainedItem(False)

    @staticmethod
    def read(stream: core.Data) -> UnobtainedItem:
        return UnobtainedItem(stream.read_bool())

    def write(self, stream: core.Data):
        stream.write_bool(self.unobtained)

    def serialize(self) -> bool:
        return self.unobtained

    @staticmethod
    def deserialize(data: bool) -> UnobtainedItem:
        return UnobtainedItem(data)

    def __repr__(self) -> str:
        return f"UnobtainedItem(unobtained={self.unobtained})"

    def __str__(self) -> str:
        return self.__repr__()


class UnobtainedItems:
    def __init__(self, unobtained_items: dict[int, UnobtainedItem]):
        self.unobtained_items = unobtained_items

    @staticmethod
    def init() -> UnobtainedItems:
        return UnobtainedItems({})

    @staticmethod
    def read(stream: core.Data) -> UnobtainedItems:
        unobtained_items: dict[int, UnobtainedItem] = {}
        for _ in range(stream.read_int()):
            key = stream.read_int()
            unobtained_items[key] = UnobtainedItem.read(stream)
        return UnobtainedItems(unobtained_items)

    def write(self, stream: core.Data):
        stream.write_int(len(self.unobtained_items))
        for item_id, unobtained_item in self.unobtained_items.items():
            stream.write_int(item_id)
            unobtained_item.write(stream)

    def serialize(self) -> dict[str, Any]:
        return {
            "unobtained_items": {
                item_id: unobtained_item.serialize()
                for item_id, unobtained_item in self.unobtained_items.items()
            }
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> UnobtainedItems:
        return UnobtainedItems(
            {
                int(item_id): UnobtainedItem.deserialize(unobtained_item)
                for item_id, unobtained_item in data.get(
                    "unobtained_items", {}
                ).items()
            }
        )

    def __repr__(self) -> str:
        return f"UnobtainedItems(unobtained_items={self.unobtained_items})"

    def __str__(self) -> str:
        return self.__repr__()


class ItemRewardChapters:
    def __init__(self, sub_chapters: list[SubChapterStars]):
        self.sub_chapters = sub_chapters
        self.item_obtains = ItemObtainSets.init()
        self.unobtained_items = UnobtainedItems.init()

    @staticmethod
    def init(gv: core.GameVersion) -> ItemRewardChapters:
        if gv < 20:
            return ItemRewardChapters([])
        if gv <= 33:
            total_subchapters = 50
            total_stages = 12
            total_stars = 3
        elif gv <= 34:
            total_subchapters = 0
            total_stages = 12
            total_stars = 3
        else:
            total_subchapters = 0
            total_stages = 0
            total_stars = 0
        return ItemRewardChapters(
            [
                SubChapterStars.init(total_stages, total_stars)
                for _ in range(total_subchapters)
            ]
        )

    @staticmethod
    def read(stream: core.Data, gv: core.GameVersion) -> ItemRewardChapters:
        if gv < 20:
            return ItemRewardChapters([])
        if gv <= 33:
            total_subchapters = 50
            total_stages = 12
            total_stars = 3
        elif gv <= 34:
            total_subchapters = stream.read_int()
            total_stages = 12
            total_stars = 3
        else:
            total_subchapters = stream.read_int()
            total_stages = stream.read_int()
            total_stars = stream.read_int()
        sub_chapters: list[SubChapterStars] = []
        for _ in range(total_subchapters):
            sub_chapters.append(
                SubChapterStars.read(stream, total_stages, total_stars)
            )
        return ItemRewardChapters(sub_chapters)

    def write(self, stream: core.Data, gv: core.GameVersion):
        if gv < 20:
            return
        if gv <= 33:
            pass
        elif gv <= 34:
            stream.write_int(len(self.sub_chapters))
        else:
            stream.write_int(len(self.sub_chapters))
            try:
                stream.write_int(
                    len(self.sub_chapters[0].sub_chapters[0].stages)
                )
            except IndexError:
                stream.write_int(0)
            try:
                stream.write_int(len(self.sub_chapters[0].sub_chapters))
            except IndexError:
                stream.write_int(0)
        for sub_chapter in self.sub_chapters:
            sub_chapter.write(stream)

    def read_item_obtains(self, stream: core.Data):
        self.item_obtains = ItemObtainSets.read(stream)
        self.unobtained_items = UnobtainedItems.read(stream)

    def write_item_obtains(self, stream: core.Data):
        self.item_obtains.write(stream)
        self.unobtained_items.write(stream)

    def serialize(self) -> dict[str, Any]:
        return {
            "sub_chapters": [
                sub_chapter.serialize() for sub_chapter in self.sub_chapters
            ],
            "item_obtains": self.item_obtains.serialize(),
            "unobtained_items": self.unobtained_items.serialize(),
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> ItemRewardChapters:
        chapters = ItemRewardChapters(
            [
                SubChapterStars.deserialize(sub_chapter)
                for sub_chapter in data.get("sub_chapters", [])
            ]
        )
        chapters.item_obtains = ItemObtainSets.deserialize(
            data.get("item_obtains", {})
        )
        chapters.unobtained_items = UnobtainedItems.deserialize(
            data.get("unobtained_items", {})
        )
        return chapters

    def __repr__(self) -> str:
        return f"Chapters(sub_chapters={self.sub_chapters}, item_obtains={self.item_obtains}, unobtained_items={self.unobtained_items})"

    def __str__(self) -> str:
        return self.__repr__()


# ============================================================
# FILE: legend_quest.py
# ============================================================
from __future__ import annotations
from typing import Any
from bcsfe import core
from bcsfe.cli import edits


class Stage:
    def __init__(self, clear_times: int):
        self.clear_times = clear_times

    @staticmethod
    def init() -> Stage:
        return Stage(0)

    @staticmethod
    def read(data: core.Data) -> Stage:
        clear_times = data.read_short()
        return Stage(clear_times)

    def write(self, data: core.Data):
        data.write_short(self.clear_times)

    def read_tries(self, data: core.Data):
        self.tries = data.read_short()

    def write_tries(self, data: core.Data):
        data.write_short(self.tries)

    def serialize(self) -> dict[str, Any]:
        return {
            "clear_times": self.clear_times,
            "tries": self.tries,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> Stage:
        stage = Stage(
            data.get("clear_times", 0),
        )
        stage.tries = data.get("tries", 0)
        return stage

    def __repr__(self):
        return f"Stage({self.clear_times}, {self.tries})"

    def __str__(self):
        return self.__repr__()

    def clear_stage(self, clear_amount: int = 1, ensure_cleared_only: bool = False):
        if ensure_cleared_only:
            self.clear_times = self.clear_times or clear_amount
            self.tries = self.tries or clear_amount
        else:
            self.clear_times = clear_amount
            self.tries = clear_amount

    def unclear_stage(self):
        self.clear_times = 0
        self.tries = 0


class Chapter:
    def __init__(self, selected_stage: int, total_stages: int = 0):
        self.selected_stage = selected_stage
        self.clear_progress = 0
        self.stages: list[Stage] = [Stage.init() for _ in range(total_stages)]
        self.chapter_unlock_state = 0

        self.total_stages = 0

    def clear_stage(
        self,
        index: int,
        clear_amount: int = 1,
        overwrite_clear_progress: bool = False,
        ensure_cleared_only: bool = False,
    ) -> bool:
        if overwrite_clear_progress:
            self.clear_progress = index + 1
        else:
            self.clear_progress = max(self.clear_progress, index + 1)
        self.stages[index].clear_stage(clear_amount, ensure_cleared_only)
        self.chapter_unlock_state = 3
        if index == self.total_stages - 1:
            return True
        return False

    def unclear_stage(self, index: int) -> bool:
        self.clear_progress = min(self.clear_progress, index)
        self.stages[index].unclear_stage()
        return True

    @staticmethod
    def init(total_stages: int) -> Chapter:
        return Chapter(0, total_stages)

    @staticmethod
    def read_selected_stage(data: core.Data) -> Chapter:
        selected_stage = data.read_byte()
        return Chapter(selected_stage)

    def write_selected_stage(self, data: core.Data):
        data.write_byte(self.selected_stage)

    def read_clear_progress(self, data: core.Data):
        self.clear_progress = data.read_byte()

    def write_clear_progress(self, data: core.Data):
        data.write_byte(self.clear_progress)

    def read_stages(self, data: core.Data, total_stages: int):
        self.stages = [Stage.read(data) for _ in range(total_stages)]
        for stage in self.stages:
            stage.read_tries(data)

    def write_stages(self, data: core.Data):
        for stage in self.stages:
            stage.write(data)

        for stage in self.stages:
            stage.write_tries(data)

    def read_chapter_unlock_state(self, data: core.Data):
        self.chapter_unlock_state = data.read_byte()

    def write_chapter_unlock_state(self, data: core.Data):
        data.write_byte(self.chapter_unlock_state)

    def serialize(self) -> dict[str, Any]:
        return {
            "selected_stage": self.selected_stage,
            "clear_progress": self.clear_progress,
            "stages": [stage.serialize() for stage in self.stages],
            "chapter_unlock_state": self.chapter_unlock_state,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> Chapter:
        chapter = Chapter(
            data.get("selected_stage", 0),
        )
        chapter.clear_progress = data.get("clear_progress", 0)
        chapter.stages = [Stage.deserialize(stage) for stage in data.get("stages", [])]
        chapter.chapter_unlock_state = data.get("chapter_unlock_state", 0)
        return chapter

    def __repr__(self):
        return f"Chapter({self.selected_stage}, {self.clear_progress}, {self.stages}, {self.chapter_unlock_state})"

    def __str__(self):
        return self.__repr__()


class ChaptersStars:
    def __init__(self, chapters: list[Chapter]):
        self.chapters = chapters

    def clear_stage(
        self,
        star: int,
        stage: int,
        clear_amount: int = 1,
        overwrite_clear_progress: bool = False,
        ensure_cleared_only: bool = False,
    ) -> bool:
        finished = self.chapters[star].clear_stage(
            stage, clear_amount, overwrite_clear_progress, ensure_cleared_only
        )
        if finished:
            if star + 1 < len(self.chapters):
                self.chapters[star + 1].chapter_unlock_state = 1
        return finished

    def unclear_stage(self, star: int, stage: int) -> bool:
        finished = self.chapters[star].unclear_stage(stage)
        if finished and star + 1 < len(self.chapters):
            for chapter in self.chapters[star + 1 :]:
                chapter.chapter_unlock_state = 0
        return finished

    @staticmethod
    def init(total_stages: int, total_stars: int) -> ChaptersStars:
        chapters = [Chapter.init(total_stages) for _ in range(total_stars)]
        return ChaptersStars(chapters)

    @staticmethod
    def read_selected_stage(data: core.Data, total_stars: int) -> ChaptersStars:
        chapters = [Chapter.read_selected_stage(data) for _ in range(total_stars)]
        return ChaptersStars(chapters)

    def write_selected_stage(self, data: core.Data):
        for chapter in self.chapters:
            chapter.write_selected_stage(data)

    def read_clear_progress(self, data: core.Data):
        for chapter in self.chapters:
            chapter.read_clear_progress(data)

    def write_clear_progress(self, data: core.Data):
        for chapter in self.chapters:
            chapter.write_clear_progress(data)

    def read_stages(self, data: core.Data, total_stages: int):
        for _ in range(total_stages):
            for chapter in self.chapters:
                chapter.stages.append(Stage.read(data))

        for i in range(total_stages):
            for chapter in self.chapters:
                chapter.stages[i].read_tries(data)

    def write_stages(self, data: core.Data):
        for i in range(len(self.chapters[0].stages)):
            for chapter in self.chapters:
                chapter.stages[i].write(data)

        for i in range(len(self.chapters[0].stages)):
            for chapter in self.chapters:
                chapter.stages[i].write_tries(data)

    def read_chapter_unlock_state(self, data: core.Data):
        for chapter in self.chapters:
            chapter.read_chapter_unlock_state(data)

    def write_chapter_unlock_state(self, data: core.Data):
        for chapter in self.chapters:
            chapter.write_chapter_unlock_state(data)

    def serialize(self) -> list[dict[str, Any]]:
        return [chapter.serialize() for chapter in self.chapters]

    @staticmethod
    def deserialize(data: list[dict[str, Any]]) -> ChaptersStars:
        chapters = [Chapter.deserialize(chapter) for chapter in data]
        return ChaptersStars(chapters)

    def __repr__(self):
        return f"ChaptersStars({self.chapters})"

    def __str__(self):
        return self.__repr__()


class LegendQuestChapters:
    def __init__(
        self, chapters: list[ChaptersStars], unknown: list[int], ids: list[int]
    ):
        self.chapters = chapters
        self.unknown = unknown
        self.ids = ids

    def clear_stage(
        self,
        map: int,
        star: int,
        stage: int,
        clear_amount: int = 1,
        overwrite_clear_progress: bool = False,
        ensure_cleared_only: bool = False,
    ) -> bool:
        finished = self.chapters[map].clear_stage(
            star, stage, clear_amount, overwrite_clear_progress, ensure_cleared_only
        )
        if finished and map + 1 < len(self.chapters):
            self.chapters[map + 1].chapters[0].chapter_unlock_state = 1

        return finished

    def unclear_stage(self, map: int, star: int, stage: int) -> bool:
        finished = self.chapters[map].unclear_stage(star, stage)
        if finished and map + 1 < len(self.chapters) and star == 0:
            for chapter in self.chapters[map + 1].chapters:
                chapter.chapter_unlock_state = 0

        return finished

    @staticmethod
    def init() -> LegendQuestChapters:
        return LegendQuestChapters([], [], [])

    @staticmethod
    def read(data: core.Data) -> LegendQuestChapters:
        total_chapters = data.read_byte()
        total_stages = data.read_byte()
        total_stars = data.read_byte()

        chapters = [
            ChaptersStars.read_selected_stage(data, total_stars)
            for _ in range(total_chapters)
        ]

        for chapter in chapters:
            chapter.read_clear_progress(data)

        for chapter in chapters:
            chapter.read_stages(data, total_stages)

        for chapter in chapters:
            chapter.read_chapter_unlock_state(data)

        unknown = [data.read_byte() for _ in range(total_chapters)]
        ids = [data.read_int() for _ in range(total_stages)]

        return LegendQuestChapters(chapters, unknown, ids)

    def write(self, data: core.Data):
        data.write_byte(len(self.chapters))
        try:
            data.write_byte(len(self.chapters[0].chapters[0].stages))
        except IndexError:
            data.write_byte(0)
        try:
            data.write_byte(len(self.chapters[0].chapters))
        except IndexError:
            data.write_byte(0)

        for chapter in self.chapters:
            chapter.write_selected_stage(data)

        for chapter in self.chapters:
            chapter.write_clear_progress(data)

        for chapter in self.chapters:
            chapter.write_stages(data)

        for chapter in self.chapters:
            chapter.write_chapter_unlock_state(data)

        for unknown in self.unknown:
            data.write_byte(unknown)

        for id in self.ids:
            data.write_int(id)

    def serialize(self) -> dict[str, Any]:
        return {
            "chapters": [chapter.serialize() for chapter in self.chapters],
            "unknown": self.unknown,
            "ids": self.ids,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> LegendQuestChapters:
        chapters = [
            ChaptersStars.deserialize(chapter) for chapter in data.get("chapters", [])
        ]
        unknown = data.get("unknown", [])
        ids = data.get("ids", [])
        return LegendQuestChapters(chapters, unknown, ids)

    def __repr__(self):
        return f"Chapters({self.chapters}, {self.unknown}, {self.ids})"

    def __str__(self):
        return self.__repr__()

    def get_total_stars(self, map: int) -> int:
        try:
            return len(self.chapters[map].chapters)
        except IndexError:
            return 0

    def get_total_stages(self, map: int, star: int) -> int:
        try:
            return len(self.chapters[map].chapters[star].stages)
        except IndexError:
            return 0

    @staticmethod
    def edit_legend_quest(save_file: core.SaveFile):
        legend_quest = save_file.legend_quest
        legend_quest.edit_chapters(save_file, "D", base_index=16000)

    def edit_chapters(
        self, save_file: core.SaveFile, letter_code: str, base_index: int
    ):
        edits.map.edit_chapters(save_file, self, letter_code, base_index=base_index)

    def unclear_rest(self, stages: list[int], stars: int, id: int):
        if not stages:
            return
        for star in range(stars, self.get_total_stars(id)):
            for stage in range(max(stages), self.get_total_stages(id, star)):
                self.chapters[id].chapters[star].stages[stage].clear_times = 0
                self.chapters[id].chapters[star].clear_progress = 0

    def set_total_stages(self, map: int, total_stages: int):
        for chapter in self.chapters[map].chapters:
            chapter.total_stages = total_stages


# ============================================================
# FILE: map_names.py
# ============================================================
from __future__ import annotations

from bcsfe import core


class MapNames:
    def __init__(
        self,
        save_file: core.SaveFile,
        code: str,
        base_index: int,
        output: bool = True,
        no_r_prefix: bool = False,
    ):
        self.save_file = save_file
        self.out = output
        self.code = code
        self.base_index = base_index
        self.no_r_prefix = no_r_prefix
        self.gdg = core.core_data.get_game_data_getter(self.save_file)
        self.map_names: dict[int, str | None] = {}
        self.stage_names: dict[int, list[str]] = {}
        self.get_map_names()

    def get_map_names_in_game(
        self, base_index: int, total_stages: int
    ) -> dict[int, str | None] | None:
        gdg = core.core_data.get_game_data_getter(self.save_file)
        map_name_data = gdg.download("resLocal", "Map_Name.csv")
        if map_name_data is None:
            return None

        csv = core.CSV(
            map_name_data, core.Delimeter.from_country_code_res(self.save_file.cc)
        )
        names: dict[int, str | None] = {}
        for row in csv:
            id = row[0].to_int()
            name = row[1].to_str().strip()

            for i in range(total_stages):
                index = i + base_index
                if id == index:
                    if name:
                        names[i] = name
                    else:
                        names[i] = None
                    break

        return names

    def get_map_names(self) -> dict[int, str | None] | None:
        gdg = core.core_data.get_game_data_getter(self.save_file)
        r_prefix = "" if self.no_r_prefix else "R"
        stage_names = gdg.download(
            "resLocal",
            f"StageName_{r_prefix}{self.code}_{core.core_data.get_lang(self.save_file)}.csv",
        )
        if stage_names is None:
            return None
        csv = core.CSV(
            stage_names,
            core.Delimeter.from_country_code_res(self.save_file.cc),
        )
        for i, row in enumerate(csv):
            stage_names_row = row.to_str_list()
            if not stage_names_row:
                continue
            self.stage_names[i] = stage_names_row

        names = self.get_map_names_in_game(self.base_index, len(self.stage_names))
        if names is None:
            return None
        self.map_names = names
        return self.map_names

    @staticmethod
    def get_code_from_id(id: int) -> str | None:
        base_id = id // 1000

        ids = {
            0: "RN",
            1: "RS",
            2: "RC",
            4: "EX",
            6: "RT",
            7: "RV",
            11: "RR",
            12: "RM",
            13: "RNA",
            14: "RB",
            16: "RD",
            20: "Z",
            21: "Z",
            22: "Z",
            24: "RA",
            25: "RH",
            27: "RCA",
            30: "DM",
            31: "RQ",
            32: "L",
            34: "RND",
        }

        return ids.get(base_id)

    @staticmethod
    def from_id(id: int, save_file: core.SaveFile) -> MapNames | None:
        code = MapNames.get_code_from_id(id)
        if code is None:
            return None
        return MapNames(save_file, code, id, no_r_prefix=True)


# ============================================================
# FILE: map_option.py
# ============================================================
from __future__ import annotations

from bcsfe import core


class MapOptionLine:
    def __init__(
        self,
        map_id: int,
        crown_count: int,
        crown_mults: list[int],
        guerrilla_set: int,
        reset_type: int,
        one_time_display: bool,
        display_order: int,
        interval: int,
        challenge_flag: bool,
        difficulty_mask: int,
        hide_after_clear: bool,
        name: str,
    ):
        self.map_id = map_id
        self.crown_count = crown_count
        self.crown_mults = crown_mults
        self.guerrilla_set = guerrilla_set
        self.reset_type = reset_type
        self.one_time_display = one_time_display
        self.display_order = display_order
        self.interval = interval
        self.challenge_flag = challenge_flag
        self.difficulty_mask = difficulty_mask
        self.hide_after_clear = hide_after_clear
        self.name = name

    @staticmethod
    def from_line(line: core.Row) -> MapOptionLine:
        return MapOptionLine(
            line.next_int(),
            line.next_int(),
            [line.next_int() for _ in range(4)],
            line.next_int(),
            line.next_int(),
            line.next_bool(),
            line.next_int(),
            line.next_int(),
            line.next_bool(),
            line.next_int(),
            line.next_bool(),
            line.next_str(),
        )


class MapOption:
    def __init__(self, maps: dict[int, MapOptionLine]):
        self.maps = maps

    @staticmethod
    def from_csv(csv: core.CSV) -> MapOption:
        data: dict[int, MapOptionLine] = {}

        for line in csv.lines[1:]:  # skip headers
            item = MapOptionLine.from_line(line)
            data[item.map_id] = item

        return MapOption(data)

    @staticmethod
    def from_save(save_file: core.SaveFile) -> MapOption | None:
        gdg = core.core_data.get_game_data_getter(save_file)
        data = gdg.download("DataLocal", "Map_option.csv")
        if data is None:
            return None

        csv = core.CSV(data)

        return MapOption.from_csv(csv)

    def get_map(self, map_id: int) -> MapOptionLine | None:
        return self.maps.get(map_id)


# ============================================================
# FILE: map_reset.py
# ============================================================
from __future__ import annotations
from bcsfe import core


class MapResetData:
    def __init__(
        self,
        yearly_end_timestamp: float,
        monthly_end_timestamp: float,
        weekly_end_timestamp: float,
        daily_end_timestamp: float,
    ):
        self.yearly_end_timestamp = yearly_end_timestamp
        self.monthly_end_timestamp = monthly_end_timestamp
        self.weekly_end_timestamp = weekly_end_timestamp
        self.daily_end_timestamp = daily_end_timestamp

    @staticmethod
    def init() -> MapResetData:
        return MapResetData(
            0.0,
            0.0,
            0.0,
            0.0,
        )

    @staticmethod
    def read(stream: core.Data) -> MapResetData:
        yearly_end_timestamp = stream.read_double()
        monthly_end_timestamp = stream.read_double()
        weekly_end_timestamp = stream.read_double()
        daily_end_timestamp = stream.read_double()
        return MapResetData(
            yearly_end_timestamp,
            monthly_end_timestamp,
            weekly_end_timestamp,
            daily_end_timestamp,
        )

    def write(self, stream: core.Data):
        stream.write_double(self.yearly_end_timestamp)
        stream.write_double(self.monthly_end_timestamp)
        stream.write_double(self.weekly_end_timestamp)
        stream.write_double(self.daily_end_timestamp)

    def serialize(self) -> dict[str, float]:
        return {
            "yearly_end_timestamp": self.yearly_end_timestamp,
            "monthly_end_timestamp": self.monthly_end_timestamp,
            "weekly_end_timestamp": self.weekly_end_timestamp,
            "daily_end_timestamp": self.daily_end_timestamp,
        }

    @staticmethod
    def deserialize(data: dict[str, float]) -> MapResetData:
        return MapResetData(
            data.get("yearly_end_timestamp", 0.0),
            data.get("monthly_end_timestamp", 0.0),
            data.get("weekly_end_timestamp", 0.0),
            data.get("daily_end_timestamp", 0.0),
        )

    def __str__(self) -> str:
        return f"MapResetData(yearly_end_timestamp={self.yearly_end_timestamp!r}, monthly_end_timestamp={self.monthly_end_timestamp!r}, weekly_end_timestamp={self.weekly_end_timestamp!r}, daily_end_timestamp={self.daily_end_timestamp!r})"

    def __repr__(self) -> str:
        return str(self)


class MapResets:
    def __init__(self, data: dict[int, list[MapResetData]]):
        self.data = data

    @staticmethod
    def init() -> MapResets:
        return MapResets({})

    @staticmethod
    def read(stream: core.Data) -> MapResets:
        data: dict[int, list[MapResetData]] = {}
        for _ in range(stream.read_int()):
            key = stream.read_int()
            value: list[MapResetData] = []
            for _ in range(stream.read_int()):
                value.append(MapResetData.read(stream))
            data[key] = value
        return MapResets(data)

    def write(self, stream: core.Data):
        stream.write_int(len(self.data))
        for key, value in self.data.items():
            stream.write_int(key)
            stream.write_int(len(value))
            for item in value:
                item.write(stream)

    def serialize(self) -> dict[int, list[dict[str, float]]]:
        return {
            key: [item.serialize() for item in value]
            for key, value in self.data.items()
        }

    @staticmethod
    def deserialize(data: dict[int, list[dict[str, float]]]) -> MapResets:
        return MapResets(
            {
                key: [MapResetData.deserialize(item) for item in value]
                for key, value in data.items()
            }
        )

    def __str__(self) -> str:
        return f"MapResets(data={self.data!r})"

    def __repr__(self) -> str:
        return str(self)


# ============================================================
# FILE: outbreaks.py
# ============================================================
from __future__ import annotations
from typing import Any
from bcsfe import core
from bcsfe.cli import dialog_creator, color


class Outbreak:
    def __init__(self, cleared: bool):
        self.cleared = cleared

    @staticmethod
    def init() -> Outbreak:
        return Outbreak(False)

    @staticmethod
    def read(stream: core.Data) -> Outbreak:
        cleared = stream.read_bool()
        return Outbreak(cleared)

    def write(self, stream: core.Data):
        stream.write_bool(self.cleared)

    def serialize(self) -> bool:
        return self.cleared

    @staticmethod
    def deserialize(data: bool) -> Outbreak:
        return Outbreak(data)

    def __repr__(self) -> str:
        return f"Outbreak(cleared={self.cleared!r})"

    def __str__(self) -> str:
        return f"Outbreak(cleared={self.cleared!r})"


class Chapter:
    def __init__(self, id: int, outbreaks: dict[int, Outbreak]):
        self.id = id
        self.outbreaks = outbreaks

    def get_true_id(self) -> int:
        if self.id < 3:
            return self.id
        return self.id - 1

    @staticmethod
    def init(id: int) -> Chapter:
        return Chapter(id, {})

    @staticmethod
    def read(stream: core.Data, id: int) -> Chapter:
        total = stream.read_int()
        outbreaks: dict[int, Outbreak] = {}
        for _ in range(total):
            outbreak_id = stream.read_int()
            outbreak = Outbreak.read(stream)
            outbreaks[outbreak_id] = outbreak

        return Chapter(id, outbreaks)

    def write(self, stream: core.Data):
        stream.write_int(len(self.outbreaks))
        for outbreak_id, outbreak in self.outbreaks.items():
            stream.write_int(outbreak_id)
            outbreak.write(stream)

    def serialize(self) -> dict[int, Any]:
        return {
            outbreak_id: outbreak.serialize()
            for outbreak_id, outbreak in self.outbreaks.items()
        }

    @staticmethod
    def deserialize(data: dict[int, Any], id: int) -> Chapter:
        return Chapter(
            id,
            {
                outbreak_id: Outbreak.deserialize(outbreak_data)
                for outbreak_id, outbreak_data in data.items()
            },
        )

    def __repr__(self) -> str:
        return f"Chapter(id={self.id!r}, outbreaks={self.outbreaks!r})"

    def __str__(self) -> str:
        return self.__repr__()


class Outbreaks:
    def __init__(self, chapters: dict[int, Chapter]):
        self.chapters = chapters
        self.zombie_event_remaining_time = 0.0
        self.current_outbreaks: dict[int, Chapter] = {}

    @staticmethod
    def init() -> Outbreaks:
        return Outbreaks({})

    @staticmethod
    def read_chapters(stream: core.Data) -> Outbreaks:
        total = stream.read_int()
        chapters: dict[int, Chapter] = {}
        for _ in range(total):
            chapter_id = stream.read_int()
            chapter = Chapter.read(stream, chapter_id)
            chapters[chapter_id] = chapter

        return Outbreaks(chapters)

    def write_chapters(self, stream: core.Data):
        stream.write_int(len(self.chapters))
        for chapter_id, chapter in self.chapters.items():
            stream.write_int(chapter_id)
            chapter.write(stream)

    def read_2(self, stream: core.Data):
        self.zombie_event_remaining_time = stream.read_double()

    def write_2(self, stream: core.Data):
        stream.write_double(self.zombie_event_remaining_time)

    def read_current_outbreaks(self, stream: core.Data, gv: core.GameVersion):
        if gv <= 43:
            total_chapters = stream.read_int()
            for _ in range(total_chapters):
                stream.read_int()
                total_stage = stream.read_int()
                for _ in range(total_stage):
                    stream.read_int()
                    stream.read_bool()

        total = stream.read_int()
        current_outbreaks: dict[int, Chapter] = {}
        for _ in range(total):
            chapter_id = stream.read_int()
            chapter = Chapter.read(stream, chapter_id)
            current_outbreaks[chapter_id] = chapter

        self.current_outbreaks = current_outbreaks

    def write_current_outbreaks(self, stream: core.Data, gv: core.GameVersion):
        if gv <= 43:
            stream.write_int(0)
        stream.write_int(len(self.current_outbreaks))
        for chapter_id, chapter in self.current_outbreaks.items():
            stream.write_int(chapter_id)
            chapter.write(stream)

    def serialize(self) -> dict[str, Any]:
        return {
            "chapters": {
                chapter_id: chapter.serialize()
                for chapter_id, chapter in self.chapters.items()
            },
            "zombie_event_remaining_time": self.zombie_event_remaining_time,
            "current_outbreaks": {
                chapter_id: chapter.serialize()
                for chapter_id, chapter in self.current_outbreaks.items()
            },
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> Outbreaks:
        outbreaks = Outbreaks(
            {
                chapter_id: Chapter.deserialize(chapter_data, chapter_id)
                for chapter_id, chapter_data in data.get("chapters", {}).items()
            }
        )
        outbreaks.zombie_event_remaining_time = data.get(
            "zombie_event_remaining_time", 0.0
        )
        outbreaks.current_outbreaks = {
            chapter_id: Chapter.deserialize(chapter_data, chapter_id)
            for chapter_id, chapter_data in data.get("current_outbreaks", {}).items()
        }

        return outbreaks

    def __repr__(self) -> str:
        return f"Outbreaks(chapters={self.chapters!r}, zombie_event_remaining_time={self.zombie_event_remaining_time!r}, current_outbreaks={self.current_outbreaks!r})"

    def __str__(self) -> str:
        return self.__repr__()

    def get_chapter_from_true_id(self, true_id: int) -> Chapter | None:
        if true_id < 3:
            return self.chapters.get(true_id)
        return self.chapters.get(true_id + 1)

    def get_current_chapter_from_true_id(self, true_id: int) -> Chapter | None:
        if true_id < 3:
            return self.current_outbreaks.get(true_id)
        return self.current_outbreaks.get(true_id + 1)

    def clear_outbreak(self, chapter_id: int, stage_id: int, clear: bool):
        chapter = self.get_chapter_from_true_id(chapter_id)
        if chapter is not None:
            stage = chapter.outbreaks.get(stage_id)
            if stage is not None:
                stage.cleared = clear
        if clear:
            chapter = self.get_current_chapter_from_true_id(chapter_id)
            if chapter is not None:
                stage = chapter.outbreaks.get(stage_id)
                if stage is not None:
                    stage.cleared = False

    @staticmethod
    def edit_outbreaks(save_file: core.SaveFile):
        outbreaks = save_file.outbreaks
        chapters = outbreaks.chapters
        if not chapters:
            color.ColoredText.localize("no_valid_outbreaks")
            return

        options = ["clear", "unclear"]
        choice = dialog_creator.ChoiceInput.from_reduced(
            options, dialog="clear_unclear_outbreaks", single_choice=True
        ).single_choice()
        if choice is None:
            return
        choice -= 1

        clear = choice == 0

        selected_ids = core.StoryChapters.select_story_chapters(
            save_file, [chapter.get_true_id() for chapter in chapters.values()]
        )
        if not selected_ids:
            return

        choice = core.StoryChapters.get_per_chapter(selected_ids)
        if choice is None:
            return
        if choice == 0:
            for chapter_id in selected_ids:
                stages = core.StoryChapters.select_stages(save_file, chapter_id)
                if not stages:
                    continue
                for stage in stages:
                    outbreaks.clear_outbreak(chapter_id, stage, clear)
        else:
            stages = core.StoryChapters.select_stages(save_file, 0)
            if not stages:
                return
            for stage in stages:
                for chapter_id in selected_ids:
                    outbreaks.clear_outbreak(chapter_id, stage, clear)

        if clear:
            color.ColoredText.localize("clear_outbreaks_success")
        else:
            color.ColoredText.localize("unclear_outbreaks_success")


# ============================================================
# FILE: story.py
# ============================================================
from __future__ import annotations
from typing import Any
from bcsfe import core
from bcsfe.cli import color, dialog_creator


class Stage:
    def __init__(self, clear_times: int):
        self.clear_times = clear_times
        self.treasure = 0
        self.itf_timed_score = 0

    @staticmethod
    def init() -> Stage:
        return Stage(0)

    @staticmethod
    def read_clear_times(stream: core.Data) -> Stage:
        return Stage(stream.read_int())

    def read_treasure(self, stream: core.Data):
        self.treasure = stream.read_int()

    def read_itf_timed_score(self, stream: core.Data):
        self.itf_timed_score = stream.read_int()

    def write_clear_times(self, stream: core.Data):
        stream.write_int(self.clear_times)

    def write_treasure(self, stream: core.Data):
        stream.write_int(self.treasure)

    def write_itf_timed_score(self, stream: core.Data):
        stream.write_int(self.itf_timed_score)

    def serialize(self) -> dict[str, Any]:
        return {
            "clear_times": self.clear_times,
            "treasure": self.treasure,
            "itf_timed_score": self.itf_timed_score,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> Stage:
        stage = Stage(data.get("clear_times", 0))
        stage.treasure = data.get("treasure", 0)
        stage.itf_timed_score = data.get("itf_timed_score", 0)
        return stage

    def __repr__(self):
        return f"Stage({self.clear_times}, {self.treasure}, {self.itf_timed_score})"

    def __str__(self):
        return self.__repr__()

    def clear_stage(self, clear_amount: int = 1):
        self.clear_times = clear_amount

    def unclear_stage(self):
        self.clear_times = 0

    def is_cleared(self) -> bool:
        return self.clear_times > 0

    def set_treasure(self, treasure: int):
        self.treasure = treasure


class Chapter:
    def __init__(self, selected_stage: int):
        self.selected_stage = selected_stage
        self.progress = 0
        self.stages = [Stage.init() for _ in range(51)]
        self.time_until_treasure_chance = 0
        self.treasure_chance_duration = 0
        self.treasure_chance_value = 0
        self.treasure_chance_stage_id = 0
        self.treasure_festival_type = 0

    def clear_stage(
        self,
        index: int,
        clear_amount: int = 1,
        overwrite_clear_progress: bool = False,
    ):
        if overwrite_clear_progress:
            self.progress = index + 1
        else:
            self.progress = max(self.progress, index + 1)
        self.stages[index].clear_stage(clear_amount)

    def set_treasure(self, stage_id: int, treasure: int):
        self.stages[stage_id].set_treasure(treasure)

    def is_stage_clear(self, stage_id: int) -> bool:
        return self.stages[stage_id].is_cleared()

    @staticmethod
    def init() -> Chapter:
        return Chapter(0)

    def get_treasure_stages(self) -> list[Stage]:
        return self.stages[:49]

    def get_valid_treasure_stages(self) -> list[Stage]:
        return self.stages[:48]

    @staticmethod
    def read_selected_stage(stream: core.Data) -> Chapter:
        return Chapter(stream.read_int())

    def read_progress(self, stream: core.Data):
        self.progress = stream.read_int()

    def read_clear_times(self, stream: core.Data):
        total_stages = 51
        self.stages = [Stage.read_clear_times(stream) for _ in range(total_stages)]

    def read_treasure(self, stream: core.Data):
        for stage in self.get_treasure_stages():
            stage.read_treasure(stream)

    def read_time_until_treasure_chance(self, stream: core.Data):
        self.time_until_treasure_chance = stream.read_int()

    def read_treasure_chance_duration(self, stream: core.Data):
        self.treasure_chance_duration = stream.read_int()

    def read_treasure_chance_value(self, stream: core.Data):
        self.treasure_chance_value = stream.read_int()

    def read_treasure_chance_stage_id(self, stream: core.Data):
        self.treasure_chance_stage_id = stream.read_int()

    def read_treasure_festival_type(self, stream: core.Data):
        self.treasure_festival_type = stream.read_int()

    def read_itf_timed_scores(self, stream: core.Data):
        for stage in self.stages:
            stage.read_itf_timed_score(stream)

    def write_selected_stage(self, stream: core.Data):
        stream.write_int(self.selected_stage)

    def write_progress(self, stream: core.Data):
        stream.write_int(self.progress)

    def write_clear_times(self, stream: core.Data):
        for stage in self.stages:
            stage.write_clear_times(stream)

    def write_treasure(self, stream: core.Data):
        for stage in self.get_treasure_stages():
            stage.write_treasure(stream)

    def write_time_until_treasure_chance(self, stream: core.Data):
        stream.write_int(self.time_until_treasure_chance)

    def write_treasure_chance_duration(self, stream: core.Data):
        stream.write_int(self.treasure_chance_duration)

    def write_treasure_chance_value(self, stream: core.Data):
        stream.write_int(self.treasure_chance_value)

    def write_treasure_chance_stage_id(self, stream: core.Data):
        stream.write_int(self.treasure_chance_stage_id)

    def write_treasure_festival_type(self, stream: core.Data):
        stream.write_int(self.treasure_festival_type)

    def write_itf_timed_scores(self, stream: core.Data):
        for stage in self.stages:
            stage.write_itf_timed_score(stream)

    def serialize(self) -> dict[str, Any]:
        return {
            "selected_stage": self.selected_stage,
            "progress": self.progress,
            "stages": [stage.serialize() for stage in self.stages],
            "time_until_treasure_chance": self.time_until_treasure_chance,
            "treasure_chance_duration": self.treasure_chance_duration,
            "treasure_chance_value": self.treasure_chance_value,
            "treasure_chance_stage_id": self.treasure_chance_stage_id,
            "treasure_festival_type": self.treasure_festival_type,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> Chapter:
        chapter = Chapter(data.get("selected_stage", 0))
        chapter.progress = data.get("progress", 0)
        chapter.stages = [Stage.deserialize(stage) for stage in data.get("stages", [])]
        chapter.time_until_treasure_chance = data.get("time_until_treasure_chance", 0)
        chapter.treasure_chance_duration = data.get("treasure_chance_duration", 0)
        chapter.treasure_chance_value = data.get("treasure_chance_value", 0)
        chapter.treasure_chance_stage_id = data.get("treasure_chance_stage_id", 0)
        chapter.treasure_festival_type = data.get("treasure_festival_type", 0)
        return chapter

    def __repr__(self):
        return f"Chapter({self.selected_stage}, {self.progress}, {self.stages}, {self.time_until_treasure_chance}, {self.treasure_chance_duration}, {self.treasure_chance_value}, {self.treasure_chance_stage_id}, {self.treasure_festival_type})"

    def __str__(self):
        return f"Chapter({self.selected_stage}, {self.progress}, {self.stages}, {self.time_until_treasure_chance}, {self.treasure_chance_duration}, {self.treasure_chance_value}, {self.treasure_chance_stage_id}, {self.treasure_festival_type})"

    def apply_progress(self, progress: int, clear_times: list[int] | None = None):
        if clear_times is None:
            clear_times = [1] * progress

        self.progress = progress
        for i in range(progress + 1, 48):
            self.stages[i].unclear_stage()

        for i in range(progress):
            self.stages[i].clear_stage(clear_times[i])

    def clear_chapter(self):
        self.apply_progress(48)


class StoryChapters:
    def __init__(self, chapters: list[Chapter]):
        self.chapters = chapters

    def get_real_chapters(self) -> list[Chapter]:
        new_chapters: list[Chapter] = []
        for i, chapter in enumerate(self.chapters):
            if i == 3:
                continue
            new_chapters.append(chapter)
        return new_chapters

    def clear_stage(
        self,
        map: int,
        stage: int,
        clear_amount: int = 1,
        overwrite_clear_progress: bool = False,
        chapters: list[Chapter] | None = None,
    ):
        if chapters is None:
            chapters = self.chapters
        chapters[map].clear_stage(stage, clear_amount, overwrite_clear_progress)

    def set_treasure(self, chapter: int, stage: int, treasure: int):
        self.chapters[chapter].set_treasure(stage, treasure)

    def is_stage_clear(self, chapter: int, stage: int) -> bool:
        return self.chapters[chapter].is_stage_clear(stage)

    @staticmethod
    def init() -> StoryChapters:
        chapters = [Chapter.init() for _ in range(10)]
        return StoryChapters(chapters)

    @staticmethod
    def read(stream: core.Data) -> StoryChapters:
        total_chapters = 10
        chapters_l = [
            Chapter.read_selected_stage(stream) for _ in range(total_chapters)
        ]
        chapters = StoryChapters(chapters_l)
        for chapter in chapters.chapters:
            chapter.read_progress(stream)
        for chapter in chapters.chapters:
            chapter.read_clear_times(stream)
        for chapter in chapters.chapters:
            chapter.read_treasure(stream)
        return chapters

    def read_treasure_festival(self, stream: core.Data):
        for chapter in self.chapters:
            chapter.read_time_until_treasure_chance(stream)
        for chapter in self.chapters:
            chapter.read_treasure_chance_duration(stream)
        for chapter in self.chapters:
            chapter.read_treasure_chance_value(stream)
        for chapter in self.chapters:
            chapter.read_treasure_chance_stage_id(stream)
        for chapter in self.chapters:
            chapter.read_treasure_festival_type(stream)

    def write(self, stream: core.Data):
        for chapter in self.chapters:
            chapter.write_selected_stage(stream)
        for chapter in self.chapters:
            chapter.write_progress(stream)
        for chapter in self.chapters:
            chapter.write_clear_times(stream)
        for chapter in self.chapters:
            chapter.write_treasure(stream)

    def write_treasure_festival(self, stream: core.Data):
        for chapter in self.chapters:
            chapter.write_time_until_treasure_chance(stream)
        for chapter in self.chapters:
            chapter.write_treasure_chance_duration(stream)
        for chapter in self.chapters:
            chapter.write_treasure_chance_value(stream)
        for chapter in self.chapters:
            chapter.write_treasure_chance_stage_id(stream)
        for chapter in self.chapters:
            chapter.write_treasure_festival_type(stream)

    def read_itf_timed_scores(self, stream: core.Data):
        # 0: eoc 1
        # 1: eoc 2
        # 2: eoc 3
        # 3: _
        # 4: itf 1
        # 5: itf 2
        # 6: itf 3
        # 7: cotc 1
        # 8: cotc 2
        # 9: cotc 3

        for i, chapter in enumerate(self.chapters):
            if i > 3 and i < 7:
                chapter.read_itf_timed_scores(stream)

    def write_itf_timed_scores(self, stream: core.Data):
        for i, chapter in enumerate(self.chapters):
            if i > 3 and i < 7:
                chapter.write_itf_timed_scores(stream)

    def serialize(self) -> list[dict[str, Any]]:
        chapters = [chapter.serialize() for chapter in self.chapters]
        return chapters

    @staticmethod
    def deserialize(data: list[dict[str, Any]]) -> StoryChapters:
        chapters = StoryChapters([Chapter.deserialize(chapter) for chapter in data])
        return chapters

    def __repr__(self):
        return f"Chapters({self.chapters})"

    def __str__(self):
        return f"Chapters({self.chapters})"

    @staticmethod
    def clear_tutorial(save_file: core.SaveFile):
        save_file.tutorial_state = max(save_file.tutorial_state, 1)
        save_file.koreaSuperiorTreasureState = max(
            save_file.koreaSuperiorTreasureState, 2
        )
        save_file.ui6 = max(save_file.ui6, 1)
        new_length = len(save_file.new_dialogs_2)
        if new_length < 6:
            save_file.new_dialogs_2.extend([0] * (6 - new_length))

        save_file.new_dialogs_2[1] = max(save_file.new_dialogs_2[1], 2)
        save_file.new_dialogs_2[5] = max(save_file.new_dialogs_2[5], 2)
        if save_file.story.chapters[0].stages[0].clear_times == 0:
            save_file.story.clear_stage(0, 0)

    @staticmethod
    def get_chapter_names(
        save_file: core.SaveFile, chapter_ids: list[int] | None = None
    ) -> list[str] | None:
        if chapter_ids is None:
            chapter_ids = [0, 1, 2, 3, 4, 5, 6, 7, 8]

        chapter_names: list[str] = []
        localizable = core.core_data.get_localizable(save_file)
        eoc_name = localizable.get("everyplay_mapname_J")
        itf_name = localizable.get("everyplay_mapname_W")
        cotc_name = localizable.get("everyplay_mapname_P")
        if eoc_name is None or itf_name is None or cotc_name is None:
            return None

        for chapter_id in chapter_ids:
            if chapter_id < 3:
                chapter_names.append(eoc_name.replace("%d", str(chapter_id + 1)))
            elif chapter_id < 6:
                chapter_names.append(itf_name.replace("%d", str(chapter_id - 2)))
            else:
                chapter_names.append(cotc_name.replace("%d", str(chapter_id - 5)))

        return chapter_names

    @staticmethod
    def select_story_chapters(
        save_file: core.SaveFile, chapters: list[int] | None = None
    ) -> list[int] | None:
        chapter_names = StoryChapters.get_chapter_names(save_file, chapters)

        if chapter_names is None:
            return None

        selected_chapters, _ = dialog_creator.ChoiceInput.from_reduced(
            chapter_names, dialog="select_story_chapters"
        ).multiple_choice(localized_options=False)

        return selected_chapters

    @staticmethod
    def get_selected_chapter_progress(max_stages: int = 48) -> int | None:
        progress = dialog_creator.IntInput(
            min=0, max=max_stages
        ).get_input_locale_while("edit_chapter_progress_all", {"max": max_stages})
        if progress is None:
            return None

        return progress

    @staticmethod
    def edit_chapter_progress(
        save_file: core.SaveFile,
        chapter_id: int,
        chapter_name: str,
        clear_amount: int,
        clear_amount_choose: int,
    ) -> bool:
        max_stages = 48
        chapter = save_file.story.get_real_chapters()[chapter_id]
        progress = dialog_creator.IntInput(
            min=0, max=max_stages
        ).get_input_locale_while(
            "edit_chapter_progress",
            {"max": max_stages, "chapter_name": chapter_name},
        )
        if progress is None:
            return False
        clear_amounts = [1] * progress
        if clear_amount_choose == 0:
            clear_amount2 = core.EventChapters.ask_clear_amount()
            if clear_amount2 is None:
                return False
            clear_amounts = [clear_amount2] * progress
        elif clear_amount_choose == 1:
            clear_amounts = [clear_amount] * progress
        elif clear_amount_choose == 2:
            for i in range(progress):
                StoryChapters.print_current_stage(save_file, chapter_id, i)
                clear_amount2 = core.EventChapters.ask_clear_amount()
                if clear_amount2 is None:
                    return False
                clear_amounts[i] = clear_amount2

        chapter.apply_progress(progress, clear_amounts)
        return progress != 0

    @staticmethod
    def convert_stage_id(index: int) -> int:
        if index == 46:
            return 46
        if index == 47:
            return 47
        index = 45 - index
        return index

    @staticmethod
    def ask_clear_count() -> int | None:
        clear_count = dialog_creator.IntInput(
            min=0,
            max=core.core_data.max_value_manager.get("stage_clear_count"),
        ).get_input_locale_while("edit_stage_clear_count", {})

        return clear_count

    @staticmethod
    def ask_if_individual_clear_counts() -> bool | None:
        options = ["individual_clear_counts", "all_clear_counts"]
        choice = dialog_creator.ChoiceInput.from_reduced(
            options, dialog="individual_clear_counts_dialog", single_choice=True
        ).single_choice()
        if choice is None:
            return None
        choice -= 1
        return choice == 0

    @staticmethod
    def edit_stage_clear_count(
        save_file: core.SaveFile, chapter_id: int, stage_id: int
    ):
        chapter = save_file.story.get_real_chapters()[chapter_id]
        stage = chapter.stages[stage_id]
        clear_count = StoryChapters.ask_clear_count()
        if clear_count is None:
            return
        stage.clear_times = clear_count

    def clear_previous_chapters(self, chapter_id: int):
        chapters = self.get_real_chapters()
        """
        0: eoc 1
        1: eoc 2 - requires eoc 1
        2: eoc 3 - requires eoc 1 + eoc 2
        3: itf 1 - requires eoc 1
        4: itf 2 - requires eoc 1 + itf 1
        5: itf 3 - requires eoc 1 + itf 1 + itf 2
        6: cotc 1 - requires eoc 1 + itf 1
        7: cotc 2 - requires eoc 1 + itf 1 + cotc 1
        8: cotc 3 - requires eoc 1 + itf 1 + cotc 1 + cotc 2

        """
        if chapter_id == 1:  # eoc 2
            chapters[0].clear_chapter()
        elif chapter_id == 2:  # eoc 3
            chapters[0].clear_chapter()
            chapters[1].clear_chapter()
        elif chapter_id == 3:  # itf 1
            chapters[0].clear_chapter()
        elif chapter_id == 4:  # itf 2
            chapters[0].clear_chapter()
            chapters[3].clear_chapter()
        elif chapter_id == 5:  # itf 3
            chapters[0].clear_chapter()
            chapters[3].clear_chapter()
            chapters[4].clear_chapter()
        elif chapter_id == 6:  # cotc 1
            chapters[0].clear_chapter()
            chapters[3].clear_chapter()
        elif chapter_id == 7:  # cotc 2
            chapters[0].clear_chapter()
            chapters[3].clear_chapter()
            chapters[6].clear_chapter()
        elif chapter_id == 8:  # cotc 3
            chapters[0].clear_chapter()
            chapters[3].clear_chapter()
            chapters[6].clear_chapter()
            chapters[7].clear_chapter()

    @staticmethod
    def print_current_chapter(save_file: core.SaveFile, chapter_id: int):
        chapter_names = StoryChapters.get_chapter_names(save_file)
        if chapter_names is None:
            return
        chapter_name = chapter_names[chapter_id]
        color.ColoredText.localize("current_chapter", chapter_name=chapter_name)

    @staticmethod
    def print_current_treasure_group(
        save_file: core.SaveFile, chapter_id: int, treasure_group_id: int
    ):
        chapter_type = StoryChapters.get_chapter_type_from_index(chapter_id)

        treasure_group_names = TreasureGroupNames(
            save_file, chapter_type
        ).treasure_group_names
        if treasure_group_names is None:
            return
        treasure_group_name = treasure_group_names[treasure_group_id]
        color.ColoredText.localize(
            "current_treasure_group", treasure_group_name=treasure_group_name
        )

    @staticmethod
    def clear_story(save_file: core.SaveFile):
        story = save_file.story
        story.edit_chapters(
            save_file,
        )

    def edit_chapters(self, save_file: core.SaveFile):
        chapters = self.get_real_chapters()
        names = StoryChapters.get_chapter_names(save_file)
        if names is None:
            return

        map_choices = StoryChapters.select_story_chapters(save_file)
        if not map_choices:
            return

        clear_type_choice = dialog_creator.ChoiceInput.from_reduced(
            ["clear_whole_chapters", "clear_specific_stages"],
            dialog="select_clear_type",
            single_choice=True,
        ).single_choice()
        if clear_type_choice is None:
            return
        clear_type_choice -= 1

        modify_clear_amounts = dialog_creator.YesNoInput().get_input_once(
            "modify_clear_amounts"
        )
        if modify_clear_amounts is None:
            return
        clear_amount = 1
        clear_amount_type = -1
        if modify_clear_amounts:
            if len(map_choices) == 1:
                clear_amount_type = 0
            else:
                options = ["clear_amount_chapter", "clear_amount_all"]
                if clear_type_choice == 1:
                    options.append("clear_amount_stages")
                clear_amount_type = dialog_creator.ChoiceInput.from_reduced(
                    options, dialog="select_clear_amount_type", single_choice=True
                ).single_choice()
                if clear_amount_type is None:
                    return
                clear_amount_type -= 1

            if clear_amount_type == 1:
                clear_amount = core.EventChapters.ask_clear_amount()
                if clear_amount is None:
                    return

        for id in map_choices:
            stage_names = StageNames(
                save_file, chapter=str(self.get_chapter_type_from_index(id))
            )
            stage_names = stage_names.stage_names
            if stage_names is None:
                return

            new_stage_names: list[str] = []
            for i in range(48):
                index_stage_id = StoryChapters.convert_stage_id(i)
                new_stage_names.append(stage_names[index_stage_id])
            stage_names = new_stage_names
            map_name = names[id]
            color.ColoredText.localize("current_sol_chapter", name=map_name, id=id)
            if clear_type_choice:
                stages = core.EventChapters.ask_stages_stage_names(stage_names)
                if stages is None:
                    return
            else:
                stages = list(range(48))

            if clear_amount_type == 0:
                clear_amount = core.EventChapters.ask_clear_amount()
                if clear_amount is None:
                    return

            could_unclear_stages = False

            if chapters[id].progress > max(stages) + 1:
                could_unclear_stages = True

            for stage in range(max(stages) + 1, 48):
                if chapters[id].stages[stage].clear_times:
                    could_unclear_stages = True

            if could_unclear_stages:
                unclear_other_stages = dialog_creator.YesNoInput().get_input_once(
                    "unclear_other_stages"
                )
                if unclear_other_stages is None:
                    return
            else:
                unclear_other_stages = False

            if unclear_other_stages:
                chapters[id].progress = 0
                for stage in range(max(stages), 48):
                    chapters[id].stages[stage].clear_times = 0

            for stage in stages:
                if clear_amount_type == 2:
                    stage_name = stage_names[stage]
                    color.ColoredText.localize(
                        "current_sol_stage", name=stage_name, id=stage
                    )
                if clear_amount_type == 2:
                    clear_amount = core.EventChapters.ask_clear_amount()
                    if clear_amount is None:
                        return
                self.clear_stage(
                    id,
                    stage,
                    overwrite_clear_progress=True,
                    clear_amount=clear_amount,
                    chapters=chapters,
                )

        color.ColoredText.localize("map_chapters_edited")

    @staticmethod
    def ask_treasure_level(save_file: core.SaveFile) -> int | None:
        treasure_text = core.core_data.get_treasure_text(save_file).treasure_text
        if treasure_text is None:
            return None
        if len(treasure_text) < 3:
            return None
        options = [
            "no_treasure",
            treasure_text[0],
            treasure_text[1],
            treasure_text[2],
            "custom_treasure_level",
        ]
        choice = dialog_creator.ChoiceInput.from_reduced(
            options, dialog="treasure_level_dialog", single_choice=True
        ).single_choice()
        if choice is None:
            return None
        choice -= 1

        max_treasure_level = core.core_data.max_value_manager.get("treasure_level")

        if choice == 4:
            treasure_level = dialog_creator.IntInput(
                min=0, max=max_treasure_level
            ).get_input_locale_while("custom_treasure_level_dialog", {})
            if treasure_level is None:
                return None
            return treasure_level

        return choice

    @staticmethod
    def get_per_chapter(chapters: list[int]) -> int | None:
        if len(chapters) == 1:
            return 0

        options = ["per_chapter", "all_selected_chapters"]
        choice = dialog_creator.ChoiceInput.from_reduced(
            options, dialog="edit_per_chapter", single_choice=True
        ).single_choice()
        if choice is None:
            return None
        choice -= 1
        return choice

    @staticmethod
    def edit_treasures_whole_chapters(save_file: core.SaveFile, chapters: list[int]):
        choice = StoryChapters.get_per_chapter(chapters)
        if choice is None:
            return

        if choice == 0:
            for chapter_id in chapters:
                StoryChapters.print_current_chapter(save_file, chapter_id)
                chapter = save_file.story.get_real_chapters()[chapter_id]
                treasure_level = StoryChapters.ask_treasure_level(save_file)
                if treasure_level is None:
                    return
                for stage in chapter.get_valid_treasure_stages():
                    stage.set_treasure(treasure_level)
        else:
            treasure_level = StoryChapters.ask_treasure_level(save_file)
            if treasure_level is None:
                return
            for chapter_id in chapters:
                chapter = save_file.story.get_real_chapters()[chapter_id]
                for stage in chapter.get_valid_treasure_stages():
                    stage.set_treasure(treasure_level)

    @staticmethod
    def get_chapter_type_from_index(index: int) -> int:
        if index < 3:
            return 0
        if index < 6:
            return 1
        return 2

    @staticmethod
    def select_stages(save_file: core.SaveFile, chapter_id: int) -> list[int] | None:
        options = ["select_stage_by_id", "select_stage_by_name"]
        choice = dialog_creator.ChoiceInput.from_reduced(
            options, dialog="select_stage_dialog", single_choice=True
        ).single_choice()
        if choice is None:
            return None
        choice -= 1

        if choice == 0:
            stage_ids = dialog_creator.RangeInput(48, 1).get_input_locale(
                "select_stage_id", {}
            )
            if stage_ids is None:
                return None
            stage_ids = [stage_id - 1 for stage_id in stage_ids]
            return stage_ids

        chapter_type = StoryChapters.get_chapter_type_from_index(chapter_id)
        stage_names = StageNames(save_file, str(chapter_type)).stage_names
        if not stage_names:
            return None
        new_stage_names: list[str] = []
        for i in range(48):
            index_stage_id = StoryChapters.convert_stage_id(i)
            new_stage_names.append(stage_names[index_stage_id])
        selected_stages, _ = dialog_creator.ChoiceInput.from_reduced(
            new_stage_names, dialog="select_stages_name"
        ).multiple_choice(localized_options=False)

        if not selected_stages:
            return None

        return selected_stages

    @staticmethod
    def edit_treasures_individual_stages(save_file: core.SaveFile, chapters: list[int]):
        choice = StoryChapters.get_per_chapter(chapters)
        if choice is None:
            return
        if choice == 0:
            for chapter_id in chapters:
                StoryChapters.print_current_chapter(save_file, chapter_id)
                chapter = save_file.story.get_real_chapters()[chapter_id]
                stage_ids = StoryChapters.select_stages(save_file, chapter_id)
                if stage_ids is None:
                    return
                treasure_level = StoryChapters.ask_treasure_level(save_file)
                if treasure_level is None:
                    return
                for stage_id in stage_ids:
                    real_stage_id = StoryChapters.convert_stage_id(stage_id)
                    chapter.set_treasure(real_stage_id, treasure_level)
        else:
            stage_ids = StoryChapters.select_stages(save_file, 0)
            if stage_ids is None:
                return
            treasure_level = StoryChapters.ask_treasure_level(save_file)
            if treasure_level is None:
                return
            for chapter_id in chapters:
                chapter = save_file.story.get_real_chapters()[chapter_id]
                for stage_id in stage_ids:
                    real_stage_id = StoryChapters.convert_stage_id(stage_id)
                    chapter.set_treasure(real_stage_id, treasure_level)

    @staticmethod
    def edit_treasures_groups(save_file: core.SaveFile, chapters: list[int]):
        for chapter_id in chapters:
            StoryChapters.print_current_chapter(save_file, chapter_id)
            chapter = save_file.story.get_real_chapters()[chapter_id]
            chapter_type = StoryChapters.get_chapter_type_from_index(chapter_id)
            treasure_group_data = TreasureGroupData(
                save_file, chapter_type
            ).treasure_group_data
            treasure_group_names = TreasureGroupNames(
                save_file, chapter_type
            ).treasure_group_names
            if not treasure_group_data or not treasure_group_names:
                return
            treasure_group_names_new: list[str] = []
            for i in range(len(treasure_group_data)):
                treasure_group_names_new.append(treasure_group_names[i])

            selected_treasure_groups, _ = dialog_creator.ChoiceInput.from_reduced(
                treasure_group_names_new, dialog="select_treasure_groups"
            ).multiple_choice(localized_options=False)

            if not selected_treasure_groups:
                return

            options = ["group_individual", "group_all_at_once"]
            choice = dialog_creator.ChoiceInput.from_reduced(
                options, dialog="select_treasure_groups_individual"
            ).single_choice()
            if choice is None:
                return
            choice -= 1

            if choice == 0:
                for treasure_group_id in selected_treasure_groups:
                    StoryChapters.print_current_treasure_group(
                        save_file, chapter_id, treasure_group_id
                    )
                    treasure_level = StoryChapters.ask_treasure_level(save_file)
                    if treasure_level is None:
                        return
                    treasure_group = treasure_group_data[treasure_group_id]
                    for stage_id in treasure_group:
                        chapter.set_treasure(stage_id, treasure_level)

            else:
                treasure_level = StoryChapters.ask_treasure_level(save_file)
                if treasure_level is None:
                    return

                for treasure_group_id in selected_treasure_groups:
                    treasure_group = treasure_group_data[treasure_group_id]
                    for stage_id in treasure_group:
                        chapter.set_treasure(stage_id, treasure_level)

    @staticmethod
    def edit_treasures(save_file: core.SaveFile):
        selected_chapters = StoryChapters.select_story_chapters(save_file)
        if not selected_chapters:
            return
        options = ["whole_chapters", "individual_stages", "treasure_groups"]
        choice = dialog_creator.ChoiceInput.from_reduced(
            options, dialog="treasure_dialog", single_choice=True
        ).single_choice()
        if choice is None:
            return
        choice -= 1

        if choice == 0:
            StoryChapters.edit_treasures_whole_chapters(save_file, selected_chapters)
        elif choice == 1:
            StoryChapters.edit_treasures_individual_stages(save_file, selected_chapters)
        elif choice == 2:
            StoryChapters.edit_treasures_groups(save_file, selected_chapters)

        color.ColoredText.localize("treasures_edited")

    @staticmethod
    def edit_itf_timed_scores(save_file: core.SaveFile):
        selected_chapters = StoryChapters.select_story_chapters(
            save_file, chapters=[3, 4, 5]
        )
        if not selected_chapters:
            return
        options = ["whole_chapters", "individual_stages"]
        choice = dialog_creator.ChoiceInput.from_reduced(
            options, dialog="itf_timed_scores_dialog", single_choice=True
        ).single_choice()
        if choice is None:
            return
        choice -= 1

        selected_chapters = [chapter_id + 3 for chapter_id in selected_chapters]

        if choice == 0:
            StoryChapters.edit_itf_timed_scores_whole_chapters(
                save_file, selected_chapters
            )
        elif choice == 1:
            StoryChapters.edit_itf_timed_scores_individual_stages(
                save_file, selected_chapters
            )

        color.ColoredText.localize("itf_timed_scores_edited")

    @staticmethod
    def edit_itf_timed_scores_whole_chapters(
        save_file: core.SaveFile, chapters: list[int]
    ):
        choice = StoryChapters.get_per_chapter(chapters)
        if choice is None:
            return

        if choice == 0:
            for chapter_id in chapters:
                print(chapter_id)
                StoryChapters.print_current_chapter(save_file, chapter_id)
                chapter = save_file.story.get_real_chapters()[chapter_id]
                score = dialog_creator.IntInput(
                    min=0,
                    max=core.core_data.max_value_manager.get("itf_timed_score"),
                ).get_input_locale_while("itf_timed_score_dialog", {})
                if score is None:
                    return
                for stage in chapter.get_valid_treasure_stages():
                    stage.itf_timed_score = score
        else:
            score = dialog_creator.IntInput(
                min=0,
                max=core.core_data.max_value_manager.get("itf_timed_score"),
            ).get_input_locale_while("itf_timed_score_dialog", {})
            if score is None:
                return
            for chapter_id in chapters:
                chapter = save_file.story.get_real_chapters()[chapter_id]
                for stage in chapter.get_valid_treasure_stages():
                    stage.itf_timed_score = score

    @staticmethod
    def print_current_stage(save_file: core.SaveFile, chapter_id: int, stage_id: int):
        chapter_names = StoryChapters.get_chapter_names(save_file)
        if chapter_names is None:
            return
        chapter_name = chapter_names[chapter_id]
        chapter_type = StoryChapters.get_chapter_type_from_index(chapter_id)
        stage_names = StageNames(save_file, str(chapter_type)).stage_names
        if stage_names is None:
            return
        stage_id = StoryChapters.convert_stage_id(stage_id)
        stage_name = stage_names[stage_id]
        color.ColoredText.localize(
            "current_stage", chapter_name=chapter_name, stage_name=stage_name
        )

    @staticmethod
    def edit_itf_timed_scores_individual_stages(
        save_file: core.SaveFile, chapters: list[int]
    ):
        choice = StoryChapters.get_per_chapter(chapters)
        if choice is None:
            return
        options = ["individual_stages", "all_selected_stages"]
        choice2 = dialog_creator.ChoiceInput.from_reduced(
            options,
            dialog="itf_timed_scores_individual_dialog",
            single_choice=True,
        ).single_choice()
        if choice2 is None:
            return
        choice2 -= 1

        if choice == 0:
            for chapter_id in chapters:
                StoryChapters.print_current_chapter(save_file, chapter_id)
                chapter = save_file.story.get_real_chapters()[chapter_id]
                stage_ids = StoryChapters.select_stages(save_file, chapter_id)
                if stage_ids is None:
                    return
                if choice2 == 0:
                    for stage_id in stage_ids:
                        StoryChapters.print_current_stage(
                            save_file, chapter_id, stage_id
                        )

                        score = dialog_creator.IntInput(
                            min=0,
                            max=core.core_data.max_value_manager.get("itf_timed_score"),
                        ).get_input_locale_while("itf_timed_score_dialog", {})
                        if score is None:
                            return
                        chapter.stages[stage_id].itf_timed_score = score
                elif choice2 == 1:
                    score = dialog_creator.IntInput(
                        min=0,
                        max=core.core_data.max_value_manager.get("itf_timed_score"),
                    ).get_input_locale_while("itf_timed_score_dialog", {})
                    if score is None:
                        return
                    for stage_id in stage_ids:
                        chapter.stages[stage_id].itf_timed_score = score
        else:
            stage_ids = StoryChapters.select_stages(save_file, 3)
            if stage_ids is None:
                return
            if choice2 == 0:
                for stage_id in stage_ids:
                    StoryChapters.print_current_stage(save_file, 3, stage_id)
                    score = dialog_creator.IntInput(
                        min=0,
                        max=core.core_data.max_value_manager.get("itf_timed_score"),
                    ).get_input_locale_while("itf_timed_score_dialog", {})
                    if score is None:
                        return
                    for chapter_id in chapters:
                        chapter = save_file.story.get_real_chapters()[chapter_id]
                        chapter.stages[stage_id].itf_timed_score = score
            elif choice2 == 1:
                score = dialog_creator.IntInput(
                    min=0,
                    max=core.core_data.max_value_manager.get("itf_timed_score"),
                ).get_input_locale_while("itf_timed_score_dialog", {})
                if score is None:
                    return
                for chapter_id in chapters:
                    chapter = save_file.story.get_real_chapters()[chapter_id]
                    for stage_id in stage_ids:
                        chapter.stages[stage_id].itf_timed_score = score


class StageNames:
    def __init__(self, save_file: core.SaveFile, chapter: str, max_stages: int = 48):
        self.save_file = save_file
        self.chapter = chapter
        self.max_stages = max_stages
        self.stage_names = self.get_stage_names()

    def get_file_name(self) -> str:
        if self.chapter.isdigit():
            return (
                f"StageName{self.chapter}_{core.core_data.get_lang(self.save_file)}.csv"
            )
        return f"StageName_{self.chapter}_{core.core_data.get_lang(self.save_file)}.csv"

    def get_stage_names(self) -> list[str] | None:
        file_name = self.get_file_name()
        gdg = core.core_data.get_game_data_getter(self.save_file)
        file = gdg.download("resLocal", file_name)
        if file is None:
            return None
        csv = core.CSV(
            file,
            delimiter=core.Delimeter.from_country_code_res(self.save_file.cc),
        )
        stage_names: list[str] = []
        if self.chapter.isdigit():
            for row in csv:
                stage_names.append(row[0].to_str())
        else:
            for row in csv:
                for value in row:
                    stage_names.append(value.to_str())
        return stage_names[: self.max_stages]

    def get_stage_name(self, stage_id: int) -> str | None:
        if self.stage_names is None:
            return None
        return self.stage_names[stage_id]


class TreasureText:
    def __init__(self, save_file: core.SaveFile):
        self.save_file = save_file
        self.treasure_text = self.get_treasure_text()

    def get_tt_file_name(self) -> str:
        return f"Treasure2_{core.core_data.get_lang(self.save_file)}.csv"

    def get_treasure_text(self) -> list[str] | None:
        file_name = self.get_tt_file_name()
        gdg = core.core_data.get_game_data_getter(self.save_file)
        file = gdg.download("resLocal", file_name)
        if file is None:
            return None
        csv = core.CSV(
            file,
            delimiter=core.Delimeter.from_country_code_res(self.save_file.cc),
        )
        treasure_text: list[str] = []
        for row in csv:
            treasure_text.append(row[0].to_str())
        return treasure_text


class TreasureGroupData:
    def __init__(self, save_file: core.SaveFile, chapter_type: int):
        self.save_file = save_file
        self.chapter_type = chapter_type
        self.treasure_group_data = self.get_treasure_group_data()

    def get_tgd_file_name(self) -> str:
        if self.chapter_type == 0:
            return "treasureData0.csv"
        if self.chapter_type == 1:
            return "treasureData1.csv"
        if self.chapter_type == 2:
            return "treasureData2_0.csv"
        return ""

    def get_treasure_group_data(self) -> list[list[int]] | None:
        gdg = core.core_data.get_game_data_getter(self.save_file)
        file = gdg.download("DataLocal", self.get_tgd_file_name())
        if file is None:
            return None
        csv = core.CSV(file)
        treasure_group_data: list[list[int]] = []
        for row in csv.lines[11:22]:
            treasure_group_data.append(
                [value.to_int() for value in row if value.to_int() != -1]
            )

        return treasure_group_data


class TreasureGroupNames:
    def __init__(self, save_file: core.SaveFile, chapter_type: int):
        self.save_file = save_file
        self.chapter_type = chapter_type
        self.treasure_group_names = self.get_treasure_group_names()

    def get_tgn_file_name(self) -> str:
        lang = core.core_data.get_lang(self.save_file)
        if self.chapter_type == 0:
            return f"Treasure3_0_{lang}.csv"
        if self.chapter_type == 1:
            return f"Treasure3_1_{lang}.csv"
        if self.chapter_type == 2:
            return f"Treasure3_2_0_{lang}.csv"
        return ""

    def get_treasure_group_names(self) -> list[str] | None:
        gdg = core.core_data.get_game_data_getter(self.save_file)
        file = gdg.download("resLocal", self.get_tgn_file_name())
        if file is None:
            return None
        csv = core.CSV(
            file,
            delimiter=core.Delimeter.from_country_code_res(self.save_file.cc),
        )
        treasure_group_names: list[str] = []
        for row in csv:
            treasure_group_names.append(row[0].to_str())
        return treasure_group_names


# ============================================================
# FILE: timed_score.py
# ============================================================
from __future__ import annotations
from bcsfe import core


class Stage:
    def __init__(self, score: int):
        self.score = score

    @staticmethod
    def init() -> Stage:
        return Stage(0)

    @staticmethod
    def read(stream: core.Data) -> Stage:
        return Stage(stream.read_int())

    def write(self, stream: core.Data):
        stream.write_int(self.score)

    def serialize(self) -> int:
        return self.score

    @staticmethod
    def deserialize(data: int) -> Stage:
        return Stage(data)

    def __repr__(self) -> str:
        return f"Stage(score={self.score})"

    def __str__(self) -> str:
        return self.__repr__()


class SubChapter:
    def __init__(self, stages: list[Stage]):
        self.stages = stages

    @staticmethod
    def init(total_stages: int) -> SubChapter:
        return SubChapter([Stage.init() for _ in range(total_stages)])

    @staticmethod
    def read(stream: core.Data, total_stages: int) -> SubChapter:
        stages: list[Stage] = []
        for _ in range(total_stages):
            stages.append(Stage.read(stream))
        return SubChapter(stages)

    def write(self, stream: core.Data):
        for stage in self.stages:
            stage.write(stream)

    def serialize(self) -> list[int]:
        return [stage.serialize() for stage in self.stages]

    @staticmethod
    def deserialize(data: list[int]) -> SubChapter:
        return SubChapter([Stage.deserialize(stage) for stage in data])

    def __repr__(self) -> str:
        return f"SubChapter(stages={self.stages})"

    def __str__(self) -> str:
        return self.__repr__()


class SubChapterStars:
    def __init__(self, sub_chapters: list[SubChapter]):
        self.sub_chapters = sub_chapters

    @staticmethod
    def init(total_stages: int, total_stars: int) -> SubChapterStars:
        return SubChapterStars(
            [SubChapter.init(total_stages) for _ in range(total_stars)]
        )

    @staticmethod
    def read(
        stream: core.Data,
        total_stages: int,
        total_stars: int,
    ) -> SubChapterStars:
        sub_chapters: list[SubChapter] = []
        for _ in range(total_stars):
            sub_chapters.append(SubChapter.read(stream, total_stages))
        return SubChapterStars(sub_chapters)

    def write(self, stream: core.Data):
        for sub_chapter in self.sub_chapters:
            sub_chapter.write(stream)

    def serialize(self) -> list[list[int]]:
        return [sub_chapter.serialize() for sub_chapter in self.sub_chapters]

    @staticmethod
    def deserialize(data: list[list[int]]) -> SubChapterStars:
        return SubChapterStars(
            [SubChapter.deserialize(sub_chapter) for sub_chapter in data]
        )

    def __repr__(self) -> str:
        return f"SubChapterStars(sub_chapters={self.sub_chapters})"

    def __str__(self) -> str:
        return self.__repr__()


class TimedScoreChapters:
    def __init__(self, sub_chapters: list[SubChapterStars]):
        self.sub_chapters = sub_chapters

    @staticmethod
    def init(gv: core.GameVersion) -> TimedScoreChapters:
        if gv < 20:
            return TimedScoreChapters([])
        if gv <= 33:
            total_subchapters = 50
            total_stages = 12
            total_stars = 3
        elif gv <= 34:
            total_subchapters = 0
            total_stages = 12
            total_stars = 3
        else:
            total_subchapters = 0
            total_stages = 0
            total_stars = 0
        return TimedScoreChapters(
            [
                SubChapterStars.init(total_stages, total_stars)
                for _ in range(total_subchapters)
            ]
        )

    @staticmethod
    def read(stream: core.Data, gv: core.GameVersion) -> TimedScoreChapters:
        if gv < 20:
            return TimedScoreChapters([])
        if gv <= 33:
            total_subchapters = 50
            total_stages = 12
            total_stars = 3
        elif gv <= 34:
            total_subchapters = stream.read_int()
            total_stages = 12
            total_stars = 3
        else:
            total_subchapters = stream.read_int()
            total_stages = stream.read_int()
            total_stars = stream.read_int()
        sub_chapters: list[SubChapterStars] = []
        for _ in range(total_subchapters):
            sub_chapters.append(
                SubChapterStars.read(stream, total_stages, total_stars)
            )
        return TimedScoreChapters(sub_chapters)

    def write(self, stream: core.Data, gv: core.GameVersion):
        if gv < 20:
            return
        if gv <= 33:
            pass
        elif gv <= 34:
            stream.write_int(len(self.sub_chapters))
        else:
            stream.write_int(len(self.sub_chapters))
            try:
                stream.write_int(
                    len(self.sub_chapters[0].sub_chapters[0].stages)
                )
            except IndexError:
                stream.write_int(0)
            try:
                stream.write_int(len(self.sub_chapters[0].sub_chapters))
            except IndexError:
                stream.write_int(0)
        for sub_chapter in self.sub_chapters:
            sub_chapter.write(stream)

    def serialize(self) -> list[list[list[int]]]:
        return [sub_chapter.serialize() for sub_chapter in self.sub_chapters]

    @staticmethod
    def deserialize(data: list[list[list[int]]]) -> TimedScoreChapters:
        return TimedScoreChapters(
            [SubChapterStars.deserialize(sub_chapter) for sub_chapter in data]
        )

    def __repr__(self) -> str:
        return f"Chapters(sub_chapters={self.sub_chapters})"

    def __str__(self) -> str:
        return self.__repr__()


# ============================================================
# FILE: tower.py
# ============================================================
from __future__ import annotations
from typing import Any
from bcsfe import core


class TowerChapters:
    def __init__(self, chapters: core.Chapters):
        self.chapters = chapters
        self.item_obtain_states: list[list[bool]] = []

    @staticmethod
    def init() -> TowerChapters:
        return TowerChapters(core.Chapters.init())

    @staticmethod
    def read(data: core.Data) -> TowerChapters:
        ch = core.Chapters.read(data)
        return TowerChapters(ch)

    def write(self, data: core.Data):
        self.chapters.write(data)

    def read_item_obtain_states(self, data: core.Data):
        total_stars = data.read_int()
        total_stages = data.read_int()
        self.item_obtain_states: list[list[bool]] = []
        for _ in range(total_stars):
            self.item_obtain_states.append(data.read_bool_list(total_stages))

    def write_item_obtain_states(self, data: core.Data):
        data.write_int(len(self.item_obtain_states))
        try:
            data.write_int(len(self.item_obtain_states[0]))
        except IndexError:
            data.write_int(0)
        for item_obtain_state in self.item_obtain_states:
            data.write_bool_list(item_obtain_state, write_length=False)

    def serialize(self) -> dict[str, Any]:
        return {
            "chapters": self.chapters.serialize(),
            "item_obtain_states": self.item_obtain_states,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> TowerChapters:
        tower = TowerChapters(
            core.Chapters.deserialize(data.get("chapters", {})),
        )
        tower.item_obtain_states = data.get("item_obtain_states", [])
        return tower

    def __repr__(self):
        return f"Tower({self.chapters}, {self.item_obtain_states})"

    def __str__(self):
        return self.__repr__()

    def get_total_stars(self, chapter_id: int) -> int:
        return len(self.chapters.chapters[chapter_id].chapters)

    def get_total_stages(self, chapter_id: int, star: int) -> int:
        return len(self.chapters.chapters[chapter_id].chapters[star].stages)

    @staticmethod
    def edit_towers(save_file: core.SaveFile):
        towers = save_file.tower
        towers.chapters.edit_chapters(save_file, "V", 7000)


# ============================================================
# FILE: uncanny.py
# ============================================================
from __future__ import annotations
from typing import Any
from bcsfe import core
from bcsfe.cli import color, dialog_creator


class UncannyChapters:
    def __init__(self, chapters: core.Chapters, unknown: list[int]):
        self.chapters = chapters
        self.unknown = unknown

    @staticmethod
    def init() -> UncannyChapters:
        return UncannyChapters(core.Chapters.init(), [])

    @staticmethod
    def read(data: core.Data) -> UncannyChapters:
        ch = core.Chapters.read(data, read_every_time=False)
        unknown = data.read_int_list(length=len(ch.chapters))
        return UncannyChapters(ch, unknown)

    def write(self, data: core.Data):
        self.chapters.write(data, write_every_time=False)
        data.write_int_list(self.unknown, write_length=False)

    def serialize(self) -> dict[str, Any]:
        return {
            "chapters": self.chapters.serialize(),
            "unknown": self.unknown,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> UncannyChapters:
        return UncannyChapters(
            core.Chapters.deserialize(data.get("chapters", {})),
            data.get("unknown", []),
        )

    def __repr__(self):
        return f"Uncanny({self.chapters}, {self.unknown})"

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def edit_uncanny(save_file: core.SaveFile):
        uncanny = save_file.uncanny
        uncanny.chapters.edit_chapters(save_file, "NA", 13000)

    @staticmethod
    def edit_catamin_stages(save_file: core.SaveFile):
        choice = dialog_creator.ChoiceInput.from_reduced(
            ["change_clear_amount_catamin", "clear_unclear_stage_catamin"],
            dialog="catamin_stage_clear_q",
        ).single_choice()
        if choice is None:
            return None

        if choice == 1:
            names = core.MapNames(save_file, "B", base_index=14000)
            map_ids = core.EventChapters.select_map_names(names.map_names)
            if map_ids is None:
                return None
            if len(map_ids) >= 2:
                choice2 = dialog_creator.ChoiceInput.from_reduced(
                    ["individual", "all_at_once"], dialog="catamin_clear_amounts_q"
                ).single_choice()
                if choice2 is None:
                    return None
            else:
                choice2 = 1

            if choice2 == 2:
                clear_amount = dialog_creator.IntInput().get_input(
                    "enter_clear_amount_catamin", {}
                )[0]
                if clear_amount is None:
                    return None
                for map_id in map_ids:
                    save_file.event_stages.chapter_completion_count[14_000 + map_id] = (
                        clear_amount
                    )
            elif choice == 1:
                for map_id in map_ids:
                    name = names.map_names.get(map_id) or core.localize("unknown_map")
                    clear_amount = dialog_creator.IntInput().get_input(
                        "enter_clear_amount_catamin_map", {"name": name, "id": map_id}
                    )[0]
                    if clear_amount is None:
                        return None
                    save_file.event_stages.chapter_completion_count[14_000 + map_id] = (
                        clear_amount
                    )

            color.ColoredText.localize("catamin_stage_success")

        elif choice == 2:
            completed_chapters = save_file.catamin_stages.chapters.edit_chapters(
                save_file, "B", 14000
            )
            if completed_chapters is None:
                return None

            # TODO: maybe in the future ask if the user wants to modify the chapter clear amounts


# ============================================================
# FILE: zero_legends.py
# ============================================================
from __future__ import annotations
from typing import Any
from bcsfe import core
from bcsfe.cli import edits, color


class Stage:
    def __init__(self, clear_times: int):
        self.clear_times = clear_times

    @staticmethod
    def init() -> Stage:
        return Stage(0)

    @staticmethod
    def read(data: core.Data) -> Stage:
        clear_times = data.read_short()
        return Stage(clear_times)

    def write(self, data: core.Data):
        data.write_short(self.clear_times)

    def serialize(self) -> int:
        return self.clear_times

    @staticmethod
    def deserialize(data: int) -> Stage:
        return Stage(
            data,
        )

    def __repr__(self):
        return f"Stage({self.clear_times})"

    def __str__(self):
        return self.__repr__()

    def clear_stage(self, clear_amount: int = 1, ensure_cleared_only: bool = False):
        if ensure_cleared_only:
            self.clear_times = self.clear_times or clear_amount
        else:
            self.clear_times = clear_amount

    def unclear_stage(self):
        self.clear_times = 0


class Chapter:
    def __init__(
        self,
        selected_stage: int,
        clear_progress: int,
        unlock_state: int,
        stages: list[Stage],
    ):
        self.selected_stage = selected_stage
        self.clear_progress = clear_progress
        self.unlock_state = unlock_state
        self.stages = stages

        self.total_stages = 0

    def clear_stage(
        self,
        index: int,
        clear_amount: int = 1,
        overwrite_clear_progress: bool = False,
        ensure_cleared_only: bool = False,
    ) -> bool:
        if overwrite_clear_progress:
            self.clear_progress = index + 1
        else:
            self.clear_progress = max(self.clear_progress, index + 1)
        self.stages[index].clear_stage(clear_amount, ensure_cleared_only)
        self.chapter_unlock_state = 3
        if index == self.total_stages - 1:
            return True
        return False

    def unclear_stage(self, index: int) -> bool:
        self.clear_progress = min(self.clear_progress, index)
        self.stages[index].unclear_stage()
        return True

    @staticmethod
    def init() -> Chapter:
        return Chapter(0, 0, 0, [])

    @staticmethod
    def read(data: core.Data) -> Chapter:
        selected_stage = data.read_byte()
        clear_progress = data.read_byte()
        unlock_state = data.read_byte()
        total_stages = data.read_short()
        stages = [Stage.read(data) for _ in range(total_stages)]
        return Chapter(
            selected_stage,
            clear_progress,
            unlock_state,
            stages,
        )

    def write(self, data: core.Data):
        data.write_byte(self.selected_stage)
        data.write_byte(self.clear_progress)
        data.write_byte(self.unlock_state)
        data.write_short(len(self.stages))
        for stage in self.stages:
            stage.write(data)

    def serialize(self) -> dict[str, Any]:
        return {
            "selected_stage": self.selected_stage,
            "clear_progress": self.clear_progress,
            "unlock_state": self.unlock_state,
            "stages": [stage.serialize() for stage in self.stages],
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> Chapter:
        return Chapter(
            data.get("selected_stage", 0),
            data.get("clear_progress", 0),
            data.get("unlock_state", 0),
            [Stage.deserialize(stage) for stage in data.get("stages", [])],
        )

    def __repr__(self):
        return f"Chapter({self.selected_stage}, {self.clear_progress}, {self.unlock_state}, {self.stages})"

    def __str__(self):
        return self.__repr__()


class ChaptersStars:
    def __init__(self, unknown: int, chapters: list[Chapter]):
        self.unknown = unknown
        self.chapters = chapters

    def clear_stage(
        self,
        star: int,
        stage: int,
        clear_amount: int = 1,
        overwrite_clear_progress: bool = False,
        ensure_cleared_only: bool = False,
    ) -> bool:
        finished = self.chapters[star].clear_stage(
            stage, clear_amount, overwrite_clear_progress, ensure_cleared_only
        )
        if finished:
            if star + 1 < len(self.chapters):
                self.chapters[star + 1].chapter_unlock_state = 1
        return finished

    def unclear_stage(self, star: int, stage: int) -> bool:
        finished = self.chapters[star].unclear_stage(stage)
        if finished and star + 1 < len(self.chapters):
            for chapter in self.chapters[star + 1 :]:
                chapter.chapter_unlock_state = 0
        return finished

    @staticmethod
    def init() -> ChaptersStars:
        return ChaptersStars(0, [])

    @staticmethod
    def read(data: core.Data) -> ChaptersStars:
        unknown = data.read_byte()
        total_stars = data.read_byte()
        chapters = [Chapter.read(data) for _ in range(total_stars)]
        return ChaptersStars(
            unknown,
            chapters,
        )

    def write(self, data: core.Data):
        data.write_byte(self.unknown)
        data.write_byte(len(self.chapters))
        for chapter in self.chapters:
            chapter.write(data)

    def serialize(self) -> dict[str, Any]:
        return {
            "unknown": self.unknown,
            "chapters": [chapter.serialize() for chapter in self.chapters],
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> ChaptersStars:
        return ChaptersStars(
            data.get("unknown", 0),
            [Chapter.deserialize(chapter) for chapter in data.get("chapters", [])],
        )

    def __repr__(self):
        return f"ChaptersStars({self.unknown}, {self.chapters})"

    def __str__(self):
        return self.__repr__()


class ZeroLegendsChapters:
    def __init__(self, chapters: list[ChaptersStars]):
        self.chapters = chapters

    def clear_stage(
        self,
        map: int,
        star: int,
        stage: int,
        clear_amount: int = 1,
        overwrite_clear_progress: bool = False,
        ensure_cleared_only: bool = False,
    ) -> bool:
        self.create(map)
        finished = self.chapters[map].clear_stage(
            star, stage, clear_amount, overwrite_clear_progress, ensure_cleared_only
        )
        if finished and map + 1 < len(self.chapters):
            self.chapters[map + 1].chapters[0].chapter_unlock_state = 1

        return finished

    def unclear_stage(self, map: int, star: int, stage: int) -> bool:
        self.create(map)
        finished = self.chapters[map].unclear_stage(star, stage)
        if finished and map + 1 < len(self.chapters) and star == 0:
            for chapter in self.chapters[map + 1].chapters:
                chapter.chapter_unlock_state = 0

        return finished

    @staticmethod
    def init() -> ZeroLegendsChapters:
        return ZeroLegendsChapters([])

    @staticmethod
    def read(data: core.Data) -> ZeroLegendsChapters:
        total_chapters = data.read_short()
        chapters = [ChaptersStars.read(data) for _ in range(total_chapters)]
        return ZeroLegendsChapters(
            chapters,
        )

    def write(self, data: core.Data):
        data.write_short(len(self.chapters))
        for chapter in self.chapters:
            chapter.write(data)

    def serialize(self) -> list[dict[str, Any]]:
        return [chapter.serialize() for chapter in self.chapters]

    @staticmethod
    def deserialize(data: list[dict[str, Any]]) -> ZeroLegendsChapters:
        return ZeroLegendsChapters(
            [ChaptersStars.deserialize(chapter) for chapter in data],
        )

    def __repr__(self):
        return f"Chapters({self.chapters})"

    def __str__(self):
        return self.__repr__()

    def get_total_stars(self, chapter_id: int) -> int:
        return len(self.chapters[chapter_id].chapters)

    def get_total_stages(self, chapter_id: int, star: int) -> int:
        return len(self.chapters[chapter_id].chapters[star].stages)

    def create(self, chapter_id: int):
        diff = chapter_id - len(self.chapters)

        if diff >= 0:
            for _ in range(diff + 1):
                stages = [Stage(0)] * self.get_total_stages(0, 0)
                chapters = [Chapter(0, 0, 0, stages)] * self.get_total_stars(0)
                chapters_stars = ChaptersStars(0, chapters)
                self.chapters.append(chapters_stars)

    @staticmethod
    def edit_zero_legends(save_file: core.SaveFile):
        color.ColoredText.localize("zero_legends_warning")
        zero_legends_chapters = save_file.zero_legends
        zero_legends_chapters.edit_chapters(save_file, "ND", base_index=34000)

    @staticmethod
    def edit_catclaw_championships(save_file: core.SaveFile):
        zero_legends_chapters = save_file.dojo_chapters
        zero_legends_chapters.edit_chapters(save_file, "G", 37000, True)

    def edit_chapters(
        self,
        save_file: core.SaveFile,
        letter_code: str,
        base_index: int,
        no_r_prefix: bool = False,
    ):
        edits.map.edit_chapters(
            save_file, self, letter_code, no_r_prefix=no_r_prefix, base_index=base_index
        )

    def unclear_rest(self, stages: list[int], stars: int, id: int):
        if not stages:
            return
        for star in range(stars, self.get_total_stars(id)):
            for stage in range(max(stages), self.get_total_stages(id, star)):
                self.chapters[id].chapters[star].stages[stage].clear_times = 0
                self.chapters[id].chapters[star].clear_progress = 0

    def set_total_stages(self, map: int, total_stages: int):
        self.create(map)
        for chapter in self.chapters[map].chapters:
            chapter.total_stages = total_stages

