"""O/R Mapper パッケージ

Modules:
    aop: デコレータによってAOP機能を提供するモジュール
    connection: DB接続処理を担うモジュール
    const: `orm`パッケージ内で使用する定数をまとめたモジュール
    entity: レコードエンティティをまとめたモジュール
    exception: `orm`パッケージの処理で送出される独自例外をまとめたモジュール
    mapper: DBレコード操作を担うモジュール
    utils: `orm`パッケージ内で使用するユーティリティをまとめたモジュール

Usage:
    `Mapper`クラスを利用したCRUD処理

    1: `Mapper.create_session()`でDB接続およびセッションの確立を行う。
    2: SQL文を作成し、問い合わせを行う。
    3: セッションを終了する。

    4: 例::

        from orm.entity import User
        from orm.mapper import Mapper
        from sqlalchemy import select

        # 1. セッションの確立
        mapper = Mapper.create_session()

        # 2. SQL問い合わせ
        mapper.insert(
            User(user_name="admin"),
            User(user_name="user1"),
            User(user_name="user2"),
        )
        mapper.commit()

        # 2. SQL問い合わせ
        select_statement = select(User).where(User.user_name.like("user%"))
        for user in mapper.select(select_statement):
            print(user)
        # User(user_id=1, user_name='user1', created_at=datetime... )
        # User(user_id=2, user_name='user2', created_at=datetime... )

        # 3. セッションの終了
        mapper.close_session()

    5: 備考

        5-1: 明示的な`mapper.commit()`の呼び出しが無い場合、セッション終了時にトランザクションはロールバックされる。
        5-2: 処理中にエラーが発生した場合、ロールバックおよびセッション終了処理が実行され`OrmError`が送出される。

    with文と`Mapper`クラスを利用したCRUD処理

    1: with文で`Mapper.create_session()`を使用し、DB接続およびセッションの確立を行う。
    2: SQL文を作成し、問い合わせを行う。
    3: with文を抜けると、トランザクションのコミットおよびセッション終了処理が実行される。

    4: 例::

        from orm.entity import User
        from orm.mapper import Mapper
        from sqlalchemy import select

        # 1. セッションの確立
        with Mapper.create_session() as mapper:

            # 2. SQL問い合わせ
            mapper.insert(
                User(user_name="admin"),
                User(user_name="user1"),
                User(user_name="user2"),
            )
            # コミット不要
            # mapper.commit()

            # 2. SQL問い合わせ
            select_statement = select(User).where(User.user_name.like("user%"))
            for user in mapper.select(select_statement):
                print(user)
            # User(user_id=1, user_name='user1', created_at=datetime... )
            # User(user_id=2, user_name='user2', created_at=datetime... )

            # mapper.close_session()

        # with文を抜けるとトランザクションがコミットされ同時にセッションが終了する。

Note:
    SELECT文の組み立て詳細については以下を参照のこと。
    [Using SELECT Statements\
    ](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html)

    `Mapper`クラスは`sqlalchemy.orm.Session`を利用しO/Rマッピングを実現している。
    [Using the Session](https://docs.sqlalchemy.org/en/20/orm/session.html)
    に沿って、さらに複雑なカスタム処理を実現したい場合は、
    内部で生成された`Session`のプロパティへもアクセス可能。
    その場合、`session`または`begun_session`プロパティを取得して利用する。
"""
