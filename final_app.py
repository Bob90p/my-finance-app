import streamlit as st
import yfinance as yf
import google.generativeai as genai
from PIL import Image
import matplotlib.pyplot as plt

# إعداد الصفحة
st.set_page_config(page_title="المحلل المالي الذكي", layout="wide")

# الربط بالمفتاح وتنظيفه
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"].strip()
    genai.configure(api_key=api_key)
    # استخدام نسخة مستقرة لتجنب خطأ 404
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ يرجى إضافة GEMINI_API_KEY في Secrets")
    st.stop()

st.title("المحلل الاستراتيجي 🤖📈")

ticker = st.text_input("أدخل رمز السهم (مثال: CASE أو AAPL):", "CASE")

if st.button("🚀 الحصول على التوصية"):
    try:
        with st.spinner("جاري التحليل..."):
            # جلب بيانات 5 أيام فقط لسرعة الرفع
            stock = yf.Ticker(ticker)
            df = stock.history(period="5d")
            
            if not df.empty:
                # عرض السعر
                st.metric(f"سعر {ticker}", f"{df['Close'].iloc[-1]:.2f}")
                
                # الرسم البياني
                fig, ax = plt.subplots(figsize=(8, 4))
                df['Close'].plot(ax=ax, color='blue')
                st.pyplot(fig)
                
                # حفظ وإرسال الصورة
                image_path = "chart.png"
                fig.savefig(image_path, dpi=70)
                img = Image.open(image_path)
                
                prompt = f"حلل سهم {ticker} بناءً على الصورة وأعطِ توصية (شراء/بيع/انتظار) بالعربية."
                
                # إرسال الطلب (هنا يحدث التحليل)
                response = model.generate_content([prompt, img])
                
                st.markdown("---")
                st.success(response.text)
            else:
                st.error("الرمز غير صحيح.")
    except Exception as e:
        st.error(f"حدث خطأ تقني: {e}")
