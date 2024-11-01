from flask import Blueprint, request, jsonify, current_app as app  # type: ignore
from src.logger import Logger
from src.events import *

bp = Blueprint("listener/", __name__)
logger = Logger(__name__)


@bp.route("/listener", methods=["POST"])
def POST():
    """
    Endpoint for processing events from Killbill's server.
    ---
    description: This is a webhook endpoint. Do not use it !! ( Just killbill automatic flow are authorized.)
    parameters:
      - in: body
        name: body
        required: true
    responses:
      200:
        description: Event processed successfully
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            message:
              type: string
              example: "Event processed"
            event_request:
              type: object
              additionalProperties: true
      400:
        description: Unknown event type
        schema:
          type: object
          properties:
            status:
              type: string
              example: "failed"
            message:
              type: string
              example: "Event not processed"
            event_request:
              type: object
              additionalProperties: true
    """
    data = request.get_json()
    event_type = data.get("eventType")
    # Dictionary mapping event types to lists of handler functions :
    #  - if handlers are registered, Execute handler function in the event_handlers mapping
    #  - if handlers are not found for the event type, log exception and returned error response (do noting)
    # NOTE: To create a sequence of actions, include them as functions executed within the handle events
    event_handlers = {
        "ACCOUNT_CREATION": handle_account_creation,
        "ACCOUNT_CHANGE": handle_account_change,
        "BLOCKING_STATE": handle_blocking_state,
        "BROADCAST_SERVICE": handle_broadcast_service,
        "SUBSCRIPTION_CREATION": handle_subscription_creation,
        "SUBSCRIPTION_PHASE": handle_subscription_phase,
        "SUBSCRIPTION_CHANGE": handle_subscription_change,
        "SUBSCRIPTION_CANCEL": handle_subscription_cancel,
        "SUBSCRIPTION_UNCANCEL": handle_subscription_uncancel,
        "SUBSCRIPTION_BCD_CHANGE": handle_subscription_bcd_change,
        "ENTITLEMENT_CREATION": handle_entitlement_creation,
        "ENTITLEMENT_CANCEL": handle_entitlement_cancel,
        "BUNDLE_PAUSE": handle_bundle_pause,
        "BUNDLE_RESUME": handle_bundle_resume,
        "OVERDUE_CHANGE": handle_overdue_change,
        "INVOICE_CREATION": handle_invoice_creation,
        "INVOICE_ADJUSTMENT": handle_invoice_adjustment,
        "INVOICE_NOTIFICATION": handle_invoice_notification,
        "INVOICE_PAYMENT_SUCCESS": handle_invoice_payment_success,
        "INVOICE_PAYMENT_FAILED": handle_invoice_payment_failed,
        "PAYMENT_SUCCESS": handle_payment_success,
        "PAYMENT_FAILED": handle_payment_failed,
        "TAG_CREATION": handle_tag_creation,
        "TAG_DELETION": handle_tag_deletion,
        "CUSTOM_FIELD_CREATION": handle_custom_field_creation,
        "CUSTOM_FIELD_DELETION": handle_custom_field_deletion,
        "TENANT_CONFIG_CHANGE": handle_tenant_config_change,
        "TENANT_CONFIG_DELETION": handle_tenant_config_deletion,
        # add new event types here if they are unsupported ...
    }

    handler = event_handlers.get(event_type)
    logger.info(f"event received from KillBill: '{event_type}' with data : {data}")
    if handler:
        handler(request)
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Event processed",
                    "event_request": data,
                }
            ),
            200,
        )
    else:
        # Handle unknown event type
        print(f"Unknown event received: {event_type} with data : {data}")
        return (
            jsonify(
                {
                    "status": "failed",
                    "message": "Event not processed",
                    "event_request": data,
                }
            ),
            400,
        )
