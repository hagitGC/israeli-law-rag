# התחל מתמונת בסיס של פייתון
FROM python:3.11-slim

# הגדר את ספריית העבודה בתוך הקונטיינר
WORKDIR /app

# העתק את קובץ הדרישות והתקן את החבילות
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# העתק את כל קוד המקור שלנו (התיקייה src)
COPY src/ ./src

# --- זה השלב החשוב ---
# העתק את מאגר הנתונים הווקטורי שבנינו באופן מקומי
COPY vectorstores/ ./vectorstores

# הגדר את הפקודה שתרוץ כשהקונטיינר יופעל
# (זו תהיה הפקודה שמפעילה את שרת הצ'אט שלך)
CMD ["python", "-m", "src.app.main"]