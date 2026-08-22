import { env } from "../config/env.js";

export type ShopifyGraphQLError = {
  message: string;
  locations?: Array<{
    line: number;
    column: number;
  }>;
  path?: Array<string | number>;
  extensions?: Record<string, unknown>;
};

type ShopifyGraphQLResponse<T> = {
  data?: T;
  errors?: ShopifyGraphQLError[];
};

export class ShopifyRequestError extends Error {
  constructor(
    message: string,
    public readonly status?: number,
    public readonly details?: unknown
  ) {
    super(message);
    this.name = "ShopifyRequestError";
  }
}

export async function shopifyGraphQL<T>(
  query: string,
  variables: Record<string, unknown> = {}
): Promise<T> {
  const endpoint =
    `https://${env.SHOPIFY_STORE_DOMAIN}` +
    `/admin/api/${env.SHOPIFY_API_VERSION}/graphql.json`;

  let response: Response;

  try {
    response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token":
          env.SHOPIFY_ADMIN_ACCESS_TOKEN
      },
      body: JSON.stringify({
        query,
        variables
      })
    });
  } catch (error) {
    throw new ShopifyRequestError(
      "Unable to reach Shopify",
      undefined,
      error
    );
  }

  let body: ShopifyGraphQLResponse<T>;

  try {
    body =
      (await response.json()) as ShopifyGraphQLResponse<T>;
  } catch (error) {
    throw new ShopifyRequestError(
      "Shopify returned a non-JSON response",
      response.status,
      error
    );
  }

  if (!response.ok) {
    throw new ShopifyRequestError(
      `Shopify HTTP request failed with ${response.status}`,
      response.status,
      body
    );
  }

  if (body.errors?.length) {
    throw new ShopifyRequestError(
      "Shopify GraphQL returned errors",
      response.status,
      body.errors
    );
  }

  if (!body.data) {
    throw new ShopifyRequestError(
      "Shopify response contained no data",
      response.status,
      body
    );
  }

  return body.data;
}