import {
  toolRegistry
} from "./tool-registry.js";

import {
  searchProductsTool
} from "./tools/search-products.js";

import {
  getOrderStatusTool
} from "./tools/get-order-status.js";

import {
  refundOrderTool
} from "./tools/refund-order.js";

export function registerAgentTools():
  void {

  toolRegistry.register(
    searchProductsTool
  );

  toolRegistry.register(
    getOrderStatusTool
  );

  toolRegistry.register(
    refundOrderTool
  );
}