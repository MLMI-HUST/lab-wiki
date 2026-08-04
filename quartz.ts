import { loadQuartzConfig, loadQuartzLayout } from "./quartz/plugins/loader/config-loader"
import { componentRegistry } from "./quartz/components/registry"

// 最近更新栏排除自动生成的 MOC 索引页（_索引.md）
// 注意：不能用 frontmatter 的 unlisted: true —— 它同时会被 backlinks 插件
// 排除，导致主页反向链接栏消失（_索引 是主页反向链接的主要来源）。
//
// 说明：ExternalPlugin.RecentNotes() 在 Quartz v5.0.0 的 npm 包场景下存在
// override key 不匹配问题（存储 key: quartz-community__recent-notes，
// 查询 key: @quartz-community/recent-notes），override 不生效。
// 因此这里直接调用 registry API，使用与 config-loader 一致的 key 设置 override。
componentRegistry.setOptionOverrides("@quartz-community/recent-notes", {
  filter: (file: { slug: string }) => !file.slug.includes("_索引"),
})

const config = await loadQuartzConfig()
export default config
export const layout = await loadQuartzLayout()
