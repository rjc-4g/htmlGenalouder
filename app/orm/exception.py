"""`orm`パッケージの処理で送出される独自例外をまとめたモジュール

Classes:
    SingletonDbEngineError: SingletonDBエンジンエラー
    DecoratedFunctionRecursiveError: デコレータ付加関数再帰呼び出しエラー
    OrmError: O/R Mapper エラー
"""

from os import linesep

from orm.const import Char, Message
from orm.utils import CollectionUtils


class SingletonDbEngineError(Exception):
    """SingletonDBエンジンエラー"""

    def __init__(self):
        """SingletonDBエンジンエラー

        `Engine`は、一度だけDBとの接続を確立し、コネクションプールを提供するグローバルオブジェクトのため、
        Singletonインスタンスであることを保証し、2度目以降のインスタンス生成試行時にこの例外が送出される。
        [Establishing Connectivity - the Engine\
        ](https://docs.sqlalchemy.org/en/20/tutorial/engine.html#establishing-connectivity-the-engine)
        """
        super().__init__(Message.SINGLETON_DB_ENGINE_ERROR)


class DecoratedFunctionRecursionError(Exception):
    """デコレータ付加関数再帰呼び出しエラー"""

    def __init__(self):
        """デコレータ付加関数再帰呼び出しエラー

        デコレータを付加した関数が、デコレータ内部で呼び出されている場合に使用される。
        事前に付加対象を確認し、再帰的呼び出しによる`RecursionError`エラーを回避する。
        `RecursionError: maximum recursion depth exceeded in comparison`
        """
        super().__init__(Message.DECORATED_FUNCTION_RECURSION_ERROR)


class OrmError(Exception):
    """O/R Mapper エラー

    Attributes:
        origin (Exception): 元の例外
        messages (tuple[str, ...]): 追加メッセージのタプル（メッセージなしの場合は空タプル）
    """

    def __init__(
        self,
        origin: Exception,
        *messages: str | list[str] | tuple[str, ...],
    ) -> None:
        """O/R Mapper の処理中に送出された例外のラッパー

        `mysql.connector.Error`や`sqlalchemy.exc.DBAPIError`等のエラーをラップし、
        固有の追加メッセージ（主にセッションの切断に関連する情報）を含めた例外を生成する。

        Args:
            origin (Exception):
                元の例外
            *messages (str | list[str] | tuple[str, ...], optional):
                追加メッセージ可変長引数（要素の型：文字列・文字列リスト・文字列タプル）
        """
        self._origin = origin
        self._messages = CollectionUtils.flat_map_to_tuple(messages)

    @property
    def origin(self) -> Exception:
        """origin (Exception): 元の例外"""
        return self._origin

    @property
    def messages(self) -> tuple[str, ...]:
        """messages (tuple[str, ...]): 追加メッセージのタプル（メッセージなしの場合は空タプル）"""
        return self._messages

    def __str__(self) -> str:

        msgs_list = [
            Message.ORM_ERROR_MESSAGE,
            Message.ORM_ERROR_MESSAGE_SUBHEADING,
            map(lambda msg: Char.INDENTATION + msg, self._messages),
            str(type(self._origin)),
            map(
                lambda msg: Char.INDENTATION + msg,
                str(self._origin).splitlines(),
            ),
        ]
        flat_msg_tuple = CollectionUtils.flat_map_to_tuple(msgs_list)
        return linesep.join(flat_msg_tuple)
