"""DBレコード操作を担うモジュール

Classes:
    Mapper: DBレコード操作用O/Rマッパー
"""

from typing import Any, Tuple, TypeVar

from orm.aop import raise_orm_error
from orm.connection import SessionManager
from orm.entity import Entity
from sqlalchemy import Delete, Select, Update
from sqlalchemy.engine.result import Result, ScalarResult

T = TypeVar("T", bound=Entity)
"""型変数（Entityまたはそのサブクラス）"""


class Mapper(SessionManager):
    """DBレコード操作用O/Rマッパー

    PythonオブジェクトとDBレコードとをマッピングし、DML操作を行う。
    また、コミット・ロールバック用のメソッドを提供し、併せてトランザクション制御も行う。
    """

    @raise_orm_error
    def insert(self, *entities: Entity) -> None:
        """INSERT文実行

        Args:
            *entities (Entity, optional): 挿入対象レコード

        Raises:
            OrmError: O/R Mapper エラー

        Examples::

            from orm.entity import User
            from orm.mapper import Mapper

            mapper = Mapper.create_session()
            mapper.insert(
                User(user_name="admin"),
                User(user_name="user1"),
                User(user_name="user2"),
            )
            mapper.commit()
            # User(user_id=0, user_name='admin', created_at=datetime... )
            # User(user_id=1, user_name='user1', created_at=datetime... )
            # User(user_id=2, user_name='user2', created_at=datetime... )

        Note:
            [Using INSERT Statements\
            ](https://docs.sqlalchemy.org/en/20/tutorial/data_insert.html)
        """
        self._session.add_all(entities)

    @raise_orm_error
    def update(self, update_statement: Update) -> None:
        """UPDATE文実行

        Args:
            update_statement (Update): UPDATE文

        Raises:
            OrmError: O/R Mapper エラー

        Examples::

            from orm.entity import User
            from orm.mapper import Mapper
            from sqlalchemy import update

            mapper = Mapper.create_session()
            # User(user_id=0, user_name='admin', created_at=datetime... )
            # User(user_id=1, user_name='user1', created_at=datetime... )
            # User(user_id=2, user_name='user2', created_at=datetime... )

            update_statement = (
                update(User).values(user_name="USER1").where(User.user_id == 1)
            )
            mapper.update(update_statement)
            mapper.commit()
            # User(user_id=0, user_name='admin', created_at=datetime... )
            # User(user_id=1, user_name='USER1', created_at=datetime... )
            # User(user_id=2, user_name='user2', created_at=datetime... )

        Note:
            [Using UPDATE and DELETE Statements\
            ](https://docs.sqlalchemy.org/en/20/tutorial/data_update.html)
        """
        self._session.execute(update_statement)

    def delete(self, delete_statement: Delete) -> None:
        """DELETE文実行

        Args:
            delete_statement (Delete): DELETE文

        Raises:
            OrmError: O/R Mapper エラー

        Examples::

            from orm.entity import User
            from orm.mapper import Mapper
            from sqlalchemy import delete

            mapper = Mapper.create_session()
            # User(user_id=0, user_name='admin', created_at=datetime... )
            # User(user_id=1, user_name='user1', created_at=datetime... )
            # User(user_id=2, user_name='user2', created_at=datetime... )

            delete_statement = delete(User).where(User.user_id == 1)
            mapper.delete(delete_statement)
            mapper.commit()
            # User(user_id=0, user_name='admin', created_at=datetime... )
            # User(user_id=2, user_name='user2', created_at=datetime... )

        Note:
            [Using UPDATE and DELETE Statements\
            ](https://docs.sqlalchemy.org/en/20/tutorial/data_update.html)
        """
        self._session.execute(delete_statement)

    @raise_orm_error
    def select(self, select_statement: Select[Tuple[T]]) -> ScalarResult[T]:
        """SELECT文実行

        SELECTの結果セットをEntityのイテラブルオブジェクトで返却する。

        Args:
            select_statement (Select[Tuple[T]]): SELECT文

        Returns:
            ScalarResult[T]: 結果セットEntityイテラブル

        Raises:
            OrmError: O/R Mapper エラー

        Examples::

            from orm.entity import User
            from orm.mapper import Mapper
            from sqlalchemy import select

            mapper = Mapper.create_session()

            select_statement = select(User)
            for user in mapper.select(select_statement):
                print(user)
            # User(user_id=0, user_name='admin', created_at=datetime... )
            # User(user_id=1, user_name='user1', created_at=datetime... )
            # User(user_id=2, user_name='user2', created_at=datetime... )

            select_statement = select(User).where(User.user_name.like("user%"))
            for user in mapper.select(select_statement):
                print(user)
            # User(user_id=1, user_name='user1', created_at=datetime... )
            # User(user_id=2, user_name='user2', created_at=datetime... )

        Note:
            [Using SELECT Statements\
            ](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html)
        """
        return self._session.scalars(select_statement)

    @raise_orm_error
    def select_as_tuples(
        self, select_statement: Select[Tuple[Any, ...]]
    ) -> Result[Tuple[Any, ...]]:
        """SELECT文実行

        SELECTの結果セットを指定したカラムのタプルのイテラブルオブジェクトで返却する。

        Args:
            select_statement (Select[Tuple[Any, ...]]): SELECT文

        Returns:
            Result[Tuple[Any, ...]]: 結果セットのタプル（カラム）イテラブル

        Raises:
            OrmError: O/R Mapper エラー

        Examples::

            from orm.entity import User
            from orm.mapper import Mapper
            from sqlalchemy import select

            mapper = Mapper.create_session()

            select_statement = select(User.user_id, User.user_name)
            for id, name in mapper.select_as_tuples(select_statement):
                print(id, name)
            # 0 admin
            # 1 user1
            # 2 user2

            stmt = select(User.user_id, User.user_name).where(User.user_id > 0)
            for id, name in mapper.select_as_tuples(stmt):
                print(id, name)
            # 1 user1
            # 2 user2

        Note:
            [Using SELECT Statements\
            ](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html)
        """
        return self._session.execute(select_statement)

    @raise_orm_error
    def commit(self) -> None:
        """コミット"""
        self._session.commit()

    @raise_orm_error
    def rollback(self) -> None:
        """ロールバック"""
        self._session.rollback()
