将本地仓库推送到 GitHub

1. 在 GitHub 上新建一个空仓库（不初始化 README/LICENSE/Gitignore）。
   - 记录仓库地址，如: git@github.com:yourname/Autologin.git 或 https://github.com/yourname/Autologin.git

2. 在本地添加远程并推送：

```powershell
# 使用 SSH
git remote add origin git@github.com:yourname/Autologin.git
# 或使用 HTTPS
git remote add origin https://github.com/yourname/Autologin.git

git branch -M main
git push -u origin main
```

3. 在 GitHub 仓库中启用 Actions（默认开启）。
   - CI 会在 push 到 `main` 时运行 `build-and-release.yml`，生成构建产物并作为 artifact 上传。

4. 下载构建产物：
   - 到 Actions 页面，选择最近一次 workflow 运行，展开 `Artifacts` 部分下载 `autologin-windows`。

5. 如果要自动创建 Release（上传 zip 到 Release），需要在 workflow 中添加 `actions/create-release` 与 `actions/upload-release-asset` 并设置 `GITHUB_TOKEN`。

安全与注意事项：
- 若使用 HTTPS 推送并要求输入用户名/密码，请使用 GitHub 的 Personal Access Token（PAT）作为密码。
- 不要将敏感凭证（超级鹰账号等）提交到仓库。使用 `settings.json.example` 作为模板，真实配置交给用户本地填写。

如需我帮您执行 `git push`，请提供仓库 URL 和访问凭证（推荐使用 SSH key 或在本地运行命令以保持凭证安全）。
