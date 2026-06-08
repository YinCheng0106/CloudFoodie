from urllib.parse import quote

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, redirect, render

from reviews.forms import ReviewForm

from .forms import FoodForm
from .gemini import GeminiError, generate_summary
from .models import Food

def _build_map_urls(food):
    if food.latitude is not None and food.longitude is not None:
        query = f'{food.latitude},{food.longitude}'
    elif food.address:
        query = food.address
    else:
        return '', ''

    q = quote(query, safe=',')
    if settings.GOOGLE_MAPS_API_KEY:
        embed_url = (
            'https://www.google.com/maps/embed/v1/place'
            f'?key={settings.GOOGLE_MAPS_API_KEY}&q={q}&zoom=16&language=zh-TW'
        )
    else:
        embed_url = f'https://maps.google.com/maps?q={q}&z=16&hl=zh-TW&output=embed'
    link_url = f'https://www.google.com/maps/search/?api=1&query={q}'
    return embed_url, link_url

def home(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    foods = Food.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews'),
    )
    if query:
        foods = foods.filter(title__icontains=query)
    if category:
        foods = foods.filter(category=category)

    return render(request, 'foods/home.html', {
        'foods': foods,
        'query': query,
        'selected_category': category,
        'categories': Food.CATEGORY_CHOICES,
        'is_searching': bool(query or category),
    })

def food_detail(request, pk):
    food = get_object_or_404(Food, pk=pk)
    reviews = food.reviews.select_related('user')
    stats = food.reviews.aggregate(avg=Avg('rating'), count=Count('id'))
    map_embed_url, map_link_url = _build_map_urls(food)
    return render(request, 'foods/detail.html', {
        'food': food,
        'reviews': reviews,
        'avg_rating': stats['avg'],
        'review_count': stats['count'],
        'review_form': ReviewForm(),
        'map_embed_url': map_embed_url,
        'map_link_url': map_link_url,
        'gemini_enabled': bool(settings.GEMINI_API_KEY),
    })

@login_required
def food_create(request):
    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES)
        if form.is_valid():
            food = form.save(commit=False)
            food.user = request.user
            food.save()
            messages.success(request, '美食新增成功!')
            return redirect('foods:detail', pk=food.pk)
    else:
        form = FoodForm()
    return render(request, 'foods/form.html', {
        'form': form,
        'page_title': '新增美食',
        'submit_label': '新增',
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    })

@login_required
def food_edit(request, pk):
    food = get_object_or_404(Food, pk=pk)
    if food.user != request.user:
        messages.error(request, '你沒有權限編輯這筆美食。')
        return redirect('foods:detail', pk=food.pk)

    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            form.save()
            messages.success(request, '美食已更新!')
            return redirect('foods:detail', pk=food.pk)
    else:
        form = FoodForm(instance=food)
    return render(request, 'foods/form.html', {
        'form': form,
        'page_title': '編輯美食',
        'submit_label': '儲存變更',
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    })

@login_required
def food_delete(request, pk):
    food = get_object_or_404(Food, pk=pk)
    if food.user != request.user:
        messages.error(request, '你沒有權限刪除這筆美食。')
        return redirect('foods:detail', pk=food.pk)

    if request.method == 'POST':
        food.delete()
        messages.success(request, '美食已刪除。')
        return redirect('foods:home')
    return render(request, 'foods/confirm_delete.html', {'food': food})

@login_required
def food_summary(request, pk):
    food = get_object_or_404(Food, pk=pk)
    if food.user != request.user:
        messages.error(request, '你沒有權限為這筆美食產生摘要。')
        return redirect('foods:detail', pk=food.pk)

    if request.method != 'POST':
        return redirect('foods:detail', pk=food.pk)

    if not food.note.strip():
        messages.error(request, '請先填寫個人筆記,再產生 AI 摘要。')
        return redirect('foods:detail', pk=food.pk)

    try:
        food.ai_summary = generate_summary(food.note)
        food.save(update_fields=['ai_summary'])
        messages.success(request, 'AI 摘要已產生!')
    except GeminiError as exc:
        messages.error(request, f'產生摘要失敗:{exc}')
    return redirect('foods:detail', pk=food.pk)
