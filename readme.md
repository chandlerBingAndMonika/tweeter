📄 Twitter Fetch & Monitor – Flow Overview
🎯 מטרה
המערכת מיועדת:

להוריד היסטוריה של ציוצים מחשבונות טוויטר (עד מגבלת ה־API).

לבצע ניטור שוטף לציוצים חדשים של אותם חשבונות.

לשמור נתונים בצורה מסודרת ב־PostgreSQL.

🛠 רכיבי המערכת
טבלאות עיקריות ב־PostgreSQL
tokens – פרטי טוקן (שם מפתח בסביבת ENV, סטטוס).

tokens_endpoint_rl – מגבלות Rate Limit לפי endpoint עבור כל טוקן.

users – פרטי משתמשי טוויטר (ID, שם, שם משתמש).

user_state – סטטוס מעקב (האם במעקב, מזהה הציוץ האחרון שנראה).

api_calls – לוג קריאות API (כולל זמן, endpoint, RL headers).

tweets – ציוצים שנאספו.

fetch_runs (אופציונלי) – תיעוד ריצות הורדה (batch-level).

🔄 זרימת הריצה
1️⃣ קבלת בקשה מהלקוח
הקלט:

json
Copy
Edit
[
  {
    "username": "elonmusk",
    "track_after": true,
    "fetch_mode": "full"
  },
  {
    "username": "nasa",
    "track_after": false,
    "fetch_mode": "limit:200"
  }
]
track_after – האם להוסיף את המשתמש למעקב שוטף.

fetch_mode – full להיסטוריה מלאה, או limit:N לעד N ציוצים אחרונים.

2️⃣ חלוקת המשימה
פיצול בזיכרון ליחידות עבודה של 50 ציוצים לכל קריאת API.

אין טבלת משימות ב־DB – הכל מתבצע בזיכרון/תור (in-memory / Redis).

3️⃣ בחירת טוקן זמין
בחירת טוקן לפי זמינות ב־tokens_endpoint_rl (לא חרג מהמגבלה).

עדיפות לטוקן עם זמן reset הקרוב ביותר.

4️⃣ קריאה ל־API
ביצוע קריאה ל־Twitter API עם הטוקן הנבחר.

תיעוד ב־api_calls (כולל RL headers).

קבלת עד 50 ציוצים בכל בקשה.

5️⃣ טיפול בתוצאה
אם הצליח:
שמירת הציוצים ב־tweets.

עדכון פרטי המשתמש ב־users.

עדכון user_state.last_seen_id.

עדכון סטטוס RL ב־tokens_endpoint_rl.

אם נכשל:
429 / Rate Limit – תזמון מחדש לפי זמן reset (בזיכרון).

401 / 403 – סימון הטוקן כ־invalid או revoked ב־tokens.

שגיאה זמנית – retry לאחר המתנה (בזיכרון).

6️⃣ מעקב שוטף
אם track_after = true:

user_state.is_tracked = true.

מנגנון polling / streaming מוסיף משימות חדשות כשמתגלים ציוצים חדשים.

📦 שמירת הטוקנים
ערכי הטוקן עצמם לא נשמרים ב־DB.

ב־tokens נשמר רק שם המפתח ב־ENV (למשל TWITTER_BEARER_1).

הטוקן בפועל נשמר ב־.env.

📊 ניהול Rate Limit
לכל קריאה מתעדכנים הערכים:

x-rate-limit-limit

x-rate-limit-remaining

x-rate-limit-reset

הנתונים נשמרים ב־tokens_endpoint_rl.

🚀 תהליך ההרצה
הפעלת הסקריפט הראשי (מקבל רשימת משתמשים).

פיצול המשימה לגושים של 50 ציוצים.

בחירת טוקנים פנויים.

ביצוע קריאות API ושמירה ב־DB.

עדכון מצב המעקב (אם נדרש).

📁 מבנה הקוד (רלוונטי ל־DB)
bash
Copy
Edit
careDataBase/models/
    00_enums.py
    01_tokens.py
    02_tokens_endpoint_rl.py
    03_users.py
    04_user_state.py
    05_api_calls.py
    06_tweets.py
    07_fetch_runs.py   (אופציונלי)