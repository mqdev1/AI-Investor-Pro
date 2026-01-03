import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- 1. إعدادات النظام ---
st.set_page_config(page_title="AI Alpha Dashboard", layout="wide", page_icon="📈")

# تحسين المظهر ليكون نظاماً متكاملاً
st.markdown("""
    <style>
    .reportview-container { background: #f8f9fa; }
    .main-header { font-size: 36px; font-weight: bold; color: #1e3a8a; text-align: center; margin-bottom: 20px; }
    .card { background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .metric-box { text-align: center; border-right: 1px solid #edf2f7; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. رأس الصفحة ---
st.markdown('<div class="main-header">🚀 نظام AI Alpha للتحليل المالي الشامل</div>', unsafe_allow_html=True)
st.write("<p style='text-align: center; color: #64748b;'>نظام ذكي لدمج المؤشرات الفنية وتقديم توصيات استثمارية مبسطة</p>", unsafe_allow_html=True)

# --- 3. قسم المدخلات (في المنتصف بدلاً من الجنب) ---
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col_in1, col_in2, col_in3 = st.columns([2, 2, 1])
    
    with col_in1:
        asset_choice = st.selectbox("1️⃣ اختر نوع السوق:", ["أسهم عالمية", "عملات رقمية", "ذهب ومعادن"])
    
    with col_in2:
        if asset_choice == "أسهم عالمية":
            ticker = st.text_input("2️⃣ أدخل رمز السهم (مثلاً AAPL):", "AAPL").upper()
        elif asset_choice == "عملات رقمية":
            ticker = st.text_input("2️⃣ أدخل رمز العملة (مثلاً BTC-USD):", "BTC-USD").upper()
        else:
            ticker = "GC=F"
            st.info("تم اختيار عقود الذهب")

    with col_in3:
        analyze_btn = st.button("🔍 ابدأ التحليل الآن", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. محرك التحليل ---
if analyze_btn:
    try:
        with st.spinner('جاري معالجة البيانات وبناء التوقعات...'):
            data = yf.download(ticker, period="1y", multi_level_index=False)

        if data.empty:
            st.error("❌ تعذر العثور على بيانات. يرجى التأكد من الرمز.")
        else:
            # حسابات المؤشرات (Technical Indicators)
            data['SMA20'] = data['Close'].rolling(window=20).mean()
            data['SMA50'] = data['Close'].rolling(window=50).mean()
            
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            data['RSI'] = 100 - (100 / (1 + rs))

            current_price = float(data['Close'].iloc[-1])
            last_rsi = float(data['RSI'].iloc[-1])
            sma20 = float(data['SMA20'].iloc[-1])
            sma50 = float(data['SMA50'].iloc[-1])

            # --- 5. عرض النتائج (Cards System) ---
            st.markdown("### 📊 ملخص الأداء اللحظي")
            res_col1, res_col2, res_col3, res_col4 = st.columns(4)

            with res_col1:
                st.metric("السعر الحالي", f"${current_price:,.2f}")
                st.caption("سعر الإغلاق الأخير في السوق")

            with res_col2:
                rsi_label = "غالٍ جداً" if last_rsi > 70 else "رخيص جداً" if last_rsi < 30 else "سعر عادل"
                st.metric("قوة الشراء (RSI)", f"{last_rsi:.1f}", rsi_label)
                st.caption("يقيس إذا كان السهم مبالغ في سعره أم لا")

            with res_col3:
                trend = "صاعد 📈" if sma20 > sma50 else "هابط 📉"
                st.metric("الاتجاه العام", trend)
                st.caption("يعتمد على تقاطع المتوسطات المتحركة")

            with res_col4:
                # منطق التوصية النهائية
                if last_rsi < 35 and sma20 > sma50:
                    advice, color = "شراء مؤكد", "green"
                elif last_rsi > 65 or sma20 < sma50:
                    advice, color = "خروج / حذر", "red"
                else:
                    advice, color = "مراقبة", "orange"
                st.subheader(f":{color}[{advice}]")
                st.caption("التوصية النهائية بناءً على دمج المؤشرات")

            # --- 6. الرسم البياني الكبير ---
            st.markdown("### 📈 المخطط البياني المتقدم")
            fig = go.Figure()
            fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name="السعر"))
            fig.add_trace(go.Scatter(x=data.index, y=data['SMA20'], line=dict(color='orange', width=1), name="متوسط 20 يوم"))
            fig.add_trace(go.Scatter(x=data.index, y=data['SMA50'], line=dict(color='blue', width=1), name="متوسط 50 يوم"))
            fig.update_layout(height=500, template="plotly_white", margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)

            # --- 7. قسم التواصل والدعم (للمستثمرين) ---
            st.markdown("---")
            foot_col1, foot_col2 = st.columns(2)
            with foot_col1:
                st.markdown("#### 🚀 ميزات النسخة الاحترافية")
                st.write("* تنبيهات فورية عبر الواتساب عند صدور إشارة شراء.")
                st.write("* ربط مباشر مع ChatGPT لتحليل أخبار الشركات.")
                st.write("* لوحة تحكم لإدارة المحفظة المالية بالكامل.")
            
            with foot_col2:
                st.markdown("#### 📞 تواصل مع المطور")
                st.write("للحصول على نسخة مخصصة لشركتك أو استراتيجيتك:")
                st.button("💬 تواصل عبر واتساب (970567256989)")
                st.write("📧 البريد الإلكتروني: mahdevproo@gmail.com")

    except Exception as e:
        st.error(f"حدث خطأ: {e}")
else:
    st.markdown("""
        <div style="text-align: center; padding: 50px; border: 2px dashed #cbd5e1; border-radius: 20px;">
            <h3>مرحباً بك في نظام AI Alpha</h3>
            <p>الرجاء إدخال رمز السهم في الأعلى والضغط على زر التحليل للبدء.</p>
        </div>
    """, unsafe_allow_html=True)
