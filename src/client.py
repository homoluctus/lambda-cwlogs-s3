from dataclasses import InitVar, dataclass, field
from typing import Type

import boto3
from mypy_boto3_logs import CloudWatchLogsClient

from src.cwlogs import LogGroup
from src.exceptions import (
    ExportToS3Error, ExportToS3Failure, GetExportTaskError
)


@dataclass
class Exporter:
    region: InitVar[str]
    client: CloudWatchLogsClient = field(init=False)

    def __post_init__(self, region: str):
        self.client = boto3.client('logs', region_name=region)

    def export(self, target: Type[LogGroup]) -> str:
        """CloudWatch Logsの任意のロググループをS3へエクスポート

        Args:
            target (Type[LogGroup])

        Raises:
            ExportToS3Error

        Returns:
            str: CloudWatch Logs APIからのレスポンスに含まれるtaskId
        """

        try:
            response = self.client.create_export_task(
                **target.to_args())  # type: ignore
            return response['taskId']
        except Exception as err:
            raise ExportToS3Error(err)

    def get_export_progress(self, task_id: str) -> str:
        try:
            response = self.client.describe_export_tasks(taskId=task_id)
            status = response['exportTasks'][0]['status']['code']
            return status
        except Exception as err:
            raise GetExportTaskError(err)

    @classmethod
    def finishes(cls, status_code: str) -> bool:
        """エクスポートタスクが終了したかをステータスコードから判別する

        Args:
            status_code (str):
                describe_export_tasksのレスポンスに含まれるステータスコード

        Raises:
            ExportToS3Failure: ステータスコードがCANCELLEDかFAILEDの場合

        Returns:
            bool
        """

        uppercase_status_code = status_code.upper()

        if uppercase_status_code == 'COMPLETED':
            return True
        elif uppercase_status_code in ['CANCELLED', 'FAILED']:
            raise ExportToS3Failure('S3へのエクスポート失敗')
        return False
