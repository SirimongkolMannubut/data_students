from django.shortcuts import render, get_object_or_404, redirect
from .forms import StudentForm, StudentSearchForm, CourseRegistrationForm
from .models import Student, Course, CourseRegistration


# ฟังก์ชันการลงทะเบียนคอร์ส
def register_course(request, student_id=None):
    student = None
    if student_id:
        student = get_object_or_404(Student, pk=student_id)  # หานักเรียนจาก ID

    if request.method == 'POST':
        form = CourseRegistrationForm(request.POST, student=student)  # ส่งข้อมูลนักเรียนไปยังฟอร์ม
        if form.is_valid():
            form.save()  # บันทึกข้อมูลการลงทะเบียน
            return redirect('registration_list')  # เปลี่ยนไปยังหน้ารายการการลงทะเบียน
    else:
        form = CourseRegistrationForm(student=student)  # ส่งข้อมูลนักเรียนไปยังฟอร์ม

    return render(request, 'register_course.html', {'form': form, 'student': student})


# ฟังก์ชันแสดงรายการการลงทะเบียน
def registration_list(request):
    registrations = CourseRegistration.objects.all()  # แสดงการลงทะเบียนทั้งหมด
    return render(request, 'registration_list.html', {'registrations': registrations})


# ฟังก์ชันค้นหานักเรียน
def student_search(request):
    search_form = StudentSearchForm(request.GET)
    students = []  # เริ่มต้นเป็นลิสต์ว่างสำหรับเก็บผลลัพธ์
    registrations = []  # เก็บการลงทะเบียนของนักเรียน

    if request.method == 'GET' and search_form.is_valid():
        search_id = search_form.cleaned_data.get('search_id')  # ดึง ID ที่กรอก

        # ค้นหาจาก ID
        if search_id:
            students = Student.objects.filter(id=search_id)

            # ดึงการลงทะเบียนของนักเรียน
            registrations = CourseRegistration.objects.filter(student__in=students)

    return render(request, 'student_search.html', {'form': search_form, 'students': students, 'registrations': registrations})


# หน้าแรก
def home(request):
    return render(request, 'home.html')


# แสดงรายชื่อนักเรียน
def student_list(request):
    search_id = request.GET.get('search_id')  # ดึงค่าจากฟอร์มค้นหานักเรียนที่กรอก ID

    if search_id:
        # ค้นหานักเรียนจาก ID
        students = Student.objects.filter(id=search_id)
    else:
        # หากไม่กรอก ID ให้แสดงรายชื่อนักเรียนทั้งหมด
        students = Student.objects.all()

    return render(request, 'student_list.html', {'students': students})


# แก้ไขข้อมูลนักเรียน
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        
        # ตรวจสอบ ID ซ้ำในระบบ
        student_id = request.POST.get('id')
        if student_id != str(student.id) and Student.objects.filter(id=student_id).exists():
            form.add_error('id', 'ID นี้มีอยู่ในระบบแล้ว')
            return render(request, 'student_form.html', {'form': form, 'student': student})
        
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_form.html', {'form': form})


# ลบนักเรียน
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'student_confirm_delete.html', {'student': student})


# สร้างนักเรียนใหม่
def student_create(request, pk=None):
    if pk:
        student = get_object_or_404(Student, pk=pk)
    else:
        student = None

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        student_id = request.POST.get('id')

        # ตรวจสอบว่า ID มีอยู่ในฐานข้อมูลหรือไม่
        if student_id and Student.objects.filter(id=student_id).exists() and not student:
            form.add_error('id', 'ID นี้มีอยู่ในระบบแล้ว')
            return render(request, 'student_form.html', {'form': form, 'student': student})

        if form.is_valid():
            form.save()
            return redirect('student_list')

    else:
        form = StudentForm(instance=student)

    return render(request, 'student_form.html', {'form': form, 'student': student})
