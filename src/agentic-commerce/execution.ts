import crypto from "node:crypto";

import {
  blockedResult,
  evaluateToolPolicy
} from "./policy-gate.js";

import {
  toolRegistry
} from "./tool-registry.js";

import type {
  AgentToolContext,
  AgentToolInput,
  AgentToolResult
} from "./types.js";

function canonicalInputHash(
  input: AgentToolInput
): string {

  return crypto
    .createHash("sha256")
    .update(
      JSON.stringify(input)
    )
    .digest("hex");
}

export async function executeAgentTool(
  toolName: string,
  input: AgentToolInput,
  context: AgentToolContext
): Promise<AgentToolResult> {

  const tool =
    toolRegistry.get(
      toolName
    );

  const inputHash =
    canonicalInputHash(
      input
    );

  void inputHash;

  const policy =
    evaluateToolPolicy(
      tool,
      input,
      context
    );

  if (
    policy.decision ===
      "DENY"
  ) {
    return blockedResult(
      policy.reason
    );
  }

  if (
    policy.decision ===
      "HUMAN_APPROVAL"
  ) {
    return blockedResult(
      policy.reason
    );
  }

  try {
    return await tool.execute(
      input,
      context
    );
  } catch (error) {
    return {
      status: "FAILED",

      reason:
        error instanceof Error
          ? error.message
          : "UNKNOWN_TOOL_FAILURE"
    };
  }
}