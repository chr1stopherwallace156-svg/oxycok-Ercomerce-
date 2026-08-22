import type {
  ServiceIntent
} from "./types.js";

const INTENT_MAP:
  Record<
    string,
    ServiceIntent
  > = {

  "产品咨询":
    "PRODUCT_QUESTION",

  "订单状态":
    "ORDER_STATUS",

  "物流":
    "SHIPPING",

  "退货":
    "RETURN",

  "退款":
    "REFUND",

  "取消订单":
    "CANCELLATION",

  "产品适配":
    "PRODUCT_FIT",

  "产品比较":
    "PRODUCT_COMPARISON",

  "付款问题":
    "PAYMENT",

  "投诉":
    "COMPLAINT",

  "其他":
    "OTHER"
};

export function
mapMlIntent(
  label: string
): ServiceIntent {

  return (
    INTENT_MAP[label]
    ??
    "OTHER"
  );
}