export type ConnectorStatus =
  | "ENABLED"
  | "DISABLED"
  | "DEGRADED"
  | "QUARANTINED";

export type AccessClass =
  | "OFFICIAL_API"
  | "OFFICIAL_EXPORT"
  | "LICENSED_PROVIDER"
  | "PUBLIC_DATASET"
  | "MANUAL_RESEARCH"
  | "APPROVED_PUBLIC_WEB";

export type ConnectorAuthority =
  | "TRANSACTIONAL_TRUTH"
  | "FIRST_PARTY_BEHAVIOR"
  | "MARKET_OBSERVATION"
  | "EXTERNAL_CONTEXT"
  | "RESEARCH_EVIDENCE";

export type RawObservation = {
  observationId: string;

  sourceId: string;

  sourceRecordId?: string;

  observationType: string;

  entityType: string;

  entityKey: string;

  geography?: string;

  currency?: string;

  observedAt: Date;

  fetchedAt: Date;

  authority:
    ConnectorAuthority;

  payload:
    Record<string, unknown>;

  provenance: {
    connectorId: string;
    connectorVersion: string;
    accessClass: AccessClass;
    requestId?: string;
  };
};

export interface MarketConnector {
  connectorId: string;

  connectorVersion: string;

  sourceId: string;

  status:
    ConnectorStatus;

  accessClass:
    AccessClass;

  authority:
    ConnectorAuthority;

  collect():
    Promise<RawObservation[]>;
}