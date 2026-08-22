import type {
  AgentToolDefinition
} from "../types.js";

export const searchProductsTool:
  AgentToolDefinition = {

  toolId:
    "TOOL-PRODUCT-SEARCH-001",

  name:
    "search_products",

  description:
    "Search eligible store products using customer intent.",

  risk:
    "R0_READ_ONLY",

  authority:
    "ALLOW",

  readOnly:
    true,

  requiresCurrentState:
    false,

  inputSchemaVersion:
    "1.0.0",

  async execute(
    input
  ) {

    const query =
      String(
        input.query ?? ""
      ).trim();

    if (!query) {
      return {
        status: "FAILED",
        reason:
          "QUERY_REQUIRED"
      };
    }

    // TODO:
    // connect to qualified
    // recommendation/search layer.

    return {
      status: "SUCCESS",

      data: {
        query,
        products: [],
        source:
          "SEARCH_LAYER_NOT_CONNECTED"
      }
    };
  }
};