# glados-checkin

## 使用说明

### 1. 更新 Cookie
GLaDOS 签到脚本使用 **Cookie** 进行登录。Cookie 可能需要定期更新，否则会签到失败。  

更新方法：  
1. 登录 [GLaDOS 官网](https://glados.rocks/)，进入[签到面板](https://glados.network/console/checkin) 
2. 按 `F12` 打开浏览器开发者工具 → 切到 **网络(Network)**
3. 点击一次“签到”按钮，浏览器开发者工具**名称**中会出现`checkin`字样，点击`checkin`
4. 在 **Cookies** 中找到以下字段：
   - `koa:sess`
   - `koa:sess.sig`
   - `user-agent`（UA，可在 Network 请求头中找到）
5. 回到 GitHub 仓库 → `Settings` → `Secrets and variables` → `Actions`  
6. 点击 **Edit**，分别更新以下 Secrets：
   - `KOA_SESS` → 对应 `koa:sess`
   - `KOA_SESS_SIG` → 对应 `koa:sess.sig`
   - `UA` → 对应你的浏览器 UA
7. 保存即可，GitHub Actions 会在下次运行时使用新的 Cookie。

---

### 2. 查看签到日志
1. 打开仓库首页 → 点击 **Actions** 标签页  
2. 在左侧选择 `GLaDOS Checkin` workflow（第一次可以运行检测，显示“✅”表示成功）
3. 点击最新一次运行记录（按日期排序）  
4. 点击 **Run checkin script** 步骤，可以查看脚本的完整输出日志  
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
