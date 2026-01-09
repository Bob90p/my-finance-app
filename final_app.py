import streamlit as st
import yfinance as yf
import google.generativeai as genai
from PIL import Image
import matplotlib.pyplot as plt

# إعداد الاتصال بـ Gemini
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("تأكد من وضع المفتاح في Secrets")

st.title("المحلل المالي الذكي 🤖📈")

ticker = st.text_input("رمز السهم (مثال: COMI.CA أو CASE للمؤشر):", "CASE")
context = st.text_area("سياق إضافي:")

if st.button("🚀 الحصول على التوصية"):
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="1mo")
        
        if df.empty:
            st.error("الرمز غير صحيح. استخدم CASE لمؤشر مصر.")
        else:
            # رسم بياني احترافي
            fig, ax = plt.subplots()
            df['Close'].plot(ax=ax)
            st.pyplot(fig)
            fig.savefig("chart.png")
            
            # تعليمات التوصية التلقائية
            instruction = f"حلل هذا السهم {ticker} وأعطِ توصية واضحة (شراء/بيع/انتظار) مع تحديد الأهداف ووقف الخسارة باللغة العربية."
            img = Image.open("chart.png")
                        # إرسال الصورة والتعليمات لـ Gemini
            response = model.generate_content([instruction, img]) # حذفنا context من هنا لتبسيط الطلب
            
            st.markdown("---")
            st.subheader("📋 التوصية:")
            st.info(response.text) # استخدمنا st.info ليكون شكل التوصية أوضح

            st.subheader("📋 التوصية:")
            st.write(response.text)
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
