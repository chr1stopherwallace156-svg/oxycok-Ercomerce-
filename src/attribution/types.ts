export type ConversionAttribution = {
  attributionId: string;

  impressionId: string;

  clickEventId?: string;

  orderId: string;

  productId: string;

  variantId?: string;

  sessionId: string;

  impressionAt: Date;

  clickedAt?: Date;

  convertedAt: Date;

  clickAttributed:
    boolean;

  conversionAttributed:
    boolean;

  attributionMethod:
    | "DETERMINISTIC_SESSION"
    | "DETERMINISTIC_CUSTOMER"
    | "OTHER";

  attributionWindowSeconds:
    number;
};