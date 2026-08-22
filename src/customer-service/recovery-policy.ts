import type {

  ResolutionAuthority,

  ServiceIntent,

  ServiceRisk

} from "./types.js";

export type RecoveryPolicyInput = {

  intent: ServiceIntent;

  risk: ServiceRisk;

  sentimentNegativeProbability:

    number;

  intentConfidence:

    number;

  evidenceAvailable:

    boolean;

  humanRequested:

    boolean;

};

export type RecoveryPolicyDecision = {

  authority:

    ResolutionAuthority;

  escalate:

    boolean;

  reason:

    string;

};

export function

evaluateRecoveryPolicy(

  input: RecoveryPolicyInput

): RecoveryPolicyDecision {

  if (

    input.humanRequested

  ) {

    return {

      authority:

        "HUMAN_APPROVAL",

      escalate:

        true,

      reason:

        "CUSTOMER_REQUESTED_HUMAN"

    };

  }

  if (

    input.risk === "CRITICAL"

  ) {

    return {

      authority:

        "HUMAN_APPROVAL",

      escalate:

        true,

      reason:

        "CRITICAL_RISK"

    };

  }

  const financiallyConsequential =

    input.intent === "REFUND"

    ||

    input.intent ===

      "CANCELLATION"

    ||

    input.intent ===

      "PAYMENT";

  if (

    financiallyConsequential

  ) {

    return {

      authority:

        "DRAFT_ACTION",

      escalate:

        true,

      reason:

        "FINANCIAL_CONSEQUENCE"

    };

  }

  if (

    !input.evidenceAvailable

  ) {

    return {

      authority:

        "ANSWER_ONLY",

      escalate:

        true,

      reason:

        "REQUIRED_EVIDENCE_MISSING"

    };

  }

  /*

   * The following scores are

   * evidence signals only.

   *

   * We deliberately DO NOT

   * hard-code "0.3 means escalate."

   *

   * Model thresholds must come from

   * qualification/configuration.

   */

  if (

    input.intentConfidence <= 0

  ) {

    return {

      authority:

        "ANSWER_ONLY",

      escalate:

        true,

      reason:

        "INTENT_UNRESOLVED"

    };

  }

  return {

    authority:

      "ANSWER_ONLY",

    escalate:

      false,

    reason:

      "AI_ASSISTANCE_ELIGIBLE"

  };

}