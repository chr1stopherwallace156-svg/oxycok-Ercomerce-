import type {
  AgentToolDefinition
} from "../types.js";

export const getOrderStatusTool:
  AgentToolDefinition = {

  toolId:
    "TOOL-ORDER-STATUS-001",

  name:
    "get_order_status",

  description:
    "Retrieve verified current order state for the authenticated customer.",

  risk:
    "R0_READ_ONLY",

  authority:
    "ALLOW",

  readOnly:
    true,

  requiresCurrentState:
    true,

  inputSchemaVersion:
    "1.0.0",

  async execute(
    input,
    context
  ) {

    const orderId =
      String(
        input.orderId ?? ""
      );

    if (!orderId) {
      return {
        status: "FAILED",
        reason:
          "ORDER_ID_REQUIRED"
      };
    }

    if (!context.customerId) {
      return {
        status: "BLOCKED",
        reason:
          "CUSTOMER_IDENTITY_REQUIRED"
      };
    }

    /*
     * NEXT:
     * bind orderId to customerId
     * before retrieving order truth.
     */

    return {
      status: "SUCCESS",

      data: {
        orderId,
        customerId:
          context.customerId,

        status:
          "ORDER_BACKEND_NOT_CONNECTED"
      }
    };
  }
};