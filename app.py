# --- تعديل الجزء الخاص بجلب البيانات ---
if analyze_btn:
    # إضافة group_by=False لضمان تنسيق بسيط للبيانات
    data = yf.download(ticker, period="1y")
    
    if data.empty:
        st.error("لم يتم العثور على بيانات لهذا الرمز، تأكد من كتابته بشكل صحيح (مثل AAPL).")
    else:
        # التأكد من اختيار عمود الإغلاق بشكل صريح وتحويله لقيمة واحدة
        # استخدمنا .iloc[-1] للحصول على آخر قيمة و .item() لتحويلها لرقم بسيط
        current_price = float(data['Close'].iloc[-1])
        avg_price = float(data['Close'].mean())
        
        # الآن ستعمل المقارنة بدون مشاكل
        signal = "انتظار"
        color = "gray"
        if current_price < avg_price * 0.95:
            signal = "شراء (فرصة)"
            color = "green"
        elif current_price > avg_price * 1.05:
            signal = "بيع (جني أرباح)"
            color = "red"
