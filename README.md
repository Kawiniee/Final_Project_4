# AI-Driven Marketing Campaign System

โปรเจกต์นี้เป็น Dashboard สำหรับวิเคราะห์กลุ่มลูกค้าและช่วยวางแผนแคมเปญการตลาดสินค้า Ready-to-Drink (RTD) โดยใช้ข้อมูลพฤติกรรมผู้บริโภค ร่วมกับผลลัพธ์จาก Machine Learning ทั้งแบบ Unsupervised Learning และ Supervised Learning

ระบบถูกพัฒนาด้วย Dash และ Dash Bootstrap Components พร้อมหน้าเว็บหลัก 4 ส่วน ได้แก่ Home, Unsupervised Learning, Business Insight และ Supervised Learning

## ความสามารถหลัก

- แสดงภาพรวมจำนวนลูกค้า จำนวน cluster และประสิทธิภาพของโมเดล
- วิเคราะห์การแบ่งกลุ่มลูกค้าด้วย K-Means Clustering
- แสดงกราฟ insight สำหรับการวางแผนแคมเปญ RTD
- ทำนาย segment ของลูกค้าจากข้อมูลที่กรอกในหน้าเว็บ
- แนะนำ campaign direction ตามกลุ่มลูกค้าที่โมเดลทำนายได้

## โครงสร้างโปรเจกต์

```text
Final_Project_4/
├── app.py
├── assets/
│   ├── style.css
│   └── charts/
├── data/
│   ├── cleaned_data.csv
│   ├── encoded_data.csv
│   └── unsupervised_results.csv
├── models/
│   ├── customer_model.pkl
│   ├── feature_cols.pkl
│   └── label_encoder.pkl
├── notebooks/
│   ├── business_insight.ipynb
│   ├── supervised.ipynb
│   └── unsupervised.ipynb
├── pages/
│   ├── home.py
│   ├── unsupervised.py
│   ├── business_insight.py
│   └── supervised.py
└── scripts/
    ├── cleaned_data.py
    ├── firebase_config.py
    └── retrain.py
```

## รายละเอียดหน้า Dashboard

### 1. Home

หน้าแรกของระบบ แสดงภาพรวมสำคัญของโปรเจกต์ เช่น จำนวนลูกค้า จำนวน cluster ความแม่นยำของโมเดล และสรุปกลุ่มลูกค้าหลัก เพื่อให้เข้าใจภาพรวมก่อนเข้าสู่หน้าวิเคราะห์เชิงลึก

### 2. Unsupervised Learning

แสดงผลการแบ่งกลุ่มลูกค้าด้วย K-Means Clustering ประกอบด้วย:

- Correlation Analysis
- Elbow Method และ Silhouette Score
- PCA Scatter Plot
- Cluster Profiling Heatmap
- Customer Persona ของแต่ละกลุ่ม

### 3. Business Insight

รวบรวมกราฟและข้อสรุปเชิงธุรกิจสำหรับการวางแผน campaign เช่น ช่องทางโฆษณาที่มีอิทธิพล แพลตฟอร์มที่ลูกค้าใช้งาน และพฤติกรรมช่วงเทศกาล

### 4. Supervised Learning

หน้า Prediction สำหรับกรอกข้อมูลพฤติกรรมลูกค้า แล้วใช้โมเดลที่เทรนไว้ทำนาย segment ได้แก่:

- ชอบกาแฟ
- ชอบชา
- ชอบทั้งกาแฟและชา

ระบบจะแสดงผลลัพธ์พร้อม probability ของแต่ละกลุ่ม และ campaign recommendation ที่เหมาะสม

## โมเดลที่ใช้

หน้า Supervised Learning ใช้โมเดลที่บันทึกไว้ในโฟลเดอร์ `models/`

- `customer_model.pkl` โมเดลสำหรับทำนายกลุ่มลูกค้า
- `feature_cols.pkl` รายชื่อ feature ที่โมเดลใช้
- `label_encoder.pkl` ตัวแปลง label ของผลลัพธ์

เมื่อผู้ใช้กรอกข้อมูลในหน้าเว็บ ระบบจะแปลงคำตอบเป็น feature vector แล้วเรียกใช้ `model.predict_proba()` เพื่อทำนายกลุ่มลูกค้า

## การติดตั้ง

ติดตั้ง dependencies ที่จำเป็น:

```bash
pip install dash dash-bootstrap-components pandas numpy joblib scikit-learn xgboost
```

## การรันโปรเจกต์

รันคำสั่ง:

```bash
python app.py
```

จากนั้นเปิดเว็บเบราว์เซอร์ที่:

```text
http://localhost:8050
```

## หมายเหตุ

- ไฟล์ข้อมูลและโมเดลต้องอยู่ในตำแหน่งตามโครงสร้างโปรเจกต์
- หน้า Predict ใช้ feature บางส่วนที่ผู้ใช้กรอก ส่วน feature ที่ไม่ได้กรอกจะถูกกำหนดค่าเริ่มต้นเป็น 0
- หากมีการเทรนโมเดลใหม่ ควรอัปเดตไฟล์ใน `models/` ให้ตรงกับ `feature_cols.pkl` และ `label_encoder.pkl`
