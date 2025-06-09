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

可部署於 Render、Heroku、Google Cloud Run、AWS、DigitalOcean 等平台。

## Docker 部署（推薦 Render、Railway、Fly.io 等平台）

1. 專案根目錄已內建 Dockerfile，內容如下：
   ```dockerfile
   FROM python:3.11-slim
   RUN apt-get update && apt-get install -y ffmpeg
   WORKDIR /app
   COPY . /app
   RUN pip install --upgrade pip
   RUN pip install -r requirements.txt
   EXPOSE 10000
   CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
   ```
2. 推送到 GitHub。
3. Render 建立 Web Service 時，選擇你的 repo，Render 會自動偵測 Dockerfile。
   - Build Command、Start Command 留空即可。
   - 其他設定照預設。
4. 等待自動建置與啟動，完成後即可用 Render 提供的網址訪問。

## 注意事項
- 請遵守 YouTube 服務條款，僅供個人學習/備份用途
- 不可用於商業用途，請尊重版權

## 技術棧
- 後端：Python / Flask
- 前端：HTML / CSS / JavaScript
- 音訊處理：FFmpeg
- YouTube 下載：yt-dlp

## 貢獻
歡迎提交 Pull Request 或 Issue 來改進這個專案！ 
