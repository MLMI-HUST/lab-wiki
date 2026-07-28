---
title: XPS
tags:
  - 表征
  - 元素分析
created: 2025-09
updated: 2025-09
---

# XPS 测试

## 制样要求

- **基底**：硅基底即可
- **信息准备**：指明需要测试的**目标元素**

---

## 数据处理方法

> [!note] 核心原则：先了解样品中大概有哪些物质，根据期望存在的物质去优化拟合，参考已知峰位来确定峰的位置。

### 在线数据库

- **XPS DATABASE** — 找峰位：[NIST XPS Database](https://srdata.nist.gov/xps/selEnergyType.aspx)

---

## 分峰拟合步骤

### 1. 打开分离软件，选择数据文件

![[Pasted image 20250904171749.png]]
![[Pasted image 20250904171805.png]]
![[Pasted image 20250904171813.png]]

### 2. 打开 XPS-peak 软件

![[Pasted image 20250904171826.png]]

### 3. 导入数据

`Data → Import`，选择 **ASCII 格式**

![[Pasted image 20250904171834.png]]

### 4. 确定峰位与轨道

在 *XPS 谱图*中查找对应元素，确定：
- 大概有几个峰
- 对应轨道（如 Ti 是 **p 轨道**）

> [!note] **p 轨道**决定峰面积比，例如 p 轨道应为 **1:2**

![[Pasted image 20250904171843.png]]
![[Pasted image 20250904171847.png]]
![[Pasted image 20250904171900.png]]

### 5. 找基线

`Background → 拟合找基线`（调整 *background type* 等参数）→ `Accept`

![[Pasted image 20250904171908.png]]

### 6. 添加峰

1. `Add peak`，先找**最高的主峰**
2. 所有峰 **FWHM < 1.2**（鼠标可查看横纵坐标）
3. 选择 *peak type*
4. `Constraint` 添加约束条件
5. `Use` 确认使用

> [!question] 具体参考 PPT 第 18 页起

![[Pasted image 20250904171920.png]]
![[Pasted image 20250904171923.png]]

### 7. 导出数据并绘图

`Data → Export spectrum` → 用 **Origin** 画图

> [!note] Origin 可直接处理 XPS 数据

---

## 参考资源

> [!warning] **不同人讲的数据处理方法不一致**，建议多方参考

- [B站教学视频](https://www.bilibili.com/video/BV1AJ411x7qR/?p=1&vd_source=580ddc27f97f00e1d20257c166d11ae1)
- [微信公众号文章](https://mp.weixin.qq.com/s?__biz=MzU1MzY0NjAyMQ==&mid=2247487227&idx=1&sn=6b7ea93c7f01f6a157fdc0e693e3516c&chksm=fbeeec51cc9965479ef9518131865e60573fe8ba50b97ec979538154f053a98fad4ac985197b&scene=27)
- [知乎文章 1](https://zhuanlan.zhihu.com/p/414426849)
- [知乎文章 2](https://zhuanlan.zhihu.com/p/561856834)
- [知乎文章 3](https://zhuanlan.zhihu.com/p/459948472)
