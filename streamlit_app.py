
import streamlit as st
import pandas as pd

# إعداد واجهة التطبيق
st.set_page_config(page_title="مستخرج الأعمدة المتعدد", layout="wide")

st.title("📑 تطبيق استخراج وتحليل الأعمدة الأربعة")
st.write("ارفع ملفك النصي وحدد نطاق كل عمود من الأعمدة الأربعة للقيام بالحسابات")

# رفع الملف
uploaded_file = st.file_uploader("اختر ملفك النصي (TXT)", type=['txt'])

if uploaded_file:
    # قراءة محتوى الملف
    content = uploaded_file.read().decode("utf-8")
    lines = content.splitlines()
    
    st.sidebar.header("⚙️ إعدادات الأعمدة الأربعة")
    
    # واجهة التحكم للأعمدة الأربعة في الشريط الجانبي
    configs = []
    for i in range(1, 5):
        st.sidebar.subheader(f"العمود {i}")
        col_name = st.sidebar.text_input(f"اسم العمود {i}", f"Column_{i}", key=f"name_{i}")
        start = st.sidebar.number_input(f"بداية الحرف (Start)", 0, 500, value=(i-1)*10, key=f"s_{i}")
        end = st.sidebar.number_input(f"نهاية الحرف (End)", start + 1, 500, value=i*10, key=f"e_{i}")
        configs.append({"name": col_name, "start": start, "end": end})

    # معالجة البيانات وتحويلها لأعمدة
    table_data = []
    for line in lines:
        row = {}
        for conf in configs:
            # استخراج النص بناءً على النطاق المحدد
            val_text = line[conf['start']:conf['end']].strip()
            # محاولة تحويله لرقم، إذا فشل نضعه كـ 0 لكي لا يتوقف الحساب
            try:
                val_num = float(val_text)
            except ValueError:
                val_num = 0.0
            row[conf['name']] = val_num
        table_data.append(row)

    # تحويل البيانات إلى DataFrame (جدول)
    df = pd.DataFrame(table_data)

    # عرض الإحصائيات (المجموع) لكل عمود
    st.subheader("📊 نتائج الحسابات الإجمالية")
    metrics_cols = st.columns(4)
    for idx, conf in enumerate(configs):
        total = df[conf['name']].sum()
        metrics_cols[idx].metric(label=f"مجموع {conf['name']}", value=f"{total:,.2f}")

    st.divider()

    # عرض الجدول النهائي
    st.subheader("📋 الجدول المستخرج")
    st.dataframe(df, use_container_width=True)

    # خيار تحميل النتيجة
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 تحميل النتائج (Excel/CSV)", csv, "results.csv", "text/csv")

else:
    st.info("يرجى رفع الملف البدء في استخراج الأعمدة.")
