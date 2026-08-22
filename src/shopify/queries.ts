export const SHOP_INFO_QUERY = `
  query ShopInfo {
    shop {
      id
      name
      email
      myshopifyDomain
      primaryDomain {
        host
        url
      }
      currencyCode
      timezoneAbbreviation
    }
  }
`;

export const PRODUCTS_BASELINE_QUERY = `
  query ProductsBaseline($first: Int!) {
    products(first: $first) {
      nodes {
        id
        title
        handle
        status
        createdAt
        updatedAt

        variants(first: 20) {
          nodes {
            id
            title
            sku
            price
          }
        }
      }
    }
  }
`;