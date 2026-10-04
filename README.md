# 京都・滋賀エリア 運用モニター

スプレッドシートの「超過」シートと「ご意見」シートをブラウザで閲覧する、単一 HTML アプリです。
ビルド不要・サーバ不要で `index.html` を開くだけで動作し、PC・Android・iPhone、Chrome・Safari・Edge で利用できます。

## 収録画面

| タブ | 内容 |
| --- | --- |
| 01 超過（時間外労働） | 対象者の超過時間・超過回数・今後の労働時間を一覧。氏名/店舗で検索、列クリックで並べ替え |
| 02 ご意見（月別） | **月を選択**して、その月の店舗×カテゴリ集計を表示。あわせて前月との増減も表示 |
| 03 分析レポート | **対象月と比較月を選択**し、カテゴリ構成・店舗別の増減・読みどころを自動計算 |

「ご意見」の月はデータ（`data.json` の `months`）から自動生成されます。月を追加すれば、
すべての選択肢・比較・分析がそのまま増えます。

### 主な機能

- **PDF出力**: 画面右上の「PDF出力」ボタン。ブラウザの印刷画面が開くので、
  「PDFに保存」を選ぶと現在のタブの内容が PDF になります（PC / Android / iPhone いずれも可）。
- **月の選択**: 固定表示ではなく、ドロップダウンで対象月を選択する方式です。
- **マルチデバイス対応**: レスポンシブ表示。狭い画面では表が横スクロールします。
- **完全オフライン動作**: 外部CDN・外部フォントに依存せず、1ファイルで完結します。

## ファイル構成

```
.
├── index.html                  # アプリ本体（データ埋め込み済み・単体動作）
├── data/data.json              # 埋め込みデータの原本（月別）
├── scripts/extract.py          # スプレッドシート(xlsx) → data.json の抽出スクリプト
├── .github/workflows/pages.yml # GitHub Pages 自動デプロイ
├── .nojekyll                   # Jekyll 処理を無効化
├── push.sh                     # 初回 push 補助
└── .gitignore                  # 元の xlsx / csv を除外
```

## ローカルで開く

`index.html` をブラウザで開くだけです。サーバ経由なら:

```bash
python3 -m http.server 8000   # → http://localhost:8000/
```

## 複数端末で使う（公開）

1. GitHub でリポジトリを作成し push

   ```bash
   git remote add origin https://github.com/<ユーザー名>/kyoto-shiga-ops-monitor.git
   git branch -M main && git push -u origin main
   ```

2. **Settings → Pages → Source** で **「GitHub Actions」** を選択

   公開URL: `https://<ユーザー名>.github.io/kyoto-shiga-ops-monitor/`

   このURLを PC・スマホで開けば、どの端末からでも同じ画面を利用できます。

## データを更新する

1. スプレッドシートを `sheet.xlsx` としてこのフォルダに保存（`.gitignore` 済み）
2. 抽出スクリプトを実行

   ```bash
   python3 -m pip install openpyxl
   python3 scripts/extract.py      # data.json を再生成
   ```

3. `data/data.json` の内容を `index.html` 内の `const DATA = { ... };` に差し替える

> `scripts/extract.py` はシート名（超過 / ご意見 / 店舗）と範囲を前提にしています。
> 月を増やす場合は `months=[block(3,6,21), block(24,27,42)]` の行に、
> 追加した月の集計ブロック（集計期間の行・明細の開始行・終了行）を足してください。

## 注意（重要）

`index.html` / `data/data.json` には **従業員の氏名・従業員番号・店舗別の時間外労働時間・
お客様のご意見件数** が含まれます（個人情報）。

- リポジトリは **Private（非公開）** での運用を推奨します。
- Private で GitHub Pages を使うには有料プラン（Pro / Team / Enterprise）が必要です。
- 無料プランで Public にする場合、上記の個人情報が誰でも閲覧できる状態になります。
  その場合は氏名を匿名化した版を別途ご用意ください。
