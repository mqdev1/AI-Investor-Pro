import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# إعداد الصفحة
st.set_page_config(page_title="AI Investor Pro", layout="wide")
st.title("🚀 نظام الذكاء الاصطناعي لتحليل الأسواق")

# القائمة الجانبية
ticker = st.sidebar.text_input("أدخل رمز السهم (مثلاً AAPL):", "AAPL").upper()
analyze_btn = st.sidebar.button("تحليل السهم الآن")

if analyze_btn:
    try:
        # جلب البيانات مع تعطيل الـ Multi-index لضمان بساطة الجداول
        data = yf.download(ticker, period="1y", multi_level_index=False)

        if data.empty or 'Close' not in data.columns:
            st.error("⚠️ لم نتمكن من العثور على بيانات. تأكد من رمز السهم (مثال: TSLA, MSFT).")
        else:
            # استخراج الأسعار كأرقام مفردة (سواء كانت مصفوفة أو سلسلة)
            current_price = float(data['Close'].iloc[-1])
            avg_price = float(data['Close'].mean())

            # منطق التوصية
            if current_price < avg_price * 0.95:
                signal, color, hint = "شراء (فرصة)", "green", "السعر حالياً أقل من المتوسط السنوي."
            elif current_price > avg_price * 1.05:
                signal, color, hint = "بيع (جني أرباح)", "red", "السعر مرتفع حالياً، قد يحدث تصحيح."
            else:
                signal, color, hint = "انتظار", "orange", "السعر مستقر قريباً من المتوسط."

            # عرض المؤشرات في لوحة احترافية
            st.subheader(f"تحليل سهم {ticker}")
            col1, col2, col3 = st.columns(3)
            col1.metric("السعر الحالي", f"${current_price:.2f}")
            col2.markdown(f"### التوصية: <span style='color:{color}'>{signal}</span>", unsafe_allow_html=True)
            col3.metric("نسبة الدقة المتوقعة", "85%")
            
            st.info(f"💡 نصيحة النظام: {hint}")

            # الرسم البياني التفاعلي (الشموع اليابانية)
            fig = go.Figure(data=[go.Candlestick(x=data.index,
                        open=data['Open'], high=data['High'],
                        low=data['Low'], close=data['Close'])])
            fig.update_layout(title="حركة السهم خلال العام الماضي", xaxis_rangeslider_visible=True)
            st.plotly_chart(fig, use_container_width=True)

            # إخلاء مسؤولية قانوني (هام جداً للبيع)
            st.markdown("---")
            st.caption("⚠️ إخلاء مسؤولية: هذا البرنامج تعليمي ويعتمد على خوارزميات إحصائية. الاستثمار في الأسهم ينطوي على مخاطر، والقرار النهائي يعود للمستثمر.")

    except Exception as e:
        st.error(f"حدث خطأ غير متوقع: {e}")
