"""履歴管理データオブジェクトモジュール

Classes:
    HistoryDto: 履歴データオブジェクト
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class HistoryDto:
    """履歴データオブジェクト

    Attributes:
        request_id (str | None, optional): リクエストID
        prompt_ja (str | None, optional): 指示（日本語）
        html (str | None, optional): HTML
        created_at (datetime | None, optional): 作成日時
        updated_at (datetime | None, optional): 更新日時
    """

    request_id: str | None = None
    prompt_ja: str | None = None
    html: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @classmethod
    def of(cls, input: str, output: str):
        """履歴データオブジェクト生成

        インプットとアウトプットの履歴データオブジェクトを生成する。

        Args:
            input (str): インプット（日本語のリクエスト内容）
            output (str): アウトプット（生成されたHTMLのテキスト）

        Returns:
            HistoryDto: 履歴データオブジェクト
        """
        dto = cls()
        dto.prompt_ja = input
        dto.html = output
        return dto
