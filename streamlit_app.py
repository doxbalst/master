import streamlit as st
import pandas as pd
import plotly.express as px

# إعدادات الصفحة
st.set_page_config(page_title="محلل ملفات PEOF المتقدم", layout="wide")

st.title("🚀 محرك استخراج البيانات المتقدم")
st.markdown("---")

# رفع الملف
uploaded_file = st.sidebar.file_uploader("ارفع الملف النصي هنا", type=['txt'])

if uploaded_file:
    # قراءة الملف
    lines = [line.decode('utf-8') for line in uploaded_file.readlines()]
    
    # واجهة التحكم في الجانب الأيسر (Sidebar)
    st.sidebar.header("⚙️ إعدادات الأعمدة")
    col_start = st.sidebar.number_input("نقطة البداية (Character Start)", 0, 100, 10)
    col_end = st.sidebar.number_input("نهاية العمود (Character End)", col_start + 1, 100, 25)
    column_name = st.sidebar.text_input("اسم العمود المستخرج", "المبالغ المالية")

    # معالجة البيانات
    extracted_data = []
    original_lines = []
    
    for line in lines:
        if len(line) >= col_end:
            segment = line[col_start:col_end].strip()
            try:
                # تحويل وتنظيف القيمة
                val = float(segment)
                extracted_data.append(val)
                original_lines.append(line.strip())
            except ValueError:
                continue

    # إنشاء DataFrame
    df = pd.DataFrame({
        "السطر الأصلي": original_lines,
        column_name: extracted_data
    })

    # العرض المرئي للنتائج
    col1, col2, col3 = st.columns(3)
    col1.metric("إجمالي المجموع", f"{sum(extracted_data):,.2f}")
    col2.metric("متوسط القيم", f"{sum(extracted_data)/len(extracted_data):,.2f}" if extracted_data else 0)
    col3.metric("عدد السطور", len(extracted_data))

    st.markdown("---")

    # تقسيم الشاشة: الجدول والرسوم البيانية
    tab1, tab2 = st.tabs(["📊 تحليل البيانات", "📋 الجدول المستخرج"])
    
    with tab1:
        if not df.empty:
            fig = px.histogram(df, x=column_name, title="توزيع القيم المستخرجة", color_discrete_sequence=['#00CC96'])
            st.plotly_chart(fig, use_container_width=True)
            
            fig2 = px.line(df, y=column_name, title="تسلسل القيم عبر الملف")
            st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        st.dataframe(df, use_container_width=True)
        
        # زر التحميل لملف Excel
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 تحميل البيانات كـ Excel (CSV)",
            data=csv,
            file_name='extracted_report.csv',
            mime='text/csv',
        )

else:
    st.info("💡 يرجى رفع الملف من القائمة الجانبية للبدء في تحليل الأعمدة.")
    st.image("https://via.placeholder.com/800x400.png?text=Waiting+for+File+Upload...", use_column_width=True)
