#!/bin/bash
# 自动提交 + 推送脚本
# 用法：bash push.sh "提交信息"

git add .
git commit -m "${1:-update}"
git push
