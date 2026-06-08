from django.db.models import Sum
from .models import Student


def process_query(message):
    message = message.lower().strip()

    # ==================================
    # GREETING
    # ==================================
    if message in ["hi", "hello", "hey"]:
        return "Hello Teacher 👋\n\nHow can I help you today?\nType 'Help' to see all available commands."

    # ==================================
    # HELP (check early so it doesn't get caught by other keywords)
    # ==================================
    if "help" in message:
        return (
            "📖 Available Commands:\n\n"
            "• Total Students\n"
            "• Total Fee Paid\n"
            "• Total Pending Fee\n"
            "• Pending Student Count\n"
            "• Pending Students\n"
            "• Paid Students\n"
            "• Highest Remaining Fee\n"
            "• Lowest Remaining Fee\n"
            "• Last 10 Students\n"
            "• Roll No 101\n"
            "• Student Rahul\n"
            "• Std 10 / Class 10"
        )

    # ==================================
    # TOTAL STUDENTS
    # ==================================
    if "total students" in message or "student count" in message:
        total = Student.objects.count()
        return f"👨‍🎓 Total Students: {total}"

    # ==================================
    # TOTAL FEE PAID
    # ==================================
    elif "total fee paid" in message or "fee paid" in message:
        total = Student.objects.aggregate(Sum("total_paid_fee"))["total_paid_fee__sum"] or 0
        return f"💰 Total Fee Paid: ₹{total:,.2f}"

    # ==================================
    # TOTAL PENDING FEE
    # ==================================
    elif "pending fee" in message or "total pending fee" in message:
        total = Student.objects.aggregate(Sum("remaining_fee"))["remaining_fee__sum"] or 0
        return f"📋 Total Pending Fee: ₹{total:,.2f}"

    # ==================================
    # PENDING STUDENT COUNT  (must be before "pending students")
    # ==================================
    elif "pending student count" in message:
        count = Student.objects.filter(fee_status__iexact="Pending").count()
        return f"⚠ Pending Students: {count}"

    # ==================================
    # PENDING STUDENTS
    # ==================================
    elif "pending students" in message:
        students = Student.objects.filter(fee_status__iexact="Pending")
        if not students.exists():
            return "✅ No pending students found."
        names = [s.name for s in students[:20]]
        return f"⚠ Pending Students ({students.count()}):\n\n" + "\n".join(f"• {n}" for n in names)

    # ==================================
    # PAID STUDENTS
    # ==================================
    elif "paid students" in message:
        students = Student.objects.filter(fee_status__iexact="Paid")
        if not students.exists():
            return "No paid students found."
        names = [s.name for s in students[:20]]
        return f"✅ Paid Students ({students.count()}):\n\n" + "\n".join(f"• {n}" for n in names)

    # ==================================
    # HIGHEST REMAINING FEE
    # ==================================
    elif "highest remaining fee" in message:
        student = Student.objects.order_by("-remaining_fee").first()
        if not student:
            return "No student data found."
        return (
            f"🏆 {student.name}\n"
            f"Roll No: {student.roll_no}\n"
            f"Remaining Fee: ₹{student.remaining_fee:,.2f}"
        )

    # ==================================
    # LOWEST REMAINING FEE
    # ==================================
    elif "lowest remaining fee" in message:
        student = Student.objects.order_by("remaining_fee").first()
        if not student:
            return "No student data found."
        return (
            f"🎯 {student.name}\n"
            f"Roll No: {student.roll_no}\n"
            f"Remaining Fee: ₹{student.remaining_fee:,.2f}"
        )

    # ==================================
    # LAST 10 STUDENTS
    # ==================================
    elif "last 10 students" in message:
        students = Student.objects.order_by("-id")[:10]
        if not students:
            return "No student data found."
        result = [f"{s.roll_no} - {s.name}" for s in students]
        return "📑 Last 10 Students\n\n" + "\n".join(result)

    # ==================================
    # SEARCH BY ROLL NO
    # ==================================
    elif "roll no" in message or "roll" in message:
        digits = "".join(filter(str.isdigit, message))
        if not digits:
            return "Please provide a Roll Number. Example: Roll No 101"
        roll_no = int(digits)
        student = Student.objects.filter(roll_no=roll_no).first()
        if not student:
            return f"❌ No student found with Roll No {roll_no}."
        return (
            f"👨‍🎓 {student.name}\n"
            f"Roll No: {student.roll_no}\n"
            f"Std: {student.std}\n"
            f"Fee Status: {student.fee_status}\n"
            f"Paid Fee: ₹{student.total_paid_fee:,.2f}\n"
            f"Remaining Fee: ₹{student.remaining_fee:,.2f}"
        )

    # ==================================
    # CLASS / STANDARD SEARCH  (before "student" to avoid conflict)
    # ==================================
    elif "std" in message or "class" in message:
        digits = "".join(filter(str.isdigit, message))
        if not digits:
            return "Please provide a class number. Example: Std 10"
        std = digits
        students = Student.objects.filter(std=std)
        if not students.exists():
            return f"No students found in Std {std}."
        names = [s.name for s in students[:20]]
        return f"🏫 Std {std} Students ({students.count()}):\n\n" + "\n".join(f"• {n}" for n in names)

    # ==================================
    # SEARCH BY NAME
    # ==================================
    elif "student" in message:
        search_text = message.replace("student", "").strip()
        if not search_text:
            return "Please provide a student name. Example: Student Rahul"
        student = Student.objects.filter(name__icontains=search_text).first()
        if not student:
            return f"❌ No student found matching '{search_text}'."
        return (
            f"👨‍🎓 {student.name}\n"
            f"Roll No: {student.roll_no}\n"
            f"Std: {student.std}\n"
            f"Fee Status: {student.fee_status}\n"
            f"Paid Fee: ₹{student.total_paid_fee:,.2f}\n"
            f"Remaining Fee: ₹{student.remaining_fee:,.2f}"
        )

    # ==================================
    # DEFAULT
    # ==================================
    return (
        "🤖 I didn't understand that question.\n\n"
        "Type 'Help' to view available commands."
    )
