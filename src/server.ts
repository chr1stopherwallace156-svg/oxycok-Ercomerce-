import express from "express";

import { env } from "./config/env.js";

import {
  shopifyGraphQL,
  ShopifyRequestError
} from "./shopify/client.js";

import {
  SHOP_INFO_QUERY
} from "./shopify/queries.js";

import {
  shopifyWebhookRouter
} from "./webhooks/route.js";

const app = express();

/**
 * Shopify webhook route MUST receive
 * the original raw request bytes.
 *
 * Therefore it is mounted BEFORE
 * express.json().
 */
app.use(
  "/webhooks/shopify",
  express.raw({
    type: "application/json"
  }),
  shopifyWebhookRouter
);

/**
 * Normal API routes can use JSON parsing.
 */
app.use(express.json());

app.get(
  "/health",
  (_req, res) => {
    res.json({
      status: "ok",
      service: "oxycok-commerce",
      timestamp:
        new Date().toISOString()
    });
  }
);

app.get(
  "/internal/shopify/shop",
  async (_req, res) => {
    try {
      const data =
        await shopifyGraphQL<{
          shop: {
            id: string;
            name: string;
            email: string;
            myshopifyDomain: string;
            primaryDomain: {
              host: string;
              url: string;
            };
            currencyCode: string;
            timezoneAbbreviation: string;
          };
        }>(SHOP_INFO_QUERY);

      res.json({
        status: "verified",
        shop: data.shop
      });
    } catch (error) {
      if (
        error instanceof
        ShopifyRequestError
      ) {
        console.error({
          event:
            "shopify_request_failed",
          message: error.message,
          status: error.status,
          details: error.details
        });

        res.status(502).json({
          status: "shopify_error",
          message: error.message
        });

        return;
      }

      console.error(error);

      res.status(500).json({
        status: "internal_error"
      });
    }
  }
);

app.listen(
  env.PORT,
  () => {
    console.log(
      JSON.stringify({
        event: "server_started",
        port: env.PORT,
        nodeEnv: env.NODE_ENV,
        shopifyApiVersion:
          env.SHOPIFY_API_VERSION
      })
    );
  }
);