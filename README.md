# 📱 Android Log Analysis Project

**Description:**  
This project demonstrates the collection and analysis of logs from Android app `StrimQA`

---

## 🔹 What Was Done

- ✅ **Enabled Developer Mode** and **USB Debugging** ongf the device.  
- ✅ Collected app logs using **`adb logcat`**.  
- ✅ Processed logs with a **Python script**:
  - Filtered **errors (E/)** and **warnings (W/)**  
  - Normalized log lines (removed timestamps, unique IDs)  
  - Counted **repeated messages**  
  - Generated reports in **TXT, CSV, and JSON**  

---

## 🔹 Results

**Top Errors / Warnings:**

| Error / Warning | Count |
|-----------------|-------|
| `E/BLASTBufferQueue: Can't acquire next buffer` | 70 |
| `E/ActivityManagerWrapper: mainTaskId=1391` | 18 |
| `W/PackageConfigPersister: App-specific configuration not found` | 10 |
| `E/ActivityManagerWrapper: mainTaskId=1392` | 9 |
| `W/WindowManager: finishDrawingWindow: mDrawState=DRAW_PENDING` | 8 |
| Other `WindowManager`, `MIUISafety-Monitor`, `Auth` warnings | 4–8 |

---

## 🔹 Conclusion

- The script **quickly highlights the most frequent errors** in large log files.  
- Helps QA engineers **identify key app issues** without manually analyzing the entire log.  

---

## ⚡ Usage Example

```bash
python analyze_logs.py --input logs/logs_strimqa.txt --top 10