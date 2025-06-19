import streamlit as st
import random
import os
import json
import base64

def inject_pwa_manifest():
    """
    PWAの「ホーム画面への追加」機能に必要なmanifest.jsonを注入します。
    Service Worker関連のコードは、Streamlitの制約により削除しました。
    """
    # manifest.jsonのパスを定義
    manifest_path = 'static/manifest.json'

    # manifest.jsonを読み込み、Data URIに変換（ファイルパス問題を回避）
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest_data = json.load(f)
        manifest_str = json.dumps(manifest_data)
        manifest_b64 = base64.b64encode(manifest_str.encode('utf-8')).decode('utf-8')
        manifest_url = f"data:application/manifest+json;base64,{manifest_b64}"
    except Exception as e:
        print(f"manifest.jsonの読み込みに失敗: {e}")
        # 失敗した場合は、公開環境でのパスをフォールバックとして使用
        manifest_url = "/static/manifest.json"

    # アイコンとテーマカラーのパス
    icon_url = "/static/icon-192x192.png" 
    theme_color = "#343434"

    # 注入するHTMLタグ（Service Workerのscriptタグを削除）
    pwa_tags = f'''
        <link rel="manifest" href="{manifest_url}">
        <link rel="apple-touch-icon" href="{icon_url}">
        <meta name="theme-color" content="{theme_color}">
    '''
    # st.markdown を使ってHTMLをページの<head>に近い部分に注入
    st.markdown(pwa_tags, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="2乗数当てゲーム",
        page_icon="static/icon-192x192.png" 
    )
    
    # PWAのマニフェストを注入
    inject_pwa_manifest()

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
