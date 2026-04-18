import streamlit as st
import pandas as pd

st.title("📊 محرر الملفات النصية المرن")
st.write("ارفع ملفك وحدد الأعمدة التي تريد تجميعها بنفسك")

# رفع الملف
uploaded_file = st.file_uploader("اختر ملف PEOF01COMP.txt", type=['txt'])

if uploaded_file:
    # قراءة الأسطر كقائمة
    lines = uploaded_file.readlines()
    lines = [line.decode('utf-8') for line in lines]
    
    st.info(f"تم تحميل {len(lines)} سطر.")

    # معاينة السطر الأول لفهم الترتيب
    st.subheader("🔍 معاينة السطر الأول (للمساعدة في التحديد)")
    sample_line = lines[0]
    st.code(sample_line)
    st.caption("تلميح: كل حرف أو رقم يمثل موضعاً (0, 1, 2...)")

    # التحكم في إحداثيات العمود
    st.subheader("⚙️ التحكم في العمود")
    col1, col2 = st.columns(2)
    with col1:
        start_pos = st.number_input("بداية العمود (رقم الحرف):", min_value=0, value=10)
    with col2:
        end_pos = st.number_input("نهاية العمود (رقم الحرف):", min_value=start_pos+1, value=25)

    # استخراج البيانات بناءً على التحكم
    data_list = []
    for line in lines:
        if len(line) >= end_pos:
            val = line[start_pos:end_pos].strip()
            # محاولة تحويل القيمة لرقم
            try:
                data_list.append(float(val))
            except ValueError:
                continue

    # عرض النتائج
    if data_list:
        df_result = pd.DataFrame(data_list, columns=["القيم المستخرجة"])
        
        col_res1, col_res2 = st.columns(2)
        col_res1.metric("إجمالي المجموع", f"{sum(data_list):,.2f}")
        col_res2.metric("عدد السطور المعالجة", len(data_list))
        
        st.dataframe(df_result)
    else:
        st.warning("لم يتم العثور على قيم رقمية في الإحداثيات المختارة.")
