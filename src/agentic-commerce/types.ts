export type AgentToolRisk =
  | "R0_READ_ONLY"
  | "R1_INTERNAL_REVERSIBLE"
  | "R2_CUSTOMER_VISIBLE"
  | "R3_FINANCIAL"
  | "R4_HIGH_CONSEQUENCE";

export type AgentToolAuthority =
  | "ALLOW"
  | "HUMAN_APPROVAL"
  | "DENY";

export type AgentToolInput =
  Record<string, unknown>;

export type AgentToolResult =
  | {
      status: "SUCCESS";
      data: unknown;
    }
  | {
      status: "BLOCKED";
      reason: string;
    }
  | {
      status: "FAILED";
      reason: string;
    };

export type AgentToolContext = {
  requestId: string;

  conversationId?: string;

  customerId?: string;

  sessionId?: string;

  shopDomain?: string;

  actor:
    | "CUSTOMER_AGENT"
    | "MERCHANT_AGENT"
    | "CUSTOMER_SERVICE_AGENT";

  approvedActionId?: string;
};

export type AgentToolDefinition = {
  toolId: string;

  name: string;

  description: string;

  risk: AgentToolRisk;

  authority:
    AgentToolAuthority;

  readOnly: boolean;

  requiresCurrentState:
    boolean;

  inputSchemaVersion:
    string;

  execute: (
    input: AgentToolInput,
    context: AgentToolContext
  ) => Promise<AgentToolResult>;
};