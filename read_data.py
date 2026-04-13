import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder

data = pd.read_csv('RTD_Brew.csv')

def unsup_prep(data):
    mask = (data['คุณดื่มกาแฟหรือไม่'] == 'ไม่ดื่ม') & (data['คุณดื่มชาหรือไม่'] == 'ไม่ดื่ม')
    data = data.drop(data[mask].index).reset_index() #drop where it's not ours customer

    #drop duplicate
    data = data.drop_duplicates()

    #Select necessary features
    coffee_cols = data.columns[54:67]
    tea_cols = data.columns[86:97]
    target_cols = list(coffee_cols) + list(tea_cols)

    #Prepare for training
    X = data[target_cols].copy()
    X = X.fillna(0)
    select_col1 = 'คุณดื่มกาแฟพร้อมดื่ม (Ready to drink) ในโอกาส/โมเมนต์ใดบ้าง (เลือกได้หลายคำตอบ)'
    select_col2 = 'คุณดื่มชาพร้อมดื่ม ในโอกาส/โมเมนต์ใดบ้าง (เลือกได้หลายคำตอบ)'
    X[select_col1]= X[select_col1].replace(0, "ไม่ดื่มกาแฟในโอกาศใดเลย")
    X[select_col2]= X[select_col2].replace(0, "ไม่ดื่มชาในโอกาศใดเลย")

    #Data Cleaning
    skip = [col for col in X.columns if '(เลือกได้หลายคำตอบ)' in col]
    
    for col in X.columns:
        if col in skip: #loop every thing except for col in skip
            continue
        
        #Replace letter with '' but keep number
        cleaned = X[col].astype(str).str.replace(r'\D', '', regex=True)
        X[col] = pd.to_numeric(cleaned, errors='coerce')

    # Rename columns before returning
    # Uncomment and add column names here to rename them
    rename_mapping = {
        # --- กลุ่มกาแฟ (Coffee) ---
        'คุณดื่มกาแฟพร้อมดื่ม (Ready to drink) ในโอกาส/โมเมนต์ใดบ้าง (เลือกได้หลายคำตอบ)': 'C_Occasion',
        'ในการดื่มกาแฟพร้อมดื่ม (Ready to drink) คุณให้ความสำคัญกับคุณสมบัติด้านล่างนี้มากน้อยเพียงใด (5 = สำคัญมากที่สุด) [รสชาติดีเหมือนกาแฟสด]': 'C_Fresh_Taste',
        'ในการดื่มกาแฟพร้อมดื่ม (Ready to drink) คุณให้ความสำคัญกับคุณสมบัติด้านล่างนี้มากน้อยเพียงใด (5 = สำคัญมากที่สุด) [รสชาติเข้มข้น]': 'C_Intense',
        'ในการดื่มกาแฟพร้อมดื่ม (Ready to drink) คุณให้ความสำคัญกับคุณสมบัติด้านล่างนี้มากน้อยเพียงใด (5 = สำคัญมากที่สุด) [รสชาตินุ่มละมุน]': 'C_Smooth',
        'ในการดื่มกาแฟพร้อมดื่ม (Ready to drink) คุณให้ความสำคัญกับคุณสมบัติด้านล่างนี้มากน้อยเพียงใด (5 = สำคัญมากที่สุด) [รสชาติเปรี้ยว]': 'C_Acidic',
        'ในการดื่มกาแฟพร้อมดื่ม (Ready to drink) คุณให้ความสำคัญกับคุณสมบัติด้านล่างนี้มากน้อยเพียงใด (5 = สำคัญมากที่สุด) [กลิ่นหอมกาแฟ]': 'C_Aroma',
        'ในการดื่มกาแฟพร้อมดื่ม (Ready to drink) คุณให้ความสำคัญกับคุณสมบัติด้านล่างนี้มากน้อยเพียงใด (5 = สำคัญมากที่สุด) [ต้องการความดีด/ตื่นตัวจากคาเฟอีน]': 'C_Alert',
        'ในการดื่มกาแฟพร้อมดื่ม (Ready to drink) คุณให้ความสำคัญกับคุณสมบัติด้านล่างนี้มากน้อยเพียงใด (5 = สำคัญมากที่สุด) [แหล่งที่มาของเมล็ดกาแฟ เช่น เมล็ดนำเข้า]': 'C_Origin',
        'ในการดื่มกาแฟพร้อมดื่ม (Ready to drink) คุณให้ความสำคัญกับคุณสมบัติด้านล่างนี้มากน้อยเพียงใด (5 = สำคัญมากที่สุด) [ความสะดวก/พกพาง่าย/ไม่เลอะเทอะ]': 'C_Portable',
        'ในการดื่มกาแฟพร้อมดื่ม (Ready to drink) คุณให้ความสำคัญกับคุณสมบัติด้านล่างนี้มากน้อยเพียงใด (5 = สำคัญมากที่สุด) [ประหยัดกว่ากินกาแฟสดตามร้าน]': 'C_Value',
        'ในการดื่มกาแฟพร้อมดื่ม (Ready to drink) คุณให้ความสำคัญกับคุณสมบัติด้านล่างนี้มากน้อยเพียงใด (5 = สำคัญมากที่สุด) [มีฉลากเห็นข้อมูลโภชนาการ (Nutrition facts)]': 'C_Nutrition',
        'ในการดื่มกาแฟพร้อมดื่ม (Ready to drink) คุณให้ความสำคัญกับคุณสมบัติด้านล่างนี้มากน้อยเพียงใด (5 = สำคัญมากที่สุด) [แบรนด์ดัง น่าเชื่อถือ]': 'C_Brand_Trust',
        'ในการดื่มกาแฟพร้อมดื่ม (Ready to drink) คุณให้ความสำคัญกับคุณสมบัติด้านล่างนี้มากน้อยเพียงใด (5 = สำคัญมากที่สุด) [ภาพลักษณ์ดูดี ดูพรีเมียม]': 'C_Premium_Look',

        # --- กลุ่มชา (Tea) ---
        'คุณดื่มชาพร้อมดื่ม ในโอกาส/โมเมนต์ใดบ้าง (เลือกได้หลายคำตอบ)': 'T_Occasion',
        'ในการดื่มชาพร้อมดื่ม (Ready to drink) คุณให้ความสำคัญกับคุณสมบัติด้านล่างนี้มากน้อยเพียงใด (5 = สำคัญมากที่สุด) [กลิ่นหอมใบชาเขียว]': 'T_Aroma',
        'ในการดื่มชาพร้อมดื่ม (Ready to drink) คุณให้ความสำคัญกับคุณสมบัติด้านล่างนี้มากน้อยเพียงใด (5 = สำคัญมากที่สุด) [รสชาติชาเขียวเข้มข้น]': 'T_Intense',
        'ในการดื่มชาพร้อมดื่ม (Ready to drink) คุณให้ความสำคัญกับคุณสมบัติด้านล่างนี้มากน้อยเพียงใด (5 = สำคัญมากที่สุด) [ไม่เติมน้ำตาล/ไม่มีน้ำตาล]': 'T_No_Sugar',
        'ในการดื่มชาพร้อมดื่ม (Ready to drink) คุณให้ความสำคัญกับคุณสมบัติด้านล่างนี้มากน้อยเพียงใด (5 = สำคัญมากที่สุด) [ไม่มีแคลอรี่ (0 kcal)]': 'T_Zero_Cal',
        'ในการดื่มชาพร้อมดื่ม (Ready to drink) คุณให้ความสำคัญกับคุณสมบัติด้านล่างนี้มากน้อยเพียงใด (5 = สำคัญมากที่สุด) [มีฉลากเห็นข้อมูลโภชนาการ (Nutrition facts)]': 'T_Nutrition',
        'ในการดื่มชาพร้อมดื่ม (Ready to drink) คุณให้ความสำคัญกับคุณสมบัติด้านล่างนี้มากน้อยเพียงใด (5 = สำคัญมากที่สุด) [แหล่งที่มาของใบชา เช่น ญี่ปุ่น]': 'T_Origin',
        'ในการดื่มชาพร้อมดื่ม (Ready to drink) คุณให้ความสำคัญกับคุณสมบัติด้านล่างนี้มากน้อยเพียงใด (5 = สำคัญมากที่สุด) [วิธีการชง/สกัดชาเขียว เช่น สกัดเย็น]': 'T_Brew_Method',
        'ในการดื่มชาพร้อมดื่ม (Ready to drink) คุณให้ความสำคัญกับคุณสมบัติด้านล่างนี้มากน้อยเพียงใด (5 = สำคัญมากที่สุด) [ความสะดวก/พกพาง่าย/ไม่เลอะเทอะ]': 'T_Portable',
        'ในการดื่มชาพร้อมดื่ม (Ready to drink) คุณให้ความสำคัญกับคุณสมบัติด้านล่างนี้มากน้อยเพียงใด (5 = สำคัญมากที่สุด) [แบรนด์ดัง น่าเชื่อถือ]': 'T_Brand_Trust',
        'ในการดื่มชาพร้อมดื่ม (Ready to drink) คุณให้ความสำคัญกับคุณสมบัติด้านล่างนี้มากน้อยเพียงใด (5 = สำคัญมากที่สุด) [ภาพลักษณ์ดูดี ดูพรีเมียม]': 'T_Premium_Look'
    }

    X = X.rename(columns=rename_mapping)

    return X   

X = unsup_prep(data)
# X.to_csv("Unsupervised.csv", index=False)


data2 = pd.read_csv('unsupervised_results.csv')
df = pd.merge(X, data2, left_index=True, right_index=True)

def sup_prep(df, data2):
    mask = (df['คุณดื่มกาแฟหรือไม่'] == 'ไม่ดื่ม') & (df['คุณดื่มชาหรือไม่'] == 'ไม่ดื่ม')
    df = df.drop(df[mask].index).reset_index() #drop where it's not ours customer

    df['Cluster_ID'] = data2['Cluster_ID']

    #drop duplicate
    df = df.drop_duplicates()

    media_cols = df[['อายุ', 'อาชีพ', 'เพศ',
       'ความถี่ในการเปิดรับสื่อในแต่ละช่องทางต่อสัปดาห์ [ออนไลน์]',       
       'ระยะเวลาในการเสพสื่อต่อวัน ในแต่ละช่องทาง [ออนไลน์]',
       'ในวันหยุดยาวหรือเทศกาล คุณใช้โซเชียลมีเดีย อย่างไร', 'Cluster_ID']].copy()

    # Separating columns for Different Encodings
    binary_cols = ['อาชีพ', 'เพศ', 'ในวันหยุดยาวหรือเทศกาล คุณใช้โซเชียลมีเดีย อย่างไร', 'Cluster_ID']
    label_cols = ['อายุ' ,'ความถี่ในการเปิดรับสื่อในแต่ละช่องทางต่อสัปดาห์ [ออนไลน์]', 'ระยะเวลาในการเสพสื่อต่อวัน ในแต่ละช่องทาง [ออนไลน์]']

    # OneHot (Binary) Encode
    ohe = OneHotEncoder(sparse_output=False)
    media_cols_binary = ohe.fit_transform(media_cols[binary_cols].astype(str))
    media_cols_binary_df = pd.DataFrame(media_cols_binary, columns=ohe.get_feature_names_out(binary_cols))

    # Label Encode
    le = LabelEncoder()
    media_cols_label_df = media_cols[label_cols].copy().reset_index(drop=True)
    for col in label_cols:
        media_cols_label_df[col] = le.fit_transform(media_cols_label_df[col].astype(str))
    
    # Combine back into media_cols
    media_cols = pd.concat([media_cols_binary_df, media_cols_label_df], axis=1)

    period_cols = df[['อายุ', 'อาชีพ', 'เพศ', 'คุณใช้โซเชียลมีเดียใดบ่อยที่สุด',
       'โปรดพิมพ์จังหวัดที่อยู่อาศัยของคุณ เช่น กทม , ขอนแก่น, ชลบุรี',
       'คุณดื่มกาแฟประเภทใดบ่อยที่สุด',
       'คุณดื่มกาแฟพร้อมดื่ม (Ready to drink) ในโอกาส/โมเมนต์ใดบ้าง (เลือกได้หลายคำตอบ)', 'Cluster_ID']].copy()
    
    period_cols = period_cols.rename(columns={
    'โปรดพิมพ์จังหวัดที่อยู่อาศัยของคุณ เช่น กทม , ขอนแก่น, ชลบุรี': 'province'
    })

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

    #Keep first element drop the rest
    period_cols['province'] = period_cols['province'].str.split(',').str[0].str.strip().str.lower()

    #Mapping
    period_cols['province'] = period_cols['province'].map(mapping).fillna(period_cols['province'])
    period_cols['คุณดื่มกาแฟประเภทใดบ่อยที่สุด'] = period_cols['คุณดื่มกาแฟประเภทใดบ่อยที่สุด'].fillna('ไม่ดื่มกาแฟประเภทใดเลย')

    #Check
    # print(period_cols.info())

    # Separating columns for Different Encodings
    binary_cols = ['อาชีพ', 'เพศ', 'province', 'คุณดื่มกาแฟประเภทใดบ่อยที่สุด', 'คุณดื่มกาแฟพร้อมดื่ม (Ready to drink) ในโอกาส/โมเมนต์ใดบ้าง (เลือกได้หลายคำตอบ)', 'Cluster_ID']
    label_cols = ['อายุ']

    # OneHot (Binary) Encode
    ohe = OneHotEncoder(sparse_output=False)
    period_cols_binary = ohe.fit_transform(period_cols[binary_cols].astype(str))
    period_cols_binary_df = pd.DataFrame(period_cols_binary, columns=ohe.get_feature_names_out(binary_cols))

    # Label Encode
    le = LabelEncoder()
    period_cols_label_df = period_cols[label_cols].copy().reset_index(drop=True)
    for col in label_cols:
        period_cols_label_df[col] = le.fit_transform(period_cols_label_df[col].astype(str))
    
    # Combine back into period_cols
    period_cols = pd.concat([period_cols_binary_df, period_cols_label_df], axis=1)
    
    return media_cols, period_cols

media_cols, period_cols = sup_prep(data, data2)
media_cols.to_csv("Media.csv", index=False)
period_cols.to_csv("Period.csv", index=False)