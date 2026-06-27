from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider

from opentelemetry.sdk.trace.export import BatchSpanProcessor, SimpleSpanProcessor, ConsoleSpanExporter

from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

import os 

ARIZE_SPACE_ID = os.environ["ARIZE_SPACE_ID"]
ARIZE_API_KEY = os.environ["ARIZE_API_KEY"]


def build_resource(config: dict) -> Resource:
    return Resource.create(config)

def build_provider(resource):
    return TracerProvider(resource=resource)

#### Exporters
def build_console():

    return ConsoleSpanExporter()

def run_telemetry_setup():
    config = {"service.name": "MCP test","openinference.project.name": "MCP test"}

    resource = build_resource(config)
    #trace_provider = build_provider(resource)

    trace_provider = TracerProvider(resource=resource)

    #exporter = ConsoleSpanExporter()
    exporter = OTLPSpanExporter(
        endpoint="https://otlp.arize.com/v1/traces",
        headers={
            "arize-space-id": ARIZE_SPACE_ID,
            "arize-api-key": ARIZE_API_KEY,
        },
    )
    #trace_provider.add_span_processor(BatchSpanProcessor(exporter))
    trace_provider.add_span_processor(SimpleSpanProcessor(exporter))

    trace.set_tracer_provider(trace_provider)
    # trace.get_tracer_provider().add_span_processor(
    #     BatchSpanProcessor(ConsoleSpanExporter())
    # )
