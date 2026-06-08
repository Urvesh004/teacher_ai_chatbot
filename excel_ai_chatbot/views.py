import io
import pandas as pd
from django.db.models import Count, Sum
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Student, ExcelUpload, ChatHistory
from .forms import StudentForm, CustomUser
from .student_service import StudentService
from .chatbot_engine import process_query
from django.contrib.auth.decorators import login_required


def home_view(request):
    return render(request, "excel_ai_chatbot/home.html")


# DASHBOARD
@login_required
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

    return render(request, "excel_ai_chatbot/dashboard.html", context)


# EXCEL UPLOAD
@login_required
def upload_excel_view(request):

    if request.method == "POST":

        try:

            excel_file = request.FILES.get("excel_file")

            if not excel_file:

                messages.error(request, "Please select an Excel file.")

                return redirect("upload_excel")

            # Read file bytes
            file_bytes = excel_file.read()

            # Reset stream before saving
            excel_file.seek(0)

            # Save upload record
            upload = ExcelUpload.objects.create(file=excel_file)

            # Read Excel
            df = pd.read_excel(io.BytesIO(file_bytes), engine="openpyxl")

            required_columns = [
                "Roll No",
                "Name",
                "Std",
                "Fee Status",
                "Remaining Fee",
                "Total Paid Fee",
            ]

            missing = [col for col in required_columns if col not in df.columns]

            if missing:

                upload.delete()

                messages.error(request, f"Missing column(s): {', '.join(missing)}")

                return redirect("upload_excel")

            created = 0
            updated = 0

            for _, row in df.iterrows():

                student, is_created = Student.objects.update_or_create(
                    roll_no=row["Roll No"],
                    defaults={
                        "excel_file": upload,
                        "name": row["Name"],
                        "std": str(row["Std"]),
                        "fee_status": row["Fee Status"],
                        "remaining_fee": row["Remaining Fee"],
                        "total_paid_fee": row["Total Paid Fee"],
                    },
                )

                if is_created:
                    created += 1
                else:
                    updated += 1

            messages.success(
                request,
                f"Excel uploaded successfully! "
                f"{created} students added, "
                f"{updated} students updated.",
            )

            return redirect("dashboard")

        except Exception as e:

            messages.error(request, f"Upload Error: {str(e)}")

            return redirect("upload_excel")

    uploads = ExcelUpload.objects.order_by("-uploaded_at")

    return render(request, "excel_ai_chatbot/upload_excel.html", {"uploads": uploads})


# STUDENT LIST
@login_required
def student_list_view(request):
    search = request.GET.get("search", "")
    if search:
        students = StudentService.search_students(search)
    else:
        students = StudentService.get_all_students()
    return render(
        request,
        "excel_ai_chatbot/student_list.html",
        {"students": students, "search": search},
    )


# STUDENT DETAIL
@login_required
def student_detail_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, "excel_ai_chatbot/student_detail.html", {"student": student})


@login_required
def student_update_view(request, id):

    student = get_object_or_404(Student, id=id)

    if request.method == "POST":

        form = StudentForm(request.POST, instance=student)

        if form.is_valid():

            form.save()

            messages.success(request, "Student updated successfully.")

            return redirect("student_detail", student_id=student.id)

        else:

            print(form.errors)  # Debug

            messages.error(request, f"Form Error: {form.errors}")

    else:

        form = StudentForm(instance=student)

    return render(
        request,
        "excel_ai_chatbot/student_update.html",
        {
            "form": form,   
            "student": student,
        },
    )


# CHATBOT AJAX
@login_required
@require_POST  # BUG FIX: Only allow POST; returns 405 for GET instead of wrong JSON
def chatbot_view(request):
    try:
        message = request.POST.get("message", "").strip()
        if not message:
            return JsonResponse({"answer": "Please enter a message."})
        answer = process_query(message)
        ChatHistory.objects.create(question=message, answer=answer)
        return JsonResponse({"answer": answer})
    except Exception as e:
        return JsonResponse({"answer": f"⚠ Server error: {str(e)}"}, status=500)
