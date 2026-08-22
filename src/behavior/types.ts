export type BehavioralEventType =
  | "SESSION_STARTED"
  | "PAGE_VIEWED"
  | "PRODUCT_VIEWED"
  | "RECOMMENDATION_IMPRESSION"
  | "PRODUCT_CLICKED"
  | "ADD_TO_CART"
  | "CHECKOUT_STARTED"
  | "PURCHASE_COMPLETED";

export type BehavioralEvent = {
  eventId: string;

  eventType: BehavioralEventType;

  occurredAt: string;

  sessionId: string;

  anonymousId?: string;

  customerId?: string;

  pageViewId?: string;

  productId?: string;

  variantId?: string;

  recommendation?: {
    requestId: string;

    rankingId: string;

    impressionId: string;

    position: number;

    candidateSetSize: number;

    modelId: string;

    modelVersion: string;

    experimentId?: string;

    experimentVariant?: string;
  };

  context: {
    pageType?:
      | "HOME"
      | "PRODUCT"
      | "COLLECTION"
      | "CART"
      | "SEARCH"
      | "OTHER";

    deviceType?: string;

    country?: string;

    timezone?: string;

    referrer?: string;
  };

  schemaVersion: "1.0.0";
};