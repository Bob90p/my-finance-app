import streamlit as st
import yfinance as yf
import google.generativeai as genai
from PIL import Image
import matplotlib.pyplot as plt

# إعدادات الصفحة
st.set_page_config(page_title="المحلل المالي الذكي", layout="wide")

# محاولة الاتصال بالمفتاح
if "GEMINI_API_KEY" in st.secrets:
    try:
        api_key = st.secrets["GEMINI_API_KEY"].strip()
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        # اختبار بسيط للمفتاح
        st.sidebar.success("✅ مفتاح الذكاء الاصطناعي متصل")
    except Exception as e:
        st.sidebar.error(f"❌ خطأ في المفتاح: {e}")
else:
    st.sidebar.warning("⚠️ المفتاح غير مضاف في Secrets")

st.title("المحلل الاستراتيجي 🤖📈")

ticker = st.text_input("رمز السهم (مثال: CASE للمؤشر أو AAPL):", "CASE")

if st.button("🚀 الحصول على التوصية"):
    try:
        with st.spinner("جاري التحليل..."):
            df = yf.Ticker(ticker).history(period="5d")
            if not df.empty:
                st.metric(f"سعر {ticker}", f"{df['Close'].iloc[-1]:.2f}")
                fig, ax = plt.subplots(figsize=(8, 4))
                df['Close'].plot(ax=ax)
                st.pyplot(fig)
                fig.savefig("chart.png", dpi=70)
                
                # إرسال التحليل
                img = Image.open("chart.png")
                prompt = f"حلل سهم {ticker} وأعطِ توصية شراء أو بيع والأهداف بالعربية."
                response = model.generate_content([prompt, img])
                
                st.markdown("---")
                st.subheader("📋 التوصية:")
                st.success(response.text)
            else:
                st.error("الرمز غير صحيح.")
    except Exception as e:
        st.error(f"⚠️ خطأ: {e}")
