from django.db import models

class Student(models.Model):
    id = models.CharField(max_length=10, primary_key=True)  # รหัสนักเรียน
    name = models.CharField(max_length=100)  # ชื่อนักเรียน
    age = models.IntegerField()  # อายุ
    grade = models.CharField(max_length=10)  # ระดับชั้น
    email = models.EmailField(unique=True)  # อีเมล (ห้ามซ้ำ)

    def __str__(self):
        return f"{self.id} - {self.name}"

class Course(models.Model):
    id = models.AutoField(primary_key=True)  # ให้ Django กำหนดค่า id อัตโนมัติ
    name = models.CharField(max_length=100)  # ชื่อหลักสูตร
    description = models.TextField()  # รายละเอียดหลักสูตร
    created_at = models.DateTimeField(auto_now_add=True)  # เวลาที่สร้าง
    max_students = models.IntegerField(default=30)  # จำนวนสูงสุดของนักเรียนในหลักสูตร

    def __str__(self):
        return self.name

class CourseRegistration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='registrations')  # เพิ่ม related_name
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='registrations')  # เพิ่ม related_name
    date_registered = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')  # ป้องกันการลงทะเบียนซ้ำ

    def __str__(self):
        return f"{self.student.name} ลงทะเบียน {self.course.name}"
