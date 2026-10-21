from flask import jsonify

def success_response(data=None, message=None, meta=None, code=200):
    response = {"status": "success"}

    if message:
        response["message"] = message

    if data is not None:
        response["data"] = data

    if meta:
        response["meta"] = meta

    return jsonify(response), code           


def error_response(message, errors=None, code=400):
    response = {
        "status": "error",
        "message": message
    }

    if errors:
        response["errors"] = errors

    return jsonify(response), code   


def custom_paginate(data: list, page: int = 1, per_page: int = 20) -> list:
    start = (page - 1) * per_page
    end = start + per_page 
    return data[start:end]


