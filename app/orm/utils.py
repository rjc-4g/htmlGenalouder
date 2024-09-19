"""`orm`パッケージ内で使用するユーティリティをまとめたモジュール

Classes:
    ConfigUtils: 設定ファイルに関するユーティリティメソッドの集合
    DbConfigReader: DB接続情報の読み取りユーティリティ
    CollectionUtils: コレクションに関するユーティリティメソッドの集合
"""

from collections.abc import Iterable
from configparser import ConfigParser
from itertools import chain
from typing import Any

from orm.const import PathConst


class ConfigUtils:
    """設定ファイルに関するユーティリティメソッドの集合"""

    @staticmethod
    def get_config_parser(file_path: str) -> ConfigParser:
        """設定ファイル解析器の取得

        Args:
            file_path (str): 設定ファイル（`.ini`）のパス

        Returns:
            ConfigParser: 設定ファイル解析器
        """
        config_parser = ConfigParser()
        config_parser.read(file_path)
        return config_parser


class DbConfigReader:
    """DB接続情報の読み取りユーティリティ"""

    @staticmethod
    def get_db_config() -> dict[str, Any]:
        """DB接続情報の取得

        Returns:
            dict[str, Any]: DB接続情報（キー：設定項目 ／ 値：設定値）の辞書
        """
        config_parser = ConfigUtils.get_config_parser(PathConst.DB_CONFIG_FILE)
        return {
            "drivername": config_parser["database"]["Driver"],
            "username": config_parser["database"]["Username"],
            "password": config_parser["database"]["Password"],
            "host": config_parser["database"]["Host"],
            "port": config_parser["database"]["Port"],
            "database": config_parser["database"]["Database"],
        }


class CollectionUtils:
    """コレクションに関するユーティリティメソッドの集合"""

    @staticmethod
    def flat_map_to_tuple(
        str_iterable: Iterable[str | list[str] | tuple[str, ...]],
    ) -> tuple[str, ...]:
        """文字列のイテラブルをフラット化しタプルにまとめる。

        文字列、文字列リスト、文字列タプルを要素に持つイテラブルに対し、
        要素のうちリストとタプルを展開してまとめた新しいタプルを返却する。

        Args:
            str_iterable (Iterable[str | list[str] | tuple[str]]): 文字列のイテラブル

        Returns:
            tuple[str, ...]: 渡された文字列イテラブルをフラット化したタプル

        Examples::

            strings = ["str_01", ["str_02", "str_03"], ("str_04", "str_05")]

            new_tuple = CollectionUtils.flat_map_to_tuple(strings)

            print(new_tuple)
            # ("str_01", "str_02", "str_03", "str_04", "str_05")
        """
        return tuple(
            chain.from_iterable(
                map(
                    lambda elem: [elem] if isinstance(elem, str) else elem,
                    str_iterable,
                )
            )
        )
