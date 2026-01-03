import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# إعدادات الصفحة
st.set_page_config(page_title="AI Trading Coach", layout="wide")

# تصميم الواجهة
st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    .stMetric { border: 1px solid #d1d5db; padding: 15px; border-radius: 10px; background: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 مساعد التداول الذكي (AI Alpha Pro)")
st.write("أداة متطورة تجمع بين التحليل الفني والتعليم المبسط للمبتدئين.")

# القائمة الجانبية
st.sidebar.header("⚙️ إعدادات التحليل")
symbol = st.sidebar.text_input("أدخل رمز السهم (مثال AAPL):", "AAPL").upper()
time_period = st.sidebar.selectbox("فترة التحليل:", ["3mo", "6mo", "1y", "2y"])
analyze_btn = st.sidebar.button("تحليل شامل للسهم")

# قسم التواصل
st.sidebar.markdown("---")
st.sidebar.write("✉️ للتواصل وطلب نسخة خاصة:")
st.sidebar.write("yourname@email.com")

if analyze_btn:
    try:
        data = yf.download(symbol, period=time_period, multi_level_index=False)
        
        if data.empty:
            st.error("لم يتم العثور على بيانات السهم.")
        else:
            # حساب المؤشرات
            data['SMA_20'] = data['Close'].rolling(window=20).mean() # متوسط 20 يوم
            data['SMA_50'] = data['Close'].rolling(window=50).mean() # متوسط 50 يوم
            
            # حساب RSI
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            data['RSI'] = 100 - (100 / (1 + rs))
            
            current_price = data['Close'].iloc[-1]
            current_rsi = data['RSI'].iloc[-1]

            # --- الجزء الأول: ملخص للمبتدئين ---
            st.subheader("💡 ماذا يحدث في السهم الآن؟")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("السعر الحالي", f"${current_price:.2f}")
                st.write("**المعنى:** هذا هو السعر الذي يتم تداول السهم به الآن في السوق.")

            with col2:
                rsi_status = "تشبع شرائي (غالٍ)" if current_rsi > 70 else "تشبع بيعي (رخيص)" if current_rsi < 30 else "مستقر"
                st.metric("حالة القوة (RSI)", f"{current_rsi:.1f}", rsi_status)
                st.write(f"**المعنى:** المؤشر يقول أن السهم حالياً {rsi_status}.")

            with col3:
                trend = "صاعد" if data['SMA_20'].iloc[-1] > data['SMA_50'].iloc[-1] else "هابط"
                st.metric("اتجاه السهم", trend)
                st.write(f"**المعنى:** بمقارنة المتوسطات، السهم في مسار {trend} العام.")

            # --- الجزء الثاني: الرسم البياني التفاعلي ---
            st.subheader("📊 المخطط الفني المفصل")
            fig = go.Figure()
            # الشموع اليابانية
            fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name="حركة السعر"))
            # المتوسطات
            fig.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], line=dict(color='orange', width=1.5), name="متوسط 20 يوم"))
            fig.add_trace(go.Scatter(x=data.index, y=data['SMA_50'], line=dict(color='blue', width=1.5), name="متوسط 50 يوم"))
            
            fig.update_layout(template="plotly_white", height=600, xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)

            # --- الجزء الثالث: التوصية والتعليم ---
            st.info("### 🏁 النتيجة النهائية")
            if current_rsi < 30 and trend == "صاعد":
                st.success("✅ **فرصة شراء ذهبية:** السهم في اتجاه صاعد لكنه رخيص الآن (تراجع مؤقت).")
            elif current_rsi > 70 and trend == "هابط":
                st.error("⚠️ **تحذير بيع:** السهم هابط حالياً وهو غالٍ جداً، احتمال هبوط وشيك.")
            else:
                st.warning("⚖️ **حالة انتظار:** لا توجد إشارة واضحة تماماً، يفضل مراقبة مناطق الدعم والمقاومة.")

    except Exception as e:
        st.error(f"خطأ: {e}")
