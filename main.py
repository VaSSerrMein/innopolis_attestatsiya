import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


def load_dataset(file):
    try:
        df = pd.read_csv(file)
        return df
    except FileNotFoundError:
        st.error("Файл не найден")
        return None

# Визуализация распределения
def plot_distribution(data, col):
    if data[col].dtype == 'object':
        # Построение pie chart для категориальных переменных
        fig, ax = plt.subplots()
        ax.pie(data[col].value_counts(), labels=data[col].value_counts().index, autopct='%1.1f%%')
        ax.set_title(f"Распределение {col}")
        st.pyplot(fig)
    else:
        # Построение гистограммы для числовых переменных
        fig, ax = plt.subplots()
        sns.histplot(data=data, x=col, kde=True)
        ax.set_title(f"Распределение {col}")
        st.pyplot(fig)

# Выполнение алгоритма проверки гипотез
def run_hypothesis_test(data, col1, col2, test):
    test_results = None
    if test == "t-test":
        test_results = stats.ttest_ind(data[col1], data[col2])
    elif test == "wilcoxon":
        test_results = stats.wilcoxon(data[col1], data[col2])
    # Добавьте другие алгоритмы проверки гипотез по выбору

    if test_results:
        st.write("Результаты проверки гипотез:")
        st.write(test_results)

# Заголовок страницы
st.title("Исследование датасета")

# Загрузка датасета
file = st.file_uploader("Загрузить CSV файл")
if file:
    data = load_dataset(file)
    if data is not None:
        # Выбор двух переменных из датасета
        col1 = st.selectbox("Выберите первую переменную", data.columns)
        col2 = st.selectbox("Выберите вторую переменную", data.columns)

        # Визуализация распределения
        plot_distribution(data, col1)
        plot_distribution(data, col2)

        # Выбор алгоритма проверки гипотез
        test = st.selectbox("Выберите алгоритм проверки гипотез", ["t-test", "wilcoxon"])

        # Выполнение алгоритма проверки гипотез
        run_hypothesis_test(data, col1, col2, test)