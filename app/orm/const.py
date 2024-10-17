"""`orm`パッケージ内で使用する定数をまとめたモジュール

Classes:
    PathConst: ファイルパス定数クラス
    Char: 文字定数クラス
    Message: メッセージ定数クラス
"""

from os import linesep
from pathlib import Path


class PathConst:
    """ファイルパス定数クラス"""

    ORM_BASE_DIR = Path(__file__).resolve().parent
    """`orm`パッケージ基底ディレクトリ"""

    CONFIG_DIR = f"{ORM_BASE_DIR}/config"
    """構成ファイルパス"""

    DB_CONFIG_FILE = f"{CONFIG_DIR}/db_config.ini"
    """DB設定ファイルパス"""


class Char:
    """文字定数クラス"""

    SPACE = " "
    """半角スペース: `" "`"""

    INDENTATION = SPACE * 4
    """
    インデント（半角スペース × 4）::

        "    "
    """


class Message:
    """メッセージ定数クラス"""

    CLOSED_SESSION_MESSAGE = "Session was closed."
    """セッション終了メッセージ"""

    ORM_ERROR_MESSAGE = "Some error has occurred in O/R Mapper."
    """O/R Mapper エラーメッセージ"""

    ORM_ERROR_MESSAGE_SUBHEADING = "<message>"
    """O/R Mapper エラーメッセージ小見出し"""

    DB_CONFIG_ERROR = "Something may be wrong with 'db_config.ini'."
    """DB構成エラーメッセージ"""

    DB_CONNECTION_ERROR = (
        "Docker container may be stopped" + " or network not configured."
    )
    """DB接続エラーメッセージ"""

    SINGLETON_DB_ENGINE_ERROR = (
        "'sqlalchemy.engine.base.Engine' has already been created."
    )
    """SingletonDBエンジンエラーメッセージ"""

    DECORATED_FUNCTION_INCORRECT_CLASS_ERROR = (
        "'self' is not an instance of 'orm.connection.SessionManager'"
        " or its subclasses."
        + linesep
        + "Cannot add '@throws_orm_error' except to SessionManager's methods"
        " because this decorator call 'close_session()' internally."
    )
    """デコレータ付加関数クラス不正エラー"""

    DECORATED_FUNCTION_RECURSION_ERROR = (
        "Must not add this decorator"
        " to 'orm.connection.SessionManager.close_session()' method"
        " because this decorator call 'close_session()' internally."
    )
    """デコレータ付加関数再帰呼び出しエラー"""
