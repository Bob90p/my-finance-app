import streamlit as st
import yfinance as yf
import google.generativeai as genai
from PIL import Image
import matplotlib.pyplot as plt

# 1. إعداد الاتصال بـ Gemini
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # تأكد من استخدام موديل 1.5-flash للسرعة
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"خطأ في إعداد المفتاح: {e}")

st.title("المحلل المالي الذكي 🤖📈")

# المدخلات
ticker = st.text_input("رمز السهم (مثال: CASE للمؤشر أو COMI.CA):", "CASE")
context = st.text_area("سياق إضافي (أخبار أو استفسار):")

if st.button("🚀 الحصول على التوصية"):
    if ticker:
        try:
            with st.spinner("جاري جلب البيانات وتحليل الرسم..."):
                stock = yf.Ticker(ticker)
                # استخدام 5 أيام فقط لسرعة الرفع والتحليل
                df = stock.history(period="5d")
                
                if df.empty:
                    st.error("الرمز غير صحيح.")
                else:
                    # عرض السعر الحالي
                    current_price = df['Close'].iloc[-1]
                    st.metric(f"السعر الحالي ({ticker})", f"{current_price:.2f}")

                    # إنشاء الرسم البياني وحفظه بجودة سريعة الرفع
                    fig, ax = plt.subplots(figsize=(8, 4))
                    df['Close'].plot(ax=ax, color='blue', linewidth=2)
                    ax.grid(True)
                    st.pyplot(fig)
                    fig.savefig("chart.png", dpi=70) # تقليل dpi للسرعة
                    
                    # تحضير الصورة والطلب
                    img = Image.open("chart.png")
                    prompt = f"حلل سهم {ticker}. أعطِ توصية (شراء/بيع/انتظار) مع الأهداف ووقف الخسارة بالعربية. سياق المستخدم: {context}"
                    
                    # إرسال الطلب (الصورة ثم النص)
                    response = model.generate_content([img, prompt])
                    
                    # عرض التوصية فوراً
                    st.markdown("---")
                    st.subheader("📋 التوصية الاستراتيجية:")
                    if response.text:
                        st.success(response.text)
                    else:
                        st.warning("لم يتم إنتاج نص، جرب الضغط مرة أخرى.")

        except Exception as e:
            st.error(f"عذراً، حدث خطأ: {e}")
