import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder

data = pd.read_csv('RTD_Brew.csv')
# segmented = pd.read_csv('unsupervised_results.csv')

print("----- Check Raw Data -----")
print(data.info())
print("----- Check Unsupervised -----")
# print(segmented.info())

def data_prep(data):
# for unsupervised
    mask = (data['คุณดื่มกาแฟหรือไม่'] == 'ไม่ดื่ม') & (data['คุณดื่มชาหรือไม่'] == 'ไม่ดื่ม')
    data = data.drop(data[mask].index).reset_index() #drop where it's not ours customer

    #drop duplicate
    data = data.drop_duplicates()

    #Select necessary features
    coffee_cols = data.columns[54:67]
    tea_cols = data.columns[86:97]
    target_cols = coffee_cols.append(tea_cols)

    for col in target_cols:
        if "(5 = สำคัญมากที่สุด)" in col:
        # \D removes all non-digits
            data[col] = pd.to_numeric(
                data[col].astype(str).str.replace(r'\D', '', regex=True), 
                errors='coerce'
        )
    
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

    data = data.rename(columns=rename_mapping)
    data = data[list(rename_mapping.values())].copy()

    data['C_Occasion'] = data['C_Occasion'].fillna('ไม่ดื่มกาแฟ')
    data['T_Occasion'] = data['T_Occasion'].fillna('ไม่ดื่มชา')
    data = data.fillna(0)
    print('----- Check missing data -----')
    print(data.isna().sum())

#for supervised
    data["Cluster_ID"] = segmented["Cluster_ID"]

    #rename some more columns
    data = data.rename(columns={'อายุ': 'Age', 'อาชีพ': 'Profession', 'เพศ': 'Sex',
                                'โปรดพิมพ์จังหวัดที่อยู่อาศัยของคุณ เช่น กทม , ขอนแก่น, ชลบุรี': 'Province',
                                'คุณดื่มกาแฟประเภทใดบ่อยที่สุด': 'C_Frequency',
                                'คุณใช้โซเชียลมีเดียใดบ่อยที่สุด': 'S_Occasion',
                                'ความถี่ในการเปิดรับสื่อในแต่ละช่องทางต่อสัปดาห์ [ออนไลน์]': 'S_Frequency',
                                'ระยะเวลาในการเสพสื่อต่อวัน ในแต่ละช่องทาง [ออนไลน์]': 'S_Screentime',
                                'ในวันจันทร์-ศุกร์ (Weekday) ช่วงเวลาใดที่คุณเปิดรับสื่อแต่ละช่องทาง [ออนไลน์]': 'S_Time(weekday)',
                                'ในวันหยุดเสาร์-อาทิตย์ (Weekend) ช่วงเวลาใดที่คุณเปิดรับสื่อแต่ละช่องทาง [ออนไลน์]': 'S_Time(weekend)',
                                'ในวันหยุดยาวหรือเทศกาล คุณใช้โซเชียลมีเดีย อย่างไร': 'S_Usage(festival)'})
    
    features = data[['Age', 'Profession', 'Sex',
        'Province',
        'S_Occasion',
        'C_Occasion',
        'C_Frequency',
        'S_Frequency',       
        'S_Screentime',
        'S_Time(weekday)',
        'S_Time(weekend)',
        'S_Usage(festival)', 'Cluster_ID']].copy()
    
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
    features['Province'] = features['Province'].str.split(',').str[0].str.strip().str.lower()

    #Mapping
    features['Province'] = features['Province'].map(mapping).fillna(features['Province'])
    features['C_Frequency'] = features['C_Frequency'].fillna('ไม่ดื่มกาแฟประเภทใดเลย')

    # Separating columns for Different Encodings
    features_binary = ['Profession', 'Sex', 'S_Usage(festival)', 'Province', 'C_Occasion', 'C_Frequency', 'Cluster_ID']
    features_label = ['Age' ,'S_Frequency', 'S_Time(weekday)', 'S_Time(weekend)', 'S_Screentime']

    # OneHot (Binary) Encode
    ohe = OneHotEncoder(sparse_output=False)
    features_cols_binary = ohe.fit_transform(features[features_binary].astype(str))
    features_cols_binary_df = pd.DataFrame(features_cols_binary, columns=ohe.get_feature_names_out(features_binary))

    # Label Encode
    le = LabelEncoder()
    features_cols_label_df = features[features_label].copy().reset_index(drop=True)
    for col in features_label:
        features_cols_label_df[col] = le.fit_transform(features_cols_label_df[col].astype(str))
    
    # Combine back into period_cols
    features = pd.concat([features_cols_binary_df, features_cols_label_df], axis=1)
    print("----- Check Encoded features -----")
    print(features)

    return data

data = data_prep(data)
# features.to_csv('for_supervised.csv', index=False)
data.to_csv('for_unsupervised.csv', index=False)