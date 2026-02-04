# glados-checkin

## 使用说明

### 1. 更新 Cookie
GLaDOS 签到脚本使用 **Cookie** 进行登录。Cookie 和 网址Api 可能需要定期更新，否则可能会签到失败。  

更新方法：  
1. 登录 [GLaDOS 官网](https://glados.rocks/)，进入[签到面板](https://glados.network/console/checkin) 
2. 按 `F12` 打开浏览器开发者工具 → 切到 **网络(Network)**
3. 点击一次“签到”按钮，浏览器开发者工具**名称**中会出现`checkin`字样，点击`checkin`
4. 在 **Cookies** 中找到以下字段：
   - `koa:sess`
   - `koa:sess.sig`

---

**多账号**：每个账号重复以上步骤，分别获取不同的 Cookie 字符串。

### 设置到 GitHub Secrets（推荐方式：使用单个变量 GLADOS）

1. 打开你的 GitHub 仓库 → **Settings** → **Secrets and variables** → **Actions**
2. 点击 **New repository secret**
3. **名称**填：`GLADOS`（必须全大写）
4. **值**填入所有账号的 Cookie，用**换行**分隔（最清晰）：
   **多账号示例**：
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
