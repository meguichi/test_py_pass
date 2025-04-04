import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import yfinance as yf
import matplotlib.pyplot as plt

# --- config.yaml の読み込み ---
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

# --- 認証オブジェクトの作成 ---
# v0.4.2 以降は、cookie 関連の情報を辞書として渡します。
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']
)

# --- ログイン処理（フォームのフィールドをカスタマイズ） ---
name, authentication_status, username = authenticator.login(
    location="main",
    fields={
        'Form name': 'Login', 
        'Username': 'Username', 
        'Password': 'Password', 
        'Login': 'Login'
    }
)

# --- 認証結果に応じた処理 ---
if authentication_status:
    authenticator.logout("Logout", location="sidebar")
    st.sidebar.success(f"ようこそ、{name} さん")
    
    st.title("日経平均チャート表示アプリ")
    st.write("以下のボタンを押すと、日経平均の過去30日チャートが表示されます。")
    
    if st.button("チャートを表示"):
        data = yf.download("^N225", period="30d")
        fig, ax = plt.subplots()
        ax.plot(data.index, data["Close"], label="日経平均")
        ax.set_title("日経平均（直近30日）")
        ax.set_xlabel("日付")
        ax.set_ylabel("株価（円）")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

elif authentication_status is False:
    st.error("ユーザー名またはパスワードが間違っています。")

elif authentication_status is None:
    st.warning("ユーザー名とパスワードを入力してください。")
