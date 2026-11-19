# **Codex VS Code 插件：丝滑使用方案**

这次我重点看了 LINUX DO 的 Codex 实战讨论，并对照了 Codex 当前官方配置文档。

我发现一个很有价值的方向：**不要把 Codex 当成一个只会接收 Prompt 的聊天机器人，而是把它配置成一套有权限管理、项目知识、工具链、自动检查和任务分工的开发环境。**

我会按照你的实际限制设计：

- Windows + VS Code 官方 Codex 插件。
- 不安装 Codex CLI、Node.js、Python 或其他独立软件。
- 已经能使用多个第三方 API 中转商。
- 可以修改 `%USERPROFILE%\.codex\config.toml`。
- 希望 Agent 能自主操作项目、执行命令、测试、修复，而不是每一步都等你点击 Allow。
- 尽可能减少无意义的 MCP、Prompt 和 Token 消耗。

先给你一个总体方案：

## **推荐的 Codex 工作环境**

**Agent 核心**

Plan

Agent

Subagents

Full Access（按需）

任务规划、执行、并行开发、自动修复

**MCP 工具层**

Context7

GitHub

Playwright / Browser

Sequential Thinking（可选）

官方文档、代码仓库、浏览器自动化、复杂任务规划

**项目知识层**

AGENTS.md

Skills

项目架构文档

任务记录

减少重复交代、统一代码风格、积累项目经验

**自动化层**

Hooks

Git 检查

自动测试

完成通知

自动检查、保存上下文、减少人工干预

我把 LINUX DO 的讨论分成了几个方向，下面会特别区分社区经验、官方已经支持的功能，以及我认为不值得安装的东西。

## **一、先解决最重要的问题：Agent 不要一直等你同意**

这是 LINUX DO 上讨论最热烈的一个问题。

我找到几篇值得看的帖子：

1. [如何让 Codex 全自动运行](https://linux.do/t/topic/1558848?utm_source=chatgpt.com)
2. [说一下我对 Codex 沙盒以及权限的理解](https://linux.do/t/topic/2303303?utm_source=chatgpt.com)
3. [Codex VSCode 自动批准](https://linux.do/t/topic/928413?utm_source=chatgpt.com)

其中最值得参考的是第二篇，它把三个概念分得很清楚：

- `sandbox_mode`：允许 Agent 在什么范围内操作。
- `approval_policy`：什么情况下需要人工审批。
- `approvals_reviewer`：需要审批时由谁审核。

**不要把自动审批和关闭沙盒混为一谈。**

### **我的推荐：日常使用 workspace-write**

在 `%USERPROFILE%\.codex\config.toml` 中：

```
sandbox_mode = "workspace-write"
approval_policy = "on-request"
approvals_reviewer = "auto_review"
```

这套设置的效果：

- 可以直接读取工作区文件。
- 可以直接修改工作区文件。
- 可以在工作区内执行大多数命令。
- 遇到需要越权、访问工作区外资源等情况时再处理审批。
- 自动审核器可以参与审批判断，但不代表所有操作都不再弹窗。

如果你想让 Agent 完全自主操作，可以在 VS Code Codex 插件的权限模式选择器中选择：

Full Access

或者配置：

```
sandbox_mode = "danger-full-access"
approval_policy = "never"
```

这是真正意义上减少审批干预的方式，但风险很大：Agent 可能修改工作区以外的文件、执行危险命令、访问网络或触及其他数据。

**我的建议：平时 workspace-write，临时需要完全自主操作时才切 Full Access。** 公司电脑尤其不建议全局永久关闭沙盒。

另外，Windows 沙盒还可以配置：

```
[windows]
sandbox = "unelevated"
```

如果遇到沙盒启动失败，可以先尝试这个模式。LINUX DO 有用户报告过 Windows 下 elevated 沙盒初始化失败的问题。

LINUX DO+1



## **二、MCP 推荐：别装一堆，先装真正有用的**

我在 LINUX DO 上找到的几篇 MCP 讨论：

- [有没有啥 MCP 推荐，Codex 必备的那种](https://linux.do/t/topic/2134885?utm_source=chatgpt.com)
- [Codex 有什么长记忆 MCP 推荐吗？](https://linux.do/t/topic/1947346?utm_source=chatgpt.com)
- [教你 Codex 配置怎么设置 MCP](https://linux.do/t/topic/950311?tl=en&utm_source=chatgpt.com)
- [Skill / MCP 推荐（2026 汇总）](https://linux.do/t/topic/2533306/1?tl=en&utm_source=chatgpt.com)

社区比较一致的几个名字是 Context7、GitHub、Sequential Thinking、Serena、Playwright、Chrome DevTools。

但考虑到你不能安装 Node.js、Python 等运行环境，我会重新筛选。

### **第一梯队：我建议配置**

[Context7 MCP: Boost Your AI Coding Assistant with Smart Context | Medium](https://images.openai.com/static-rsc-4/NvP9bt4PzYbEDjWaxSuqIKxGHVlUOqtq1PQXzN3BpnA13kPXfu8W5zTGy_GXwIcDLhRKy9YuDw6CcxzTJX6Zh6TFOCA5qPqP2XHMfMDHe6rKXvu5fJ_mjl2db9sxTLONWjdeXI3TYCvpEV5WauSRBHUBZFb67YBEALT49FtgjpQ?purpose=inline)

**1.** **Context7**

强烈推荐

官方文档检索 MCP

解决的问题：模型经常凭记忆写过时 API、错误参数、错误版本的框架代码。

- 查询指定库的官方文档。

- 获取当前版本的 API 用法。

- 降低模型凭空编造 SDK 参数的概率。

- 特别适合 React、Vue、Next.js、Spring Boot 等开发。

  接入：优先使用远程 HTTP MCP，避免需要 npx 的本地版本。

  [Context7 官方网站](https://context7.com/?utm_source=chatgpt.com)

[Oakstone & Github | Executive Search for GTM SaaS](https://images.openai.com/static-rsc-4/HQnzkeZepdcbz6yki5F911xaI7qZFrq-EjoAnoh5focKQlZBBR_xVRxmdszYIh8CF9ZImt1zDUWQIDbeJm9vx6gJmTSUYpEpChiHmY_gLt1gXp9uq4lq-oxfEEM9g7FJhQpCYi7WHrUwBF9vcV_4-kwArSHYrPmmA6I2uBI6wFE?purpose=inline)

**2.** **GitHub MCP Server**

强烈推荐

代码仓库和 GitHub 操作

- 查找仓库、Issue、PR。

- 阅读其他项目的源码。

- 查看提交记录。

- 辅助代码审查和问题排查。

- 需要时可以操作 GitHub 资源，但应谨慎配置写入权限。

  [GitHub MCP Server 官方仓库](https://github.com/github/github-mcp-server?utm_source=chatgpt.com)

[Playwright Logo PNG Vector (SVG) Free Download](https://images.openai.com/static-rsc-4/LPhp5WGFs8AsPwkA7RmoAkYT6701vGdG47geLkGSQevIZhbryTBOdW8tXQjnI41K4_cWYD-C96onm7VCnjjtX5TT3xzeansU0mqC5KqXSxLIIOjWPs51DxGr3-6SBCNPQOmaVmw59V2ITdFfB8o2lqY65ner3viTnkZkZMPBWp0?purpose=inline)

**3.** **Playwright** **/ Browser**

按需推荐

浏览器自动化和 Web 测试

- 打开网页。

- 操作表单和按钮。

- 自动化测试。

- 检查页面元素、截图和交互。

- 对前端项目进行端到端验证。

  注意：Playwright MCP 常见部署需要 Node.js。你的环境应优先使用 Codex 自带的浏览器能力，或已部署的远程浏览器 MCP，不要直接安装 npm 包。

  [Playwright 官方网站](https://playwright.dev/?utm_source=chatgpt.com)

### **第二梯队：按任务选择**

| MCP                 | 用途                       | 我的意见                             |
| ------------------- | -------------------------- | ------------------------------------ |
| Sequential Thinking | 复杂任务拆解               | 可选，不必每次调用                   |
| Serena              | 代码符号级检索、跨文件重构 | 大项目有价值，但通常需要本地运行环境 |
| Chrome DevTools     | 浏览器调试、性能分析       | 前端开发有价值，注意运行依赖         |
| Memory MCP          | 跨项目长期记忆             | 不建议一开始就装                     |
| DeepWiki            | 阅读 GitHub 项目架构       | 研究陌生开源项目时有用               |
| Fetch               | 抓取指定网页               | 适合资料检索                         |

我特别想强调 Sequential Thinking：它不应该成为每次任务都强制调用的工具。

社区有些 Prompt 会要求「编码前必须调用 Sequential Thinking MCP」，这可能反而增加请求轮数和 Token 消耗。复杂架构设计时再调用就够了。

LINUX DO 的讨论也有人提到 Serena、Ace Tool 能够提高代码检索效率，但这些工具的价值取决于项目规模。

LINUX DO+2



### **适合你的一套 MCP 配置**

先配置远程 HTTP 类型，避免额外安装运行时。

下面是配置结构示例，具体 URL 和认证方式需要以各服务商当前官方文档为准：

```
[mcp_servers.context7]
url = "https://mcp.context7.com/mcp"

[mcp_servers.github]
url = "https://api.githubcopilot.com/mcp/"
```

注意：

- GitHub MCP 的远程认证需要按照其 OAuth 流程处理。
- Context7 的 API Key 如果使用需要认证的版本，应使用其官方支持的认证配置。
- 如果公司代理、防火墙禁止远程 MCP，不能靠修改配置绕过公司策略。

Codex 官方支持 STDIO 和 Streamable HTTP 两种 MCP 连接方式；后者更适合你不允许安装 Node.js/Python 的情况。

ChatGPT Learn+1



## **三、Prompt 推荐：别把几千行规则全部塞进 System Prompt**

我看了 LINUX DO 上几份 Codex Prompt 分享：

- [Codex 通用系统提示词（含 AGENTS 约束 + MCP 约定）](https://linux.do/t/topic/1275669?utm_source=chatgpt.com)
- [分享一下最近使用 Codex 优化的提示词](https://linux.do/t/topic/1796914?utm_source=chatgpt.com)
- [自用 Codex AGENTS.md 分享（包含 MCP 调用）](https://linux.do/t/topic/1176376?tl=zh_CN&utm_source=chatgpt.com)

我的结论是：这些配置中最有价值的不是某个神奇的角色扮演 Prompt，而是**把项目规则、工具使用规则、执行流程和验收标准分开管理**。

我建议你建立一个全局 `AGENTS.md`，再在项目根目录建立一个项目专属 `AGENTS.md`。

### **1. 全局 AGENTS.md**

位置：

```
%USERPROFILE%\.codex\AGENTS.md
```

这是我建议你采用的版本：

```
# Global Agent Instructions

## 1. Communication
- 默认使用中文回答。
- 技术名词、代码标识符保留英文。
- 回答直接、准确，不要无意义重复用户需求。
- 不要虚构执行结果、测试结果或文件内容。

## 2. Development Principles
- 优先理解现有项目，再开始修改。
- 优先复用现有架构、依赖和代码风格。
- 不要为了简单需求引入复杂架构。
- 修改范围应尽可能小。
- 不要擅自删除已有功能。
- 不要擅自升级依赖或修改锁文件。

## 3. Agent Workflow

### Simple Tasks
直接执行，不要过度规划。

### Medium Tasks
1. 阅读相关代码。
2. 明确修改方案。
3. 修改代码。
4. 执行相关测试。
5. 汇报结果。

### Complex Tasks
1. 先分析需求和约束。
2. 阅读项目结构和关键文件。
3. 制定可执行计划。
4. 拆分独立任务。
5. 必要时使用 Subagents 并行工作。
6. 分阶段实现。
7. 执行测试和代码审查。
8. 汇报未解决问题。

## 4. Tool Usage
- 查官方 API 时优先使用 Context7。
- 查 GitHub 仓库和 PR 时使用 GitHub MCP。
- 浏览器测试优先使用可用的 Browser / Playwright 工具。
- 不要为了使用 MCP 而使用 MCP。
- 本地文件可以直接读取时，不要重复调用外部工具。

## 5. Coding Rules
- 修改之前先定位调用链。
- 修改之后检查相关引用。
- 不要伪造 API、参数、库函数。
- 不要无故创建重复文件。
- 优先使用项目已有测试框架。

## 6. Safety
- 不读取、输出或上传密钥、Token、密码。
- 不执行与任务无关的破坏性操作。
- 不擅自删除数据库、生产数据或备份。
- 不执行 git push、发布、部署，除非用户明确要求。
- 涉及工作区以外的文件时先确认。

## 7. Completion
任务完成时说明：
1. 修改了哪些文件。
2. 具体修改内容。
3. 执行了哪些测试。
4. 测试是否通过。
5. 尚存的问题。
```

这份 Prompt 有一个重要特点：它不强制每次都进行复杂规划，也不强制每次调用 MCP。

**我不建议你照搬论坛中那些动辄几百行、强制 Sequential Thinking、强制 MCP 优先的 Prompt。** 这类配置可能让模型每次都多走好几轮。

### **2. 项目级 AGENTS.md**

全局文件负责你的通用偏好，项目级文件负责具体项目。

例如：

```
# Project Instructions

## 项目概况
- 项目名称：
- 技术栈：
- 项目入口：
- 核心模块：

## 项目架构
- 前端：
- 后端：
- 数据库：
- API：

## 开发约定
- 遵循当前项目代码风格。
- 不随意改变目录结构。
- 不随意增加依赖。
- 优先使用已有组件和工具函数。

## 测试要求
- 修改后运行相关测试。
- 修改 API 后检查调用方。
- 修改数据库结构时检查迁移兼容性。

## 特殊限制
- 不修改以下目录：
- 不使用以下依赖：
- 不允许以下操作：
```

不要把项目文档全部复制进 AGENTS.md。

只写索引和最重要的规则，其余内容拆分成：

```
项目/
├── AGENTS.md
├── docs/
│   ├── architecture.md
│   ├── database.md
│   ├── api.md
│   └── development.md
└── .codex/
    └── ...
```

这样 Codex 只在需要时读取对应文档，避免每次都带着大量上下文。

### **3. 我非常推荐你使用 Skills**

Skills 比一份巨大 Prompt 更适合长期使用。

它可以让 Codex 在特定任务时加载对应工作流程，而不是每次对话都把全部规则塞进去。

我建议先准备这些：

| Skill               | 作用                   | 推荐程度 |
| ------------------- | ---------------------- | -------- |
| Code Review         | 检查代码质量、潜在 Bug | 很高     |
| Debugging           | 系统性排查错误         | 很高     |
| Architecture Review | 架构分析和设计审查     | 高       |
| Test Generation     | 自动生成测试           | 高       |
| Git Commit          | 规范化提交信息         | 高       |
| Frontend Design     | 前端界面设计           | 按需     |
| Database Migration  | 数据库迁移审查         | 按需     |
| Security Review     | 安全检查               | 高       |

可以重点关注：

- [Matt Pocock — Skills for Real Engineers](https://github.com/mattpocock/skills?utm_source=chatgpt.com)
- [Agent Skills 开放标准](https://agentskills.io/?utm_source=chatgpt.com)

其中 LINUX DO 的推荐帖特别提到了 Grill Me、Grill With Docs、Sequential Thinking 等工具。

LINUX DO



我尤其推荐 Grill Me：

它不是让 AI 一味赞同你的方案，而是让它在实现之前主动挑战需求、寻找遗漏和设计缺陷。

但不要把它设置为每个简单任务的必经流程。

## **四、Hooks：让 Codex 自动做事，而不是只会回答**

这是我认为你值得重点研究的功能。

LINUX DO 上有一篇相关项目介绍：

[Trellis changelog：支持 Codex 的 hook + sub agent](https://linux.do/t/topic/1806875?utm_source=chatgpt.com)

它通过 Hooks 在 SessionStart 时自动注入工作流和任务上下文。

不过，当前 Codex 已经有官方 Hooks 机制，不需要为了实现基本功能安装 Trellis。

官方文档：[Codex Hooks](https://learn.chatgpt.com/docs/hooks?utm_source=chatgpt.com)。

### **Codex 支持哪些 Hook？**

| Hook              | 触发时机      | 实际用途             |
| ----------------- | ------------- | -------------------- |
| SessionStart      | 会话开始      | 加载项目说明         |
| UserPromptSubmit  | 用户提交任务  | 检查输入、添加上下文 |
| PreToolUse        | 工具执行前    | 检查危险命令         |
| PermissionRequest | 请求权限时    | 处理权限策略         |
| PostToolUse       | 工具执行后    | 自动检查修改         |
| PreCompact        | 上下文压缩前  | 保存重要信息         |
| PostCompact       | 压缩后        | 恢复重要上下文       |
| SubagentStart     | 子 Agent 启动 | 注入角色说明         |
| SubagentStop      | 子 Agent 结束 | 收集任务结果         |
| Stop              | Agent 停止    | 质量检查、生成总结   |
| SessionEnd        | 会话结束      | 保存任务状态         |

### **我建议优先做的 5 个 Hook**

01

**SessionStart：自动加载项目上下文**

启动时读取项目架构说明、当前分支、任务记录。避免每次重新解释项目。

02

**PreToolUse：危险操作拦截**

对 `git push`、删除目录、数据库清空、修改环境变量等命令进行检查。

03

**PostToolUse：代码修改后检查**

修改代码后自动检查格式、语法或相关测试。

04

**PreCompact：上下文压缩前保存进度**

保存当前目标、已完成事项、待办事项、关键文件和已知问题。

05

**Stop：任务完成时检查质量**

检查是否有遗漏的测试、未解决错误和未完成任务。

### **一个特别适合你的 Hook：PreCompact**

我认为它比很多所谓的长期记忆 MCP 更值得先配置。

因为 Codex 在长时间工作时会压缩上下文，容易丢失：

- 最初的任务目标。
- 已经确定的技术方案。
- 已经尝试过但失败的方法。
- 当前修改进度。
- 尚未解决的问题。

可以让 Hook 在压缩前将这些内容写入项目里的 `docs/ai-progress.md`，下一次会话再恢复。

这样你甚至可以让 Codex 连续完成一个持续数小时的任务，中间不需要反复重新交代。

**注意：Hooks 不是免费的，也不是无风险的。** 每次触发都会执行脚本，若向模型额外注入大量内容也会消耗 Token。建议使用本地轻量脚本，只返回必要上下文。

还有一个重要细节：当前官方 Hooks 的 `command` 需要有可执行程序。对于你的环境，可以考虑 Windows 自带 PowerShell，但不应该为了运行 Hook 再安装 Python 或 Node.js。官方还支持 `commandWindows` 字段。

ChatGPT Learn+1



## **五、直接给你一套 Hooks 配置思路**

Codex 的 Hook 配置文件：

```
%USERPROFILE%\.codex\hooks.json
```

你可以先建立一个最简单的 SessionStart Hook：

```
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume|compact",
        "hooks": [
          {
            "type": "command",
            "commandWindows": "powershell.exe -NoProfile -Command \"Write-Output '请先检查当前项目的 AGENTS.md，并确认当前任务进度。不要重复读取无关文件。'\"",
            "statusMessage": "正在加载项目上下文"
          }
        ]
      }
    ]
  }
}
```

这是一个演示用的 Hook：它向会话注入简短提示，不会自动读取或保存项目文件。

实际部署时，我建议把它升级为读取 `docs/ai-progress.md` 的 PowerShell 脚本，并将输出限制在合理长度。

**注意：Hooks 首次启用或修改后，需要在 Codex 中审查并信任对应 Hook。** 不要直接信任来历不明的 Hook 脚本。

另外，`suppressOutput` 目前并非所有事件都真正支持，不能指望它完全隐藏 Hook 输出。

ChatGPT Learn



## **六、Subagents：让一个 Codex 变成一个小团队**

这个功能我很推荐。

LINUX DO 的讨论里也有不少人开始使用多 Agent 工作流，例如：

- 一个 Agent 负责分析。
- 一个 Agent 负责实现。
- 一个 Agent 负责测试。
- 一个 Agent 负责审查。

参考：[Trellis 的 Codex Hook + Subagent 方案](https://linux.do/t/topic/1806875?utm_source=chatgpt.com)。

### **我建议你建立 4 个角色**

**Researcher — 研究员**

只读

阅读项目、寻找相关代码、分析调用链、确认技术方案。

**Implementer — 开发者**

读写

按照主 Agent 的方案修改代码，不擅自扩大范围。

**Tester — 测试员**

验证

运行测试、检查错误、验证功能，不随意修改业务代码。

**Reviewer — 审查员**

只读

检查代码质量、潜在 Bug、安全问题和架构一致性。

### **配置示例**

在 `config.toml` 中可以声明自定义 Agent：

```
[features]
multi_agent = true

[agents.researcher]
description = "负责代码研究、调用链分析和技术调研"
developer_instructions = """
只读分析，不修改项目文件。
必须引用真实文件路径和代码位置。
不要编造项目结构。
"""

[agents.reviewer]
description = "负责代码审查和安全审查"
developer_instructions = """
只读检查代码。
重点检查逻辑错误、边界条件、安全漏洞和回归风险。
按照严重程度排序问题。
"""
```

这只是角色定义的示例，真正的并行执行还要由主 Agent 进行任务委派，不能只写了几个角色就认为它们会自动工作。

### **重要：多 Agent 不一定更快**

我建议：

- 简单任务：一个 Agent。
- 中型任务：一个主 Agent + 一个 Reviewer。
- 大型任务：Researcher + Implementer + Tester + Reviewer。

多个 Agent 同时读取大量文件、重复分析相同上下文，Token 可能增长得非常快。

还有一个关键限制：你配置了多个 API Provider，并不意味着每个 Subagent 都会自动使用不同供应商。子 Agent 的模型选择需要结合 Codex 的 Agent 配置和当前 Provider 支持情况验证。

## **七、真正能让 Codex 好用的功能：Browser、通知、Git**

这几个往往比再装 10 个 MCP 更实用。

### **1. 浏览器自动化**

如果你做 Web 开发，我会把浏览器操作放在很高的优先级。

目标工作流：

1. Codex 修改前端代码。
2. 启动项目已有的开发服务器。
3. 打开浏览器。
4. 登录测试账号。
5. 操作页面。
6. 检查控制台错误。
7. 截图并验证 UI。
8. 发现问题后继续修复。

如果你的 Codex 版本支持内置 Browser 工具，优先使用它，不要先安装 Playwright MCP。

如果需要复杂的端到端测试，再考虑 Playwright。

### **2. 完成通知**

你可以配置 Codex 在任务完成后给 Windows 发通知。

Codex 支持 `notify` 配置，Windows 可以调用系统自带的 PowerShell。

例如：

```
notify = [
  "powershell.exe",
  "-NoProfile",
  "-Command",
  "[console]::Beep(800,300)"
]
```

这个例子是简单的声音提示。你也可以进一步改成 Windows Toast 通知。

这样就可以把任务交给 Agent，然后切出去做其他事情，不必一直盯着 Chat 面板。

### **3. Git 工作流**

我建议把 Git 规则加进 AGENTS：

- 开始任务前检查当前分支和工作区状态。
- 不要覆盖用户未提交的改动。
- 完成阶段性任务后总结 Diff。
- 允许在明确授权下创建本地提交。
- 默认禁止 push 和部署。
- 不要擅自执行 `git reset --hard`、`git clean -fd`。

特别推荐让 Codex 每个阶段都汇报变更文件列表，而不是最后一次性给你一个巨大的 Diff。

## **八、其他容易被忽略，但我认为很值得配置的东西**

### **1. 多套 Profile：不同任务用不同配置**

你已经配置多个供应商了，我建议再利用 Codex Profile。

例如：

| Profile     | 用途     | 模型选择         |
| ----------- | -------- | ---------------- |
| `coding`    | 日常编程 | 稳定、工具调用强 |
| `architect` | 架构设计 | 推理能力强       |
| `fast`      | 简单修改 | 速度快、成本低   |
| `review`    | 代码审查 | 分析能力强       |

配置文件可以是：

```
%USERPROFILE%\.codex\
├── config.toml
├── coding.config.toml
├── architect.config.toml
├── fast.config.toml
└── review.config.toml
```

通过不同 Profile 保存模型和推理参数，避免频繁手动修改主配置。

官方参考：[Codex Configuration Profiles](https://learn.chatgpt.com/docs/config-file/config-basic?utm_source=chatgpt.com)。

### **2. 使用任务记录，而不是无限延长对话**

建议每个复杂项目维护：

```
docs/
├── architecture.md
├── decisions.md
├── ai-progress.md
├── known-issues.md
└── development-log.md
```

特别是 `ai-progress.md`：

```
# 当前任务进度

## 目标
实现 XXX 功能

## 已完成
- [x] 数据模型
- [x] API 接口

## 进行中
- [ ] 前端页面

## 待处理
- [ ] 单元测试
- [ ] 异常处理

## 重要决策
- 使用现有数据库结构
- 不新增第三方依赖

## 已知问题
- XXX
```

这样即使换模型、换会话、压缩上下文，也能恢复工作。

### **3. Token 和请求透明度**

鉴于你之前特别在意 Kilo Code 的 Token 统计问题，我建议你给 Codex 建立一套独立核对方式：

- 中转站后台记录输入 Token。
- 中转站后台记录输出 Token。
- 检查请求次数。
- 检查工具调用轮数。
- 对比不同模型的消耗。
- 观察长任务上下文是否反复重复提交。

不要默认 MCP 越多越好。

一个高质量的 Agent 配置，应该是减少无意义的模型请求，而不是增加工具数量。

# **九、最终推荐配置清单**

这是我认为适合你的落地顺序。

**Codex 环境改造清单**

0/25 已完成

**1****.** **基础配置**

保留多个 API Provider 和模型配置

设置 workspace-write 为日常权限

配置全局 AGENTS.md

建立项目级 AGENTS.md

配置 coding / architect / fast Profile

**2****.** **MCP 工具**

配置 Context7 远程 MCP

配置 GitHub 远程 MCP

确认 Codex Browser 是否可用

按需考虑 Sequential Thinking

暂不安装依赖 Node/Python 的本地 MCP

**3****.** **Agent 增强**

开启并测试 Subagents

建立 Researcher / Reviewer 角色

准备 Code Review Skill

准备 Debugging Skill

建立项目任务进度文件

**4****.** **自动化**

配置 SessionStart Hook

配置 PreCompact Hook

配置 PostToolUse 检查

配置危险命令保护

配置 Windows 完成通知

**5****.** **验证**

测试自动读写文件

测试自动执行项目命令

测试网络和 MCP 连接

测试上下文压缩后能否恢复

检查中转站 Token 与请求记录

重置清单

## **十、我认为最值得你先做的三件事**

如果让我替你安排优先级：

# **01**

**权限和自动执行**

先解决每次都要点 Allow 的问题。建立合理的沙盒权限，不要一上来就全局无沙盒。

# **02**

**AGENTS.md + Skills**

让 Codex 真正理解你的开发习惯和项目结构，减少重复沟通和无效 Token。

# **03**

**Context7 + GitHub + Hooks**

给它可靠的外部知识来源，并自动完成检查、进度保存和通知。