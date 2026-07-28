import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"

export const sharedLayout: SharedLayout = {
  head: Component.Head(),
  header: [Component.PageTitle()],
  footer: Component.Footer({
    links: {
      GitHub: "https://github.com/MLMI-HUST/lab-wiki",
    },
  }),
}

export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    Component.Breadcrumbs(),
    Component.ArticleTitle(),
    Component.TableOfContents(),
  ],
  left: [
    Component.Explorer({
      sortFn: (a, b) => {
        // 目录优先，其次按名称排序
        if ((!a.file) && b.file) return -1
        if (a.file && !b.file) return 1
        return a.displayName.localeCompare(b.displayName, "zh-CN")
      },
      filterFn: (node) => {
        const name = node.name
        // 隐藏 Obsidian 配置与图片目录
        const hidden = [".obsidian", ".DS_Store", "插入的图片"]
        return !hidden.includes(name)
      },
    }),
  ],
  right: [
    Component.Backlinks(),
    Component.Graph(),
    Component.TagList(),
  ],
  header: [
    Component.Search(),
    Component.Darkmode(),
  ],
  footer: [
    Component.ContentMeta(),
  ],
}
