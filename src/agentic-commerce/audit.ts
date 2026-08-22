export type ToolExecutionAudit = {
  executionId: string;

  requestId: string;

  toolId: string;

  toolName: string;

  actor: string;

  customerId?: string;

  sessionId?: string;

  inputHash: string;

  policyDecision:
    | "ALLOW"
    | "HUMAN_APPROVAL"
    | "DENY";

  resultStatus:
    | "SUCCESS"
    | "BLOCKED"
    | "FAILED";

  startedAt: string;

  completedAt: string;

  error?: string;
};