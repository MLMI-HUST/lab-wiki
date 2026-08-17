---
title: ICP-RIE Recipe
tags:
  - 刻蚀
  - ICP-RIE
  - Recipe
created: 2025-01-01
updated: 2026-01-01
---

<!-- stale-warning -->
> [!warning] 此笔记已超过 228 天未更新
> 最后更新：2026-01-01。内容可能已过时，请有经验的组员复核后移除此提示。
> 复核后将 frontmatter 的 `updated` 字段更新为今天即可自动移除。
<!-- /stale-warning -->

## 浅硅 ICP

| 材料 | 速率 | 更新时间 | 腔压 | 温度 | RF | ICP | SF₆ | C₄F₈ | CHF₃ | Ar | O₂ |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 压印胶 | 2.50 nm/s | — | 10 mTorr | 5℃ | 200W | 300W | | | 25 sccm | | 6 sccm |
| TiO₂ | 1.83 nm/s | — | 15 mTorr | 5℃ | 25W | 900W | 25 sccm | 10 sccm | | | 20 sccm |
| SiO₂ | 3.05 nm/s | <mark>25/11/24</mark> | 12 mTorr | 5℃ | 50W | 900W | 27 sccm | 5 sccm | | | |
| Si | 12.0 nm/s | — | 15 mTorr | ?? | 30W | 900W | 30 sccm | 39 sccm | | | |
| PMMA | 11.3 nm/s | — | 10 mTorr | 5℃ | 100W | 150W | | | | | 20 sccm |
| BK7 | 0.13 nm/s | — | 15 mTorr | 5℃ | 25W | 900W | 25 sccm | 20 sccm | | | |

> [!bug] 疑似错误：Si 刻蚀温度标注为 "??"，需要确认实际温度。

---

## 旧 III-V 族 ICP

| 材料 | 速率 | 更新时间 | 腔压 | 温度 | 散热 | RF | ICP | SF₆ | CF₄ | Cl₂ | Ar | O₂ |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 压印胶 | 3.67 nm/s | — | 10 mTorr | 20℃ | 6 sccm | 200W | 200W | | 30 sccm | | | 10 sccm |
| TiO₂ | — nm/s | <mark>25/9/3</mark> | 10 mTorr | 20℃ | 0 sccm | 150W | 500W | 20 sccm | | | 30 sccm | |
| SiO₂ | 3.21 nm/s | — | 7.5 mTorr | 25℃ | | 50W | 700W | | 90 sccm | | | 10 sccm |
| Si | 2.33 nm/s | — | ??? | ??? | | ??? | ??? | | 40 sccm | | | |
| PMMA | 6.30 nm/s | — | 10 mTorr | ?5℃ | | 100W | 150W | | | | | 20 sccm |
| CsPbBr₃ | ?? | — | 10 mTorr | ?5℃ | | 13W | 1kW | | | 40 sccm | 10 sccm | |
| Cr | ??? | — | 5 mTorr | 20℃ | | 30W | 500W | | | 40 sccm | | 10 sccm |

> [!bug] 疑似错误：旧设备 Si 刻蚀的腔压、温度、RF、ICP 均标注为 "???"，需要补充数据。TiO₂ 速率未填写。

---

## 关联笔记

- [[EBL-硅片工艺|EBL 硅片工艺]]（ICP 刻蚀步骤）
- [[磁控溅射（B821大磁控）|磁控溅射]]（薄膜沉积）
- [[光学镀膜机|光学镀膜]]（DBR 制备）
