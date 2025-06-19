import streamlit as st
import random
import os
import json
import base64

def inject_pwa_script():
    """
    PWA化に必要なHTMLタグをStreamlitアプリに注入する最終版。
    st.markdownを使い、iframeを回避してメインページに直接タグを埋め込む。
    """
    # manifest.json を読み込み、Data URIに変換（ファイルパス問題を回避）
    try:
        with open('static/manifest.json', 'r', encoding='utf-8') as f:
            manifest_data = json.load(f)
        manifest_str = json.dumps(manifest_data)
        manifest_b64 = base64.b64encode(manifest_str.encode('utf-8')).decode('utf-8')
        manifest_url = f"data:application/manifest+json;base64,{manifest_b64}"
    except Exception as e:
        # ローカルでのファイル読み込みエラーは、デプロイ時には解決する可能性あり
        print(f"manifest.jsonの読み込みに失敗しました: {e}")
        manifest_url = "/static/manifest.json" # 失敗時のフォールバック

    # Service Workerとアイコンへのパス
    sw_url = "/static/sw.js"
    icon_url = "/static/icon-192x192.png" 
    theme_color = "#343434"

    # 注入するHTMLタグ
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

    # PWAスクリプトを注入
    inject_pwa_script()

    # --- ここからが、元のアプリケーションコード ---

    st.title("ランダムな数字!")

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
