import crypto from "node:crypto";
import { env } from "../config/env.js";

export function verifyShopifyWebhook(
  rawBody: Buffer,
  receivedHmac: string | undefined
): boolean {
  if (!receivedHmac) {
    return false;
  }

  const calculatedHmac = crypto
    .createHmac(
      "sha256",
      env.SHOPIFY_WEBHOOK_SECRET
    )
    .update(rawBody)
    .digest("base64");

  const expected = Buffer.from(
    calculatedHmac,
    "utf8"
  );

  const received = Buffer.from(
    receivedHmac,
    "utf8"
  );

  if (expected.length !== received.length) {
    return false;
  }

  return crypto.timingSafeEqual(
    expected,
    received
  );
}