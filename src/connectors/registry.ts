import type {
  AccessClass,
  ConnectorAuthority,
  ConnectorStatus
} from "./types.js";

export type ConnectorRegistryEntry = {
  connectorId: string;

  sourceId: string;

  name: string;

  status:
    ConnectorStatus;

  accessClass:
    AccessClass;

  authority:
    ConnectorAuthority;

  containsPersonalData:
    boolean;

  credentialRequired:
    boolean;

  rateLimitPolicy:
    "PROVIDER_DEFINED"
    | "INTERNAL_CONSERVATIVE";

  productionEligible:
    boolean;
};

export const CONNECTOR_REGISTRY:
  Record<
    string,
    ConnectorRegistryEntry
  > = {

  "CONN-SHOPIFY-001": {
    connectorId:
      "CONN-SHOPIFY-001",

    sourceId:
      "SRC-SHOPIFY-001",

    name:
      "Shopify Admin GraphQL",

    status:
      "ENABLED",

    accessClass:
      "OFFICIAL_API",

    authority:
      "TRANSACTIONAL_TRUTH",

    containsPersonalData:
      true,

    credentialRequired:
      true,

    rateLimitPolicy:
      "PROVIDER_DEFINED",

    productionEligible:
      true
  },

  "CONN-GTRENDS-001": {
    connectorId:
      "CONN-GTRENDS-001",

    sourceId:
      "SRC-GTRENDS-001",

    name:
      "Google Trends API",

    status:
      "DISABLED",

    accessClass:
      "OFFICIAL_API",

    authority:
      "EXTERNAL_CONTEXT",

    containsPersonalData:
      false,

    credentialRequired:
      true,

    rateLimitPolicy:
      "PROVIDER_DEFINED",

    productionEligible:
      true
  },

  "CONN-AMAZON-001": {
    connectorId:
      "CONN-AMAZON-001",

    sourceId:
      "SRC-AMAZON-001",

    name:
      "Amazon Creators API",

    status:
      "DISABLED",

    accessClass:
      "OFFICIAL_API",

    authority:
      "MARKET_OBSERVATION",

    containsPersonalData:
      false,

    credentialRequired:
      true,

    rateLimitPolicy:
      "PROVIDER_DEFINED",

    productionEligible:
      true
  },

  "CONN-ALIEXPRESS-001": {
    connectorId:
      "CONN-ALIEXPRESS-001",

    sourceId:
      "SRC-ALIEXPRESS-001",

    name:
      "AliExpress Market Data",

    status:
      "QUARANTINED",

    accessClass:
      "LICENSED_PROVIDER",

    authority:
      "MARKET_OBSERVATION",

    containsPersonalData:
      false,

    credentialRequired:
      true,

    rateLimitPolicy:
      "PROVIDER_DEFINED",

    productionEligible:
      false
  }
};