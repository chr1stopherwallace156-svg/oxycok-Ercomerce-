// Project-authored static inspection fixture. No external code or dependency.
export function total(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}
