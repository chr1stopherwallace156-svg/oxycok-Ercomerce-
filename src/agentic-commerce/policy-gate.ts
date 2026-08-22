import type {
  AgentToolContext,
  AgentToolDefinition,
  AgentToolInput,
  AgentToolResult
} from "./types.js";

export type PolicyDecision =
  | {
      decision: "ALLOW";
    }
  | {
      decision: "HUMAN_APPROVAL";
      reason: string;
    }
  | {
      decision: "DENY";
      reason: string;
    };

export function evaluateToolPolicy(
  tool: AgentToolDefinition,
  input: AgentToolInput,
  context: AgentToolContext
): PolicyDecision {

  void input;

  if (
    tool.authority === "DENY"
  ) {
    return {
      decision: "DENY",
      reason:
        "TOOL_AUTHORITY_DENIED"
    };
  }

  if (
    tool.authority ===
      "HUMAN_APPROVAL" &&
    !context.approvedActionId
  ) {
    return {
      decision:
        "HUMAN_APPROVAL",

      reason:
        "EXPLICIT_APPROVAL_REQUIRED"
    };
  }

  if (
    tool.risk ===
      "R3_FINANCIAL" &&
    !context.approvedActionId
  ) {
    return {
      decision:
        "HUMAN_APPROVAL",

      reason:
        "FINANCIAL_ACTION_REQUIRES_APPROVAL"
    };
  }

  if (
    tool.risk ===
      "R4_HIGH_CONSEQUENCE"
  ) {
    return {
      decision: "DENY",
      reason:
        "HIGH_CONSEQUENCE_AGENT_EXECUTION_DISABLED"
    };
  }

  return {
    decision: "ALLOW"
  };
}

export function blockedResult(
  reason: string
): AgentToolResult {

  return {
    status: "BLOCKED",
    reason
  };
}