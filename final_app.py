import streamlit as st
import yfinance as yf
import google.generativeai as genai
from PIL import Image
import matplotlib.pyplot as plt

# إعداد الصفحة
st.set_page_config(page_title="المحلل الذكي", layout="wide")

# الربط بالمفتاح من Secrets
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"].strip()
    genai.configure(api_key=api_key)
    # استخدام الموديل المستقر
    model = genai.GenerativeModel('gemini-1.5-flash-latest') 
else:
    st.error("⚠️ يرجى إضافة GEMINI_API_KEY في Secrets")
    st.stop()

st.title("المحلل المالي الذكي 🤖📈")

ticker = st.text_input("أدخل رمز السهم:", "CASE")

if st.button("🚀 الحصول على التوصية"):
    try:
        with st.spinner("جاري التحليل..."):
            data = yf.Ticker(ticker).history(period="1mo")
            if not data.empty:
                # رسم وحفظ الصورة
                fig, ax = plt.subplots()
                data['Close'].plot(ax=ax)
                st.pyplot(fig)
                fig.savefig("chart.png")
                
                # إرسال الصورة للتحليل
                img = Image.open("chart.png")
                prompt = "أنت خبير مالي، حلل هذا الرسم البياني وأعطني توصية دقيقة بالعربية."
                response = model.generate_content([prompt, img])
                
                st.success(response.text)
            else:
                st.error("الرمز غير صحيح.")
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
