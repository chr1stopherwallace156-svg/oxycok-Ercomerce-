import {
  shopifyGraphQL
} from "../shopify/client.js";

import {
  SHOP_INFO_QUERY
} from "../shopify/queries.js";

async function main() {
  console.log(
    "Verifying Shopify connectivity..."
  );

  const data =
    await shopifyGraphQL<{
      shop: {
        id: string;
        name: string;
        myshopifyDomain: string;
      };
    }>(SHOP_INFO_QUERY);

  console.log(
    JSON.stringify(
      {
        verdict:
          "SHOPIFY_CONNECTIVITY_PASS",
        shop: data.shop
      },
      null,
      2
    )
  );
}

main().catch((error) => {
  console.error(
    "SHOPIFY_CONNECTIVITY_FAIL"
  );

  console.error(error);

  process.exit(1);
});