from fastapi import HTTPException, Request
from core.config import CLERK_WEBHOOK_SECRET
from svix import Webhook
import logging
from users.schemas import WebhookSchema

logger = logging.getLogger("router")


async def verify_webhook_signature(request: Request) -> WebhookSchema:
    webhook = Webhook(CLERK_WEBHOOK_SECRET)

    try:
        # Read the request body
        payload = await request.body()

        # Retrieve the headers from the request
        headers = dict(request.headers)

        # Get the Svix headers for verification
        svix_id = headers.get("svix-id")
        svix_timestamp = headers.get("svix-timestamp")
        svix_signature = headers.get("svix-signature")

        # If there are missing Svix headers, error out
        if not svix_id or not svix_timestamp or not svix_signature:
            return HTTPException("Error occurred -- no svix headers", status_code=400)

        # Attempt to verify the incoming webhook
        # If successful, the payload will be available from 'evt'
        # If the verification fails, error out and return error code
        evt = webhook.verify(
            payload,
            {
                "svix-id": svix_id,
                "svix-timestamp": svix_timestamp,
                "svix-signature": svix_signature,
            },
        )

    except Exception as err:
        # Log the error and return an error response
        logger.error(f"Webhook failed to verify. Error: {str(err)}")
        raise HTTPException(status_code=400, detail=str(err))

    # Grab the ID and TYPE of the Webhook
    wh_id = evt["data"]["id"]
    event_type = evt["type"]

    logger.info(f"Webhook with an ID of {wh_id} and type of {event_type}")
    # Console log the full payload to view

    return evt
