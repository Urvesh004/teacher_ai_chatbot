import pandas as pd

from .models import Student


def import_students_from_excel(excel_file):
    """
    Read Excel file and save students to database
    """

    df = pd.read_excel(excel_file)

    required_columns = [
        "Roll No",
        "Name",
        "Std",
        "Fee Status",
        "Remaining Fee",
        "Total Paid Fee",
    ]

    missing_columns = [
        col
        for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        return {
            "success": False,
            "message": f"Missing columns: {', '.join(missing_columns)}"
        }

    students_created = 0

    for _, row in df.iterrows():

        Student.objects.update_or_create(
    roll_no=row["Roll No"],
    defaults={
        "name": row["Name"],
        "std": row["Std"],
        "fee_status": row["Fee Status"],
        "remaining_fee": row["Remaining Fee"],
        "total_paid_fee": row["Total Paid Fee"],
    },
)

        students_created += 1

    return {
        "success": True,
        "message": f"{students_created} students imported successfully"
    }