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