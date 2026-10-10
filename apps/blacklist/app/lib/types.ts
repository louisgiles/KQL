export type Source = { title: string; url: string; publisher: string; type: 'Primary research' | 'Reporting' | 'Documentation' };
export type Fact = { text: string; source: number };
export type Article = { id: string; title: string; url: string; publisher: string; publishedAt: string; discoveredAt: string; category: string; priority: 'High' | 'Medium' | 'Context'; score: number; summary: string; reason: string; facts: Fact[]; sources: Source[]; packs: string[]; tags: string[]; kind: 'research' | 'feed' | 'catalogue'; caveat: string; customPacks?: Pack[] };
export type Hunt = { id: string; articleId: string; status: string; assignee: string; scope: string; verdict: string; updatedAt: string; updatedBy: string; version: number };
export type Note = { id: string; huntId: string; actor: string; body: string; createdAt: string };
export type ArticleAction = { articleId: string; actionedAt: string | null; actionedBy: string; updatedAt: string; version: number };
export type Pack = { id: string; title: string; hypothesis: string; tables: string[]; prerequisites: string; query: string; steps: string[]; expected: string; falsePositives: string[]; limitations: string; techniques: string[] };
export type Workspace = { articles: Article[]; actions: ArticleAction[]; hunts: Hunt[]; notes: Note[]; members: { id: string; name: string }[]; feeds: { id: string; name: string; url: string; checkedAt: string; status: string; count: number; error: string }[]; settings: Record<string, string>; user: { userId: string; displayName: string } | null; serverTime: string };
