from django.shortcuts import render, redirect
from school.forms import CreateSchoolForm
from school.models import School


def school_list(request):
    return render(request, 'school/list.html', {'list': School.objects.all()})


def school_create(request):
    form = CreateSchoolForm

    if request.method == 'POST':
        form = CreateSchoolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'school/create.html', context)


def school_update(request, pk):
    school = School.objects.get(id=pk)
    form = CreateSchoolForm(instance=school)

    if request.method == 'POST':
        form = CreateSchoolForm(request.POST, instance=school)
        if form.is_valid():
            form.save()
            return redirect('school-list')

    context = {'form': form}
    return render(request, 'school/update.html', context)


def school_delete(request, pk):
    school = School.objects.get(id=pk)

    if request.method == "POST":
        school.delete()
        return redirect('school-list')

    return render(request, 'school/delete.html', {'item': school})
