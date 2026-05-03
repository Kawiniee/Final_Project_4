import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

# โหลด data เดิม
data = pd.read_csv("cleaned_data.csv")

# โหลด feedback
feedback = pd.read_csv("feedback_data.csv")

# เอาเฉพาะ feedback ที่ user บอกว่าถูก
feedback = feedback[feedback["feedback"] == "yes"]

# รวมข้อมูล
data = pd.concat([data, feedback], ignore_index=True)

# train ใหม่ (ตัวอย่าง customer)
X = data[['Age', 'Sex', 'Profession', 'Province']]
y = data['customer_segment']

model = RandomForestClassifier()
model.fit(X, y)

# save model ใหม่
joblib.dump(model, "app/customer_model.pkl")

print("Model updated!")