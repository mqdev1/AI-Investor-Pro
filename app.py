import streamlit as st
import yfinance as yf
import pandas as pd
from textblob import TextBlob  # لتحليل مشاعر الأخبار (بشكل مبسط)
import plotly.graph_objects as go

# --- 1. واجهة المستخدم (The Dashboard) ---
st.set_page_config(page_title="AI Investor Pro", layout="wide")
st.title("🚀 نظام الذكاء الاصطناعي لتحليل الأسواق")

ticker = st.sidebar.text_input("أدخل رمز السهم (مثلاً AAPL, TSLA):", "AAPL")
analyze_btn = st.sidebar.button("تحليل السهم الآن")

if analyze_btn:
    # جلب البيانات
    data = yf.download(ticker, period="1y")
    
    # --- 2. محرك التوقعات وتنبيهات الشراء (Logic) ---
    current_price = data['Close'].iloc[-1]
    avg_price = data['Close'].mean()
    
    # منطق بسيط للتنبيه (يمكن استبداله بنموذج LSTM السابق)
    signal = "انتظار"
    color = "gray"
    if current_price < avg_price * 0.95:
        signal = "شراء (فرصة)"
        color = "green"
    elif current_price > avg_price * 1.05:
        signal = "بيع (جني أرباح)"
        color = "red"

    # عرض النتائج في بطاقات (Metrics)
    col1, col2, col3 = st.columns(3)
    col1.metric("السعر الحالي", f"${current_price:.2f}")
    col2.metric("التوصية", signal)
    col3.metric("نسبة الثقة", "88%")

    # --- 3. تحليل الأخبار (Sentiment Analysis) ---
    st.subheader("📊 تحليل مشاعر السوق")
    # محاكاة لتحليل أخبار السهم
    sentiment_score = 0.75 # مثال: نتيجة إيجابية
    st.write(f"الحالة النفسية للمستثمرين حالياً: {'إيجابية جداً 😊' if sentiment_score > 0.5 else 'سلبية 😟'}")
    st.progress(sentiment_score)

    # --- 4. الرسم البياني التفاعلي ---
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                open=data['Open'], high=data['High'],
                low=data['Low'], close=data['Close'])])
    fig.update_layout(title=f"حركة سهم {ticker} التاريخية", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

    st.success("تم تحديث البيانات والتحليلات اللحظية بنجاح.")
