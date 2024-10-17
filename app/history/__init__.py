"""履歴管理パッケージ

Modules:
    dto: 履歴管理データオブジェクトモジュール
    service: 履歴管理サービスモジュール

Usage:
    履歴登録::

        from history.dto import HistoryDto
        from history.service import HistoryService

        history_service = HistoryService()
        history_service.register_history(HistoryDto.of("input", "output"))

    履歴一覧取得::

        from history.service import HistoryService

        history_service = HistoryService()
        for history in history_service.get_all_histories():
            print(history)
        # HistoryDto(request_id='24070100001', prompt_ja='input', html=... )
        # HistoryDto(request_id='24070100002', prompt_ja='input', html=... )
        # HistoryDto(request_id='24070100003', prompt_ja='input', html=... )
"""
