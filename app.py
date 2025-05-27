import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Симулация на сблъсък", layout="wide")

st.title("🧪 3D Симулация на сблъсък на частици с резултати и хипотези")

st.markdown("""
Добре дошъл в интерактивна симулация, вдъхновена от експериментите в ЦЕРН!

Тук ще симулираш сблъсък между две частици, ще наблюдаваш резултатите,  
ще анализираш енергията и импулса и ще направиш своя хипотеза.  
""")

# Въвеждане на параметри
st.markdown("## 🔧 Настройки на частиците")

col1, col2 = st.columns(2)

with col1:
    m1 = st.number_input("Маса на частица 1 (kg)", min_value=0.1, value=5.0, step=0.1)
    v1 = st.number_input("Скорост на частица 1 (m/s)", value=5.0, step=0.1)

with col2:
    m2 = st.number_input("Маса на частица 2 (kg)", min_value=0.1, value=5.0, step=0.1)
    v2 = st.number_input("Скорост на частица 2 (m/s)", value=-3.0, step=0.1)

# Изчисления
v1_final = ((m1 - m2) / (m1 + m2)) * v1 + ((2 * m2) / (m1 + m2)) * v2
v2_final = ((2 * m1) / (m1 + m2)) * v1 + ((m2 - m1) / (m1 + m2)) * v2

# Времева линия
t = np.linspace(0, 2, 30)
x1 = v1 * t
x2 = 10 + v2 * t

# Създаване на кадри
frames = []
for i in range(len(t)):
    frames.append(go.Frame(data=[
        go.Scatter3d(x=[x1[i]], y=[0], z=[0], mode='markers+text',
                     marker=dict(size=10, color='blue'),
                     text=["Частица 1"], textposition="top center"),
        go.Scatter3d(x=[x2[i]], y=[0], z=[0], mode='markers+text',
                     marker=dict(size=10, color='red'),
                     text=["Частица 2"], textposition="top center")
    ]))

layout = go.Layout(
    scene=dict(
        xaxis=dict(range=[-10, 30], title='Позиция X'),
        yaxis=dict(range=[-5, 5], title='Y'),
        zaxis=dict(range=[-5, 5], title='Z'),
    ),
    title="3D Анимация на сблъсък",
    margin=dict(l=0, r=0, b=0, t=40),
    height=500,
    updatemenus=[dict(type="buttons", showactive=False,
                      buttons=[dict(label="▶ Пусни анимацията",
                                    method="animate",
                                    args=[None, {"frame": {"duration": 100, "redraw": True},
                                                 "fromcurrent": True}])])]
)

fig = go.Figure(
    data=[
        go.Scatter3d(x=[x1[0]], y=[0], z=[0], mode='markers', marker=dict(size=10, color='blue')),
        go.Scatter3d(x=[x2[0]], y=[0], z=[0], mode='markers', marker=dict(size=10, color='red'))
    ],
    layout=layout,
    frames=frames
)

st.markdown("## 🎥 Анимация")
st.plotly_chart(fig)

# Резултати
st.markdown("## 📊 Резултати от сблъсъка")

impulse_before = m1 * v1 + m2 * v2
impulse_after = m1 * v1_final + m2 * v2_final

energy_before = 0.5 * m1 * v1 ** 2 + 0.5 * m2 * v2 ** 2
energy_after = 0.5 * m1 * v1_final ** 2 + 0.5 * m2 * v2_final ** 2

st.write(f"**Импулс преди сблъсъка:** {impulse_before:.2f} kg·m/s")
st.write(f"**Импулс след сблъсъка:** {impulse_after:.2f} kg·m/s")
st.write(f"**Кинетична енергия преди сблъсъка:** {energy_before:.2f} J")
st.write(f"**Кинетична енергия след сблъсъка:** {energy_after:.2f} J")

# Въпроси
st.markdown("""---  
## ❓ Въпроси за размисъл

- Запазва ли се импулсът?
- Запазва ли се кинетичната енергия?
- Какво би станало ако едната частица е по-тежка?
- Какъв тип сблъсък е това (еластичен, нееластичен)?
""")

# Хипотеза
st.markdown("---")
st.markdown("## 🧠 Въведи своя хипотеза:")

hypothesis = st.text_area("Какво очакваш да се случи при сблъсъка?", height=150)

if st.button("📤 Изпрати хипотезата"):
    if hypothesis.strip():
        # запис в CSV файл
        df = pd.DataFrame([{
            "timestamp": datetime.now().isoformat(),
            "mass1": m1,
            "velocity1": v1,
            "mass2": m2,
            "velocity2": v2,
            "hypothesis": hypothesis
        }])
        df.to_csv("hypotheses.csv", mode='a', index=False, header=False)
        st.success("Хипотезата ти е записана успешно! 🚀")
    else:
        st.warning("Моля, въведи текст преди да изпратиш.")
