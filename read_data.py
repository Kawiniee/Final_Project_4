import pandas as pd
from sklearn.preprocessing import LabelEncoder

data = pd.read_csv('RTD_Brew.csv')

def unsup_prep(data):
    mask = (data['คุณดื่มกาแฟหรือไม่'] == 'ไม่ดื่ม') & (data['คุณดื่มชาหรือไม่'] == 'ไม่ดื่ม')
    data = data.drop(data[mask].index).reset_index() #drop where it's not ours customer

    #select necessary features
    coffee_cols = data.columns[54:67]
    tea_cols = data.columns[86:97]
    target_cols = list(coffee_cols) + list(tea_cols)

    #prepare for training
    X = data[target_cols].copy()

    #Data Cleaning
    skip = [col for col in X.columns if '(เลือกได้หลายคำตอบ)' in col]
    
    for col in X.columns:
        if col in skip: #loop every thing except for col in skip
            continue
        
        #Replace letter with '' but keep number
        cleaned = X[col].astype(str).str.replace(r'\D', '', regex=True)
        X[col] = pd.to_numeric(cleaned, errors='coerce')

    return X   
X = unsup_prep(data)
# X.to_excel("Clustering.xlsx")

def sup_prep(data):
    media_cols = data[['อายุ', 'อาชีพ',
       'ความถี่ในการเปิดรับสื่อในแต่ละช่องทางต่อสัปดาห์ [ออนไลน์]',       
       'ระยะเวลาในการเสพสื่อต่อวัน ในแต่ละช่องทาง [ออนไลน์]',
       'ในวันหยุดยาวหรือเทศกาล คุณใช้โซเชียลมีเดีย อย่างไร']].copy()

    #Encode
    for col in media_cols.columns:
        le = LabelEncoder()
        media_cols[col] = le.fit_transform(media_cols[col].astype(str))

    period_cols = data[['อายุ', 'คุณใช้โซเชียลมีเดียใดบ่อยที่สุด',
       'โปรดพิมพ์จังหวัดที่อยู่อาศัยของคุณ เช่น กทม , ขอนแก่น, ชลบุรี',   
       'คุณดื่มกาแฟประเภทใดบ่อยที่สุด',
       'คุณดื่มกาแฟพร้อมดื่ม (Ready to drink) ในโอกาส/โมเมนต์ใดบ้าง (เลือกได้หลายคำตอบ)']].copy()

    mapping = {
        'กทม': 'กรุงเทพมหานคร',
        'กทม.': 'กรุงเทพมหานคร',
        'กรุงเทพ': 'กรุงเทพมหานคร',
        'กมม': 'กรุงเทพมหานคร',
        'bkk': 'กรุงเทพมหานคร',
        'bangkok': 'กรุงเทพมหานคร',
        'dกทม': 'กรุงเทพมหานคร',
        'แอลเอ': 'ร้อยเอ็ด',
        'bonn': 'อุบลราชธานี'
    }
    for col in period_cols.columns:
        period_cols[col] = period_cols[col].str.strip().str.lower()
        period_cols[col] = period_cols[col].replace(mapping)
        period_cols[col] = period_cols[col].str.split(r'[,\s]+')
        

    print(period_cols['โปรดพิมพ์จังหวัดที่อยู่อาศัยของคุณ เช่น กทม , ขอนแก่น, ชลบุรี'].value_counts(dropna=False))
    # print(period_cols['คุณดื่มกาแฟประเภทใดบ่อยที่สุด'].value_counts(dropna=False))

    return period_cols

period_cols = sup_prep(data)
# period_cols.to_excel("Text.xlsx", index=False)