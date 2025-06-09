# YouTube 轉 MP3 網頁工具

這是一個現代化、互動式的 YouTube 轉 MP3 網頁應用，支援多種音質選擇、即時進度與狀態顯示，並擁有美觀的淡紫色主題介面。適合所有需要快速、方便、免費下載 YouTube 音樂為 MP3 的用戶。

## 主要功能

- 支援所有 YouTube 影片一鍵轉 MP3
- 多種音質選擇（64kbps ~ 320kbps，預設最高音質）
- 即時顯示「下載進度條」與「下載/轉換狀態」
- 下載完成時顯示完整檔案資訊（標題、檔名、音質、檔案大小）
- 下載按鈕直接觸發下載，不會跳轉分頁
- 響應式設計，手機/電腦皆美觀
- 主色調淡紫色，搭配浮動畫面音符、圓角卡片、漸層按鈕、動畫 icon
- 操作簡單、免安裝用戶端軟體

## 介面特色

- 標題與音符 icon 動畫，主題氛圍明確
- 背景有多個淡紫色音符元素，並有緩慢浮動動畫
- 進度條下方即時顯示「正在下載...」、「正在轉換...」等狀態
- 下載完成時，顯示美化資訊卡，包含標題、檔名、音質、檔案大小
- 所有互動按鈕、進度條、卡片皆有現代化動畫與漸層

## 安裝與使用

### 前置需求
- Python 3.9 或更高版本
- FFmpeg（用於音訊轉檔，僅需安裝於伺服器端）

### 安裝步驟
1. 下載專案原始碼：
```bash
git clone https://github.com/your-username/yt2mp3.git
cd yt2mp3
```
2. 建立虛擬環境並啟動：
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# 或
venv\Scripts\activate  # Windows
```
3. 安裝依賴：
```bash
pip install -r requirements.txt
```
4. 安裝 FFmpeg：
- MacOS: `brew install ffmpeg`
- Ubuntu: `sudo apt-get install ffmpeg`
- Windows: 下載 FFmpeg 並加入系統路徑
5. 啟動伺服器：
```bash
python app.py
```
6. 在瀏覽器開啟：
- 本地：http://127.0.0.1:5001
- 同一區網：http://你的IP:5001

## 雲端部署

可部署於 Render、Heroku、Google Cloud Run、AWS、DigitalOcean、Linode 等平台。

## Docker 部署（推薦 Render、Railway、Fly.io、Linode 等平台）

1. 專案根目錄已內建 Dockerfile 和 docker-compose.yml，內容如下：

   **Dockerfile**:
   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   RUN apt-get update && apt-get install -y \
       ffmpeg \
       && rm -rf /var/lib/apt/lists/*

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 5000

   CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
   ```

   **docker-compose.yml**:
   ```yaml
   version: '3'
   services:
     web:
       build: .
       ports:
         - "5000:5000"
       volumes:
         - ./downloads:/app/downloads
       restart: always
   ```

2. 推送到 GitHub。

### Render 部署
1. Render 建立 Web Service 時，選擇你的 repo，Render 會自動偵測 Dockerfile。
   - Build Command、Start Command 留空即可。
   - 其他設定照預設。
2. 等待自動建置與啟動，完成後即可用 Render 提供的網址訪問。

### Linode 部署（推薦）

1. **註冊與建立 Linode 主機**
   - 前往 [Linode 官網](https://www.linode.com/) 註冊帳號（需綁定信用卡）。
   - 登入後，點選「Create」→「Linode」。
   - 選擇映像檔（Image）：**Ubuntu 22.04 LTS**。
   - 選擇地區（Region）：建議選亞洲（如 Tokyo、Singapore）。
   - 選擇方案（Plan）：**Shared CPU / Nanode 1GB ($5/mo)**。
   - 設定 root 密碼（請記好！）。
   - 點「Create Linode」建立主機。
   - 等待幾分鐘，Linode 會分配一個 **公開 IP**。

2. **連線到 Linode 主機**
   ```bash
   ssh root@你的Linode IP
   ```
   （第一次連線會問你是否信任，輸入 yes）

3. **安裝 Docker & Docker Compose**
   ```bash
   apt update
   apt install -y docker.io docker-compose git
   systemctl enable --now docker
   ```

4. **下載你的專案**
   ```bash
   git clone https://github.com/patrick0516/yt2mp3.git
   cd yt2mp3
   ```

5. **啟動專案（Docker Compose）**
   ```bash
   docker-compose up -d
   ```

6. **開放防火牆（如有）**
   Linode 預設所有 port 都開放，但建議只開 80/443/5000：
   ```bash
   ufw allow 22
   ufw allow 80
   ufw allow 443
   ufw allow 5000
   ufw enable
   ```
   （如有用 UFW 防火牆）

7. **安裝 Nginx 反向代理（可選，建議）**
   這樣你可以用 80/443 port（http/https）存取，不用記 port 號。
   ```bash
   apt install -y nginx
   ```
   
   建立 Nginx 設定檔 `/etc/nginx/sites-available/yt2mp3`：
   ```nginx
   server {
       listen 80;
       server_name _;

       location / {
           proxy_pass http://localhost:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```
   
   啟用設定並重啟 Nginx：
   ```bash
   ln -s /etc/nginx/sites-available/yt2mp3 /etc/nginx/sites-enabled/
   nginx -t
   systemctl restart nginx
   ```

8. **用瀏覽器測試**
   打開 `http://你的Linode IP/`  
   應該就能看到你的 yt2mp3 網頁！

9. **（可選）綁定自訂網域**
   - 在你的網域 DNS 設定 A 記錄，指向 Linode IP。
   - 修改 Nginx 設定 `server_name` 為你的網域。
   - 可用 [Let's Encrypt](https://certbot.eff.org/instructions) 免費申請 SSL。

10. **（可選）自動重啟/開機自啟**
    Docker Compose 會自動重啟容器。  
    如需更進階監控，可用 systemd 或 supervisor。

### Linode 部署常見問題

1. **如果 docker-compose 報錯**  
   請確認 `docker-compose.yml` 內容正確，且檔案名稱是 `docker-compose.yml`（不是 `docker-compose.yaml`）。

2. **如果容器啟動失敗**  
   請執行 `docker-compose logs` 看錯誤訊息。

3. **如果網站打不開**  
   請確認 Linode 防火牆有開放 5000 port，或改用 Nginx 反向代理（用 80 port）。

## 注意事項
- 請遵守 YouTube 服務條款，僅供個人學習/備份用途
- 不可用於商業用途，請尊重版權

## 技術棧
- 後端：Python / Flask
- 前端：HTML / CSS / JavaScript
- 音訊處理：FFmpeg
- YouTube 下載：yt-dlp

## linode
停用重啟
sudo systemctl stop yt2mp3
sudo systemctl restart yt2mp3
sudo systemctl disable yt2mp3

## 貢獻
歡迎提交 Pull Request 或 Issue 來改進這個專案！ 
