import type { ArticleAction } from './types';

export const ACTIONED_RETENTION_MS = 7 * 24 * 60 * 60 * 1000;
export function actionExpiresAt(action: ArticleAction | undefined): number | null {
  if (!action?.actionedAt) return null;
  const marked = Date.parse(action.actionedAt);
  return Number.isFinite(marked) ? marked + ACTIONED_RETENTION_MS : null;
}
export function isRecentlyActioned(action: ArticleAction | undefined, now: number): boolean {
  const expires = actionExpiresAt(action);
  return expires !== null && now < expires;
}
// Keep the marker after expiry: handled intelligence must not reappear as new work.
export function isInInbox(action: ArticleAction | undefined): boolean {
  return !action?.actionedAt;
}
