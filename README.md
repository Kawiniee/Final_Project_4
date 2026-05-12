# AI-Driven Marketing Campaign System

โปรเจกต์นี้เป็น Dashboard สำหรับวิเคราะห์กลุ่มลูกค้าและช่วยวางแผนแคมเปญการตลาดสินค้า Ready-to-Drink (RTD) โดยใช้ข้อมูลพฤติกรรมผู้บริโภค ร่วมกับผลลัพธ์จาก Machine Learning ทั้งแบบ Unsupervised Learning และ Supervised Learning

ระบบถูกพัฒนาด้วย Dash และ Dash Bootstrap Components พร้อมหน้าเว็บหลัก 4 ส่วน ได้แก่ Home, Unsupervised Learning, Business Insight และ Supervised Learning

## ความสามารถหลัก

- แสดงภาพรวมจำนวนลูกค้า จำนวน cluster และประสิทธิภาพของโมเดล
- วิเคราะห์การแบ่งกลุ่มลูกค้าด้วย K-Means Clustering
- แสดงกราฟ insight สำหรับการวางแผนแคมเปญ RTD
- ทำนาย segment ของลูกค้าจากข้อมูลที่กรอกในหน้าเว็บแบบรายคน
- อัปโหลดไฟล์ CSV ข้อมูลดิบเพื่อทำนาย segment หลายรายการพร้อมกัน
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

หน้า Prediction สำหรับใช้โมเดลที่เทรนไว้ทำนาย segment ของลูกค้า โดยแบ่งเป็น 2 โหมด:

#### Single Prediction

กรอกข้อมูลพฤติกรรมลูกค้าทีละคน เช่น อายุ ความถี่การใช้โซเชียลมีเดีย แพลตฟอร์มที่ใช้ประจำ ประเภทกาแฟ/ชาที่ชอบ และช่องทางซื้อชา จากนั้นระบบจะทำนายกลุ่มลูกค้าพร้อม probability และ campaign recommendation

#### Batch Prediction

อัปโหลดไฟล์ CSV ข้อมูลดิบรูปแบบเดียวกับ `RTD_Brew.csv` แล้วระบบจะ:

- อ่านและจัดคอลัมน์สำคัญจากไฟล์อัตโนมัติ
- แปลงคำตอบให้ตรงกับ feature ที่โมเดลใช้
- ทำนาย segment ให้ทุกแถวในไฟล์
- แสดงสรุปจำนวนลูกค้าแต่ละกลุ่ม
- แสดง preview ผลลัพธ์ 10 แถวแรก
- ดาวน์โหลดไฟล์ CSV ผลลัพธ์ที่มี `Predicted_Segment` และ probability ของแต่ละกลุ่ม

กลุ่มลูกค้าที่ระบบทำนาย ได้แก่:

- ชอบกาแฟ
- ชอบชา
- ชอบทั้งกาแฟและชา

ระบบยังคงรองรับการใช้งานแบบกรอกทีละคนไว้ เพื่อให้ทดลอง prediction ได้รวดเร็วโดยไม่ต้องเตรียมไฟล์ CSV

## โมเดลที่ใช้

หน้า Supervised Learning ใช้โมเดลที่บันทึกไว้ในโฟลเดอร์ `models/`

- `customer_model.pkl` โมเดลสำหรับทำนายกลุ่มลูกค้า
- `feature_cols.pkl` รายชื่อ feature ที่โมเดลใช้
- `label_encoder.pkl` ตัวแปลง label ของผลลัพธ์

เมื่อผู้ใช้กรอกข้อมูลหรืออัปโหลดไฟล์ CSV ระบบจะแปลงคำตอบเป็น feature vector ตาม `feature_cols.pkl` แล้วเรียกใช้ `model.predict_proba()` เพื่อทำนายกลุ่มลูกค้า

ในโหมด Batch Prediction ระบบจะใช้คอลัมน์สำคัญจากไฟล์ดิบ เช่น:

- อายุ
- ความถี่และระยะเวลาการใช้สื่อออนไลน์
- โซเชียลมีเดียที่ใช้บ่อยที่สุด
- ประเภทกาแฟและชาที่ดื่ม/ชอบ
- โอกาสในการดื่มกาแฟและชาพร้อมดื่ม
- ช่องทางซื้อชาพร้อมดื่ม

## Firebase

โปรเจกต์นี้เชื่อม Firebase Realtime Database แบบ `write-only` เพื่อบันทึกผลการทำนายจากหน้า Supervised โดยไม่ทำให้หน้าเว็บล้มถ้าฐานข้อมูลมีปัญหา

### ไฟล์ที่ต้องมี

- `.env` ที่ระบุค่าต่อไปนี้:

```env
FIREBASE_KEY_PATH=Your_Service_Account_Key.json
FIREBASE_DB_URL=https://your-project-default-rtdb.asia-southeast1.firebasedatabase.app/
```

### ข้อมูลที่ระบบบันทึก

- โหมดการทำนาย (`single` หรือ `batch`)
- เวลาที่ทำนาย
- ค่าที่ใช้ทำนาย
- ผล segment ที่ทำนายได้
- probability ของแต่ละกลุ่ม
- สำหรับ batch: ชื่อไฟล์ จำนวนแถว และสรุปจำนวนแต่ละ segment

### หมายเหตุ

- ถ้า key หรือ URL ไม่พร้อม ระบบยังใช้งาน prediction ได้ตามปกติ

## การติดตั้ง

ติดตั้ง dependencies ที่จำเป็น:

```bash
pip install dash dash-bootstrap-components pandas numpy joblib scikit-learn xgboost
```

## การ Deploy บน Render

โปรเจกต์นี้ deploy บน Render และสามารถเข้าใช้งานได้ที่:

```text
https://project-444444.onrender.com
```

### สำหรับ Local Development

รันคำสั่ง:

```bash
python app.py
```

จากนั้นเปิดเว็บเบราว์เซอร์ที่:

```text
http://localhost:8050
```

### สำหรับ Deploy บน Render

1. Push โค้ดขึ้น GitHub repository
2. เข้าเว็บ [Render Dashboard](https://dashboard.render.com/)
3. สร้าง Web Service ใหม่ เลือก GitHub repository
4. ตั้งค่า:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:server --workers 4 --threaded`
5. เพิ่ม Environment Variables:
   - `FIREBASE_KEY_PATH` (ถ้ามี Firebase)
   - `FIREBASE_DB_URL` (ถ้ามี Firebase)
6. Deploy และรอจนเสร็จ

## หมายเหตุ

- ไฟล์ข้อมูลและโมเดลต้องอยู่ในตำแหน่งตามโครงสร้างโปรเจกต์
- โหมด Single Prediction ใช้เฉพาะ feature ที่ผู้ใช้กรอกในฟอร์ม ส่วน feature อื่นจะถูกกำหนดค่าเริ่มต้นเป็น 0
- โหมด Batch Prediction เหมาะกับการทำนายจากข้อมูลดิบที่มี field ครบกว่า และให้ผลใกล้เคียง pipeline จริงมากกว่าโหมดกรอกทีละคน
- หากไฟล์ CSV มี category ใหม่ที่โมเดลไม่เคยเห็น ระบบจะข้าม feature นั้นและยังทำนายต่อได้
- หากมีการเทรนโมเดลใหม่ ควรอัปเดตไฟล์ใน `models/` ให้ตรงกับ `feature_cols.pkl` และ `label_encoder.pkl`
