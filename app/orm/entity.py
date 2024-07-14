"""レコードエンティティをまとめたモジュール

Classes:
    Entity: テーブルのレコードに対応するEntity基底クラス
    User: `users`テーブルのレコードに対応するEntityクラス
"""

from dataclasses import asdict, dataclass
from datetime import datetime

from sqlalchemy import DATETIME, String, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


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
            `user_id`カラム。主キー。
            `optional`引数であり`None`を許容する。
            引数未指定の場合は`AUTO_INCREMENT`により既存レコードに +1 加算した通番が登録される。

        user_name (Mapped[str], optional):
            `user_name`カラム。`NOT NULL`制約あり。

        created_at (Mapped[datetime | None], optional):
            `created_at`カラム。
            `optional`引数であり`None`を許容する。
            引数未指定の場合は`CURRENT_TIMESTAMP`により現在の日時で初期化される。
            [11.2.5 TIMESTAMP および DATETIME の自動初期化および更新機能\
            ](https://dev.mysql.com/doc/refman/8.0/ja/timestamp-initialization.html)

        updated_at (Mapped[datetime | None], optional):
            `updated_at`カラム。
            `optional`引数であり`None`を許容する。
            引数未指定の場合は`CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP`
            により現在の日時で初期化および更新される。
            [11.2.5 TIMESTAMP および DATETIME の自動初期化および更新機能\
            ](https://dev.mysql.com/doc/refman/8.0/ja/timestamp-initialization.html)
    """

    __tablename__ = "users"

    user_id: Mapped[int | None] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(50), nullable=False)
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
