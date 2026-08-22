import {
  type Request,
  type Response,
  Router
} from "express";

import {
  verifyShopifyWebhook
} from "./verify.js";

export const shopifyWebhookRouter = Router();

shopifyWebhookRouter.post(
  "/",
  async (
    req: Request,
    res: Response
  ) => {
    const rawBody = req.body as Buffer;

    const hmac = req.header(
      "X-Shopify-Hmac-Sha256"
    );

    const topic = req.header(
      "X-Shopify-Topic"
    );

    const shopDomain = req.header(
      "X-Shopify-Shop-Domain"
    );

    const webhookId = req.header(
      "X-Shopify-Webhook-Id"
    );

    const valid = verifyShopifyWebhook(
      rawBody,
      hmac
    );

    if (!valid) {
      console.warn(
        JSON.stringify({
          event: "shopify_webhook_rejected",
          reason: "invalid_hmac",
          topic,
          shopDomain,
          webhookId
        })
      );

      res.status(401).json({
        status: "rejected"
      });

      return;
    }

    let payload: unknown;

    try {
      payload = JSON.parse(
        rawBody.toString("utf8")
      );
    } catch {
      console.warn(
        JSON.stringify({
          event: "shopify_webhook_rejected",
          reason: "invalid_json",
          topic,
          shopDomain,
          webhookId
        })
      );

      res.status(400).json({
        status: "invalid_json"
      });

      return;
    }

    console.log(
      JSON.stringify({
        event:
          "shopify_webhook_verified",
        topic,
        shopDomain,
        webhookId,
        receivedAt:
          new Date().toISOString()
      })
    );

    // IMPORTANT:
    //
    // payload is verified but NOT yet authoritative
    // internal commerce state.
    //
    // Gen2 will add:
    //
    // - normalized event schema
    // - durable storage
    // - idempotency enforcement
    // - duplicate detection
    // - processing status
    // - replay behavior
    //
    void payload;

    res.status(200).json({
      status: "accepted"
    });
  }
);