CREATE TABLE `article_actions` (
	`article_id` text PRIMARY KEY NOT NULL,
	`actioned_at` text,
	`actioned_by` text DEFAULT '' NOT NULL,
	`updated_at` text NOT NULL,
	`version` integer DEFAULT 1 NOT NULL
);
