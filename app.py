import streamlit as st
import random
import os

def inject_pwa():
    """
    PWA化に必要なHTMLタグをStreamlitアプリに注入する関数。
    Streamlit CloudのURL構造に合わせてパスを定義します。
    """
    # Streamlit Cloudでは /static/ で提供される
    manifest_url = "/static/manifest.json"
    sw_url = "/static/sw.js"
    icon_url = "/static/icon-192x192.png" 
    theme_color = "#343434"

    pwa_tags = f'''
        <link rel="manifest" href="{manifest_url}">
        <link rel="apple-touch-icon" href="{icon_url}">
        <meta name="theme-color" content="{theme_color}">
        <script>
            if ('serviceWorker' in navigator) {{
                window.addEventListener('load', function() {{
                    navigator.serviceWorker.register('{sw_url}').then(function(registration) {{
                        console.log('ServiceWorker registration successful with scope: ', registration.scope);
                    }}, function(err) {{
                        console.log('ServiceWorker registration failed: ', err);
                    }});
                }});
            }}
        </script>
    '''
    # st.markdown を使ってHTMLをページの<head>に近い部分に注入する
    st.markdown(pwa_tags, unsafe_allow_html=True)

def main():
    # ページ設定は、他のStreamlitコマンドより先に一度だけ呼び出す
    st.set_page_config(
        page_title="2乗数当てゲーム",
        page_icon="static/icon-192x192.png" 
    )

    # アプリのタイトル
    st.title("ランダムな数字!")

    # PWAスクリプトを注入
    inject_pwa()

    # --- ここからが、元のアプリケーションコード ---

    st.sidebar.title("範囲を指定してください！！")
    min_value = st.sidebar.number_input("最小値", value=10, step=1)
    max_value = st.sidebar.number_input("最大値", value=99, step=1)

    if min_value >= max_value:
        st.sidebar.error("最小値は最大値より小さくしてください！")
        return

    if "random_number" not in st.session_state:
        st.session_state.random_number = None

    if st.button("二桁の数字を生成"):
        st.session_state.random_number = random.randint(min_value, max_value)

    if st.session_state.random_number is not None:
        st.markdown(f"<p style='font-size: 5em; text-align: center;'>{st.session_state.random_number}</p>", unsafe_allow_html=True)

    if st.session_state.random_number is not None and st.button("2乗数を当ててください"):
        square = st.session_state.random_number ** 2
        st.markdown(f"<p style='font-size: 5em; text-align: center;'>{square}</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
