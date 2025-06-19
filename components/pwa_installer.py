import streamlit as st
import streamlit.components.v1 as components
import os

# このコンポーネントのビルドディレクトリを宣言
_component_func = components.declare_component(
    "pwa_installer",
    path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend/build")
)

# Pythonから呼び出すためのラッパー関数
def pwa_installer():
    """PWAのインストールに必要なHTMLタグを注入するコンポーネント"""
    _component_func()

