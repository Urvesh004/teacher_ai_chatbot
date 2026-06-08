from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
import json
from functools import wraps

from excel_ai_chatbot.models import ExcelUpload, ChatHistory, CustomUser, Student
from .models import UserLog, SystemSettings

# ======================================
# AUTH DECORATOR — FIX: also checks is_authenticated
# ======================================


def superadmin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # BUG FIX: was commented out — unauthenticated users bypassed check
        if not request.user.is_authenticated:
            return redirect("login")

        if not hasattr(request.user, "role"):
            return redirect("login")

        if request.user.role != "superadmin":
            return redirect("dashboard")

        return view_func(request, *args, **kwargs)

    return wrapper


# ======================================
# DASHBOARD
# ======================================


@superadmin_required
def dashboard_view(request):

    students = Student.objects.all()

    # Statistics
    total_students = students.count()

    paid_students = students.filter(fee_status__iexact="Paid").count()

    pending_students = students.filter(fee_status__iexact="Pending").count()

    total_fee_paid = students.aggregate(total=Sum("total_paid_fee"))["total"] or 0

    total_fee_pending = students.aggregate(total=Sum("remaining_fee"))["total"] or 0

    # Last 10 Students
    last_students = students.order_by("-id")[:10]

    # Standard-wise Student Count
    standards = {}

    for student in students:

        std = str(student.std).strip()

        standards[std] = standards.get(std, 0) + 1

    # Sort Standards Numerically
    sorted_standards = sorted(
        standards.items(), key=lambda x: int(x[0]) if str(x[0]).isdigit() else 999
    )

    std_labels = [item[0] for item in sorted_standards]

    std_counts = [item[1] for item in sorted_standards]

    context = {
        # Cards
        "total_students": total_students,
        "paid_students": paid_students,
        "pending_students": pending_students,
        "total_users": CustomUser.objects.count(),
        "total_uploads": ExcelUpload.objects.count(),
        # Fee Charts
        "total_fee_paid": total_fee_paid,
        "total_fee_pending": total_fee_pending,
        # Standard Chart
        "std_labels": json.dumps(std_labels),
        "std_counts": json.dumps(std_counts),
        # Table
        "last_students": last_students,
    }

    return render(request, "admin_panel/dashboard.html", context)


# ======================================
# EXCEL SHEET LIST
# ======================================


@superadmin_required
def excel_sheet_list_view(request):
    search = request.GET.get("search", "")
    uploads = ExcelUpload.objects.order_by("-uploaded_at")

    if search:
        # BUG FIX: was file__icontains which searches the full file path object;
        # correct field is file__name (the actual filename string)
        uploads = uploads.filter(file__name__icontains=search)

    return render(
        request,
        "admin_panel/excel_sheet_list.html",
        {"uploads": uploads, "search": search},
    )


# ======================================
# DELETE EXCEL
# ======================================


@superadmin_required
def delete_excel_view(request, excel_id):

    excel = get_object_or_404(ExcelUpload, id=excel_id)

    if request.method == "POST":

        # Delete related students
        Student.objects.filter(excel_file=excel).delete()

        # Delete physical file
        if excel.file:
            excel.file.delete(save=False)

        # Delete upload record
        excel.delete()

        messages.success(
            request, "Excel file and related student records deleted successfully."
        )

    return redirect("admin_panel:excel_sheets")


# ======================================
# USER LIST
# ======================================


@superadmin_required
def user_list_view(request):
    search = request.GET.get("search", "")
    users = CustomUser.objects.all()

    if search:
        users = users.filter(username__icontains=search)

    return render(
        request, "admin_panel/user_list.html", {"users": users, "search": search}
    )


# ======================================
# EDIT USER
# ======================================


@superadmin_required
def edit_user_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        user.first_name = request.POST.get("first_name", "").strip()
        user.last_name = request.POST.get("last_name", "").strip()
        user.email = request.POST.get("email", "").strip()
        user.role = request.POST.get("role", "").strip()
        user.save()
        messages.success(request, "User updated successfully.")
        return redirect("admin_panel:users")

    return render(request, "admin_panel/edit_user.html", {"edit_user": user})


# ======================================
# DELETE USER
# ======================================


@superadmin_required
def delete_user_view(request, user_id):
    # BUG FIX: was using GET link — changed to POST-only for safety
    if request.method != "POST":
        return redirect("admin_panel:users")

    user = get_object_or_404(CustomUser, id=user_id)

    if user == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect("admin_panel:users")

    # BUG FIX: user.delete() was missing — user was never actually deleted!
    user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect("admin_panel:users")


# ======================================
# USER LOGS
# ======================================


@superadmin_required
def user_logs_view(request):
    search = request.GET.get("search", "")
    logs = UserLog.objects.order_by("-created_at")

    if search:
        logs = logs.filter(activity__icontains=search)

    return render(
        request, "admin_panel/user_logs.html", {"logs": logs, "search": search}
    )


# ======================================
# CHATBOT LOGS
# ======================================


@superadmin_required
def chatbot_logs_view(request):
    search = request.GET.get("search", "")
    logs = ChatHistory.objects.order_by("-created_at")

    if search:
        logs = logs.filter(question__icontains=search)

    return render(
        request, "admin_panel/chatbot_logs.html", {"logs": logs, "search": search}
    )


# ======================================
# SETTINGS
# ======================================


@superadmin_required
def settings_view(request):
    settings_obj, _ = SystemSettings.objects.get_or_create(id=1)

    if request.method == "POST":
        settings_obj.school_name = request.POST.get("school_name", "").strip()
        settings_obj.system_name = request.POST.get("system_name", "").strip()
        settings_obj.email = request.POST.get("email", "").strip()
        settings_obj.phone = request.POST.get("phone", "").strip()
        settings_obj.address = request.POST.get("address", "").strip()

        if request.FILES.get("logo"):
            settings_obj.logo = request.FILES["logo"]

        settings_obj.save()
        messages.success(request, "Settings updated successfully.")
        return redirect("admin_panel:settings")

    return render(request, "admin_panel/settings.html", {"settings": settings_obj})
