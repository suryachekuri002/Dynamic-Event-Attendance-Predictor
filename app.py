from flask import Flask, render_template, request, redirect, url_for,flash
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
app.secret_key = "secret123"  #it is needed for flash messages

# Loading model and preprocessors
model = joblib.load("rf_model.pkl")
ohe = joblib.load("ohe_encoder.pkl")
scaler = joblib.load("scaler.pkl")

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

    # Gmail account credentials
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
    event_type = request.form.get('event', '')
    sub_event_type = request.form.get('type', '')
    venue_city = request.form.get('city', '')
    weekday = request.form.get('day', '')
    month = request.form.get('month', '')
    weather = request.form.get('weather', '')
    season = request.form.get('season', '')

    def safe_float(value, default=0.0):
        try:
            return float(value)
        except ValueError:
            return default

    venue_capacity = safe_float(request.form.get('capacity'))
    ticket_price = safe_float(request.form.get('ticketprice'))
    avg_past_attendance = safe_float(request.form.get('avg_past_attendance'))

    is_holiday = int(request.form.get('is_holiday', 0))
    is_weekend = int(request.form.get('is_weekend', 0))

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
    num_features = ['venue_capacity', 'ticket_price', 'is_holiday', 'is_weekend', 'avg_past_attendance']

    # Transforming categorical
    X_cat = ohe.transform(data[cat_features])
    if hasattr(X_cat, "toarray"):
        X_cat = X_cat.toarray()

    # Transforming numerical
    X_num = scaler.transform(data[num_features])

    # Combining both
    X_final = np.concatenate([X_num, X_cat], axis=1)

    # Predicting attendance
    predicted_attendance = float(model.predict(X_final)[0])
    predicted_attendance = max(0, min(predicted_attendance, venue_capacity))
    
    # Redirecting to result page
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
    avg_past_attendance=avg_past_attendance
))

@app.route('/result')
def result():
    attendance = float(request.args.get('attendance', 0))
    capacity = float(request.args.get('capacity', 0))

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

    return render_template('chart.html', attendance=attendance, capacity=capacity, **event_data)



if __name__ == '__main__':
    app.run(debug=True)