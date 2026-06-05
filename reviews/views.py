from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from foods.models import Food

from .forms import ReviewForm
from .models import Review


@login_required
def review_create(request, food_pk):
    """新增評論(T018):僅登入者可送出,評論者與所屬美食自動帶入。"""
    food = get_object_or_404(Food, pk=food_pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.food = food
            review.save()
            messages.success(request, '評論已送出,感謝你的分享!')
            return redirect('foods:detail', pk=food.pk)
    else:
        form = ReviewForm()
    # 驗證失敗時,改用獨立表單頁顯示錯誤訊息
    return render(request, 'reviews/form.html', {
        'form': form,
        'food': food,
        'page_title': '撰寫評論',
        'submit_label': '送出評論',
    })


@login_required
def review_edit(request, pk):
    """編輯評論(T021):僅限評論作者本人。"""
    review = get_object_or_404(Review, pk=pk)
    if review.user != request.user:
        messages.error(request, '你沒有權限編輯這則評論。')
        return redirect('foods:detail', pk=review.food.pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, '評論已更新!')
            return redirect('foods:detail', pk=review.food.pk)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'reviews/form.html', {
        'form': form,
        'food': review.food,
        'page_title': '編輯評論',
        'submit_label': '儲存變更',
    })


@login_required
def review_delete(request, pk):
    """刪除評論(T021):僅限作者本人,需以 POST 確認。"""
    review = get_object_or_404(Review, pk=pk)
    if review.user != request.user:
        messages.error(request, '你沒有權限刪除這則評論。')
        return redirect('foods:detail', pk=review.food.pk)

    food_pk = review.food.pk
    if request.method == 'POST':
        review.delete()
        messages.success(request, '評論已刪除。')
        return redirect('foods:detail', pk=food_pk)
    return render(request, 'reviews/confirm_delete.html', {'review': review})
