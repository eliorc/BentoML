import typing as t
from typing import TYPE_CHECKING

from multipart.multipart import parse_options_header
from starlette.requests import Request
from starlette.responses import Response

from ...exceptions import BentoMLException, InvalidArgument
from ..utils.formparser import (
    concat_to_multipart_responses,
    populate_multipart_requests,
)
from .base import IODescriptor, IOType

if TYPE_CHECKING:
    # noqa: F811
    from .file import File
    from .image import Image
    from .json import JSON
    from .numpy import NumpyNdarray
    from .pandas import PandasDataFrame, PandasSeries
    from .text import Text


MultipartIO = t.Dict[str, IOType]


class Multipart(IODescriptor[MultipartIO]):
    """
    `Multipart` defines API specification for the inputs/outputs of a Service, where inputs/outputs
     of a Service can receive/send a `multipart` request/responses as specified in your API function signature.

    .. Toy implementation of a sklearn service::
        # sklearn_svc.py
        import bentoml
        from bentoml.io import NumpyNdarray, Multipart, JSON
        import bentoml.sklearn

        runner = bentoml.sklearn.load_runner("sklearn_model_clf")

        svc = bentoml.Service("iris-classifier", runners=[runner])
        input_spec = Multipart(arr=NumpyNdarray(), annotations=JSON())
        output_spec = Multipart(output=NumpyNdarray(), result=JSON())

        @svc.api(input=input_spec, output=output_spec)
        def predict(arr, annotations):
            res = runner.run(arr)
            return {"output":res, "result":annotations}

    Users then can then serve this service with `bentoml serve`::
        % bentoml serve ./sklearn_svc.py:svc --reload

        (Press CTRL+C to quit)
        [INFO] Starting BentoML API server in development mode with auto-reload enabled
        [INFO] Serving BentoML Service "iris-classifier" defined in "sklearn_svc.py"
        [INFO] API Server running on http://0.0.0.0:5000

    Users can then send a cURL requests like shown in different terminal session::
        % curl -X POST -H "Content-Type: multipart/form-data" -F annotations=@test.json -F arr='[5,4,3,2]' http://0.0.0.0:5000/predict

        --b1d72c201a064ecd92a17a412eb9208e
        Content-Disposition: form-data; name="output"
        content-length: 1
        content-type: application/json

        1
        --b1d72c201a064ecd92a17a412eb9208e
        Content-Disposition: form-data; name="result"
        content-length: 13
        content-type: application/json

        {"foo":"bar"}
        --b1d72c201a064ecd92a17a412eb9208e--

    Args:
        inputs (`Dict[str, IODescriptor]`):
            Dictionary consisting keys as inputs definition for a Multipart request/response, values
             as IODescriptor supported by BentoML. Currently we support Image, NumpyNdarray, PandasDataFrame,
             PandasSeries, Text, File.

    .. notes::
        Make sure to match your input params in your API function to the keys defined under `Multipart`::
            ┌───────────────────────────────────────────────────────┐
            │                                                       │
            │ ┌───────────────────────────────────────────────────┐ │
            │ │ Multipart(arr=NumpyNdarray(), annotations=JSON()) │ │
            │ └─────────────────────┬─────────────┬───────────────┘ │
            │                       │             │                 │
            │                       │       ┌─────┘                 │
            │                       │       │                       │
            │       ┌───────────────▼───────▼─────────┐             │
            │       │  def predict(arr, annotations): │             │
            │       └─────────────────────────────────┘             │
            │                                                       │
            └───────────────────────────────────────────────────────┘

    Returns:
        IO Descriptor that represents Multipart request/response.
    """  # noqa: LN001

    def __init__(
        self,
        **inputs: t.Union[
            "Image",
            "JSON",
            "Text",
            "NumpyNdarray",
            "PandasDataFrame",
            "PandasSeries",
            "File",
        ],
    ):
        for descriptor in inputs.values():
            if isinstance(descriptor, Multipart):  # pragma: no cover
                raise InvalidArgument(
                    "Multipart IO can not contain nested Multipart item"
                )
        self._inputs: t.Dict[
            str,
            t.Union[
                "Image",
                "JSON",
                "Text",
                "NumpyNdarray",
                "PandasDataFrame",
                "PandasSeries",
                "File",
            ],
        ] = inputs

    def openapi_schema_type(self) -> t.Dict[str, t.Any]:
        return {
            "type": "object",
            "properties": {
                k: io.openapi_schema_type() for k, io in self._inputs.items()
            },
        }

    def openapi_request_schema(self) -> t.Dict[str, t.Any]:
        """Returns OpenAPI schema for incoming requests"""
        return {"multipart/form-data": {"schema": self.openapi_schema_type()}}

    def openapi_responses_schema(self) -> t.Dict[str, t.Any]:
        """Returns OpenAPI schema for outcoming responses"""
        return {"multipart/form-data": {"schema": self.openapi_schema_type()}}

    async def from_http_request(self, request: Request) -> MultipartIO:
        ctype, _ = parse_options_header(request.headers["content-type"])
        if ctype != b"multipart/form-data":
            raise BentoMLException(
                f"{self.__class__.__name__} only accepts `multipart/form-data` as Content-Type header, got {ctype} instead."
            )

        res: MultipartIO = dict()
        reqs = await populate_multipart_requests(request)

        for k, i in self._inputs.items():
            req = reqs[k]
            v = await i.from_http_request(req)
            res[k] = v
        return res

    async def to_http_response(self, obj: MultipartIO) -> Response:
        res_mapping: t.Dict[str, Response] = {}
        for k, io_ in self._inputs.items():
            data = obj[k]
            # TODO(aarnphm): fix with stubs
            res_mapping[k] = await io_.to_http_response(data)  # type: ignore[reportGeneralTypeIssue]
        return await concat_to_multipart_responses(res_mapping)