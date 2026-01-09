import streamlit as st
import yfinance as yf
import google.generativeai as genai
from PIL import Image
import matplotlib.pyplot as plt
import os

# 1. إعداد واجهة التطبيق أولاً
st.set_page_config(page_title="المحلل الاستراتيجي الذكي", layout="wide")
st.title("المحلل المالي الذكي 🤖📈")

# 2. التحقق من مفتاح الـ API
if "GEMINI_API_KEY" not in st.secrets:
    st.error("⚠️ مفتاح API غير موجود! يرجى إضافته في إعدادات Secrets باسم GEMINI_API_KEY")
    st.stop()

try:
    # تهيئة النموذج
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip()) # strip لإزالة أي مسافات زائدة
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"❌ خطأ في تهيئة الذكاء الاصطناعي: {e}")
    st.stop()

# 3. منطقة الإدخال
ticker = st.text_input("اكتب رمز السهم (مثال: CASE للمؤشر أو COMI.CA):", "CASE")
context = st.text_area("إضافة سياق (أخبار أو استفسار محدد):")

if st.button("🚀 الحصول على التوصية"):
    if ticker:
        try:
            with st.spinner("جاري جلب البيانات وتحليل الرسم..."):
                stock = yf.Ticker(ticker)
                # استخدام بيانات أسبوع واحد لضمان سرعة الرفع والتحليل
                df = stock.history(period="5d")
                
                if df.empty:
                    st.error("❌ الرمز غير صحيح أو لا توجد بيانات. (استخدم CASE لمؤشر مصر الرئيسي)")
                else:
                    # عرض السعر الحالي
                    current_price = df['Close'].iloc[-1]
                    st.metric(f"السعر الحالي لـ {ticker}", f"{current_price:.2f}")

                    # إنشاء الرسم البياني وحفظه بجودة سريعة
                    fig, ax = plt.subplots(figsize=(10, 5))
                    df['Close'].plot(ax=ax, color='#1f77b4', linewidth=2)
                    ax.set_title(f"Chart: {ticker}")
                    ax.grid(True, alpha=0.3)
                    st.pyplot(fig)
                    
                    # حفظ الصورة مؤقتاً
                    image_path = "chart.png"
                    fig.savefig(image_path, dpi=80)
                    plt.close(fig) # إغلاق الشكل لتوفير الذاكرة
                    
                    # تحضير الصورة للذكاء الاصطناعي
                    img = Image.open(image_path)
                    
                    # صياغة الطلب (Prompt)
                    prompt = f"""
                    أنت محلل مالي محترف. حلل صورة السهم {ticker} المرفقة:
                    1. أعطِ توصية واضحة (شراء/بيع/انتظار).
                    2. حدد نقطة الدخول، الهدف، ووقف الخسارة.
                    3. اذكر السبب بناءً على الرسم البياني.
                    4. خذ في الاعتبار هذا السياق: {context if context else 'لا يوجد'}
                    اجعل الرد باللغة العربية ومنظماً جداً.
                    """
                    
                    # إرسال الطلب
                    response = model.generate_content([prompt, img])
                    
                    if response:
                        st.markdown("---")
                        st.subheader("📋 التوصية الاستراتيجية:")
                        st.success(response.text)
                    else:
                        st.warning("⚠️ تعذر الحصول على رد من الذكاء الاصطناعي، جرب مرة أخرى.")

        except Exception as e:
            st.error(f"❌ حدث خطأ تقني: {e}")
    else:
        st.error("من فضلك أدخل رمز السهم أولاً.")
