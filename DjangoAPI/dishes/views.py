from django.shortcuts import render, get_object_or_404, redirect
from .models import Dish
from .forms import DishForm

def dish_list(request):
    dishes = Dish.objects.order_by('-priority', 'name')
    return render(request, 'dishes/dish_list.html', {'dishes': dishes})


def dish_create(request):
    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dish_list')
    else:
        form = DishForm()
    return render(request, 'dishes/dish_form.html', {'form': form, 'title': 'Додати страву'})


def dish_update(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES, instance=dish)
        if form.is_valid():
            form.save()
            return redirect('dish_list')
    else:
        form = DishForm(instance=dish)
    return render(request, 'dishes/dish_form.html', {'form': form, 'title': 'Редагувати страву'})


def dish_delete(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    if request.method == 'POST':
        dish.delete()
        return redirect('dish_list')
    return render(request, 'dishes/dish_confirm_delete.html', {'dish': dish})
