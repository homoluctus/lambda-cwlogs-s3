class ExportToS3Error(Exception):
    """S3へのエスクポートが失敗した場合の例外"""


class GetExportTaskError(Exception):
    """S3へのエクスポートタスクの取得失敗時の例外"""


class ExportToS3Failure(Exception):
    """S3へのエクスポート失敗"""
