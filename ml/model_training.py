import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

X_train = pd.read_csv("ml/X_train_scaled.csv")
X_test = pd.read_csv("ml/X_test_scaled.csv")

y_cost_train = pd.read_csv("ml/y_cost_train.csv")
y_cost_test = pd.read_csv("ml/y_cost_test.csv")

y_co2_train = pd.read_csv("ml/y_co2_train.csv")
y_co2_test = pd.read_csv("ml/y_co2_test.csv")

cost_model = LinearRegression()
cost_model.fit(X_train, y_cost_train)

co2_model = LinearRegression()
co2_model.fit(X_train, y_co2_train)

cost_pred = cost_model.predict(X_test)
co2_pred = co2_model.predict(X_test)

print("Cost Prediction R2 Score:", r2_score(y_cost_test, cost_pred))
print("CO2 Impact Prediction R2 Score:", r2_score(y_co2_test, co2_pred))

print("✅ Model training completed")
