import {
  and,
  eq,
  gte,
  lt,
  sum
} from "drizzle-orm";

import {
  db
} from "../db/client.js";

import {
  signals
} from "../db/intelligence-schema.js";

async function trailingMetric(
  entityId: string,
  metricName: string,
  days: number,
  asOf: Date
): Promise<number> {

  const windowStart =
    new Date(
      asOf.getTime() -
      days *
      24 *
      60 *
      60 *
      1000
    );

  const result =
    await db
      .select({
        value:
          sum(
            signals.numericValue
          )
      })
      .from(signals)
      .where(
        and(
          eq(
            signals.entityType,
            "product"
          ),
          eq(
            signals.entityId,
            entityId
          ),
          eq(
            signals.metricName,
            metricName
          ),
          gte(
            signals.observedAt,
            windowStart
          ),
          lt(
            signals.observedAt,
            asOf
          )
        )
      );

  return Number(
    result[0]?.value ?? 0
  );
}

export async function
computeProductFeatures(
  productId: string,
  asOf: Date
) {
  const [
    revenue7d,
    revenue30d,
    units7d
  ] =
    await Promise.all([
      trailingMetric(
        productId,
        "product_revenue",
        7,
        asOf
      ),

      trailingMetric(
        productId,
        "product_revenue",
        30,
        asOf
      ),

      trailingMetric(
        productId,
        "units_sold",
        7,
        asOf
      )
    ]);

  return {
    productId,
    asOf,

    features: {
      "FEATURE-PRODUCT-REVENUE-7D":
        revenue7d,

      "FEATURE-PRODUCT-REVENUE-30D":
        revenue30d,

      "FEATURE-PRODUCT-UNITS-7D":
        units7d
    }
  };
}