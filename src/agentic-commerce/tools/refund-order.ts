import type {
  AgentToolDefinition
} from "../types.js";

export const refundOrderTool:
  AgentToolDefinition = {

  toolId:
    "TOOL-REFUND-001",

  name:
    "refund_order",

  description:
    "Create a refund action candidate for an eligible order.",

  risk:
    "R3_FINANCIAL",

  authority:
    "HUMAN_APPROVAL",

  readOnly:
    false,

  requiresCurrentState:
    true,

  inputSchemaVersion:
    "1.0.0",

  async execute(
    input
  ) {

    /*
     * No Shopify mutation yet.
     *
     * Eventually this tool will:
     *
     * 1. validate order
     * 2. validate refund eligibility
     * 3. validate amount
     * 4. validate current state
     * 5. validate approval receipt
     * 6. call protected mutation sink
     */

    return {
      status: "FAILED",

      reason:
        "REFUND_MUTATION_NOT_IMPLEMENTED"
    };
  }
};