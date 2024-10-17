"""デコレータによってAOP機能を提供するモジュール

Functions:
    raise_orm_error: O/R Mapper エラー送出デコレータ
"""

from mysql.connector import Error as MysqlError
from mysql.connector import errorcode
from orm.const import Message
from orm.exception import DecoratedFunctionRecursionError, OrmError
from sqlalchemy.exc import DBAPIError


def raise_orm_error(decorated_function):
    """O/R Mapper エラー送出デコレータ

    `orm.connection.SessionManager`またはその子クラスのメソッドに付加することで、
    エラー発生時に以下の処理を行う。
    - 実行中のトランザクションをロールバックし、セッションを終了する。
    - 発生したエラーをラップした`orm.exception.OrmError`を送出する。

    Raises:
        OrmError: O/R Mapper エラー（デコレータを付加したメソッド内で例外が送出された場合）

        `SessionManager`またはその子クラス以外のメソッドに付加された場合は、`TypeError`をラップした`OrmError`を送出する。

        `SessionManager.close_session()`に付加された場合は、`DecoratedFunctionRecursiveError`をラップした`OrmError`を送出する。
        これはエラー発生時の挙動であるセッション終了に`close_session()`を使用しており、再帰的に呼び出しが繰り返されてしまうため。

    Examples::

        class Mapper(SessionManager):
            @raise_orm_error # add @raise_orm_error decorator
            def insert(self) -> None:
                raise Exception("Some SQL error has occurred.")

        try:
            mapper = Mapper.create_session()
            mapper.insert()
        except Exception as e:
            print(e)

        # mapper.insert()内でエラーが発生すると、
        # 先にセッション終了処理が実行され、その後 Exception をラップした OrmError が送出される。
        > python main.py
        Some error has occurred in O/R Mapper.
        <message>
            Session was closed.
        <class 'Exception'>
            Some SQL error has occurred.
    """

    def function_with_exception_handler(self=None, *args, **kwargs):
        # デコレータが付加された関数をtry文で囲み、例外ハンドラを追加したメソッドとして再定義する。

        # 型チェック用import（循環参照回避）
        from orm.connection import SessionManager

        # 事前処理：デコレータが付加された関数がSessionManagerまたはその子クラスのメソッドでない場合は型エラー送出
        if not isinstance(self, SessionManager):
            raise OrmError(
                TypeError(Message.DECORATED_FUNCTION_INCORRECT_CLASS_ERROR),
            )

        # 事前処理：デコレータが付加された関数がSessionManagerまたはその子クラスのclose_session()メソッドの場合は独自エラー送出
        if decorated_function.__name__ == "close_session":
            raise OrmError(DecoratedFunctionRecursionError())

        try:

            # デコレータが付加された関数を実行
            return decorated_function(self, *args, **kwargs)

        except KeyError as e:

            self.close_session()
            msgs = (Message.CLOSED_SESSION_MESSAGE, Message.DB_CONFIG_ERROR)
            raise OrmError(e, msgs)

        except DBAPIError as e:

            if not isinstance(e.orig, MysqlError):
                self.close_session()
                raise OrmError(e, Message.CLOSED_SESSION_MESSAGE)

            msg_list = []

            if (
                e.orig.errno == errorcode.ER_DBACCESS_DENIED_ERROR
                or e.orig.errno == errorcode.ER_ACCESS_DENIED_ERROR
                or e.orig.errno == errorcode.CR_CONN_HOST_ERROR
            ):
                msg_list.append(Message.DB_CONFIG_ERROR)

            if e.orig.errno == errorcode.CR_CONN_HOST_ERROR:
                msg_list.append(Message.DB_CONNECTION_ERROR)

            self.close_session()
            raise OrmError(e, Message.CLOSED_SESSION_MESSAGE, msg_list)

        except Exception as e:

            self.close_session()
            raise OrmError(e, Message.CLOSED_SESSION_MESSAGE)

    return function_with_exception_handler
