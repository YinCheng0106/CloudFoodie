# 雲端美食 Cloud Foodie

> 個人美食收藏與社群評論平台 — 「動態網頁開發」課程專案

以 Django 打造的美食收藏網站:使用者可註冊登入、收藏美食、上傳照片、瀏覽 Google 地圖位置、撰寫與閱讀評論評分,並可用 Gemini AI 為個人筆記產生摘要。整體採用深色玻璃擬態(Glassmorphism)介面。

---

## ✨ 功能特色

- 👤 **會員系統** — 註冊、登入、登出(Django 內建驗證,密碼 PBKDF2 雜湊)
- 🍜 **美食收藏** — 新增/檢視/編輯/刪除,支援照片上傳、分類、地址、個人筆記
- 🔍 **搜尋** — 依美食名稱與分類即時篩選(Django ORM 查詢)
- ⭐ **評論評分** — 1.0~5.0 星評分、平均分數聚合、多人評論同一美食
- 🗺️ **Google Maps** — 地址自動定位、地圖選點(Places 自動完成)、一鍵開啟 Google 地圖
- 🤖 **Gemini AI 摘要** — 依個人筆記自動產生繁體中文摘要
- 🔒 **安全** — CSRF 保護、輸入驗證、擁有者權限控管

---

## 🧱 技術堆疊

| 分層 | 技術 |
| --- | --- |
| 前端 | HTML5、CSS3、Bootstrap 5、原生 JavaScript |
| 後端 | Django 5.2(LTS)、Django ORM |
| 資料庫 | SQLite |
| 第三方 API | Google Maps API、Gemini API |
| 身分驗證 | Django Authentication |

---

## 📦 環境需求

- Python 3.11 以上(開發環境為 **Python 3.13**)
- pip / venv

主要套件(詳見 `requirements.txt`):

```
Django==5.2.15
pillow==12.2.0
```

---

## 🚀 安裝與啟動

### 1. 取得專案並建立虛擬環境

```bash
cd cloudFoodie

# 建立並啟用虛擬環境(macOS / Linux)
python3 -m venv .venv
source .venv/bin/activate

# Windows(PowerShell)
# python -m venv .venv
# .venv\Scripts\Activate.ps1
```

### 2. 安裝相依套件

```bash
pip install -r requirements.txt
```

### 3. 初始化資料庫

```bash
python manage.py migrate
```

### 4.(選用)建立管理員帳號

```bash
python manage.py createsuperuser
```

### 5. 啟動開發伺服器

```bash
python manage.py runserver
```

開啟瀏覽器前往 **http://127.0.0.1:8000/** 即可使用。

> ⚠️ 所有 Python 指令請在**已啟用的虛擬環境**(`.venv`)中執行。

---

## 🔑 環境變數設定(`.env`)

Google Maps 與 Gemini 屬加分功能,**未設定金鑰時會自動降級**:地圖改用免金鑰內嵌、AI 摘要功能隱藏,其餘頁面照常運作。金鑰一律從環境變數讀取,不寫死在程式碼中。

專案啟動時會由 [`python-dotenv`](https://pypi.org/project/python-dotenv/)(已列於 `requirements.txt`)自動載入專案根目錄的 `.env`,因此**只要把金鑰寫進 `.env` 即可,不必每次手動 `export`**。

### 可設定的變數

| 變數 | 用途 | 未設定時 |
| --- | --- | --- |
| `GOOGLE_MAPS_API_KEY` | 地圖選點、Places 自動完成、Embed 地圖 | 改用免金鑰內嵌地圖 |
| `GEMINI_API_KEY` | Gemini AI 摘要 | 隱藏 AI 摘要功能 |
| `GEMINI_MODEL` | 指定 Gemini 模型 | 預設 `gemini-2.5-flash`(免費額度友善) |

### 設定步驟

1. 由範本複製出自己的 `.env`(`.env.example` 為不含金鑰的範本,會進版控;`.env` 已列入 `.gitignore`,不會被提交):

   ```bash
   cp .env.example .env
   ```

2. 編輯 `.env`,填入你的金鑰(等號後直接接值,**不需引號**):

   ```dotenv
   GOOGLE_MAPS_API_KEY=你的_Google_Maps_金鑰
   GEMINI_API_KEY=你的_Gemini_金鑰
   GEMINI_MODEL=gemini-2.5-flash
   ```

3. **重新啟動**開發伺服器,讓新的 `.env` 生效:

   ```bash
   python manage.py runserver
   ```

> 💡 修改 `.env` 後一定要重啟伺服器才會套用。也可改用傳統 `export`(臨時測試),其優先序高於 `.env`:`export GEMINI_API_KEY="你的金鑰"`。

### 金鑰申請

- **Google Maps**:於 [Google Cloud Console](https://console.cloud.google.com/) 建立專案 → 啟用 **Maps JavaScript API**、**Places API**、**Maps Embed API** → 建立 API 金鑰。
- **Gemini**:於 [Google AI Studio](https://aistudio.google.com/app/apikey) 取得免費金鑰(`gemini-2.5-flash` 等 flash 系列模型免費額度即可使用)。

> ⚠️ **請勿**將真實金鑰寫進 `.env.example` 或提交 `.env`;金鑰僅應存在本機的 `.env` 或環境變數中。

---

## 🗂️ 專案結構

```
cloudFoodie/
├── cloudfoodie/          # 專案設定(settings、urls、wsgi)
├── users/                # 會員:註冊 / 登入 / 登出
├── foods/                # 美食:CRUD / 搜尋 / 地圖 / AI 摘要
│   └── gemini.py         #   Gemini API 串接
├── reviews/              # 評論:CRUD / 評分
├── templates/            # HTML 模板(依 app 分目錄)
│   ├── base.html
│   ├── users/  foods/  reviews/
├── static/css/main.css   # 深色主題 / 玻璃擬態樣式
├── media/                # 使用者上傳的照片
├── docs/PRESENTATION.md  # 簡報資料(ER 圖 / 路由圖 / JSON 範例 / 截圖清單)
├── db.sqlite3            # SQLite 資料庫
├── requirements.txt
└── manage.py
```

每個 app 皆包含 `models.py`、`views.py`、`urls.py`、`forms.py`、`admin.py`。

---

## 🧭 主要路由

| 路徑 | 說明 |
| --- | --- |
| `/` | 首頁 / 美食列表 / 搜尋 |
| `/foods/create/` | 新增美食(需登入) |
| `/foods/<id>/` | 美食詳細頁(地圖、評論、AI 摘要) |
| `/foods/<id>/edit/`、`/delete/` | 編輯 / 刪除(限擁有者) |
| `/users/register/`、`/login/`、`/logout/` | 註冊 / 登入 / 登出 |

> 完整路由表、ER 圖與資料模型請見 [`docs/PRESENTATION.md`](docs/PRESENTATION.md)。

---

## 🔐 安全設計

- **密碼雜湊** — Django 內建 PBKDF2,資料庫不存明文
- **CSRF 保護** — 所有 POST 表單皆帶 CSRF token
- **輸入驗證** — 評分 1.0~5.0、經緯度地理範圍、必填欄位、密碼強度驗證
- **權限控管** — `@login_required` + 擁有者檢查,無法存取他人資料

---

## 📝 資料模型摘要

| 模型 | 主要欄位 | 關聯 |
| --- | --- | --- |
| `User`(Django 內建) | username、email、password(雜湊) | 1:N → Food、Review |
| `Food` | title、category、address、note、image、latitude、longitude、ai_summary、created_at | 屬於 User;1:N → Review |
| `Review` | rating(1.0~5.0)、content、created_at | 屬於 User 與 Food |

---

## 📄 授權

本專案為大學「動態網頁開發」課程作業,僅供學習與展示用途。
