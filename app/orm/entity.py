"""レコードエンティティをまとめたモジュール

Classes:
    Entity: テーブルのレコードに対応するEntity基底クラス
    User: `users`テーブルのレコードに対応するEntityクラス
    GenerationHistory: `generation_history`テーブルのレコードに対応するEntityクラス
"""

from dataclasses import asdict, dataclass
from datetime import datetime

from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import CHAR, DATETIME, INT, TEXT, VARCHAR


class Entity(DeclarativeBase):
    """テーブルのレコードに対応するEntity基底クラス

    MetaDataコレクション関連付け用の宣言基底クラスの役割も担い、
    各テーブルのレコードに対応するEntityクラスは、このクラスを継承して定義する。
    [Establishing a Declarative Base\
    ](https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#establishing-a-declarative-base)
    """

    pass


@dataclass
class User(Entity):
    """`users`テーブルのレコードに対応するEntityクラス

    Attributes:
        user_id (Mapped[int | None], optional):
            ユーザID `user_id` カラム。主キー。
            `optional`引数であり`None`を許容する。
            引数未指定の場合は`AUTO_INCREMENT`により既存レコードに +1 加算した通番が登録される。

        user_name (Mapped[str], optional):
            ユーザ名 `user_name` カラム。`NOT NULL`制約あり。

        created_at (Mapped[datetime | None], optional):
            作成日時 `created_at` カラム。
            `optional`引数であり`None`を許容する。
            引数未指定の場合は`CURRENT_TIMESTAMP`により現在の日時で初期化される。
            [11.2.5 TIMESTAMP および DATETIME の自動初期化および更新機能\
            ](https://dev.mysql.com/doc/refman/8.0/ja/timestamp-initialization.html)

        updated_at (Mapped[datetime | None], optional):
            更新日時 `updated_at` カラム。
            `optional`引数であり`None`を許容する。
            引数未指定の場合は`CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP`
            により現在の日時で初期化および更新される。
            [11.2.5 TIMESTAMP および DATETIME の自動初期化および更新機能\
            ](https://dev.mysql.com/doc/refman/8.0/ja/timestamp-initialization.html)
    """

    __tablename__ = "users"

    user_id: Mapped[int | None] = mapped_column(INT, primary_key=True)
    user_name: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    created_at: Mapped[datetime | None] = mapped_column(
        DATETIME,
        # https://docs.sqlalchemy.org/en/20/dialects/mysql.html#timestamp-datetime-issues
        server_default=text("CURRENT_TIMESTAMP"),
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DATETIME,
        # https://docs.sqlalchemy.org/en/20/dialects/mysql.html#timestamp-datetime-issues
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )

    def to_dict(self) -> dict[str, int | str | datetime | None]:
        """`User`オブジェクトを辞書へ変換する。

        Returns:
            dict[str, int | str | datetime | None]: `User`情報を保持する辞書
        """
        return asdict(self)


@dataclass
class GenerationHistory(Entity):
    """`generation_history`テーブルのレコードに対応するEntityクラス

    Attributes:
        request_id (Mapped[str | None], optional):
            リクエストID `request_id` カラム。主キー。
            `optional`引数であり`None`を許容する。
            デフォルト値は`'00000000000'`であるものの実際には、
            引数未指定の場合は`create_request_id`トリガーにより
            登録日（YYMMDD）+ シーケンス（5桁0埋め）の通番11桁が設定される。

        prompt_ja (Mapped[str | None], optional):
            指示（日本語）`prompt_ja` カラム。文字起こし結果。
            `optional`引数であり`None`を許容する。

        html (Mapped[str | None], optional):
            HTML `html` カラム。生成結果。
            `optional`引数であり`None`を許容する。

        created_at (Mapped[datetime | None], optional):
            作成日時 `created_at` カラム。
            `optional`引数であり`None`を許容する。
            引数未指定の場合は`CURRENT_TIMESTAMP`により現在の日時で初期化される。
            [11.2.5 TIMESTAMP および DATETIME の自動初期化および更新機能\
            ](https://dev.mysql.com/doc/refman/8.0/ja/timestamp-initialization.html)

        updated_at (Mapped[datetime | None], optional):
            更新日時 `updated_at` カラム。
            `optional`引数であり`None`を許容する。
            引数未指定の場合は`CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP`
            により現在の日時で初期化および更新される。
            [11.2.5 TIMESTAMP および DATETIME の自動初期化および更新機能\
            ](https://dev.mysql.com/doc/refman/8.0/ja/timestamp-initialization.html)
    """

    __tablename__ = "generation_history"

    request_id: Mapped[str | None] = mapped_column(
        CHAR(11), primary_key=True, default="0" * 11
    )
    prompt_ja: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    html: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(
        DATETIME,
        # https://docs.sqlalchemy.org/en/20/dialects/mysql.html#timestamp-datetime-issues
        server_default=text("CURRENT_TIMESTAMP"),
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DATETIME,
        # https://docs.sqlalchemy.org/en/20/dialects/mysql.html#timestamp-datetime-issues
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )

    def to_dict(self) -> dict[str, str | datetime | None]:
        """`GenerationHistory`オブジェクトを辞書へ変換する。

        Returns:
            dict[str, str | datetime | None]: `GenerationHistory`情報を保持する辞書
        """
        return asdict(self)
