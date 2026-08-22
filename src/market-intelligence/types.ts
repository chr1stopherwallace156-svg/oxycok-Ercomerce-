export type MarketSignalAuthority =
  | "EXTERNAL_CONTEXT"
  | "MARKET_OBSERVATION"
  | "FIRST_PARTY_BEHAVIOR"
  | "TRANSACTIONAL_TRUTH"
  | "SUPPLY_EVIDENCE";

export type MarketSignal = {
  signalId: string;

  sourceId: string;

  productKey?: string;
  categoryKey?: string;

  geography?: string;

  metric: string;

  value: number;

  authority: MarketSignalAuthority;

  observedAt: Date;

  expiresAt?: Date;

  metadata?: Record<string, unknown>;
};

export type ProductEconomics = {
  sellingPrice: number;

  productCost: number;

  inboundFreight: number;

  outboundFulfillment: number;

  paymentFees: number;

  platformFees: number;

  averageDiscount: number;

  expectedRefundCost: number;

  expectedReturnCost: number;

  creatorAffiliateCost: number;

  variableAdCost: number;

  otherVariableCost: number;
};