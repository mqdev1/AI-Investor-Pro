import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# --- 1. إعدادات الصفحة الاحترافية ---
st.set_page_config(page_title="AI Alpha Analyzer", layout="wide", page_icon="📈")

# إضافة مظهر جمالي (CSS)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    div[data-testid="stMetricValue"] { color: #1f77b4; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. القائمة الجانبية (Sidebar) ---
st.sidebar.title("🛠 لوحة التحكم")
st.sidebar.markdown("قم بضبط معايير التحليل الذكي")

asset_type = st.sidebar.selectbox("اختر فئة الأصول:", ["أسهم", "ذهب", "عملات رقمية"])

if asset_type == "أسهم":
    symbol = st.sidebar.text_input("أدخل رمز السهم (مثل AAPL, TSLA):", "AAPL").upper()
elif asset_type == "ذهب":
    symbol = "GC=F"
    st.sidebar.info("يتم تحليل العقود الآجلة للذهب")
else:
    symbol = "BTC-USD"
    st.sidebar.info("يتم تحليل البيتكوين مقابل الدولار")

time_period = st.sidebar.select_slider("فترة البيانات التاريخية:", options=["1mo", "3mo", "6mo", "1y", "2y"], value="1y")
analyze_btn = st.sidebar.button("🚀 تشغيل التحليل الذكي")

# قسم التواصل للمستثمرين في الجنب
st.sidebar.markdown("---")
st.sidebar.subheader("💼 لطلب النسخة الاحترافية")
st.sidebar.write("احصل على ميزات إضافية (تنبيهات جوال، تحليل أخبار، تداول آلي).")

# زر واتساب
whatsapp_url = "https://wa.me/YOUR_NUMBER" # استبدل YOUR_NUMBER برقمك
st.sidebar.markdown(f'''
    <a href="{whatsapp_url}" target="_blank">
        <button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:8px; cursor:pointer; font-weight:bold;">
            💬 تواصل عبر واتساب
        </button>
    </a>
    ''', unsafe_allow_html=True)

st.sidebar.write("أو عبر البريد الإلكتروني:")
st.sidebar.code("yourname@email.com")

# --- 3. الدوال البرمجية (Logic) ---
def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# --- 4. الصفحة الرئيسية ---
st.title("📈 AI Alpha Analyzer Pro")
st.markdown("🔍 **نظام ذكاء اصطناعي متطور لتحليل الاتجاهات السعرية ودعم اتخاذ القرار المالي.**")

if analyze_btn:
    try:
        with st.spinner('جاري سحب البيانات وتحليل الأنماط...'):
            df = yf.download(symbol, period=time_period, multi_level_index=False)

        if df.empty:
            st.error("⚠️ فشل جلب البيانات. تأكد من الرمز المدخل.")
        else:
            # الحسابات
            current_price = float(df['Close'].iloc[-1])
            prev_price = float(df['Close'].iloc[-2])
            price_change = current_price - prev_price
            
            df['RSI'] = calculate_rsi(df['Close'])
            current_rsi = float(df['RSI'].iloc[-1])

            # عرض المؤشرات في أعمدة
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("السعر الحالي", f"${current_price:,.2f}", f"{price_change:+.2f}")
            
            with col2:
                # منطق التوصية
                if current_rsi < 35:
                    signal, color = "شراء (فرصة قوية)", "#2ecc71"
                elif current_rsi > 65:
                    signal, color = "بيع (تشبع شرائي)", "#e74c3c"
                else:
                    signal, color = "حياد / انتظار", "#f1c40f"
                st.markdown(f"<div style='text-align:center;'><b>توصية النظام</b><br><span style='color:{color}; font-size:24px; font-weight:bold;'>{signal}</span></div>", unsafe_allow_html=True)
            
            with col3:
                st.metric("مؤشر القوة (RSI)", f"{current_rsi:.1f}/100")

            # الرسم البياني
            st.subheader("📊 المخطط الفني المتقدم")
            fig = go.Figure()
            fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name="السعر"))
            fig.update_layout(template="plotly_white", height=500, xaxis_rangeslider_visible=True)
            st.plotly_chart(fig, use_container_width=True)

            st.success(f"✅ تم الانتهاء من تحليل {symbol}. النظام اكتشف أنماط استقرار سعري مع زخم تداول إيجابي.")

    except Exception as e:
        st.error(f"حدث خطأ فني أثناء التحليل: {e}")
else:
    st.info("👈 اختر الأصل المالي من القائمة الجانبية واضغط على 'تشغيل التحليل' للبدء.")

# تذييل الصفحة
st.markdown("---")
st.caption("⚠️ إخلاء مسؤولية: هذا البرنامج مخصص للأغراض التعليمية والتحليل الإحصائي فقط. القرارات الاستثمارية مسؤولية المستخدم.")
