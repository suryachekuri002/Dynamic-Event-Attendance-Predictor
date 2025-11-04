from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import joblib
import numpy as np
import pandas as pd
import warnings
from sklearn.exceptions import InconsistentVersionWarning

warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

app = Flask(__name__)
app.secret_key = "secret123"

# --- Load models / preprocessors ---
model = joblib.load("models/rf_model.pkl")
ohe = joblib.load("models/ohe_encoder.pkl")
scaler = joblib.load("models/scaler.pkl")

# Load dataset containing death_count and event_date
try:
    df = pd.read_csv("Data/event_dataset.csv")
    # Ensure event_date parsed as datetime (coerce errors)
    if "event_date" in df.columns:
        df["event_date"] = pd.to_datetime(df["event_date"], errors="coerce")
    else:
        # If event_date missing, create NaT column so code still runs
        df["event_date"] = pd.NaT
except Exception as e:
    # If dataset loading fails, create an empty df with expected columns
    print("Warning: Could not load event_dataset.csv:", e)
    df = pd.DataFrame(columns=[
        "venue_city", "sub_event_type", "death_count", "event_date"
    ])

# --- Routes ---
@app.route('/home')
def home_page():
    return render_template('Home.html')


@app.route('/About')
def about_page():
    return render_template('About.html')


@app.route('/Contact')
def contact_page():
    return render_template('contact.html')


@app.route('/contact', methods=['POST'])
def send_contact_message():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Prepare email
    subject = f"📩 New Contact Message from {name}"
    body = f"""
    You received a new message from the DYNATT Contact Form:

    👤 Name: {name}
    📧 Email: {email}

    💬 Message:
    {message}
    """

    # Gmail account credentials (as in your original file)
    sender_email = "suryachekuri119@gmail.com"
    receiver_email = "suryachekuri119@gmail.com"
    password = "hqre liec qyye fxlf"

    try:
        # Creating email structure
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Send mail via Gmail SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.send_message(msg)

        flash("Your message has been sent successfully!", "success")
    except Exception as e:
        print("Email sending error:", e)
        flash("Sorry, there was a problem sending your message. Please try again.", "danger")

    return redirect(url_for('contact_page'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return render_template('index.html')

    # Getting form inputs
    event_type = request.form.get('event', '').strip()
    sub_event_type = request.form.get('type', '').strip()
    venue_city = request.form.get('city', '').strip()
    weekday = request.form.get('day', '').strip()
    month = request.form.get('month', '').strip()
    weather = request.form.get('weather', '').strip()
    season = request.form.get('season', '').strip()

    def safe_float(value, default=0.0):
        try:
            return float(value)
        except (ValueError, TypeError):
            return default

    venue_capacity = safe_float(request.form.get('capacity'))
    ticket_price = safe_float(request.form.get('ticketprice'))
    avg_past_attendance = safe_float(request.form.get('avg_past_attendance'))

    try:
        is_holiday = int(request.form.get('is_holiday', 0))
    except (ValueError, TypeError):
        is_holiday = 0

    try:
        is_weekend = int(request.form.get('is_weekend', 0))
    except (ValueError, TypeError):
        is_weekend = 0

    # Preparing input data
    data = pd.DataFrame([{
        'event_type': event_type,
        'sub_event_type': sub_event_type,
        'venue_city': venue_city,
        'venue_capacity': venue_capacity,
        'season': season,
        'weather': weather,
        'ticket_price': ticket_price,
        'weekday': weekday,
        'month': month,
        'is_holiday': is_holiday,
        'is_weekend': is_weekend,
        'avg_past_attendance': avg_past_attendance
    }])

    # Transforming categorical and numerical features
    cat_features = ['event_type', 'sub_event_type', 'venue_city', 'season', 'weather', 'weekday', 'month']
    num_features = ['venue_capacity', 'ticket_price', 'avg_past_attendance']
    normal=data[['is_holiday', 'is_weekend']]
    # Transforming categorical
    X_cat = ohe.transform(data[cat_features])
    if hasattr(X_cat, "toarray"):
        X_cat = X_cat.toarray()

    # Transforming numerical
    X_num = scaler.transform(data[num_features])
    # Combining both
    X_final = np.concatenate([X_num,normal, X_cat], axis=1)

    # Predicting attendance
    predicted_attendance = float(model.predict(X_final)[0])
    # Ensure prediction is non-negative and not more than capacity
    if isinstance(venue_capacity, (int, float)) and venue_capacity > 0:
        predicted_attendance = max(0, min(predicted_attendance, venue_capacity))
    else:
        predicted_attendance = max(0, predicted_attendance)

    # ---- Death Count Logic: case-insensitive match and require death_count >= 1 ----
    city_lower = venue_city.strip().lower()
    sub_event_lower = sub_event_type.strip().lower()

    # If df has columns, perform filtering; else set zeros
    if not df.empty and 'venue_city' in df.columns and 'sub_event_type' in df.columns and 'death_count' in df.columns:
        # Lowercase comparison - do not modify original df
        mask_city = df['venue_city'].fillna('').astype(str).str.lower() == city_lower
        mask_sub = df['sub_event_type'].fillna('').astype(str).str.lower() == sub_event_lower
        mask_death = pd.to_numeric(df['death_count'], errors='coerce').fillna(0) >= 1

        filtered_df = df[mask_city & mask_sub & mask_death].copy()
    else:
        filtered_df = pd.DataFrame(columns=['venue_city', 'sub_event_type', 'death_count', 'event_date'])

    if not filtered_df.empty:
        # Ensure death_count numeric
        filtered_df['death_count'] = pd.to_numeric(filtered_df['death_count'], errors='coerce').fillna(0).astype(int)

        total_deaths = int(filtered_df['death_count'].sum())
        count_records = int(filtered_df.shape[0])
        avg_deaths = float(filtered_df['death_count'].mean())
        max_deaths = int(filtered_df['death_count'].max())
        min_deaths = int(filtered_df['death_count'].min())

        # Latest 5 incidents by event_date. If event_date is NaT, those rows go to the bottom.
        if 'event_date' in filtered_df.columns:
            # Sort descending, NaT will be last by default when na_position='last'
            recent = filtered_df.sort_values(by='event_date', ascending=False).head(5)
        else:
            recent = filtered_df.head(5)

        # Build recent incidents list with only: city, sub_event_type, death_count
        recent_incidents = []
        for _, r in recent.iterrows():
            recent_incidents.append({
                "city": str(r.get('venue_city', '')).strip(),
                "sub_event_type": str(r.get('sub_event_type', '')).strip(),
                "death_count": int(r.get('death_count', 0))
            })
    else:
        total_deaths = 0
        count_records = 0
        avg_deaths = 0.0
        max_deaths = 0
        min_deaths = 0
        recent_incidents = []

    # Redirecting to result page carrying all values
    return redirect(url_for(
        'result',
        attendance=predicted_attendance,
        capacity=venue_capacity,
        event_type=event_type,
        sub_event_type=sub_event_type,
        city=venue_city,
        season=season,
        weather=weather,
        weekday=weekday,
        month=month,
        ticket_price=ticket_price,
        avg_past_attendance=avg_past_attendance,
        total_deaths=total_deaths,
        count_records=count_records,
        avg_deaths=avg_deaths,
        max_deaths=max_deaths,
        min_deaths=min_deaths
    ))


@app.route('/result')
def result():
    # Primary prediction values
    attendance = float(request.args.get('attendance', 0))
    capacity = float(request.args.get('capacity', 0))

    # Event meta
    event_data = {
        "event_type": request.args.get("event_type", ""),
        "sub_event_type": request.args.get("sub_event_type", ""),
        "city": request.args.get("city", ""),
        "season": request.args.get("season", ""),
        "weather": request.args.get("weather", ""),
        "weekday": request.args.get("weekday", ""),
        "month": request.args.get("month", ""),
        "ticket_price": request.args.get("ticket_price", ""),
        "avg_past_attendance": request.args.get("avg_past_attendance", "")
    }

    # Death stats
    total_deaths = int(float(request.args.get("total_deaths", 0)))
    count_records = int(float(request.args.get("count_records", 0)))
    avg_deaths = float(request.args.get("avg_deaths", 0.0))
    max_deaths = int(float(request.args.get("max_deaths", 0)))
    min_deaths = int(float(request.args.get("min_deaths", 0)))

    # For recent incidents, we cannot pass complex list via query easily.
    city_lower = event_data["city"].strip().lower()
    sub_event_lower = event_data["sub_event_type"].strip().lower()

    recent_incidents = []
    if not df.empty and 'venue_city' in df.columns and 'sub_event_type' in df.columns and 'death_count' in df.columns:
        mask_city = df['venue_city'].fillna('').astype(str).str.lower() == city_lower
        mask_sub = df['sub_event_type'].fillna('').astype(str).str.lower() == sub_event_lower
        mask_death = pd.to_numeric(df['death_count'], errors='coerce').fillna(0) >= 1
        filtered_df = df[mask_city & mask_sub & mask_death].copy()

        if not filtered_df.empty:
            filtered_df['death_count'] = pd.to_numeric(filtered_df['death_count'], errors='coerce').fillna(0).astype(int)
            if 'event_date' in filtered_df.columns:
                recent = filtered_df.sort_values(by='event_date', ascending=False).head(5)
            else:
                recent = filtered_df.head(5)

            for _, r in recent.iterrows():
                recent_incidents.append({
                    "city": str(r.get('venue_city', '')).strip(),
                    "sub_event_type": str(r.get('sub_event_type', '')).strip(),
                    "death_count": int(r.get('death_count', 0))
                })

    # Render chart.html with all variables:
    return render_template(
        'chart.html',
        attendance=attendance,
        capacity=capacity,
        total_deaths=total_deaths,
        count_records=count_records,
        avg_deaths=avg_deaths,
        max_deaths=max_deaths,
        min_deaths=min_deaths,
        recent_incidents=recent_incidents,
        **event_data
    )


if __name__ == '__main__':
    app.run(debug=True)