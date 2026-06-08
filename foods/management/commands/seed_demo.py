from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from foods.models import Food
from reviews.models import Review

DEMO_PASSWORD = 'demopass123'

DEMO_USERS = [
    ('demo_amy', 'amy@example.com'),
    ('demo_ken', 'ken@example.com'),
    ('demo_lin', 'lin@example.com'),
]

DEMO_FOODS = [
    {
        'title': '鼎泰豐(信義店)',
        'category': 'chinese',
        'address': '台北市信義區市府路45號',
        'note': '小籠包皮薄餡多,18 摺工藝,湯汁飽滿;服務細緻,價格偏高但用餐體驗很好,適合招待客人。',
        'latitude': 25.0398, 'longitude': 121.5645,
        'owner': 'demo_amy',
        'reviews': [
            ('demo_ken', '5.0', '小籠包真的名不虛傳,湯汁超多,值得排隊!'),
            ('demo_lin', '4.5', '品質穩定,就是假日人潮多要等位。'),
        ],
    },
    {
        'title': '春水堂(概念店)',
        'category': 'drink',
        'address': '台北市信義區松高路19號',
        'note': '珍珠奶茶創始店,茶香濃、珍珠 Q 彈,甜度可調;座位舒適,也有提供簡餐。',
        'latitude': 25.0400, 'longitude': 121.5670,
        'owner': 'demo_ken',
        'reviews': [
            ('demo_amy', '4.5', '經典珍奶,茶味很夠,不會太甜。'),
            ('demo_lin', '4.0', '環境很好,價格稍高但可以接受。'),
        ],
    },
    {
        'title': '一蘭拉麵(本店)',
        'category': 'japanese',
        'address': '台北市中山區南京東路三段',
        'note': '豚骨湯頭濃郁,麵條軟硬可選,味玉入味;獨立座位適合一個人安靜用餐。',
        'latitude': 25.0520, 'longitude': 121.5440,
        'owner': 'demo_lin',
        'reviews': [
            ('demo_amy', '5.0', '湯頭一級棒,加麵也很佛心!'),
            ('demo_ken', '4.0', '味道很好,只是偏鹹,記得點清淡一點。'),
        ],
    },
    {
        'title': '莉莉水果店',
        'category': 'dessert',
        'address': '台南市中西區府前路一段199號',
        'note': '台南老字號冰品,芒果牛奶冰料多實在,水果新鮮;夏天必訪,價格親民。',
        'latitude': 22.9908, 'longitude': 120.2040,
        'owner': 'demo_amy',
        'reviews': [
            ('demo_ken', '4.0', '芒果冰好吃,份量大,兩個人share剛好。'),
            ('demo_lin', '5.0', '古早味滿滿,水果超新鮮,CP 值高!'),
        ],
    },
    {
        'title': '韓姨家常料理',
        'category': 'korean',
        'address': '台北市大安區忠孝東路四段',
        'note': '道地韓式家常菜,部隊鍋料多湯濃,小菜免費續;適合朋友聚餐,份量足。',
        'latitude': 25.0418, 'longitude': 121.5540,
        'owner': 'demo_ken',
        'reviews': [
            ('demo_amy', '3.5', '味道不錯,但店面較小,尖峰時段要等。'),
            ('demo_lin', '4.5', '部隊鍋很夠味,小菜也好吃!'),
        ],
    },
    {
        'title': '貳樓餐廳 Second Floor',
        'category': 'western',
        'address': '台北市大安區敦化南路一段',
        'note': '美式早午餐與義大利麵選擇多,鬆餅鬆軟、咖啡順口;空間明亮適合拍照打卡。',
        'latitude': 25.0445, 'longitude': 121.5495,
        'owner': 'demo_lin',
        'reviews': [
            ('demo_amy', '4.0', '早午餐選擇多,鬆餅好吃,假日要訂位。'),
            ('demo_ken', '4.5', '環境舒服,份量足,聚餐首選。'),
        ],
    },
]

class Command(BaseCommand):
    help = '建立示範用種子資料(使用者、美食、評論),方便展示與截圖。'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='先清除所有示範資料(demo_ 開頭使用者及其美食/評論)再重建。',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options['clear']:
            deleted, _ = User.objects.filter(username__startswith='demo_').delete()
            self.stdout.write(self.style.WARNING(f'已清除示範資料(含關聯共 {deleted} 筆物件)。'))

        users = {}
        for username, email in DEMO_USERS:
            user, created = User.objects.get_or_create(
                username=username, defaults={'email': email}
            )
            if created:
                user.set_password(DEMO_PASSWORD)
                user.save(update_fields=['password'])
            users[username] = user
            self.stdout.write(('  ＋ 建立' if created else '  ・ 已存在') + f' 使用者 {username}')

        food_created = review_created = 0
        for data in DEMO_FOODS:
            owner = users[data['owner']]
            food, created = Food.objects.get_or_create(
                title=data['title'],
                user=owner,
                defaults={
                    'category': data['category'],
                    'address': data['address'],
                    'note': data['note'],
                    'latitude': data['latitude'],
                    'longitude': data['longitude'],
                },
            )
            if created:
                food_created += 1
            self.stdout.write(('  ＋ 建立' if created else '  ・ 已存在') + f' 美食「{food.title}」')

            for reviewer_name, rating, content in data['reviews']:
                _, r_created = Review.objects.get_or_create(
                    food=food,
                    user=users[reviewer_name],
                    defaults={'rating': Decimal(rating), 'content': content},
                )
                if r_created:
                    review_created += 1

        self.stdout.write(self.style.SUCCESS(
            f'\n完成!示範帳號密碼皆為「{DEMO_PASSWORD}」。'
            f'\n本次新增:美食 {food_created} 筆、評論 {review_created} 則。'
            f'\n(可用 demo_amy / demo_ken / demo_lin 登入展示)'
        ))
