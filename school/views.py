from django.shortcuts import render, redirect

from school.forms import CreateSchoolForm
from school.models import School


def school_list(request):
    return render(request, 'school_list.html', {'list': School.objects.all()})


def school_create(request):

    form = CreateSchoolForm

    if request.method == 'POST':
        form = CreateSchoolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'school_create.html', context)


def school_update(request, pk):

    school = School.objects.get(id=pk)
    form = CreateSchoolForm(instance=school)

    if request.method == 'POST':
        form = CreateSchoolForm(request.POST, instance=school)
        if form.is_valid():
            form.save()
            return redirect('school-list')

    context = {'form': form}
    return render(request, 'school_update.html', context)


def school_delete(request, pk):

    school = School.objects.get(id=pk)

    if request.method == "DELETE":
        school.delete()
        return redirect('')

    return render(request, 'school_delete')



