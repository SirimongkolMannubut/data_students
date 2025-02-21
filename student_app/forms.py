from django import forms
from django.core.exceptions import ValidationError
from .models import CourseRegistration, Course, Student

class StudentForm(forms.ModelForm):
    id = forms.CharField(label='ID นักเรียน', max_length=10)
    
    class Meta:
        model = Student
        fields = ['id', 'name', 'age', 'grade', 'email']

class StudentSearchForm(forms.Form):
    search_id = forms.CharField(required=True, label="ค้นหาจาก ID", max_length=10)  # เปลี่ยนเป็น CharField

class CourseRegistrationForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="เลือกหลักสูตร")

    class Meta:
        model = CourseRegistration
        fields = ['course']

    def __init__(self, *args, **kwargs):
        self.student = kwargs.pop('student', None)  # รับ student จาก kwargs
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        # เรียก method save() ของ model เพื่อสร้าง instance ของ CourseRegistration
        instance = super().save(commit=False)

        # กำหนด student จากฟอร์ม
        if self.student:
            instance.student = self.student  # กำหนด student ที่ลงทะเบียน

        # ตรวจสอบจำนวนผู้ลงทะเบียนของหลักสูตร
        if instance.course.course_registration_set.count() >= instance.course.max_students:
            raise ValidationError(f"หลักสูตร {instance.course.name} เต็มแล้ว")  # ถ้าหลักสูตรเต็มแล้ว จะเกิด ValidationError

        # ถ้า commit เป็น True ก็จะบันทึกข้อมูลลงฐานข้อมูล
        if commit:
            instance.save()

        return instance
