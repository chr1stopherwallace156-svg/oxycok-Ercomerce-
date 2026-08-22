import "dotenv/config";
import { z } from "zod";

const EnvSchema = z.object({
  NODE_ENV: z
    .enum(["development", "test", "production"])
    .default("development"),

  PORT: z.coerce
    .number()
    .int()
    .positive()
    .default(3000),

  SHOPIFY_STORE_DOMAIN: z
    .string()
    .min(1)
    .regex(
      /^[a-zA-Z0-9][a-zA-Z0-9-]*\.myshopify\.com$/,
      "SHOPIFY_STORE_DOMAIN must look like store-name.myshopify.com"
    ),

  SHOPIFY_ADMIN_ACCESS_TOKEN: z
    .string()
    .min(1),

  SHOPIFY_WEBHOOK_SECRET: z
    .string()
    .min(1),

  SHOPIFY_API_VERSION: z
    .string()
    .regex(
      /^\d{4}-\d{2}$/,
      "SHOPIFY_API_VERSION must use YYYY-MM format"
    )
    .default("2026-07")
});

const parsed = EnvSchema.safeParse(process.env);

if (!parsed.success) {
  console.error("Invalid environment configuration:");

  for (const issue of parsed.error.issues) {
    console.error(`- ${issue.path.join(".")}: ${issue.message}`);
  }

  process.exit(1);
}

export const env = parsed.data;