import streamlit as st
import yfinance as yf
import google.generativeai as genai

st.set_page_config(page_title="المحلل السريع")

# تنظيف وجلب المفتاح
if "GEMINI_API_KEY" in st.secrets:
    # [span_2](start_span)السجلات أظهرت رموزاً غير صالحة، هذا السطر سيحذفها[span_2](end_span)
    raw_key = st.secrets["GEMINI_API_KEY"]
    clean_key = raw_key.replace('"', '').replace("'", "").strip()
    genai.configure(api_key=clean_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("المفتاح غير موجود في Secrets")
    st.stop()

st.title("المحلل المالي الذكي 🤖")
ticker = st.text_input("رمز السهم:", "CASE")

if st.button("تحليل"):
    try:
        # جلب السعر الحالي فقط لسرعة الاستجابة
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")['Close'].iloc[-1]
        
        st.metric("السعر الحالي", f"{price:.2f}")
        
        with st.spinner("ذكاء اصطناعي يفكر..."):
            # طلب نصي قصير جداً
            res = model.generate_content(f"سعر سهم {ticker} هو {price:.2f}. أعطني نصيحة سريعة بالعربية.")
            st.success(res.text)
            
    except Exception as e:
        st.error(f"خطأ: {e}")
