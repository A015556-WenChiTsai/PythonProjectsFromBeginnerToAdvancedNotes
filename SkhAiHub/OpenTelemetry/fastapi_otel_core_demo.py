import asyncio
import logging
from fastapi import FastAPI
from fastapi.testclient import TestClient

# 這是你指定的 4 個核心匯入
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
import json
# ==========================================
# 設定 Logging
# ==========================================
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# ==========================================
# 場景 1：沒有 OpenTelemetry (純 FastAPI)
# ==========================================
def run_without_otel():
    print("\n>>> [場景 1: 沒有 OTel]")
    app = FastAPI()

    @app.get("/")
    async def root():
        # 嘗試獲取追蹤資訊
        current_span = trace.get_current_span()
        if current_span.is_recording():
        # 只有真正的 Span 才有 attributes
        # 注意：在某些版本中，attributes 可能需要透過 .attributes 存取
            attrs = dict(current_span.attributes) if hasattr(current_span, "attributes") else {}
            current_span_info = json.dumps(attrs, indent=4)
            logger.info(f"完整的 current_span 資訊:\n{current_span_info}")
        else:
            logger.info("目前的 Span 是 NonRecordingSpan (空殼子)，沒有屬性可看。")
        trace_id = current_span.get_span_context().trace_id
        logger.info(f"  [Log] 處理請求中... (目前的 TraceID: {trace_id})")
        return {"message": "Hello World"}

    client = TestClient(app)
    client.get("/")
    print("  (結論：TraceID 為 0，代表沒有任何追蹤機制在運作)")

# ==========================================
# 場景 2：有了 OpenTelemetry (你 main.py 中的寫法)
# ==========================================
def run_with_otel():
    print("\n>>> [場景 2: 有了 OTel 核心配置]")
    
    # 1. Resource: 定義服務身份
    resource = Resource(attributes={
        "service.name": "skh_aihub_demo",
        "service.namespace": "skh"
    })
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)
    app = FastAPI()

    # 3. FastAPIInstrumentor: 最關鍵的一行！
    # 它就像一個「自動監視器」，會攔截所有進入 app 的請求
    FastAPIInstrumentor.instrument_app(app)

    @app.get("/")
    async def root():
        # 獲取目前的追蹤資訊
        current_span = trace.get_current_span()
        ctx = current_span.get_span_context()
        # 將 trace_id 轉為 16 進位字串方便閱讀
        trace_id_hex = format(ctx.trace_id, '032x')
        
        logger.info(f"  [Log] 處理請求中... (目前的 TraceID: {trace_id_hex})")
        return {"message": "Hello World"}

    client = TestClient(app)
    client.get("/")
    print("  (結論：TraceID 不再是 0！這串唯一的 ID 會跟隨這個請求直到結束)")

# ==========================================
# 執行入口 (參考你的 async_cm_scenarios.py 寫法)
# ==========================================
async def main():
    # 這裡不需要 async，因為 TestClient 是同步觸發的，但為了符合你的結構：
    # run_without_otel()
    run_with_otel()

if __name__ == "__main__":
    try:
        # 嘗試直接執行
        asyncio.run(main())
    except RuntimeError:
        # 針對 Jupyter / VS Code Interactive 環境的處理
        import asyncio
        loop = asyncio.get_event_loop()
        # 如果是在互動式環境，我們直接呼叫函數即可
        run_without_otel()
        run_with_otel()