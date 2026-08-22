export type FeatureDefinition = {
  featureId: string;

  name: string;

  description: string;

  entityType: string;

  valueType:
    | "number"
    | "string"
    | "boolean";

  version: string;

  requiredSignals:
    string[];

  leakageRisk:
    | "LOW"
    | "MEDIUM"
    | "HIGH";

  productionEligible:
    boolean;
};

export const FEATURE_REGISTRY:
  Record<
    string,
    FeatureDefinition
  > = {

  "FEATURE-PRODUCT-REVENUE-7D":
    {
      featureId:
        "FEATURE-PRODUCT-REVENUE-7D",

      name:
        "Product revenue trailing 7 days",

      description:
        "Total transactional product revenue in the seven days preceding the feature as-of time.",

      entityType:
        "product",

      valueType:
        "number",

      version:
        "1.0.0",

      requiredSignals: [
        "product_revenue"
      ],

      leakageRisk:
        "LOW",

      productionEligible:
        true
    },

  "FEATURE-PRODUCT-UNITS-7D":
    {
      featureId:
        "FEATURE-PRODUCT-UNITS-7D",

      name:
        "Product units sold trailing 7 days",

      description:
        "Units sold in the seven days before the feature cutoff.",

      entityType:
        "product",

      valueType:
        "number",

      version:
        "1.0.0",

      requiredSignals: [
        "units_sold"
      ],

      leakageRisk:
        "LOW",

      productionEligible:
        true
    },

  "FEATURE-PRODUCT-REVENUE-30D":
    {
      featureId:
        "FEATURE-PRODUCT-REVENUE-30D",

      name:
        "Product revenue trailing 30 days",

      description:
        "Total transactional product revenue in the thirty days preceding the as-of time.",

      entityType:
        "product",

      valueType:
        "number",

      version:
        "1.0.0",

      requiredSignals: [
        "product_revenue"
      ],

      leakageRisk:
        "LOW",

      productionEligible:
        true
    }
};