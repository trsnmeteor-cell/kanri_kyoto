# 京都・滋賀エリア 運用モニター

スプレッドシートの「超過」シートと「ご意見」シートの指定範囲を、ブラウザで閲覧するための
単一 HTML アプリです。ビルド不要・サーバ不要で、`index.html` を開くだけで動作します。

## 収録画面

| タブ | 内容 | 元シート / 範囲 |
| --- | --- | --- |
| 01 超過（時間外労働） | 対象21名の超過時間・超過回数・今後の労働時間。検索と並べ替えに対応 | 超過シート（11〜31行） |
| 02 ご意見 9月 | 店舗×カテゴリの件数ヒートマップ | ご意見 `AG3:AN23`（2026/09/01〜09/30） |
| 03 ご意見 8月 | 店舗×カテゴリの件数ヒートマップ | ご意見 `AG24:AN46`（2026/08/01〜08/31） |
| 04 分析レポート | 2範囲の比較、カテゴリ別・店舗別の増減、読み取れるポイント | 上記2範囲 |

店舗№は「店舗」シートの店舗コードで店舗名に変換して表示しています。

## ファイル構成

```
.
├── index.html                  # アプリ本体（データ埋め込み済み・単体で動作）
├── data/data.json              # アプリに埋め込んだ集計データ（再生成用の原本）
├── scripts/extract.py          # スプレッドシート(xlsx)から data.json を作る抽出スクリプト
├── .github/workflows/pages.yml # GitHub Pages 自動デプロイ
├── .nojekyll                   # Jekyll 処理を無効化（そのまま配信）
└── .gitignore                  # 元の xlsx / csv はコミットしない
```

## ローカルで開く

`index.html` をブラウザで開くだけです。

```bash
# サーバ経由で開きたい場合
python3 -m http.server 8000
# → http://localhost:8000/
```

## GitHub に公開する手順

### 1. リポジトリを作成して push

GitHub で空のリポジトリを作成したうえで、このフォルダで実行します。

```bash
git remote add origin https://github.com/<ユーザー名>/kyoto-shiga-ops-monitor.git
git branch -M main
git push -u origin main
```

（初回コミットは同梱の `.git` に含まれています。`git log` で確認できます。）

### 2. GitHub Pages を有効化

リポジトリの **Settings → Pages → Build and deployment → Source** で
**「GitHub Actions」** を選択します。以降は `main` への push のたびに
`.github/workflows/pages.yml` が自動デプロイします。

公開URL: `https://<ユーザー名>.github.io/kyoto-shiga-ops-monitor/`

## データを更新する

1. スプレッドシートを `sheet.xlsx` として保存（`.gitignore` 済み）
2. 抽出スクリプトを実行

```bash
python3 -m pip install openpyxl
python3 scripts/extract.py          # data.json を再生成
```

3. `data/data.json` の内容を `index.html` 内の `const DATA = { ... };` に差し替える

> `scripts/extract.py` はシート名（超過 / ご意見 / 店舗）と
> 対象範囲（11〜31行、AG3:AN23、AG24:AN46）を前提にしています。
> 範囲が変わった場合は定数を調整してください。

## 注意（重要）

このアプリの `index.html` / `data/data.json` には、**従業員の氏名・従業員番号、
店舗別の時間外労働時間、お客様のご意見件数**が含まれます。

- リポジトリは **Private（非公開）** での運用を推奨します。
- Private リポジトリで GitHub Pages を使うには、GitHub の有料プラン（Pro / Team / Enterprise）が必要です。
- 無料プランで Public リポジトリにする場合、上記の個人情報が誰でも閲覧できる状態になります。
  その場合は氏名を匿名化するなど、マスキングした版を別途ご用意ください。
- 共有相手を限定したいだけなら、Private リポジトリのままメンバーを招いて
  ローカルで `index.html` を開く運用でも要件を満たせます。
