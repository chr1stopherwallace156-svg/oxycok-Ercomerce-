import crypto from "node:crypto";

import type {
  InterventionCandidate
} from "./types.js";

export type TriggerContext = {
  customerId?: string;

  sessionId?: string;

  dwellSeconds?: number;

  productViewsLastHour?: number;

  hasCart:
    boolean;

  hasPurchase:
    boolean;

  proactiveInterventionsThisSession:
    number;

  lastInterventionDismissed:
    boolean;
};

function createId(
  input: unknown
): string {
  return crypto
    .createHash("sha256")
    .update(
      JSON.stringify(
        input
      )
    )
    .digest("hex");
}

export function evaluateTriggers(
  context: TriggerContext
): InterventionCandidate | null {

  if (
    context
      .proactiveInterventionsThisSession
      >= 1
  ) {
    return null;
  }

  if (
    context
      .lastInterventionDismissed
  ) {
    return null;
  }

  if (
    context.hasCart &&
    !context.hasPurchase
  ) {
    return {
      interventionId:
        createId({
          type:
            "CART_ASSISTANCE",
          sessionId:
            context.sessionId
        }),

      customerId:
        context.customerId,

      sessionId:
        context.sessionId,

      triggerType:
        "CART_WITHOUT_PURCHASE",

      interventionType:
        "CHAT_INVITE",

      reason:
        "Customer has items in cart and may benefit from assistance.",

      priority:
        "HIGH"
    };
  }

  if (
    (
      context
        .productViewsLastHour ??
      0
    ) >= 3
  ) {
    return {
      interventionId:
        createId({
          type:
            "REPEAT_PRODUCT_VIEW",
          sessionId:
            context.sessionId
        }),

      customerId:
        context.customerId,

      sessionId:
        context.sessionId,

      triggerType:
        "REPEATED_PRODUCT_VIEWS",

      interventionType:
        "PRODUCT_HELP",

      reason:
        "Repeated product views suggest a possible unresolved question.",

      priority:
        "MEDIUM"
    };
  }

  if (
    (
      context
        .dwellSeconds ??
      0
    ) >= 60
  ) {
    return {
      interventionId:
        createId({
          type:
            "LONG_DWELL",
          sessionId:
            context.sessionId
        }),

      customerId:
        context.customerId,

      sessionId:
        context.sessionId,

      triggerType:
        "LONG_DWELL",

      interventionType:
        "CHAT_INVITE",

      reason:
        "Long product-page dwell may justify a low-pressure assistance prompt.",

      priority:
        "LOW"
    };
  }

  return null;
}