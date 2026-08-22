import type {
  ServiceDecision,
  ServiceIntent,
  ServiceRequest,
  ServiceRisk
} from "./types.js";

function detectIntent(
  message: string
): ServiceIntent {
  const normalized =
    message.toLowerCase();

  if (
    normalized.includes(
      "refund"
    )
  ) {
    return "REFUND";
  }

  if (
    normalized.includes(
      "cancel"
    )
  ) {
    return "CANCELLATION";
  }

  if (
    normalized.includes(
      "charged twice"
    ) ||
    normalized.includes(
      "double charge"
    )
  ) {
    return "PAYMENT";
  }

  if (
    normalized.includes(
      "where is my order"
    ) ||
    normalized.includes(
      "order status"
    )
  ) {
    return "ORDER_STATUS";
  }

  if (
    normalized.includes(
      "shipping"
    ) ||
    normalized.includes(
      "delivery"
    )
  ) {
    return "SHIPPING";
  }

  if (
    normalized.includes(
      "return"
    )
  ) {
    return "RETURN";
  }

  if (
    normalized.includes(
      "complaint"
    ) ||
    normalized.includes(
      "angry"
    ) ||
    normalized.includes(
      "terrible"
    )
  ) {
    return "COMPLAINT";
  }

  if (
    normalized.includes(
      "size"
    ) ||
    normalized.includes(
      "fit"
    )
  ) {
    return "PRODUCT_FIT";
  }

  if (
    normalized.includes(
      "compare"
    ) ||
    normalized.includes(
      "difference"
    )
  ) {
    return "PRODUCT_COMPARISON";
  }

  return "PRODUCT_QUESTION";
}

function determineRisk(
  intent: ServiceIntent,
  message: string
): ServiceRisk {

  const normalized =
    message.toLowerCase();

  if (
    normalized.includes(
      "fraud"
    ) ||
    normalized.includes(
      "stolen card"
    ) ||
    normalized.includes(
      "chargeback"
    )
  ) {
    return "CRITICAL";
  }

  if (
    intent === "REFUND" ||
    intent ===
      "CANCELLATION" ||
    intent === "PAYMENT"
  ) {
    return "HIGH";
  }

  if (
    intent === "COMPLAINT" ||
    intent === "RETURN"
  ) {
    return "MEDIUM";
  }

  return "LOW";
}

export function evaluateServiceRequest(
  request: ServiceRequest
): ServiceDecision {

  const intent =
    request.intent ??
    detectIntent(
      request.message
    );

  const risk =
    request.risk ??
    determineRisk(
      intent,
      request.message
    );

  if (
    request.humanRequested
  ) {
    return {
      conversationId:
        request.conversationId,

      intent,

      risk,

      authority:
        "HUMAN_APPROVAL",

      shouldEscalate:
        true,

      escalationReason:
        "customer_requested_human",

      canAnswerWithAI:
        false
    };
  }

  if (
    risk === "CRITICAL"
  ) {
    return {
      conversationId:
        request.conversationId,

      intent,

      risk,

      authority:
        "HUMAN_APPROVAL",

      shouldEscalate:
        true,

      escalationReason:
        "critical_risk",

      canAnswerWithAI:
        false
    };
  }

  if (
    risk === "HIGH"
  ) {
    return {
      conversationId:
        request.conversationId,

      intent,

      risk,

      authority:
        "DRAFT_ACTION",

      shouldEscalate:
        true,

      escalationReason:
        "financial_or_account_consequence",

      canAnswerWithAI:
        true
    };
  }

  return {
    conversationId:
      request.conversationId,

    intent,

    risk,

    authority:
      "ANSWER_ONLY",

    shouldEscalate:
      false,

    canAnswerWithAI:
      true
  };
}