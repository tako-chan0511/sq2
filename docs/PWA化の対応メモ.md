StreamlitアプリをPWA化する実践ガイド
このガイドでは、Streamlit Cloudで公開されているアプリケーションをPWA（Progressive Web App）に対応させるための手順を解説します。

PWA化の仕組み
Streamlitでは、vite.config.tsのような設定ファイルは使用しません。代わりに、Pythonスクリプトからst.html()を使い、PWAに必須となるManifestファイルとService Workerを読み込むためのHTMLタグを直接ページに埋め込みます。

ステップ1: PWAアセットの準備
まず、PWAに必要なアイコンと設定ファイルを準備し、リポジトリに追加します。

1. アイコンの準備
icon-192x192.pngとicon-512x512.pngの2つのアイコンファイルを用意します。
もし必要であれば、以下のボタンからサンプルをダウンロードしてお使いください。

2. staticフォルダの作成とファイルの配置
プロジェクトのルートディレクトリ（your_app.pyと同じ階層）に、static という名前の新しいフォルダを作成し、その中に以下の3つのファイルを配置します。

icon-192x192.png

icon-512x512.png

manifest.json （次のステップで作成）

3. manifest.jsonファイルの作成
staticフォルダの中に、manifest.jsonという名前で新しいファイルを作成し、以下の内容をコピー＆ペーストしてください。アプリ名や説明は自由に変更できます。

// static/manifest.json
{
  "name": "Streamlit Squared App",
  "short_name": "Squared",
  "description": "A simple app to calculate the square of a number.",
  "start_url": ".",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#ff4b4b",
  "icons": [
    {
      "src": "/app/static/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/app/static/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}

【重要】 Streamlit Cloudでは、staticフォルダ内のファイルは/app/static/というURLパスで提供されます。そのため、srcのパスは必ず/app/static/...としてください。

4. Service Workerファイルの作成
PWAのオフライン機能を司るsw.jsファイルを作成します。staticフォルダの中に、sw.jsという名前で新しいファイルを作成し、以下の内容をコピー＆ペーストしてください。これは、アプリをオフラインで動作させるための基本的なキャッシュ設定です。

// static/sw.js
const CACHE_NAME = 'my-streamlit-app-cache-v1';
const urlsToCache = [
  '/',
  // ここにキャッシュしたい他のリソース（CSS, JSファイルなど）を追加できますが、
  // Streamlitでは動的に生成されるため、ルート'/'のキャッシュが基本となります。
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // キャッシュがあればそれを返す
        if (response) {
          return response;
        }
        return fetch(event.request);
      }
    )
  );
});

ステップ2: Pythonスクリプトの修正
最後に、メインのPythonファイル（例: your_app.py）を編集し、PWAに必要なタグをページに埋め込みます。

以下のコードを参考に、ご自身のスクリプトの冒頭部分にinject_pwa_script()関数とその呼び出しを追加してください。

# your_app.py

import streamlit as st

# --- PWA化のためのコード（ここから） ---

def inject_pwa_script():
    # Streamlit CloudのURL構造に合わせてパスを修正
    manifest_url = "/app/static/manifest.json"
    sw_url = "/app/static/sw.js"
    icon_url = "/app/static/icon-192x192.png" 

    # PWAに必要なタグをHTMLとして注入
    # st.html()はbody内に挿入するため、厳密には正しくないが、現在のStreamlitでは最も確実な方法
    pwa_tags = f'''
        <link rel="manifest" href="{manifest_url}">
        <link rel="apple-touch-icon" href="{icon_url}">
        <meta name="theme-color" content="#ff4b4b">
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
    st.html(pwa_tags)

# スクリプトの最初に一度だけ呼び出す
inject_pwa_script()

# --- ここからが、あなたの元のアプリケーションコード ---

st.title("Squared App")

number = st.number_input("Enter a number", value=0)
squared_number = number ** 2
st.write(f"The square of {number} is **{squared_number}**")


ステップ3: デプロイと確認
変更をコミットしてプッシュ:

新しく作成したstaticフォルダと、その中の3つのファイル（icon-192.png, icon-512.png, manifest.json, sw.js）

修正したPythonスクリプト
これらすべてをGitリポジトリにコミットし、プッシュしてください。

自動デプロイを待つ:
Vercelと同様に、Streamlit CloudもGitHubへのプッシュを検知して自動でデプロイを開始します。

動作確認:
デプロイが完了したら、公開URL（https://squared-cypm...）にアクセスし、PCやモバイルでインストールアイコンが表示されるか、またオフラインで動作するかを確認してください。

この手順で、StreamlitアプリもPWAとして機能するようになります。