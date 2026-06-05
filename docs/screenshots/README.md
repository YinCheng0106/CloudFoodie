# 截圖存放區

請把瀏覽器擷取的頁面截圖放在此資料夾,**檔名需與下表一致**,
`docs/PRESENTATION.md` §5.2 嵌入區即會自動顯示。

| 檔名 | 頁面 | 路徑 |
| --- | --- | --- |
| `01-home.png` | 首頁(列表) | `/` |
| `02-home-search.png` | 首頁(搜尋結果) | `/?q=拉麵&category=japanese` |
| `03-detail.png` | 美食詳細頁 | `/foods/<id>/` |
| `04-create.png` | 新增美食 | `/foods/create/` |
| `05-login.png` | 登入頁 | `/users/login/` |
| `06-register.png` | 註冊頁 | `/users/register/` |
| `07-reviews.png` | 評論系統(評論區) | `/foods/<id>/` |
| `08-ai-summary.png` | AI 摘要(加分) | `/foods/<id>/` |

## 快速步驟

```bash
source .venv/bin/activate
python manage.py seed_demo     # 建立示範資料,首頁才有滿版卡片
python manage.py runserver
```

1. 開啟 http://127.0.0.1:8000/,依上表逐頁擷取畫面。
2. 以 `demo_amy` / `demo_ken` / `demo_lin`(密碼 `demopass123`)登入,可截到擁有者專屬的「編輯/刪除」「產生 AI 摘要」。
3. 將圖片依檔名存進本資料夾(建議 `.png`)。
4. 開啟 `docs/PRESENTATION.md` 預覽,確認圖片正確顯示。

> macOS 區域截圖:**⌘ + Shift + 4**;視窗截圖:**⌘ + Shift + 4** 再按 **空白鍵**。
