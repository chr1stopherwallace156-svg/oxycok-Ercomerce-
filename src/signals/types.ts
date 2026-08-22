export type SignalAuthority =
  | "TRANSACTIONAL_TRUTH"
  | "FIRST_PARTY_BEHAVIOR"
  | "EXTERNAL_CONTEXT"
  | "RESEARCH_EVIDENCE"
  | "DERIVED_ANALYSIS";

export type Signal = {
  signalId: string;

  sourceId: string;

  sourceEventId?: string;

  signalType: string;

  entityType: string;

  entityId: string;

  metricName: string;

  numericValue?: number;

  textValue?: string;

  geography?: string;

  authority:
    SignalAuthority;

  confidence?: number;

  observedAt: Date;

  expiresAt?: Date;

  metadata:
    Record<
      string,
      unknown
    >;
};