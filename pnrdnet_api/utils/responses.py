from flask import make_response, jsonify

INVALID_FIELD_NAME_SENT_422 = {
    "http_code": 422,
    "status": "invalidField",
    "message": "Invalid Field",
}
INVALID_INPUT_422 = {
    "http_code": 422,
    "status": "invalidInput",
    "message": "Invalid Input",
}
INVALID_OR_KEY_422 = {
    "http_code": 422,
    "status": "duplicatedOrInvalidKey",
    "message": "Duplicated or Invalid Key",
}
MAX_SIZE_LIMIT_422 = {
    "http_code": 422,
    "status": "maxSizeLimit",
    "message": "The request exceeded the maximum size limit",
}
MISSING_PARAMETERS_422 = {
    "http_code": 422,
    "status": "missingParameter",
    "message": "Missing Parameter",
}
BAD_REQUEST_400 = {
    "http_code": 400,
    "status": "badRequest",
    "message": "Dar Request",
}
SERVER_ERROR_500 = {
    "http_code": 500,
    "status": "serverError",
    "message": "Server Error",
}
SERVER_ERROR_404 = {
    "http_code": 404,
    "status": "notFound",
    "message": "Resource not found",
}
UNAUTHORIZED_403 = {
    "http_code": 403,
    "status": "notAuthorized",
    "message": "You are not authorized to executed this action",
}
SUCCESS_200 = {"http_code": 200, "status": "success"}
SUCCESS_201 = {"http_code": 201, "status": "success"}
SUCCESS_204 = {"http_code": 204, "status": "success"}


def response_with(
    response, value=None, message=None, error=None, headers={}, pagination=None
):
    """
    Cria as respostas de retorno da API
        request:
            any
        response:
            status: String
            any
    """

    result = {}
    if value is not None:
        result.update(value)

    if response.get("message", None) is not None:
        result.update({"message": response["message"]})

    result.update({"status": response["status"]})

    if error is not None:
        result.update({"errors": error})

    if pagination is not None:
        result.update({"pagination": pagination})

    headers.update({"Access-Control-Allow-Origin": "*"})
    headers.update({"server": "PNRD NET"})

    return make_response(jsonify(result), response["http_code"], headers)
