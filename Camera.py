import streamlit as st
import pandas as pd
import calendar
from datetime import date, datetime, timedelta

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Y2K Camera Rental", page_icon="💖", layout="centered")

# --- 2. DATA LOADING ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRjQW_nvu3CR0SZIPcPVs9eVXVDjJPMDUJeZUciKbnqABBzxGF6YJI_Fq09i-oemUur88KkoUoOF47R/pub?gid=0&single=true&output=csv"


@st.cache_data(ttl=60)
def load_bookings():
    try:
        df = pd.read_csv(SHEET_URL)
        df = df.iloc[:, :3]
        df.columns = ['Model', 'Start', 'End']
        df['Start'] = pd.to_datetime(df['Start'], dayfirst=True, errors='coerce')
        df['End'] = pd.to_datetime(df['End'], dayfirst=True, errors='coerce')
        df = df.dropna(subset=['Start', 'End'])

        all_booked_dates = []
        for _, row in df.iterrows():
            try:
                date_range = pd.date_range(start=row['Start'], end=row['End'])
                for d in date_range:
                    all_booked_dates.append({
                        'Model': str(row['Model']).strip(),
                        'Date': d.date()
                    })
            except:
                continue
        return pd.DataFrame(all_booked_dates)
    except Exception as e:
        return pd.DataFrame()


df_bookings = load_bookings()

# --- 3. ASSETS ---
target_model = "Canon IXY 10s"
hero_image = "https://i.ebayimg.com/images/g/jtoAAOSwWH9m6YaC/s-l1600.webp"
mood_board_images = [
    "https://scontent.fbkk... (ลิงก์จากเฟสคุณ)",
    "https://instagram.com... (ลิงก์จากไอจีคุณ)"
]

# --- 4. CSS STYLING ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600&family=Playfair+Display:ital,wght@1,700&display=swap');

        /* MAIN THEME */
        .stApp {
            background: linear-gradient(180deg, #FFF0F5 0%, #F8C8DC 100%);
            font-family: 'Kanit', sans-serif;
            color: #5D3A42;
        }

        #MainMenu, footer, header {visibility: hidden;}
        .block-container { padding-top: 70px !important; padding-bottom: 40px !important; }

        /* APP BAR */
        .app-bar {
            background: rgba(255,255,255,0.9);
            backdrop-filter: blur(10px);
            padding: 10px;
            border-bottom: 1px solid #FFC0CB;
            text-align: center;
            position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
        }
        .app-title {
            font-family: 'Playfair Display', serif; font-weight: 700; font-style: italic;
            color: #D63384; font-size: 20px; margin: 0;
        }

        /* MODEL TITLE (ชื่อรุ่นเด่นๆ) */
        .model-title {
            font-family: 'Playfair Display', serif;
            font-weight: 700;
            color: #D63384;
            text-align: center;
            font-size: 32px; /* ขนาดใหญ่ */
            margin-top: 25px;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(214, 51, 132, 0.2); /* เงาสีชมพูเบาๆ */
            letter-spacing: 1px;
        }

        /* HERO CARD */
        .hero-container {
            position: relative; border-radius: 20px; overflow: hidden;
            box-shadow: 0 10px 20px rgba(255, 105, 180, 0.3); margin-bottom: 20px;
            border: 4px solid #FFF;
        }
        .status-badge {
            position: absolute; bottom: 15px; right: 15px;
            background: rgba(255, 255, 255, 0.95); padding: 8px 20px;
            border-radius: 30px; font-weight: bold; font-size: 14px;
            backdrop-filter: blur(5px); box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        }

        /* CALENDAR GRID */
        .calendar-grid {
            display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px; margin-top: 10px;
        }
        .cal-header {
            font-size: 10px; font-weight: bold; text-align: center; color: #D63384;
        }
        .cal-cell {
            background: #FFF; border-radius: 8px; height: 40px;
            display: flex; justify-content: center; align-items: center;
            font-size: 12px; color: #444; border: 1px solid #FFE4E1;
            position: relative;
        }

        /* 🎨 สถานะวันต่างๆ */
        .is-busy { 
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23DC143C' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='18' y1='6' x2='6' y2='18'%3E%3C/line%3E%3Cline x1='6' y1='6' x2='18' y2='18'%3E%3C/line%3E%3C/svg%3E") !important;
            background-position: center; background-repeat: no-repeat; background-size: 70%;
            background-color: #FFF0F5 !important; color: #DC143C !important;
            font-weight: bold; border: 1px solid #FFB6C1 !important;
        }
        .is-past { 
            background: #F2F2F2 !important; color: #CCC !important; border: 1px solid #EEE;
        }
        .is-today { 
            border: 2px solid #D4AF37 !important; font-weight: bold; z-index: 10;
        }
        .is-faded { opacity: 0.1; background: transparent; border:none; }

        /* SOCIAL BUTTONS */
        .social-btn {
            display: block; width: 100%; padding: 12px; margin-bottom: 8px;
            text-align: center; border-radius: 12px; text-decoration: none;
            font-weight: 600; font-size: 14px; color: white !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.2s;
        }
        .social-btn:active { transform: scale(0.96); }
        .btn-ig { background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); }
        .btn-fb { background: #1877F2; }

    </style>
""", unsafe_allow_html=True)


# --- 5. FUNCTIONS & UI LOGIC ---

def render_cal(year, month, booked_list):
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdatescalendar(year, month)
    days_th = ['อา', 'จ', 'อ', 'พ', 'พฤ', 'ศ', 'ส']

    header = "".join([f"<div class='cal-header'>{d}</div>" for d in days_th])
    body = ""
    today = date.today()

    for week in month_days:
        for day in week:
            cls = ["cal-cell"]
            if day.month != month:
                cls.append("is-faded")
            elif day < today:
                cls.append("is-past")
            elif day in booked_list:
                cls.append("is-busy")

            if day == today:
                cls.append("is-today")
                if day in booked_list: cls.append("is-busy")

            body += f"<div class='{' '.join(cls)}'>{day.day}</div>"

    st.markdown(f"<div class='calendar-grid'>{header}{body}</div>", unsafe_allow_html=True)


# --- 6. RENDER LAYOUT ---

# Top Bar
st.markdown('<div class="app-bar"><p class="app-title">✨ Y2K RENTAL ✨</p></div>', unsafe_allow_html=True)

# Data Prep
if not df_bookings.empty and 'Model' in df_bookings.columns:
    booked_dates = df_bookings[df_bookings['Model'].str.strip() == target_model.strip()]['Date'].tolist()
else:
    booked_dates = []

is_busy_today = date.today() in booked_dates
status_text = "❌ ไม่ว่าง" if is_busy_today else "✅ ว่างพร้อมเช่า"
status_color = "#D63384" if is_busy_today else "#00C851"

# --- ส่วนที่แก้ไข: ย้ายชื่อรุ่นมาไว้ตรงนี้ ---
st.markdown(f'<h2 class="model-title">{target_model}</h2>', unsafe_allow_html=True)

# Hero Section (รูปภาพ)
st.markdown(f"""
    <div class="hero-container">
        <img src="{hero_image}" style="width:100%; display:block; object-fit:cover;">
        <div class="status-badge" style="color:{status_color};">
            {status_text}
        </div>
    </div>
""", unsafe_allow_html=True)

# Calendar Section
month_options = []
today = date.today()
th_months = ["", "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
             "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]
map_month_year = {}

for i in range(12):
    next_month = today.month + i
    next_year = today.year + ((next_month - 1) // 12)
    next_month = ((next_month - 1) % 12) + 1
    label = f"{th_months[next_month]} {next_year + 543}"
    month_options.append(label)
    map_month_year[label] = (next_year, next_month)

st.markdown("<br>", unsafe_allow_html=True)
c_spacer, c_select, c_spacer2 = st.columns([0.2, 4, 0.2])
with c_select:
    st.markdown(
        "<p style='text-align:center; margin-bottom:0px; font-size:12px; color:#888;'>📅 เลือกเดือนที่ต้องการเช็ค</p>",
        unsafe_allow_html=True)
    selected_label = st.selectbox("Select Month", month_options, label_visibility="collapsed")

sel_year, sel_month = map_month_year[selected_label]
render_cal(sel_year, sel_month, booked_dates)

# Mood Board
st.markdown("<br>", unsafe_allow_html=True)
with st.expander(f"📸 ดูรูปตัวอย่างโทนภาพ"):
    mc1, mc2 = st.columns(2)
    for i, img in enumerate(mood_board_images):
        if i % 2 == 0:
            mc1.image(img, use_container_width=True)
        else:
            mc2.image(img, use_container_width=True)

# Action Bar
st.markdown("<br>", unsafe_allow_html=True)
c_ig, c_fb = st.columns(2)
with c_ig:
    st.markdown(f'<a href="https://www.instagram.com/miwvie_shop/" target="_blank" class="social-btn btn-ig">IG จองเลย</a>',
                unsafe_allow_html=True)
with c_fb:
    st.markdown(f'<a href="https://facebook.com/your_shop" target="_blank" class="social-btn btn-fb">FB ทักแชท</a>',
                unsafe_allow_html=True)
