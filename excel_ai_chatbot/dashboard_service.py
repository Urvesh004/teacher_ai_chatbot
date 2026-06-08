from django.db.models import Sum

from .models import Student


def dashboard_summary():

    total_students = Student.objects.count()

    total_fee_paid = (
        Student.objects.aggregate(
            Sum("total_paid_fee")
        )["total_paid_fee__sum"]
        or 0
    )

    total_fee_pending = (
        Student.objects.aggregate(
            Sum("remaining_fee")
        )["remaining_fee__sum"]
        or 0
    )

    pending_students = Student.objects.filter(
        fee_status__iexact="Pending"
    ).count()

    paid_students = Student.objects.filter(
        fee_status__iexact="Paid"
    ).count()

    last_10_students = Student.objects.order_by(
        "-id"
    )[:10]

    return {
        "total_students": total_students,
        "total_fee_paid": total_fee_paid,
        "total_fee_pending": total_fee_pending,
        "pending_students": pending_students,
        "paid_students": paid_students,
        "last_10_students": last_10_students,
    }