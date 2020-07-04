from datetime import datetime, timedelta


def get_yesterday(fmt: str = "%Y%m%d") -> str:
    """フォーマットされた前日の日付を取得

    Args:
        fmt (str, optional): Defaults to "%Y%m%d".

    Returns:
        str: fmtに従った前日の日付
    """

    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime(fmt)


def get_specific_time_on_yesterday(
        *, hour: int = 0, minute: int = 0, second: int = 0) -> int:
    """
    前日の特定の日時のタイムスタンプを取得する
    タイムスタンプの単位はミリ秒である

    Args:
        hour (int, optional): Defaults to 0
        minute (int, optional): Defaults to 0
        second (int, optional): Defaults to 0

    Returns:
        int: 単位がミリ秒のタイムスタンプ
    """

    yesterday = datetime.today() - timedelta(days=1)
    start_time = yesterday.replace(hour=hour, minute=minute, second=second)
    timestamp = int(start_time.timestamp()) * 1000
    return timestamp
