import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

# Sample dataset
data = pd.DataFrame({
    'age': [25, 30, 35, 28, 40, 33, 27, 31],
    'region': ['South Asia', 'Africa', 'Europe', 'South Asia', 'Africa', 'Europe', 'South Asia', 'Africa'],
    'breastfeeding_stage': ['Lactation', 'Weaning', 'Extended', 'Lactation', 'Weaning', 'Extended', 'Lactation', 'Weaning'],
    'health_condition': ['Anemia', 'Diabetes', 'None', 'Thyroid', 'Anemia', 'None', 'Diabetes', 'Thyroid'],
    'nutrition_plan': [
        'High iron foods, spinach, legumes',
        'Low sugar, high fiber diet',
        'Balanced diet with calcium-rich foods',
        'Iron + iodine rich foods',
        'Iron supplements, beetroot',
        'General maintenance plan',
        'Low glycemic diet, fruits, oats',
        'Iodized salt, lean protein'
    ]
})

# Encode categorical values
le_region = LabelEncoder()
le_stage = LabelEncoder()
le_health = LabelEncoder()
le_output = LabelEncoder()

data['region_enc'] = le_region.fit_transform(data['region'])
data['stage_enc'] = le_stage.fit_transform(data['breastfeeding_stage'])
data['health_enc'] = le_health.fit_transform(data['health_condition'])
data['plan_enc'] = le_output.fit_transform(data['nutrition_plan'])

# Model training
X = data[['age', 'region_enc', 'stage_enc', 'health_enc']]
y = data['plan_enc']
model = DecisionTreeClassifier()
model.fit(X, y)

# Prediction function
def predict_nutrition(age, region, stage, health):
    input_df = pd.DataFrame([[
        age,
        le_region.transform([region])[0],
        le_stage.transform([stage])[0],
        le_health.transform([health])[0]
    ]])
    prediction = model.predict(input_df)
    return le_output.inverse_transform(prediction)[0]
