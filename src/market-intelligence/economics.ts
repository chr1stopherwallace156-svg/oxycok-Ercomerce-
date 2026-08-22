import type {
  ProductEconomics
} from "./types.js";

export type EconomicsResult = {
  revenue: number;

  variableCosts: number;

  contributionProfit: number;

  contributionMargin: number;
};

export function calculateEconomics(
  input: ProductEconomics
): EconomicsResult {

  if (input.sellingPrice <= 0) {
    throw new Error(
      "sellingPrice must be greater than zero"
    );
  }

  const variableCosts =
    input.productCost +
    input.inboundFreight +
    input.outboundFulfillment +
    input.paymentFees +
    input.platformFees +
    input.averageDiscount +
    input.expectedRefundCost +
    input.expectedReturnCost +
    input.creatorAffiliateCost +
    input.variableAdCost +
    input.otherVariableCost;

  const contributionProfit =
    input.sellingPrice -
    variableCosts;

  return {
    revenue:
      input.sellingPrice,

    variableCosts,

    contributionProfit,

    contributionMargin:
      contributionProfit /
      input.sellingPrice
  };
}