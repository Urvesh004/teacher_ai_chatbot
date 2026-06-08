from django import forms
from .models import Student, CustomUser
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):

    class Meta:

        model = CustomUser

        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )

class ExcelUploadForm(forms.Form):

    excel_file = forms.FileField(
        label="Upload Excel File"
    )
    
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        # These fields must match exactly what you defined in your Student model
        fields = [
            'roll_no', 
            'name', 
            'std', 
            'fee_status', 
            'total_paid_fee', 
            'remaining_fee'
        ]
        
        # Optional: You can add specific HTML attributes (like placeholders or custom classes) here
        widgets = {
            'roll_no': forms.TextInput(attrs={'placeholder': 'Enter Roll Number'}),
            'name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'std': forms.TextInput(attrs={'placeholder': 'e.g., 10th, 12th Science'}),
            'fee_status': forms.Select(), # Assuming this is a CharField with 'choices' in your models.py
            'total_paid_fee': forms.NumberInput(attrs={'placeholder': '0'}),
            'remaining_fee': forms.NumberInput(attrs={'placeholder': '0'}),
        }