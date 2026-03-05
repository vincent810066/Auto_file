# Quick Open 小工具

這是一個用 Python 寫的簡單 CLI 工具，可讓你：

- 預先設定要開啟的檔案路徑
- 新增或刪除清單項目
- 一鍵開啟全部預設檔案

## 需求

- Python 3.8+

## 快速開始

```bash
python3 quick_open.py init
```

會建立設定檔：`quick_open_files.json`。

## 使用方式

### 1) 新增要一鍵開啟的檔案

```bash
python3 quick_open.py add ~/Desktop/todo.txt ~/Documents/report.docx
```

### 2) 檢視目前清單

```bash
python3 quick_open.py list
```

### 3) 刪除項目

```bash
python3 quick_open.py remove ~/Desktop/todo.txt
```

### 4) 一鍵開啟所有檔案

```bash
python3 quick_open.py open
```

## 其他參數

- 指定自訂設定檔：

```bash
python3 quick_open.py --config /path/to/my_files.json list
```

- 只預覽要開啟哪些檔案（不真的開）：

```bash
python3 quick_open.py open --dry-run
```

## 設定檔格式

`quick_open_files.json` 是一個 JSON 陣列，例如：

```json
[
  "/home/user/Desktop/todo.txt",
  "/home/user/Documents/report.docx"
]
```
