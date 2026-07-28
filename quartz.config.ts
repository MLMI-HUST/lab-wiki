import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

const config: QuartzConfig = {
  configuration: {
    title: "MLMI Wiki",
    description: "MLMI 实验笔记知识库",
    baseUrl: "lab-wiki",
    locale: "zh-CN",
    ignorePatterns: [
      "\\.obsidian",
      "\\.DS_Store",
      "插入的图片",
      "_整理报告\\.md",
      "_整理总报告\\.md",
      "^「",
    ],
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: {
          dark: "github-dark",
          light: "github-light",
        },
      }),
      Plugin.ObsidianFlavoredMarkdown({
        enableInHtmlEmbed: false,
        enableYouTubeEmbed: true,
        enableVideoEmbed: true,
      }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents({
        showByDefault: true,
      }),
      Plugin.CrawlLinks({
        passLinkNonExistentLinks: false,
        latency: 0,
      }),
      Plugin.Description(),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: true,
        rssLimit: 10,
        rssFullHtml: false,
        includeEmptyFiles: true,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
    ],
  },
}

export default config
