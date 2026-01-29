import json
import time
import socket

# ==========================================
# 1. 傳統的 Logging (就像隨手寫的紙條)
# ==========================================
def traditional_logging(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    # 輸出只是一串文字
    return f"[{timestamp}] INFO: {message}"

# ==========================================
# 2. OpenTelemetry + OTLP (就像標準化的國際快遞包裹)
# ==========================================
def otel_otlp_simulation(message, attributes):
    # OTLP 協議要求資料必須是「結構化」的
    # 它包含了：誰發出的(Resource)、內容是什麼(Body)、額外資訊(Attributes)
    otlp_packet = {
        "resourceLogs": [{
            "resource": {
                "attributes": [
                    {"key": "service.name", "value": {"stringValue": "MyPythonApp"}},
                    {"key": "host.name", "value": {"stringValue": socket.gethostname()}}
                ]
            },
            "scopeLogs": [{
                "logRecords": [{
                    "timeUnixNano": int(time.time() * 1e9),
                    "severityText": "INFO",
                    "body": {"stringValue": message},
                    "attributes": [
                        {"key": k, "value": {"stringValue": str(v)}} 
                        for k, v in attributes.items()
                    ]
                }]
            }]
        }]
    }
    return json.dumps(otlp_packet, indent=2, ensure_ascii=False)

# --- 執行對比 ---

msg = "使用者登入成功"
extra_info = {"user_id": "A123", "ip": "192.168.1.1"}

print("=== 1. 傳統 Logging 的樣子 ===")
print(traditional_logging(msg))

print("\n" + "="*30 + "\n")

print("=== 2. OpenTelemetry 轉換成 OTLP 格式後的樣子 ===")
print(otel_otlp_simulation(msg, extra_info))