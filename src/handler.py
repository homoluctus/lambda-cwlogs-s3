from time import sleep
from typing import Any, Type

from src.client import Exporter
from src.cwlogs import LogGroup
from src.exceptions import GetExportTaskError
from src.log import get_logger


logger = get_logger(__name__)


def export_to_s3(exporter: Exporter, target: Type[LogGroup]) -> bool:
    task_id = exporter.export(target)
    logger.info(f'{target.log_group}をS3へエクスポート中 ({task_id=})')

    while True:
        status = exporter.get_export_progress(task_id)
        if exporter.finishes(status):
            return True
        sleep(5)


def main(event: Any, context: Any) -> bool:
    exporter = Exporter(region='ap-northeast-1')
    targets = LogGroup.__subclasses__()
    logger.info(f'エクスポート対象のロググループは{len(targets)}個')

    for target in targets:
        try:
            export_to_s3(exporter, target)
        except GetExportTaskError as err:
            logger.warning(err)
            logger.warning(f'{target.log_group}の進捗状況の取得失敗')
        except Exception as err:
            logger.error(err)
            logger.error(f'{target.log_group}のS3へエクスポート失敗')
        else:
            logger.info(f'{target.log_group}のS3へエクスポート完了')

    return True


if __name__ == '__main__':
    # ローカルテスト用
    main(None, None)
