import type {
  CommerceDomain
} from "./types.js";

export const DOMAIN_REGISTRY:
  Record<string, CommerceDomain> = {

  "DOMAIN-STORE-BEHAVIOR": {
    domainId:
      "DOMAIN-STORE-BEHAVIOR",

    name:
      "OXYCOK Store Behavior",

    description:
      "First-party storefront impressions, views, clicks, carts and sessions.",

    authority:
      "FIRST_PARTY_BEHAVIOR",

    identityMode:
      "SHARED_EXPLICIT_IDENTITY",

    entityTypes: [
      "session",
      "customer",
      "product"
    ],

    allowedTransferUses: [
      "recommendation research",
      "behavior modeling",
      "cold-start experiments"
    ],

    prohibitedTransferUses: [
      "sensitive attribute inference"
    ]
  },

  "DOMAIN-SHOPIFY-TRANSACTIONS": {
    domainId:
      "DOMAIN-SHOPIFY-TRANSACTIONS",

    name:
      "Shopify Transactions",

    description:
      "Orders, refunds and transactional outcomes.",

    authority:
      "FIRST_PARTY_TRANSACTIONAL",

    identityMode:
      "SHARED_EXPLICIT_IDENTITY",

    entityTypes: [
      "customer",
      "order",
      "product",
      "variant"
    ],

    allowedTransferUses: [
      "conversion labels",
      "retention modeling",
      "recommendation evaluation"
    ],

    prohibitedTransferUses: []
  },

  "DOMAIN-SOCIAL-TRENDS": {
    domainId:
      "DOMAIN-SOCIAL-TRENDS",

    name:
      "Aggregate Social Trends",

    description:
      "Aggregate market/content signals without person-level linkage.",

    authority:
      "AGGREGATE_EXTERNAL_CONTEXT",

    identityMode:
      "AGGREGATE_ONLY",

    entityTypes: [
      "keyword",
      "category",
      "market"
    ],

    allowedTransferUses: [
      "context features",
      "opportunity discovery"
    ],

    prohibitedTransferUses: [
      "person-level user embedding transfer",
      "customer identity stitching"
    ]
  }
};