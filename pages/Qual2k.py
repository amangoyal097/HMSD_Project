import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.offline import iplot
import plotly.express as px

st.title("Qual2k Model")

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """

st.markdown(hide_menu_style, unsafe_allow_html=True)


uploaded_file = st.file_uploader("Upload Qual2k Output file (csv)", type=[".csv"])

if uploaded_file is not None and st.session_state.uploaded:
    print(uploaded_file)
    data = pd.read_csv(uploaded_file)
    df = pd.DataFrame(
        data,
        columns=["DO(mgO2/L)", "pH", "CBODu", "NO3(ugN/L)", "TP", "(mgD/L)", "x(km)"],
    )

    arr = df.to_numpy()
    ans = []
    y = []
    c = []
    c1 = c2 = c3 = c4 = c5 = 0
    k = []
    for i in arr:
        # print(0.17*i[0] + 0.12*i[1] + 0.1*(i[2] + i[3] + i[4]) + 0.08*i[5])
        wqi = (
            0.17 * i[0] + 0.12 * i[1] + 0.1 * (i[2] + i[3] + i[4]) + 0.08 * i[5]
        ) / 8.5
        ans.append(wqi)
        y.append(i[6])
        a = wqi
        if a < 20:
            c.append(1)
            c1 = c1 + 1
            k.append("Very Bad Quality")
        elif a >= 20 and a < 40:
            c.append(2)
            c2 = c2 + 1
            k.append("Bad Quality")
        elif a >= 40 and a < 60:
            c.append(3)
            c3 = c3 + 1
            k.append("Dubious quality")
        elif a >= 60 and a < 80:
            c.append(4)
            c4 = c4 + 1
            k.append("Satisfactory Quality")
        else:
            c.append(5)
            c5 = c5 + 1
            k.append("Good quality")

    xs = y
    ys = ans
    df = pd.DataFrame({"x": xs, "y": ys, "z": c, "Class distribution": k})
    theshhold = 20

    fig = go.Figure()

    fig.add_scattergl(
        x=xs, y=df.y.where(df.z == 1), line={"color": "red"}, name="Very Bad Quality"
    )
    fig.add_scattergl(
        x=xs, y=df.y.where(df.z == 2), line={"color": "orange"}, name="Bad Quality"
    )
    fig.add_scattergl(
        x=xs, y=df.y.where(df.z == 3), line={"color": "yellow"}, name="Dubious quality"
    )
    fig.add_scattergl(
        x=xs,
        y=df.y.where(df.z == 4),
        line={"color": "green"},
        name="Satisfactory Quality",
    )
    fig.add_scattergl(
        x=xs,
        y=df.y.where(df.z == 5),
        line={"color": "blue"},
        name="Good quality",
    )
    fig.update_layout(
        title="WQI vs Distance",
        width=1000,
        height=500,
        font=dict(size=18),
        xaxis=dict(title="Distance (in km)"),
        yaxis=dict(title="Water Quality Index"),
    )
    st.plotly_chart(fig)
    an = [1, 2, 3, 4, 5]
    bn = []
    bn.append(c1)
    bn.append(c2)
    bn.append(c3)
    bn.append(c4)
    bn.append(c5)
    colors = [
        "Very Bad Quality",
        "Bad Quality",
        "Dubious quality",
        "Satisfactory Quality",
        "Good quality",
    ]
    fig = px.bar(
        df,
        x=an,
        y=bn,
        color=colors,
        text=bn,
        title="Data points per category of water quality",
        labels=dict(x="Water Quality", y="Count"),
    )
    fig.update_layout(
        width=1000,
        height=500,
        font=dict(size=18),
    )
    st.plotly_chart(fig)
