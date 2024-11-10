# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1h659UeqA4b79e_LPqOkoj6VHVcExikbP
"""



!pip install joblib
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
import joblib
import os

# Hàm mã hóa tần suất
def frequency_encoding(df, column):
    frequency_map = df[column].value_counts(normalize=True)
    df[column + '_freq_encoded'] = df[column].map(frequency_map)
    return df

# Đường dẫn để lưu/tải mô hình
best_model_save_path = '/content/drive/MyDrive/MyModel.pkl'

# Kiểm tra nếu mô hình đã tồn tại
if os.path.exists(best_model_save_path):
    # Tải mô hình đã huấn luyện
    best_model = joblib.load(best_model_save_path)
    st.write("Đã tải mô hình huấn luyện sẵn.")
else:
    # Dữ liệu huấn luyện mô phỏng và nhãn (cần thay bằng dữ liệu thật của bạn)
    X_train = np.random.rand(10, 10)  # Sử dụng số cột phù hợp với dữ liệu thực
    y_train = np.random.randint(0, 2, 10)

    # Huấn luyện mô hình AdaBoost với cây quyết định
    best_model = AdaBoostClassifier(base_estimator=DecisionTreeClassifier(max_depth=1), n_estimators=50)
    best_model.fit(X_train, y_train)

    # Lưu mô hình đã huấn luyện
    joblib.dump(best_model, best_model_save_path)
    st.write(f"Mô hình đã được lưu tại: {best_model_save_path}")

# Dữ liệu đầu vào để dự đoán
instances_to_predict = pd.DataFrame({
    'Customer_ID': [710793783, 719756709],
    'Sender_account': [4253533793, 5479357050],
    'Receiver_account': [2248766608, 3456789401],
    'Amount': [17110.31, 4500.5],
    'Payment_currency': ['UK pounds','UK pounds'],
    'Received_currency': ['UK pounds', 'Dirham'],
    'Sender_bank_location': ['UK', 'UAE'],
    'Payment_type': ['Credit card', 'Cheque'],
    'Laundering_type': ['Normal_Fan_In', 'Normal_Fan_Out'],
    'Time': ['10:35:20 AM', '10:35:19 AM'],
    'Date': ['10/7/2022', '10/7/2022']
})

# Danh sách các cột cần mã hóa tần suất
columns_to_encode = ['Payment_currency', 'Sender_bank_location','Laundering_type','Received_currency', 'Payment_type']
# Thực hiện mã hóa tần suất cho mỗi cột
for column in columns_to_encode:
    instances_to_predict = frequency_encoding(instances_to_predict, column)

# Chuyển đổi các cột Date và Time sang định dạng datetime
instances_to_predict['Date'] = pd.to_datetime(instances_to_predict['Date'])
instances_to_predict['Time'] = pd.to_datetime(instances_to_predict['Time'], errors='coerce')

# Xóa các cột ban đầu sau khi mã hóa và chuẩn hóa
instances_to_predict.drop(columns=columns_to_encode, inplace=True)
instances_to_predict.drop(columns=['Date', 'Time'], inplace=True)

# Chuẩn hóa dữ liệu
scaler = StandardScaler()
instances_to_predict_scaled = scaler.fit_transform(instances_to_predict)

# Dự đoán mức độ tin cậy sử dụng mô hình đã load hoặc huấn luyện
predictions = best_model.predict(instances_to_predict_scaled)

# Hiển thị kết quả dự đoán trên giao diện Streamlit
st.write("Kết quả dự đoán:")
st.write(f"Trường hợp 1: Có khả năng là rửa tiền không? {predictions[0]}")
st.write(f"Trường hợp 2: Có khả năng là rửa tiền không? {predictions[1]}")