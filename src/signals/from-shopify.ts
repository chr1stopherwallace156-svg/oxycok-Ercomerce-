import crypto from "node:crypto";

import type {
  Signal
} from "./types.js";

type ShopifyOrder = {
  id?: number | string;
  admin_graphql_api_id?: string;
  created_at?: string;
  currency?: string;
  total_price?: string;
  subtotal_price?: string;
  customer?: {
    id?: number | string;
  } | null;
  line_items?: Array<{
    id?: number | string;
    product_id?: number | string;
    variant_id?: number | string;
    quantity?: number;
    price?: string;
  }>;
};

function stableSignalId(
  input: unknown
): string {
  return crypto
    .createHash("sha256")
    .update(
      JSON.stringify(input)
    )
    .digest("hex");
}

export function signalsFromOrderCreated(
  payload: ShopifyOrder,
  sourceEventId: string,
  shopDomain?: string
): Signal[] {
  const signals: Signal[] = [];

  const orderId =
    String(
      payload.admin_graphql_api_id ??
      payload.id ??
      "unknown"
    );

  const observedAt =
    payload.created_at
      ? new Date(
          payload.created_at
        )
      : new Date();

  const total =
    Number(
      payload.total_price ?? 0
    );

  signals.push({
    signalId:
      stableSignalId({
        sourceEventId,
        metric:
          "order_count",
        orderId
      }),

    sourceId:
      "SRC-SHOPIFY-001",

    sourceEventId,

    signalType:
      "ORDER_CREATED",

    entityType:
      "order",

    entityId:
      orderId,

    metricName:
      "order_count",

    numericValue:
      1,

    authority:
      "TRANSACTIONAL_TRUTH",

    confidence:
      1,

    observedAt,

    metadata: {
      shopDomain,
      currency:
        payload.currency
    }
  });

  signals.push({
    signalId:
      stableSignalId({
        sourceEventId,
        metric:
          "gross_revenue",
        orderId
      }),

    sourceId:
      "SRC-SHOPIFY-001",

    sourceEventId,

    signalType:
      "ORDER_CREATED",

    entityType:
      "order",

    entityId:
      orderId,

    metricName:
      "gross_revenue",

    numericValue:
      total,

    authority:
      "TRANSACTIONAL_TRUTH",

    confidence:
      1,

    observedAt,

    metadata: {
      shopDomain,
      currency:
        payload.currency
    }
  });

  for (
    const line
    of payload.line_items ?? []
  ) {
    const productId =
      String(
        line.product_id ??
        "unknown"
      );

    const quantity =
      Number(
        line.quantity ?? 0
      );

    const unitPrice =
      Number(
        line.price ?? 0
      );

    signals.push({
      signalId:
        stableSignalId({
          sourceEventId,
          metric:
            "product_units_sold",
          productId,
          lineId:
            line.id
        }),

      sourceId:
        "SRC-SHOPIFY-001",

      sourceEventId,

      signalType:
        "ORDER_LINE",

      entityType:
        "product",

      entityId:
        productId,

      metricName:
        "units_sold",

      numericValue:
        quantity,

      authority:
        "TRANSACTIONAL_TRUTH",

      confidence:
        1,

      observedAt,

      metadata: {
        variantId:
          line.variant_id,
        unitPrice
      }
    });

    signals.push({
      signalId:
        stableSignalId({
          sourceEventId,
          metric:
            "product_revenue",
          productId,
          lineId:
            line.id
        }),

      sourceId:
        "SRC-SHOPIFY-001",

      sourceEventId,

      signalType:
        "ORDER_LINE",

      entityType:
        "product",

      entityId:
        productId,

      metricName:
        "product_revenue",

      numericValue:
        quantity *
        unitPrice,

      authority:
        "TRANSACTIONAL_TRUTH",

      confidence:
        1,

      observedAt,

      metadata: {
        variantId:
          line.variant_id
      }
    });
  }

  return signals;
}