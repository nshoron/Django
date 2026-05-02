from django.shortcuts import render, redirect, get_object_or_404
from .models import Student

# CREATE + READ
def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        Student.objects.create(name=name, age=age)
        return redirect('home')

    students = Student.objects.all()
    return render(request, 'home.html', {'students': students})


# UPDATE
def update_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        student.name = request.POST.get('name')
        student.age = request.POST.get('age')
        student.save()
        return redirect('home')

    return render(request, 'update.html', {'student': student})


# DELETE
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect('home')