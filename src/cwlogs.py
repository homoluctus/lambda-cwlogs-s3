from abc import ABCMeta
from typing import ClassVar, Dict, Union

from src.utils import get_specific_time_on_yesterday, get_yesterday


class LogGroup(object, metaclass=ABCMeta):
    """CloudWatch LogsをS3へエクスポートするための設定用基底クラス

    エクスポートするロググループの追加方法

    class Example(LogGroup):
        log_group = 'test'
    """

    # log_groupは必須でそれ以外はオプション
    log_group: ClassVar[str]

    log_stream: ClassVar[str] = ''
    start_time: ClassVar[int] = get_specific_time_on_yesterday(
        hour=0, minute=0, second=0)
    end_time: ClassVar[int] = get_specific_time_on_yesterday(
        hour=23, minute=59, second=59)
    dest_bucket: ClassVar[str] = 'lambda-cwlogs-s3'
    dest_obj_first_prefix: ClassVar[str] = ''
    dest_obj_final_prefix: ClassVar[str] = get_yesterday('%Y-%m-%d')

    @classmethod
    def get_dest_obj_prefix(cls) -> str:
        """完全なS3のobject prefixを取得

        S3の階層構造
        dest_bucket/dest_obj_first_prefix/dest_obj_final_prefix/*

        Returns:
            str
        """

        first_prefix = cls.dest_obj_first_prefix or cls.log_group
        return f'{first_prefix}/{cls.dest_obj_final_prefix}'

    @classmethod
    def to_args(cls) -> Dict[str, Union[str, int]]:
        args: Dict[str, Union[str, int]] = {
            'logGroupName': cls.log_group,
            'fromTime': cls.start_time,
            'to': cls.end_time,
            'destination': cls.dest_bucket,
            'destinationPrefix': cls.get_dest_obj_prefix()
        }

        if cls.log_stream:
            args['logStreamNamePrefix'] = cls.log_stream

        return args
