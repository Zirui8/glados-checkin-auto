# glados-checkin

GLaDOS（glados.cloud / glados.rocks / glados.network）每日自动签到脚本，使用 GitHub Actions 实现。

**当前版本特点**(2026.2.4)：
- 支持**多个账号**同时签到
- 失败会让 Actions 失败并发送绑定GitHub账号的邮箱提醒，重复签到视为正常，不触发失败邮件

**参考项目**：本仓库参考/部分 fork 自 [actions-integration/checkin](https://github.com/actions-integration/checkin)，本仓库改为纯 Python 实现。

## 使用说明

### 1.0 更新 Cookie
GLaDOS 签到脚本使用 **Cookie** 进行登录。Cookie 和 网址Api 可能需要定期更新，否则可能会签到失败。  

更新方法：  
1. 登录 [GLaDOS 官网](https://glados.rocks/)，进入[签到面板](https://glados.network/console/checkin) 
2. 按 `F12` 打开浏览器开发者工具 → 切到 **网络(Network)**
3. 刷新一下网页或点击一次“签到”按钮，浏览器开发者工具**Name**(名称)中会出现`checkin`字样，点击`checkin`
4. 在 **Headers** 中下滑找到 **Cookies** ，找到以下字段并完整复制：

```txt
koa:sess=xxx; koa:sess.sig=xxx
```

---

**多账号**：每个账号重复以上步骤，分别获取不同的 Cookie 字符串。

### 1.1 设置到 GitHub Secrets

1. 打开你的 GitHub 仓库 → **Settings** → **Secrets and variables** → **Actions**
2. 点击 **New repository secret**
3. **Name**(名称)填：`GLADOS`（必须全大写）
4. **Secret**(密钥)填入所有账号的 Cookie，多账号用换行分隔
5. **单账号示例**：

```txt
koa:sess=xxx; koa:sess.sig=xxx
```

6. **多账号示例**：

```txt
koa:sess=账号1; koa:sess.sig=账号1;
koa:sess=账号2; koa:sess.sig=账号2;
koa:sess=账号3; koa:sess.sig=账号3;
```


---

### 2. 查看签到日志
1. 打开仓库首页 → 点击 **Actions** 标签页  
2. 在左侧选择 `GLaDOS Checkin` workflow（第一次可以运行检测，显示“✅”表示成功）
3. 点击最新一次运行记录（按日期排序）  
4. 点击 **Run checkin script** 步骤，可以查看所有账号的输出日志  
   - 如果签到成功，会显示类似 `Checkin! Got X Points` 的提示  
   - 如果返回 `"Checkin Repeats! Please Try Tomorrow"` 表示今天已经签过到  
   - 如果是 Cookie 过期或其他错误，会有对应的报错信息，并会发送报错信息至绑定GitHub账号的邮箱

---

### 3. 修改签到时间
当前自动签到时间为 **每天北京时间 00:30**（UTC 时间 16:30）。  

如果需要调整时间，可以修改 `.github/workflows/xxx.yml` 中的：
```yaml
schedule:
  - cron: '30 16 * * *'  # UTC 时间 16:30
```
**注意：GitHub Actions 使用 UTC 时间，需要自己换算成北京时间（+8 小时）。**
