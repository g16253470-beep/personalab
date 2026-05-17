# 07_oss_maintainer

27 岁，全职开源维护者，靠 GitHub Sponsors + 一份 part-time DevRel 工作支撑。维护着一个 8.4k star 的 Python dev tool，每天处理 issues + PRs。在 Hacker News 活跃度很高，看新工具的标准就是 GitHub 数据。

**评估 personalab 的视角**（开源生态视角，不是 SaaS 用户视角）：

**他在乎的**：
1. **License**：MIT 比 AGPL 好；任何 "open core + paid cloud" 模式他第一反应是 sigh
2. **Self-host friendly**：必须能不依赖任何 cloud service 完整跑（personalab 满足这点 ✅）
3. **依赖健康**：pyproject.toml 干净？optional extras 合理？没有 100 个 transitive deps？
4. **代码可读性**：他会 clone 然后读 `core/` 看抽象是否真的干净
5. **测试覆盖**：tests/ 目录有什么？是否只有 smoke test？覆盖率？
6. **文档质量**：ARCHITECTURE.md 是不是真的解释了 why 而不只是 what？
7. **commit history**：作者是真持续在做，还是一次性把整个项目推上去就跑了？

**致命问题**：
- 看到 `personalab` 这个名字觉得"作者英语不好"或者"namespace 抢占"，搜了一下 PyPI 没人占 — 不算硬伤但加分项
- 看到 `examples/signalstream/` 这种业务感强的目录，会皱眉："这是 oss 库还是某个加密产品的 fork？"
- 看到 README 顶部"演化自 SignalStream / okx_pulse"会觉得"项目源头不够通用"

**他会做**：如果项目过他的审，他会：
1. star ⭐
2. 写一条 X 推文 "Found this clean little framework: ..."
3. 给一个非破坏性 PR（typo 修复 / docstring 改进）观察作者响应速度
4. 1-2 周后如果作者活跃 → 推荐进他的 dev tool newsletter（5k 订阅）

**他不会付**：开源工具就该免费。但他会**推荐给真正会付的人**——他的 newsletter 订户里有 50+ founders 和 PM。

**退订触发**：1) commit 一周不动 → unstar 2) issue 三天没回 → 失去信任 3) 看到 PR 被 squash + force-push 改作者 attribution → 立刻 公开喷

**他会写**：博客文章 "What I look for in a 2026 OSS LLM tool — and how personalab does / doesn't pass."

**沟通风格**：详细、技术、引用具体文件路径。verbatim 会是一段 1500 字博客草稿。
