from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from django.db import transaction

from .models import TagProposal


@shared_task(name="apps.projectmanage.tasks.purge_old_tag_proposals")
def purge_old_tag_proposals(days_rejected_canceled: int = 30, days_approved: int = 180) -> dict:
    """
    定期清理历史标签申请记录，减少表数据量。
    - 清理已拒绝/已取消且超期的申请（默认 30 天前）
    - 清理已通过且已落地（final_tag 不为空）且超期的申请（默认 180 天前）

    可通过 Celery 调度定期执行。
    返回删除统计信息，便于监控。
    """
    now = timezone.now()
    cutoff_rej = now - timedelta(days=days_rejected_canceled)
    cutoff_appr = now - timedelta(days=days_approved)

    with transaction.atomic():
        qs_rej = TagProposal.objects.filter(
            status__in=[TagProposal.Status.REJECTED, TagProposal.Status.CANCELED],
            update_time__lt=cutoff_rej,
        )
        del_rej, _ = qs_rej.delete()

        qs_appr = TagProposal.objects.filter(
            status=TagProposal.Status.APPROVED,
            final_tag__isnull=False,
            approved_time__lt=cutoff_appr,
        )
        del_appr, _ = qs_appr.delete()

    return {
        "deleted_rejected_canceled": del_rej,
        "deleted_approved": del_appr,
        "cutoff_rejected_canceled": cutoff_rej.isoformat(),
        "cutoff_approved": cutoff_appr.isoformat(),
    }
