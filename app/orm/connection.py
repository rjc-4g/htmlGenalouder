"""DB接続処理を担うモジュール

Classes:
    SessionManager: セッション管理クラス
"""

from contextlib import AbstractContextManager
from typing import Any

from orm.aop import raise_orm_error
from orm.exception import OrmError, SingletonDbEngineError
from orm.utils import DbConfigReader
from sqlalchemy import URL, create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session, sessionmaker


class _Factory:
    """DB接続関連ファクトリー

    `connection`モジュール内（セッション管理クラス）でのみ利用し、外部に公開しない。
    """

    _engine: Engine | None = None
    """DB接続確立エンジン"""

    @staticmethod
    def create_engine() -> Engine:
        """DB接続確立エンジン作成

        DB接続情報に基づきDB接続を確立する。

        Returns:
            Engine: DB接続確立エンジン

        Raises:
            SingletonDbEngineError: SingletonDBエンジンエラー

            DB接続確立エンジンが既に生成されていた場合に送出される。
            `Engine`は、一度だけDBとの接続を確立し、コネクションプールを提供するグローバルオブジェクトのため。
            [Establishing Connectivity - the Engine\
            ](https://docs.sqlalchemy.org/en/20/tutorial/engine.html#establishing-connectivity-the-engine)
        """

        # インスタンス生成済の場合は例外送出
        if _Factory._engine is not None:
            raise SingletonDbEngineError()

        # 設定ファイル情報からエンジンを生成して返却
        config = DbConfigReader.get_db_config()
        url = URL.create(**config)
        return create_engine(url)

    @staticmethod
    def create_session_factory() -> sessionmaker[Session]:
        """セッションファクトリー作成

        セッション用のファクトリーオブジェクト（`sessionmaker`）を作成する。
        [Using a sessionmaker\
        ](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#using-a-sessionmaker)

        Returns:
            sessionmaker[Session]: セッション用ファクトリーオブジェクト
        """
        return sessionmaker(_Factory.create_engine())


class SessionManager(AbstractContextManager):
    """セッション管理クラス"""

    _Session: sessionmaker[Session] | None = None
    """セッション確立用ファクトリー"""

    @raise_orm_error
    def __init__(self) -> None:
        """セッション管理クラス

        DB接続およびセッションの確立～終了の処理全般を管理する。
        DB接続処理は初回のインスタンス生成時に一度だけ行い、
        以降はその際に用意されたセッション確立用ファクトリーを使用してセッションの確立を処理する。
        """

        # sessionmakerが無い場合のみ生成
        if SessionManager._Session is None:
            SessionManager._Session = _Factory.create_session_factory()

        # sessionmakerを使用してこのインスタンス用のセッションを確立
        self._session = SessionManager._Session()

    def __enter__(self):
        # with文のas句にて型が推論されないためエディタ上での可読性向上のために再定義する
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:

        if all(arg is None for arg in (exc_type, exc_value, traceback)):
            # with文を抜ける際にエラーが無ければコミット
            self._session.commit()

        if exc_type == OrmError:
            # OrmErrorの場合は@throws_orm_errorデコレータにより処理済のためclose不要
            return

        self.close_session()

    def close_session(self) -> None:
        """セッションの終了

        厳密には切断ではなくリセットに近い挙動であり、
        セッションを再使用可能なクリーンな状態にする。
        `Session.reset()`と同義。
        [Using the Session > Session Basics > Closing\
        ](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#closing)
        """
        if not hasattr(self, "_session"):
            # セッションが無い場合（セッション確立失敗時等）は何もしない
            return

        self._session.close()

    @property
    def session(self) -> Session:
        """セッション

        このクラスに用意されたメソッドで足りず、
        呼び出し側で直接 [sqlalchemy.orm.Session\
        ](https://docs.sqlalchemy.org/en/20/orm/session.html) を
        使用したカスタム処理を行いたい場合はこのプロパティからアクセス可能。

        Returns:
            Session: セッション
        """
        return self._session

    @property
    def begun_session(self) -> AbstractContextManager[Session, bool | None]:
        """開始済セッション

        既存のセッションを終了し、新たに開始されたセッションを取得する。

        このクラスに用意されたメソッドで足りず、呼び出し側で直接
        [sqlalchemy.orm.sessionmaker.begin()\
        ](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker.begin)
        により取得した`Session`を使用してカスタム処理を行いたい場合はこのプロパティからアクセス可能。

        `sessionmaker[Session].begin()`により取得したものであり、このセッションはwith文で使用することで、
        with文を抜ける際にトランザクションをコミットし、セッションを終了する。
        [Framing out a begin / commit / rollback block\
        ](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#framing-out-a-begin-commit-rollback-block)

        Returns:
            Session: 開始済セッション

        Examples::

            class Mapper(SessionManager):
                pass

            with Mapper().begun_session as session:
                user1 = User(name="user1")
                user2 = User(name="user2")
                session.add(user1)
                session.add(user2)
                # session.commit()
            # commits the transaction, closes the session
        """
        self._session.close()
        if SessionManager._Session is None:
            SessionManager._Session = _Factory.create_session_factory()
        return SessionManager._Session.begin()

    @classmethod
    def create_session(cls):
        """セッションの確立

        インスタンス生成を行う。例::

            class Mapper(SessionManager):
                pass

        の時、以下は同義。
        - `mapper = Mapper()`
        - `mapper = Mapper.create_session()`
        """
        return cls()
