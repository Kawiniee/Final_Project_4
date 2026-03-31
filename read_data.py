import pandas as pd
from sklearn.preprocessing import LabelEncoder

data = pd.read_csv('RTD_Brew.csv')

def data_prep(data):
    mask = (data['คุณดื่มกาแฟหรือไม่'] == 'ไม่ดื่ม') & (data['คุณดื่มชาหรือไม่'] == 'ไม่ดื่ม')
    data = data.drop(data[mask].index) #drop where it's not ours customer

    #select necessary features
    df = data[['อายุ', 'ความถี่ในการเปิดรับสื่อในแต่ละช่องทางต่อสัปดาห์ [ออนไลน์]',
              'ระยะเวลาในการเสพสื่อต่อวัน ในแต่ละช่องทาง [ออนไลน์]', 
              'ในวันจันทร์-ศุกร์ (Weekday) ช่วงเวลาใดที่คุณเปิดรับสื่อแต่ละช่องทาง [ออนไลน์]',
              'ในวันหยุดเสาร์-อาทิตย์ (Weekend) ช่วงเวลาใดที่คุณเปิดรับสื่อแต่ละช่องทาง [ออนไลน์]',
              'ในวันหยุดยาวหรือเทศกาล คุณใช้โซเชียลมีเดีย อย่างไร']]
    
    #Rename each column
    df = df.rename(columns={
        'อายุ': 'Age',
        'ความถี่ในการเปิดรับสื่อในแต่ละช่องทางต่อสัปดาห์ [ออนไลน์]': 'Frequency',
        'ระยะเวลาในการเสพสื่อต่อวัน ในแต่ละช่องทาง [ออนไลน์]': 'ScreenTime',
        'ในวันจันทร์-ศุกร์ (Weekday) ช่วงเวลาใดที่คุณเปิดรับสื่อแต่ละช่องทาง [ออนไลน์]': 'Weekday_period',
        'ในวันหยุดเสาร์-อาทิตย์ (Weekend) ช่วงเวลาใดที่คุณเปิดรับสื่อแต่ละช่องทาง [ออนไลน์]': 'Weekend_period',
        'ในวันหยุดยาวหรือเทศกาล คุณใช้โซเชียลมีเดีย อย่างไร': 'Holiday_usage'
    })

    #Encode
    le = LabelEncoder()
    Age = le.fit_transform(df['Age'])
    Frequency = le.fit_transform(df['Frequency'])
    ScreenTime = le.fit_transform(df['ScreenTime'])
    Weekday_period = le.fit_transform(df['Weekday_period'])
    Weekend_period = le.fit_transform(df['Weekend_period'])
    Holiday_usage = le.fit_transform(df['Holiday_usage'])

    encode_df = pd.DataFrame({
        'Age': Age,
        'Frequency': Frequency,
        'ScreenTime': ScreenTime,
        'Weekday_period': Weekday_period,
        'Weekend_period': Weekend_period,
        'Holiday_usage': Holiday_usage
    })

    return data, df, encode_df

data, df, encode_df = data_prep(data)
print(encode_df)