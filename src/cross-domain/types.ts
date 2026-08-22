export type DomainAuthority =
  | "FIRST_PARTY_TRANSACTIONAL"
  | "FIRST_PARTY_BEHAVIOR"
  | "AGGREGATE_EXTERNAL_CONTEXT"
  | "RESEARCH_FIXTURE";

export type DomainIdentityMode =
  | "SHARED_EXPLICIT_IDENTITY"
  | "CONSENTED_LINKAGE"
  | "AGGREGATE_ONLY"
  | "NO_LINKAGE";

export type CommerceDomain = {
  domainId: string;

  name: string;

  description: string;

  authority:
    DomainAuthority;

  identityMode:
    DomainIdentityMode;

  entityTypes: string[];

  allowedTransferUses:
    string[];

  prohibitedTransferUses:
    string[];
};

export type DomainPair = {
  sourceDomainId: string;
  targetDomainId: string;

  semanticRelatedness:
    | "HIGH"
    | "MEDIUM"
    | "LOW"
    | "UNKNOWN";

  overlapAvailable:
    boolean;

  overlapDefinition?: string;

  transferStatus:
    | "DISCOVERED"
    | "ELIGIBLE_FOR_RESEARCH"
    | "TESTING"
    | "SUPPORTED"
    | "NEGATIVE_TRANSFER"
    | "REJECTED";
};