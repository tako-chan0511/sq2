import streamlit as st
import random

def inject_pwa_script():
    """
    PWA化に必要なHTMLタグをStreamlitアプリに注入する関数。
    manifest.json、Service Worker、およびiOS用のアイコンなどを設定します。
    """
    # Streamlit CloudのURL構造に合わせて、staticフォルダへのパスを定義
    manifest_url = "/app/static/manifest.json"
    sw_url = "/app/static/sw.js"
    icon_url = "/app/static/icon-192x192.png"
    theme_color = "#343434" # アイコンの背景色に合わせる

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
    # HTMLとしてページに注入
    st.html(pwa_tags)

def main():
    # --- PWA化のためのコード呼び出し ---
    inject_pwa_script()

    # --- ここからが、元のアプリケーションコード ---

    # アプリのタイトル
    st.title("ランダムな数字!")

    # 数字の範囲を指定するスライダー
    st.sidebar.title("範囲を指定してください！！")
    min_value = st.sidebar.number_input("最小値", value=10, step=1)
    max_value = st.sidebar.number_input("最大値", value=99, step=1)

    if min_value >= max_value:
        st.sidebar.error("最小値は最大値より小さくしてください！")
        return

    # セッション状態を使用してランダムな数字を保持
    if "random_number" not in st.session_state:
        st.session_state.random_number = None

    # 2桁の数字を生成ボタン
    if st.button("二桁の数字を生成"):
        st.session_state.random_number = random.randint(min_value, max_value)

    # 現在のランダムな数字を表示
    if st.session_state.random_number is not None:
        st.markdown(f"<p style='font-size: 5em; text-align: center;'>{st.session_state.random_number}</p>", unsafe_allow_html=True)

    # 答えを表示するボタン
    if st.session_state.random_number is not None and st.button("2乗数を当ててください"):
        square = st.session_state.random_number ** 2
        st.markdown(f"<p style='font-size: 5em; text-align: center;'>{square}</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
