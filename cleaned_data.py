import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder, MultiLabelBinarizer

data = pd.read_csv('RTD_Brew.csv')
segmented = pd.read_csv('unsupervised_results.csv')

print("========== Check Raw Data ==========")
print(data.info())

# print("========== Check Unsupervised ==========")
print(segmented.info())

def data_prep(data):
    # Filter
    mask = (data['คุณดื่มกาแฟหรือไม่'] == 'ไม่ดื่ม') & (data['คุณดื่มชาหรือไม่'] == 'ไม่ดื่ม')
    data = data.drop(data[mask].index).reset_index() #drop where it's not ours customer

    # Drop duplicate
    data = data.drop_duplicates()

    for col in data:
        if "(5 = สำคัญมากที่สุด)" in col:
        # \D removes all non-digits
            data[col] = pd.to_numeric(
                data[col].astype(str).str.replace(r'\D', '', regex=True), 
                errors='coerce'
        )
            
    rename_mapping = {
        # --- กลุ่ม general and โซเชียลมีเดีย (Social) ---
        'อายุ': 'Age', 'อาชีพ': 'Profession', 'เพศ': 'Sex',
        'โปรดพิมพ์จังหวัดที่อยู่อาศัยของคุณ เช่น กทม , ขอนแก่น, ชลบุรี': 'Province',
        'คุณใช้โซเชียลมีเดียใดบ่อยที่สุด': 'S_Occasion',
        'ความถี่ในการเปิดรับสื่อในแต่ละช่องทางต่อสัปดาห์ [ออนไลน์]': 'S_Frequency',
        'ระยะเวลาในการเสพสื่อต่อวัน ในแต่ละช่องทาง [ออนไลน์]': 'S_Screentime',
        'ในวันจันทร์-ศุกร์ (Weekday) ช่วงเวลาใดที่คุณเปิดรับสื่อแต่ละช่องทาง [ออนไลน์]': 'S_Time(weekday)',
        'ในวันหยุดเสาร์-อาทิตย์ (Weekend) ช่วงเวลาใดที่คุณเปิดรับสื่อแต่ละช่องทาง [ออนไลน์]': 'S_Time(weekend)',
        'ในวันหยุดยาวหรือเทศกาล คุณใช้โซเชียลมีเดีย อย่างไร': 'S_Usage(festival)',
        'การรับชมโฆษณาผ่านช่องทางใดที่มีอิทธิพลต่อการตัดสินใจซื้อผลิตภัณฑ์ (เลือกได้หลายคำตอบ)': 'S_Influence',

        # --- กลุ่มกาแฟ (Coffee) ---
        'คุณดื่มกาแฟประเภทใดบ่อยที่สุด': 'C_Frequency',
        'คุณชอบกาแฟประเภทใดมากที่สุด': 'C_Favorite',  
        'คุณดื่มกาแฟพร้อมดื่ม (Ready to drink) แบรนด์ใดบ่อยที่สุด': 'C_BestBrand',
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
        'คุณดื่มชาประเภทใดบ่อยที่สุด': 'T_Frequency', 
        'คุณชอบดื่มชาประเภทใดมากที่สุด': 'T_Favorite',    
        'จากตัวเลือกด้านบน รบกวนบอกเหตุผลสั้นๆ ทำไมคุณถึงชอบดื่มชาประเภทนั้นๆ (ชาแก้ว/ชาพร้อมดื่ม/ชงเอง)': 'T_Reason',
        'ถ้ามีแบรนด์ชาพร้อมดื่ม (Ready to drink) ออกใหม่ คุณจะลองหรือไม่': 'T_Trial',
        'คุณซื้อชาพร้อมดื่ม (Ready to drink) จากช่องทางใดบ้าง': 'T_Channel',
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

    #Select necessary features
    target_cols = list(rename_mapping.values())

    # Filter the dataframe to keep only these columns
    data = data[target_cols].copy()
    print("========== Before Handle Missing Value ==========")
    print(data.isna().sum())

    data[['C_Occasion', 'C_Favorite']] = data[['C_Occasion', 'C_Favorite']].fillna('ไม่ดื่มกาแฟ')
    data['C_Frequency'] = data['C_Frequency'].fillna('ไม่ดื่มกาแฟประเภทใดเลย')
    data['C_BestBrand'] = data['C_BestBrand'].fillna('ไม่ดื่มกาแฟ Ready to Drink เลย')
    data[['T_Occasion', 'T_Favorite', 'T_Frequency', 'T_Reason']] = data[['T_Occasion', 'T_Favorite', 'T_Frequency', 'T_Reason']].fillna('ไม่ดื่มชา')
    data['T_Trial'] = data['T_Trial'].fillna('ไม่ลอง')
    data['T_Channel'] = data['T_Channel'].fillna('ไม่ซื้อชา ready to drink')
    data = data.fillna(0)
    print('========== After Handle Missing Value =========')
    print(data.isna().sum())

#for supervised
    data["Cluster_ID"] = segmented["Cluster_ID"]

    cluster_map = {0: 'ชอบกาแฟ', 2: 'ชอบชา', 1: 'ชอบทั้งกาแฟและชา', -1: 'Outlier'}
    data['Cluster_ID'] = data['Cluster_ID'].map(cluster_map)
    
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
    data['Province'] = data['Province'].str.split(',').str[0].str.strip().str.lower()
    data['Province'] = data['Province'].map(mapping).fillna(data['Province'])

    # Separating columns for Different Encodings
    binary = ['Profession', 'Sex', 'Province', 'S_Occasion', 'S_Usage(festival)', 'C_Frequency', 
              'C_Favorite', 'C_BestBrand', 'T_Frequency', 'T_Favorite', 'Cluster_ID']
   
    label = ['Age' ,'S_Frequency', 'S_Screentime']

    multi_label = ['S_Time(weekday)', 'S_Time(weekend)', 'T_Channel', 'C_Occasion', 'T_Occasion', 'T_Trial']

    # OneHot (Binary) Encode
    ohe = OneHotEncoder(sparse_output=False)
    cols_binary = ohe.fit_transform(data[binary].astype(str))
    cols_binary_df = pd.DataFrame(cols_binary, columns=ohe.get_feature_names_out(binary))

    # MultiLabel Encode
    multi_label_dfs = []
    for col in multi_label:
        mlb = MultiLabelBinarizer()
        # Split by comma and strip whitespace
        split_data = data[col].astype(str).str.split(',').apply(lambda x: [i.strip() for i in x])
        binarized = mlb.fit_transform(split_data)
        # Prefix column names to avoid collisions
        binarized_df = pd.DataFrame(binarized, columns=[f"{col}_{c}" for c in mlb.classes_])
        multi_label_dfs.append(binarized_df)
    
    cols_multi_df = pd.concat(multi_label_dfs, axis=1)

    print("========== Check Multi-Label Encoded features ==========")
    print(cols_multi_df.info())

    # Label Encode
    le = LabelEncoder()
    cols_label_df = data[label].copy().reset_index(drop=True)
    for col in label:
        cols_label_df[col] = le.fit_transform(cols_label_df[col].astype(str))
    
    # Combine all encoded features
    encoded_data = pd.concat([cols_binary_df, cols_label_df, cols_multi_df], axis=1)
    print("========== Check Label Encoded features ==========")
    print(encoded_data)

    return data, encoded_data

data, encoded_data = data_prep(data)
encoded_data.to_csv('encoded_data.csv', index=False)
data.to_csv('cleaned_data.csv', index=False)