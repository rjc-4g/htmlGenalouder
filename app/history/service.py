"""履歴管理サービスモジュール

Classes:
    HistoryService: 履歴サービス
"""

from history.dto import HistoryDto
from orm.entity import GenerationHistory
from orm.mapper import Mapper
from sqlalchemy import select


class HistoryService:
    """履歴サービス

    履歴管理に関わる処理を提供する。
    - 履歴の登録
    - 履歴の一覧取得
    """

    def register_history(self, history_dto: HistoryDto) -> None:
        """履歴を登録する。

        Args:
            history_dto (HistoryDto): 履歴データオブジェクト

        Raises:
            OrmError: O/R Mapper エラー
        """

        with Mapper.create_session() as mapper:
            generation_history = GenerationHistory(
                prompt_ja=history_dto.prompt_ja,
                html=history_dto.html,
            )
            mapper.insert(generation_history)

    def get_all_histories(self) -> tuple[HistoryDto, ...]:
        """登録された全ての履歴を取得する。

        Returns:
            tuple[HistoryDto, ...]: 履歴データオブジェクトのタプル

        Raises:
            OrmError: O/R Mapper エラー
        """

        with Mapper.create_session() as mapper:
            select_statement = select(GenerationHistory)
            return tuple(
                map(
                    lambda gh: HistoryDto(**gh.to_dict()),
                    mapper.select(select_statement),
                )
            )
