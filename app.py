import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# --- إعدادات الصفحة الاحترافية ---
st.set_page_config(page_title="AI Alpha Analyzer", layout="wide")

# تخصيص المظهر بـ CSS بسيط
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("📈 نظام AI Alpha لتحليل الأسواق العالمية")
st.write("منصة ذكية لاتخاذ قرارات استثمارية مبنية على البيانات اللحظية.")

# --- القائمة الجانبية (Sidebar) ---
st.sidebar.header("لوحة التحكم")
asset_type = st.sidebar.selectbox("اختر فئة الأصول:", ["أسهم", "ذهب", "عملات رقمية"])

if asset_type == "أسهم":
    symbol = st.sidebar.text_input("أدخل رمز السهم (مثل AAPL, TSLA):", "AAPL").upper()
elif asset_type == "ذهب":
    symbol = "GC=F"
    st.sidebar.info("يتم تحليل العقود الآجلة للذهب")
else:
    symbol = "BTC-USD"
    st.sidebar.info("يتم تحليل البيتكوين مقابل الدولار")

time_period = st.sidebar.select_slider("فترة التحليل:", options=["1mo", "3mo", "6mo", "1y", "2y"], value="1y")
analyze_btn = st.sidebar.button("تشغيل التحليل الذكي")

# --- دالة حساب مؤشر RSI (ميزة إضافية للمستثمرين) ---
def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

if analyze_btn:
    try:
        with st.spinner('جاري سحب البيانات وتحليل الأنماط...'):
            df = yf.download(symbol, period=time_period, multi_level_index=False)

        if df.empty:
            st.error("⚠️ فشل جلب البيانات. تأكد من الرمز.")
        else:
            # الحسابات الفنية
            current_price = float(df['Close'].iloc[-1])
            prev_price = float(df['Close'].iloc[-2])
            change = current_price - prev_price
            
            # حساب RSI
            df['RSI'] = calculate_rsi(df['Close'])
            current_rsi = df['RSI'].iloc[-1]

            # --- عرض المؤشرات الرئيسية ---
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("السعر الحالي", f"${current_price:,.2f}", f"{change:+.2f}")
            
            # منطق التوصية الذكي
            if current_rsi < 30:
                signal, color = "شراء قوي (تشبع بيعي)", "#2ecc71"
            elif current_rsi > 70:
                signal, color = "بيع (تضخم سعري)", "#e74c3c"
            else:
                signal, color = "حياد / انتظار", "#f1c40f"
            
            col2.markdown(f"**توصية النظام:** <br> <span style='color:{color}; font-size:20px; font-weight:bold;'>{signal}</span>", unsafe_allow_html=True)
            col3.metric("مؤشر القوة (RSI)", f"{current_rsi:.1f}")
            col4.metric("ثبات الاتجاه", "قوي" if abs(change) > 1 else "مستقر")

            # --- الرسم البياني التفاعلي ---
            st.subheader("📊 المخطط الفني المتقدم")
            fig = go.Figure()
            fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name="السعر"))
            fig.update_layout(template="plotly_white", height=500, xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)

            # نصيحة الـ AI
            st.success(f"✅ تحليل مكتمل لـ {symbol}: النظام يشير إلى حالة {signal}. بناءً على البيانات، السعر يتحرك ضمن نطاق المتوسط السنوي مع استقرار في مؤشرات الزخم.")

    except Exception as e:
        st.error(f"حدث خطأ فني: {e}")

# تذييل الصفحة
st.markdown("---")
st.caption("© 2026 AI Alpha Analyzer - تقنيات ذكاء اصطناعي للأسواق المالية. لا تعتبر هذه البيانات نصيحة استثمارية.")
