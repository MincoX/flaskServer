""" celery 抽象任务
"""

from celery import Task
from logs import get_logger

logger = get_logger('celery_task')


class DebugTask(Task):
    abstract = True

    def on_success(self, res, task_id, args, kwargs):
        """
        任务执行成功时执行
        :param res:
        :param task_id:
        :param args:
        :param kwargs:
        :return:
        """
        logger.info(' 任务执行成功 '.center(100, '*'))

    def on_retry(self, exc, task_id, args, kwargs, error_info):
        """ 任务重试时执行，可以通过判断任务重复执行的次数，在这里进行控制重试策略
        注：第 1 次任务开始执行，也会执行此函数
        :param exc:
        :param task_id:
        :param args:
        :param kwargs:
        :param error_info:
        :return:
        """
        retries = self.request.retries
        logger.info(f' task_retry >>> 第 {retries} 次任务重试 '.center(100, '*')) if retries != 0 else ''

    def on_failure(self, exc, task_id, args, kwargs, error_info):
        """
        任务失败时执行
        :param exc:
        :param task_id:
        :param args:
        :param kwargs:
        :param error_info:
        :return:
        """
        logger.info(' 任务执行失败 '.center(100, '*'))

    def after_return(self, *args, **kwargs):
        """ Handler called after the task returns.
        当函数 return 时执行，对于失败任务，在任务失败之后再执行
        :param args:
        :param kwargs:
        :return:
        """
        logger.info(' Task returned: {0!r} '.format(self.request))
