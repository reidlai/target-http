"""http target class."""

from __future__ import annotations

from singer_sdk import typing as th
from singer_sdk.target_base import Target

from target_http.sinks import (
    httpSink,
)


class Targethttp(Target):
    """Sample target for http."""

    name = "target-http"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "url",
            th.StringType,
            description="The URL to which to send data",
            
        ),
        th.Property(
            "method",
            th.StringType,
            description="HTTP Method",
            allowed_values=["GET", "POST"],
        ),
        th.Property(
            "tls",
            th.ObjectType(
                th.Property("skip_verify", th.BooleanType, default=False),
                th.Property("cert_file_path", th.StringType, required=False),
                th.Property("key_file_path", th.StringType, required=False),
                th.Property("cacert_file_path", th.StringType, required=False),
            ),
            description="TLS Properties",
        ),
        th.Property(
            "headers",
            th.ArrayType(
                th.ObjectType(
                    th.Property("name", th.StringType),
                    th.Property("value", th.StringType),
                )
            ),
            description="The path to the target output file",
        ),
    ).to_dict()

    default_sink_class = httpSink


if __name__ == "__main__":
    Targethttp.cli()
