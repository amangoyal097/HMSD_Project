import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
    for i in arr:
        # print(0.17*i[0] + 0.12*i[1] + 0.1*(i[2] + i[3] + i[4]) + 0.08*i[5])
        ans.append(
            (0.17 * i[0] + 0.12 * i[1] + 0.1 * (i[2] + i[3] + i[4]) + 0.08 * i[5]) / 8.5
        )
        y.append(i[6])
    fig, ax = plt.subplots()
    ax.plot(y, ans)
    ax.set_title("Water Quality Index vs Distance")
    ax.set_xlabel("Distance (km)")
    ax.set_ylabel("WQI")
    st.pyplot(fig)
