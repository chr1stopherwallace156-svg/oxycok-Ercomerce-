import { z } from "zod";

const RecommendationContextSchema =
  z.object({
    requestId: z.string().min(1),

    rankingId: z.string().min(1),

    impressionId: z.string().min(1),

    position: z
      .number()
      .int()
      .nonnegative(),

    candidateSetSize: z
      .number()
      .int()
      .positive(),

    modelId: z.string().min(1),

    modelVersion:
      z.string().min(1),

    experimentId:
      z.string().optional(),

    experimentVariant:
      z.string().optional()
  });

export const BehavioralEventSchema =
  z.object({
    eventId:
      z.string().min(1),

    eventType:
      z.enum([
        "SESSION_STARTED",
        "PAGE_VIEWED",
        "PRODUCT_VIEWED",
        "RECOMMENDATION_IMPRESSION",
        "PRODUCT_CLICKED",
        "ADD_TO_CART",
        "CHECKOUT_STARTED",
        "PURCHASE_COMPLETED"
      ]),

    occurredAt:
      z.string().datetime(),

    sessionId:
      z.string().min(1),

    anonymousId:
      z.string().optional(),

    customerId:
      z.string().optional(),

    pageViewId:
      z.string().optional(),

    productId:
      z.string().optional(),

    variantId:
      z.string().optional(),

    recommendation:
      RecommendationContextSchema
        .optional(),

    context:
      z.object({
        pageType:
          z.enum([
            "HOME",
            "PRODUCT",
            "COLLECTION",
            "CART",
            "SEARCH",
            "OTHER"
          ])
          .optional(),

        deviceType:
          z.string()
          .optional(),

        country:
          z.string()
          .optional(),

        timezone:
          z.string()
          .optional(),

        referrer:
          z.string()
          .optional()
      }),

    schemaVersion:
      z.literal("1.0.0")
  })
  .superRefine(
    (event, ctx) => {
      if (
        event.eventType ===
          "RECOMMENDATION_IMPRESSION" &&
        !event.recommendation
      ) {
        ctx.addIssue({
          code:
            z.ZodIssueCode.custom,

          message:
            "RECOMMENDATION_IMPRESSION requires recommendation context"
        });
      }

      if (
        event.eventType ===
          "RECOMMENDATION_IMPRESSION" &&
        !event.productId
      ) {
        ctx.addIssue({
          code:
            z.ZodIssueCode.custom,

          message:
            "RECOMMENDATION_IMPRESSION requires productId"
        });
      }
    }
  );

export type ValidatedBehavioralEvent =
  z.infer<
    typeof BehavioralEventSchema
  >;
export const behavioralEvents =
  pgTable(
    "behavioral_events",
    {
      id: uuid("id")
        .defaultRandom()
        .primaryKey(),

      eventId:
        text("event_id")
          .notNull(),

      eventType:
        text("event_type")
          .notNull(),

      sessionId:
        text("session_id")
          .notNull(),

      anonymousId:
        text("anonymous_id"),

      customerId:
        text("customer_id"),

      pageViewId:
        text("page_view_id"),

      productId:
        text("product_id"),

      variantId:
        text("variant_id"),

      requestId:
        text("request_id"),

      rankingId:
        text("ranking_id"),

      impressionId:
        text("impression_id"),

      position:
        integer("position"),

      candidateSetSize:
        integer(
          "candidate_set_size"
        ),

      modelId:
        text("model_id"),

      modelVersion:
        text("model_version"),

      experimentId:
        text("experiment_id"),

      experimentVariant:
        text(
          "experiment_variant"
        ),

      occurredAt:
        timestamp(
          "occurred_at",
          {
            withTimezone: true
          }
        ).notNull(),

      context:
        jsonb("context")
          .notNull(),

      schemaVersion:
        text(
          "schema_version"
        ).notNull(),

      createdAt:
        timestamp(
          "created_at",
          {
            withTimezone: true
          }
        )
          .notNull()
          .defaultNow()
    },
    (table) => ({
      eventUnique:
        uniqueIndex(
          "behavioral_events_event_id_unique"
        ).on(
          table.eventId
        ),

      impressionIndex:
        index(
          "behavioral_events_impression_idx"
        ).on(
          table.impressionId
        ),

      sessionIndex:
        index(
          "behavioral_events_session_idx"
        ).on(
          table.sessionId
        ),

      productIndex:
        index(
          "behavioral_events_product_idx"
        ).on(
          table.productId
        ),

      occurredIndex:
        index(
          "behavioral_events_occurred_idx"
        ).on(
          table.occurredAt
        )
    })
  );