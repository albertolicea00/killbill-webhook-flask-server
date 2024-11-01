from flask import Blueprint, request, jsonify, current_app as app  # type: ignore
from src.logger import Logger

bp = Blueprint("config/", __name__)
logger = Logger(__name__)


@bp.route("/config", methods=["POST"], strict_slashes=False)
def POST():
    """
    Endpoint to config Killbill callback notifications.
    ---
    description: This endpoint refresh notifications subscription to Killbill.
    parameters:
      - name: cb
        in: body
        type: string
        required: false
        description: The callback URL for Killbill notifications. If not provided, the default URL will be used.
    responses:
      200:
        description: Successful operation
      503:
        description: KillBill retrieve push notification response
          schema:
            type: object
            properties:
              auditLogs:
                type: string
              key:
                type: string
              values:
                type: array
    """
    default_CALLBACK = f"{app.config.FLASK_PROTOCOL}://{app.config.FLASK_HOST}:{app.config.FLASK_PORT}/listeners/kb_callback"
    CALLBACK_URL = request.json.get("cb", default_CALLBACK)

    killbill_api = app.services.killbill.api
    killbill_header = app.services.killbill.header

    # Add new notifications subscription
    killbill_api.tenant.create_push_notification(
        header=killbill_header, callback_url=CALLBACK_URL
    )

    # Check notifications subscription
    response = killbill_api.tenant.retrieve_push_notifications(header=killbill_header)
    if CALLBACK_URL in response["values"]:
        return jsonify(), 200
    else:
        return jsonify(response), 503


@bp.route("/config", methods=["GET"], strict_slashes=False)
def GET():
    """
    Endpoint to get Killbill callback notifications.
    ---
    description: This endpoint get notifications subscription to Killbill.
    responses:
      200:
        description: KillBill retrieve push notification response
        schema:
          type: object
          properties:
            auditLogs:
              type: string
            key:
              type: string
            values:
              type: array
    """
    killbill_api = app.services.killbill.api
    killbill_header = app.services.killbill.header

    # Check notifications subscription
    response = killbill_api.tenant.retrieve_push_notifications(header=killbill_header)
    return jsonify(response), 200


@bp.route("/config", methods=["DELETE"], strict_slashes=False)
def DELETE():
    """
    Endpoint to clean Killbill callback notifications.
    ---
    description: This endpoint delete notifications subscription to Killbill.
    responses:
      200:
        description: Successful operation
    """
    killbill_api = app.services.killbill.api
    killbill_header = app.services.killbill.header

    # Delete existing notifications subscription
    response = killbill_api.tenant.delete_push_notification(header=killbill_header)
    return jsonify(), 200
