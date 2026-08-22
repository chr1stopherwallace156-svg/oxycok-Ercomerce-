import type {
  ServiceDecision
} from "./types.js";

export type ResponsePolicyInput = {
  decision:
    ServiceDecision;

  hasOrderEvidence:
    boolean;

  hasProductEvidence:
    boolean;

  hasPolicyEvidence:
    boolean;
};

export type ResponsePolicyResult = {
  mayRespond:
    boolean;

  mayPromiseRefund:
    boolean;

  mayPromiseCancellation:
    boolean;

  mustEscalate:
    boolean;

  reason:
    string;
};

export function evaluateResponsePolicy(
  input: ResponsePolicyInput
): ResponsePolicyResult {

  const {
    decision,
    hasOrderEvidence,
    hasProductEvidence,
    hasPolicyEvidence
  } = input;

  if (
    decision.shouldEscalate &&
    !decision.canAnswerWithAI
  ) {
    return {
      mayRespond:
        false,

      mayPromiseRefund:
        false,

      mayPromiseCancellation:
        false,

      mustEscalate:
        true,

      reason:
        "AI_RESPONSE_BLOCKED_BY_RISK"
    };
  }

  if (
    decision.intent ===
      "ORDER_STATUS" &&
    !hasOrderEvidence
  ) {
    return {
      mayRespond:
        false,

      mayPromiseRefund:
        false,

      mayPromiseCancellation:
        false,

      mustEscalate:
        true,

      reason:
        "ORDER_EVIDENCE_REQUIRED"
    };
  }

  if (
    (
      decision.intent ===
        "PRODUCT_QUESTION" ||
      decision.intent ===
        "PRODUCT_FIT" ||
      decision.intent ===
        "PRODUCT_COMPARISON"
    ) &&
    !hasProductEvidence
  ) {
    return {
      mayRespond:
        false,

      mayPromiseRefund:
        false,

      mayPromiseCancellation:
        false,

      mustEscalate:
        false,

      reason:
        "PRODUCT_EVIDENCE_REQUIRED"
    };
  }

  if (
    (
      decision.intent ===
        "REFUND" ||
      decision.intent ===
        "RETURN" ||
      decision.intent ===
        "CANCELLATION"
    ) &&
    !hasPolicyEvidence
  ) {
    return {
      mayRespond:
        false,

      mayPromiseRefund:
        false,

      mayPromiseCancellation:
        false,

      mustEscalate:
        true,

      reason:
        "POLICY_EVIDENCE_REQUIRED"
    };
  }

  return {
    mayRespond:
      true,

    mayPromiseRefund:
      false,

    mayPromiseCancellation:
      false,

    mustEscalate:
      decision.shouldEscalate,

    reason:
      "ANSWER_ALLOWED"
  };
}