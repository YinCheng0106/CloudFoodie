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
    """組出 Google 地圖內嵌網址與開啟連結(T026/T027)。

    定位優先序:有填精確座標就用座標,否則用地址讓 Google 自動定位;
    兩者皆無則回傳空字串(詳細頁不顯示地圖)。地址含中文/空白需先 URL 編碼。
    有設定金鑰時使用官方 Maps Embed API,未設定則退回免金鑰內嵌地圖。
    """
    if food.latitude is not None and food.longitude is not None:
        query = f'{food.latitude},{food.longitude}'  # 精確座標(選填覆蓋)
    elif food.address:
        query = food.address                          # 以地址自動定位(預設)
    else:
        return '', ''

    q = quote(query, safe=',')  # 保留座標逗號,其餘(地址中文/空白)編碼
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
    """首頁:顯示美食卡片並支援關鍵字 / 分類搜尋(T022~T024)。

    平均評分以 ORM 聚合一次算出(T020),避免每張卡片各查一次。
    """
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    foods = Food.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews'),
    )
    if query:
        foods = foods.filter(title__icontains=query)  # T022 依名稱關鍵字搜尋
    if category:
        foods = foods.filter(category=category)        # T023 依分類篩選

    return render(request, 'foods/home.html', {
        'foods': foods,
        'query': query,
        'selected_category': category,
        'categories': Food.CATEGORY_CHOICES,
        'is_searching': bool(query or category),
    })


def food_detail(request, pk):
    """美食詳細頁(T015):顯示評論列表(T019)與平均評分(T020)。"""
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
    """新增美食(T013):僅登入者可操作,建立者自動帶入目前使用者。"""
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
    """編輯美食(T016):僅限該筆美食的建立者。"""
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
    """刪除美食(T017):僅限建立者,需經確認頁以 POST 送出。"""
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
    """產生 Gemini AI 摘要(T029/T030):僅限建立者,以 POST 觸發後存回該筆美食。"""
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
