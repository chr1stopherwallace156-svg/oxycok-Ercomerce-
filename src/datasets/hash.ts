import crypto from "node:crypto";

export function hashDataset(
  rows: unknown[]
): string {

  const normalized =
    JSON.stringify(rows);

  return crypto
    .createHash("sha256")
    .update(normalized)
    .digest("hex");
}