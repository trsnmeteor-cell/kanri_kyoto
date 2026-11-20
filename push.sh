#!/usr/bin/env bash
# GitHub へ初回 push するための補助スクリプト
# 使い方: bash push.sh <GitHubユーザー名> [リポジトリ名]
set -euo pipefail
USER_NAME="${1:?GitHubのユーザー名を指定してください: bash push.sh <user> [repo]}"
REPO_NAME="${2:-kyoto-shiga-ops-monitor}"
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/${USER_NAME}/${REPO_NAME}.git"
git branch -M main
echo "==> git push -u origin main"
git push -u origin main
echo "完了。GitHub の Settings → Pages → Source で「GitHub Actions」を選択してください。"
