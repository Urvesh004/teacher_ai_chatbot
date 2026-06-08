from django.db.models import Sum

from .models import Student


class StudentService:

    # ==========================
    # DASHBOARD DATA
    # ==========================

    @staticmethod
    def get_total_students():
        return Student.objects.count()

    @staticmethod
    def get_total_fee_paid():
        return (
            Student.objects.aggregate(
                Sum("total_paid_fee")
            )["total_paid_fee__sum"]
            or 0
        )

    @staticmethod
    def get_total_pending_fee():
        return (
            Student.objects.aggregate(
                Sum("remaining_fee")
            )["remaining_fee__sum"]
            or 0
        )

    @staticmethod
    def get_pending_students_count():
        return Student.objects.filter(
            fee_status__iexact="Pending"
        ).count()

    @staticmethod
    def get_last_10_students():
        return Student.objects.order_by(
            "-id"
        )[:10]

    # ==========================
    # STUDENT LIST
    # ==========================

    @staticmethod
    def get_all_students():
        return Student.objects.all().order_by(
            "roll_no"
        )

    @staticmethod
    def search_students(search_text):

        return Student.objects.filter(
            name__icontains=search_text
        ).order_by("roll_no")

    @staticmethod
    def get_student_by_roll_no(roll_no):

        return Student.objects.filter(
            roll_no=roll_no
        ).first()

    # ==========================
    # FILTERS
    # ==========================

    @staticmethod
    def get_students_by_standard(std):

        return Student.objects.filter(
            std=std
        ).order_by("roll_no")

    @staticmethod
    def get_paid_students():

        return Student.objects.filter(
            fee_status__iexact="Paid"
        )

    @staticmethod
    def get_pending_students():

        return Student.objects.filter(
            fee_status__iexact="Pending"
        )

    # ==========================
    # ANALYTICS
    # ==========================

    @staticmethod
    def get_highest_fee_paid_student():

        return Student.objects.order_by(
            "-total_paid_fee"
        ).first()

    @staticmethod
    def get_highest_pending_fee_student():

        return Student.objects.order_by(
            "-remaining_fee"
        ).first()

    @staticmethod
    def get_class_wise_student_count():

        result = {}

        standards = Student.objects.values_list(
            "std",
            flat=True
        ).distinct()

        for std in standards:

            result[f"Std {std}"] = Student.objects.filter(
                std=std
            ).count()

        return result

    @staticmethod
    def get_class_wise_fee_collection():

        result = {}

        standards = Student.objects.values_list(
            "std",
            flat=True
        ).distinct()

        for std in standards:

            total = (
                Student.objects.filter(
                    std=std
                ).aggregate(
                    Sum("total_paid_fee")
                )["total_paid_fee__sum"]
                or 0
            )

            result[f"Std {std}"] = total

        return result