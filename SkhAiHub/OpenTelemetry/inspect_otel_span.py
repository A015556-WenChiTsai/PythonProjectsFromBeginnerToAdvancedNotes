import asyncio
import logging
from fastapi import FastAPI
from fastapi.testclient import TestClient

# 你指定的 4 個核心匯入
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
import json
# 設定 Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# ==========================================
# 初始化 OTel (跟你的 main.py 一樣)
# ==========================================
resource = Resource(attributes={"service.name": "inspect_service"})
logger.info(f"resource:{resource}")
logger.info(f"Resource 屬性: {resource.attributes}")
pretty_resource = json.dumps(dict(resource.attributes), indent=4)
logger.info(f"完整的 Resource 資訊:\n{pretty_resource}")
provider = TracerProvider(resource=resource)
logger.info("provider:{provider}")
trace.set_tracer_provider(provider)

app = FastAPI()
FastAPIInstrumentor.instrument_app(app)

@app.get("/inspect")
async def inspect_otel():
    # 1. 獲取目前的 Span 物件
    current_span = trace.get_current_span()
    
    # 2. 從 Span 中獲取 Context (上下文)
    # Context 包含了 Trace ID 和 Span ID
    ctx = current_span.get_span_context()
    
    # 3. 提取資訊
    # trace_id: 識別「整個請求」的唯一碼 (32位字元)
    # span_id: 識別「目前這個動作」的唯一碼 (16位字元)
    t_id = format(ctx.trace_id, '032x') if ctx.trace_id else "無 TraceID"
    s_id = format(ctx.span_id, '016x') if ctx.span_id else "無 SpanID"
    is_recording = current_span.is_recording() # 檢查是否正在記錄中

    # 4. 使用 logger.info 印出來
    logger.info("-" * 40)
    logger.info(f"【OpenTelemetry 內部資訊窺探】")
    logger.info(f"  > Trace ID: {t_id}")
    logger.info(f"  > Span ID : {s_id}")
    logger.info(f"  > 正在記錄中? : {is_recording}")
    logger.info("-" * 40)

    return {"trace_id": t_id, "span_id": s_id}

# ==========================================
# 執行與測試
# ==========================================
def run_demo():
    client = TestClient(app)
    logger.info("發送請求到 /inspect...")
    client.get("/inspect")

if __name__ == "__main__":
    # 參考你的 async_cm_scenarios.py 結構
    try:
        run_demo()
    except Exception as e:
        # 如果在某些特殊環境下需要 loop
        import asyncio
        loop = asyncio.get_event_loop()
        run_demo()