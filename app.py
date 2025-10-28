from fastapi import FastAPI, UploadFile, Request

from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

provider = TracerProvider()
processor = SimpleSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

app = FastAPI()
FastAPIInstrumentor.instrument_app(app)

def trace_id():
    return trace.get_current_span().get_span_context().trace_id

@app.post("/large")
async def large(request: Request):
    await request.body()
    print("reproduce", "large", trace_id())


@app.get("/any")
async def any():
    print("reproduce", "any  ", trace_id())
