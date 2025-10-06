from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from django.db import transaction

from .models import TagProposal, TagProposalEvent


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

    archived_rej = 0
    archived_appr = 0
    with transaction.atomic():
        # 软归档：拒绝/取消，超期
        qs_rej = TagProposal.objects.select_for_update().filter(
            archived_at__isnull=True,
            status__in=[TagProposal.Status.REJECTED, TagProposal.Status.CANCELED],
            update_time__lt=cutoff_rej,
        )
        for p in qs_rej:
            p.archived_at = now
            p.archived_reason = f"auto_archive_rejected_canceled_older_than_{days_rejected_canceled}_days"
            p.save(update_fields=["archived_at", "archived_reason", "update_time"])
            try:
                TagProposalEvent.objects.create(
                    proposal=p,
                    action=TagProposalEvent.Action.AUTO_ARCHIVED,
                    by_user=None,
                    comment=p.archived_reason or "",
                    snapshot_name=p.name,
                    snapshot_final_tag=p.final_tag,
                )
            except Exception:
                pass
            archived_rej += 1

        # 软归档：已通过且已落地，超期
        qs_appr = TagProposal.objects.select_for_update().filter(
            archived_at__isnull=True,
            status=TagProposal.Status.APPROVED,
            final_tag__isnull=False,
            approved_time__lt=cutoff_appr,
        )
        for p in qs_appr:
            p.archived_at = now
            p.archived_reason = f"auto_archive_approved_older_than_{days_approved}_days"
            p.save(update_fields=["archived_at", "archived_reason", "update_time"])
            try:
                TagProposalEvent.objects.create(
                    proposal=p,
                    action=TagProposalEvent.Action.AUTO_ARCHIVED,
                    by_user=None,
                    comment=p.archived_reason or "",
                    snapshot_name=p.name,
                    snapshot_final_tag=p.final_tag,
                )
            except Exception:
                pass
            archived_appr += 1

    return {
        "archived_rejected_canceled": archived_rej,
        "archived_approved": archived_appr,
        "cutoff_rejected_canceled": cutoff_rej.isoformat(),
        "cutoff_approved": cutoff_appr.isoformat(),
    }
