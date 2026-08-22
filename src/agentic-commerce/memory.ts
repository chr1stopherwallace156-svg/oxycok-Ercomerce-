export type MemoryClass =
  | "SESSION_CONTEXT"
  | "EXPLICIT_PREFERENCE"
  | "ORDER_CONTEXT"
  | "EXPERIMENT_CONTEXT"
  | "TEMPORARY_REASONING_STATE";

export type CommerceMemoryRecord = {
  memoryId: string;

  customerId?: string;

  sessionId?: string;

  memoryClass:
    MemoryClass;

  key: string;

  value: unknown;

  source:
    string;

  createdAt:
    Date;

  expiresAt?:
    Date;

  consentBasis?:
    string;
};