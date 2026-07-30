# xiyouji-mcp — 《详解西游记》项目工程化工具 MCP Server

> **轨标**：工程化工具
> **版本**：v0.1.0（W201 v2.2.24 mcp-builder skill 落地）
> **Transport**：stdio（本地 server）
> **依赖**：Python ≥3.10 + fastmcp

将项目内 5 个高价值只读工具封装为 MCP（Model Context Protocol）工具，让 LLM 能直接调用项目工程化能力，辅助跨 session 接续、DRL spot-check、数据校验、链接校验、可访问性审查。

## 工具清单

| 工具 | 功能 | 对应脚本 | readOnlyHint |
|:---|:---|:---|:---:|
| `xiyouji_drl_spotcheck` | DRL 真循环 spot-check（E1 铁律验证） | scripts/drl_spotcheck.py | ✓ |
| `xiyouji_data_validate` | output/data/ JSON 完整性校验 | scripts/data_validate.py | ✓ |
| `xiyouji_docs_index` | docs/ 索引生成/校验（只读 --check 模式） | scripts/docs_index.py | ✓ |
| `xiyouji_lint_links` | 站内/外链校验 | scripts/lint_links.py | ✓ |
| `xiyouji_a11y_audit` | HTML 可访问性审查 | scripts/a11y_audit.py | ✓ |

所有工具均为只读（`readOnlyHint=true`），不修改文件。

## 安装与启动

### 方式 1：直接运行

```bash
pip install fastmcp
python mcp-server/xiyouji_mcp.py
```

### 方式 2：通过 fastmcp run

```bash
pip install fastmcp
fastmcp run mcp-server/xiyouji_mcp.py
```

### 方式 3：pip 安装（开发模式）

```bash
cd mcp-server
pip install -e .
xiyouji-mcp
```

## MCP 客户端配置

### Claude Desktop / Cursor / TRAE

```json
{
  "mcpServers": {
    "xiyouji-mcp": {
      "command": "python",
      "args": ["d:/1/xiyouji/mcp-server/xiyouji_mcp.py"],
      "cwd": "d:/1/xiyouji"
    }
  }
}
```

## 工具使用示例

### 1. xiyouji_drl_spotcheck — DRL spot-check

验证 prior session 的"修复已落地"声明（E1 铁律）。

```
参数：
  file_path: "CHANGELOG.md"
  old: "W199"           # 修复前的值（应 0 命中）
  new: "W200"           # 修复后的值（应 >=1 命中）

返回：
  { "ok": true, "checks": [...], "summary": "全部通过 · 1 项检查" }
```

### 2. xiyouji_data_validate — JSON 校验

```
参数：
  file: null    # None = 扫描全部
  quiet: true   # 仅返回问题文件

返回：
  { "ok": true, "total": 100, "passed": 100, "failed": 0, "issues": [] }
```

### 3. xiyouji_docs_index — docs 索引校验

```
参数：
  include_dev: false

返回：
  { "ok": true, "total_files": 200, "sections": [...], "outdated": false }
```

### 4. xiyouji_lint_links — 链接校验

```
参数：
  scan_dir: "site"
  external: false

返回：
  { "ok": true, "scanned_files": 38, "total_links": 500, "broken": [] }
```

### 5. xiyouji_a11y_audit — a11y 审查

```
参数：
  file: null
  scan_dir: "site/data"

返回：
  { "ok": false, "p0_count": 0, "p1_count": 18, "p2_count": 62 }
```

## 设计原则

1. **只读优先**：所有工具 `readOnlyHint=true`，不修改文件（docs_index 默认 --check 模式）
2. **结构化输出**：返回 JSON dict，便于 LLM 解析
3. **可操作错误**：错误信息包含具体文件名和原因
4. **项目路径感知**：自动解析相对路径为项目根目录绝对路径
5. **无外部 API 依赖**：纯标准库 + fastmcp，无需网络

## 与原脚本的关系

| MCP 工具 | 原脚本 | 差异 |
|:---|:---|:---|
| xiyouji_drl_spotcheck | scripts/drl_spotcheck.py | 内联实现，无需 subprocess |
| xiyouji_data_validate | scripts/data_validate.py | 内联实现，EXPECTED_TYPES 内嵌 |
| xiyouji_docs_index | scripts/docs_index.py | 仅 --check 模式，不生成文件 |
| xiyouji_lint_links | scripts/lint_links.py | 仅站内校验，外链默认跳过 |
| xiyouji_a11y_audit | scripts/a11y_audit.py | 简化版，5 条核心规则 |

原脚本保持不变，MCP 工具为独立实现，避免 subprocess 开销。

## 测试

```bash
# 语法检查
python -m py_compile mcp-server/xiyouji_mcp.py

# 单元测试（见 tests/test_xiyouji_mcp.py）
pytest tests/test_xiyouji_mcp.py -v
```

## 关联文档

- [mcp-builder skill](file:///c:/Users/12739/.trae-cn/skills/mcp-builder/SKILL.md)
- [DRL真循环.md](file:///d:/1/xiyouji/docs/10-方法论沉淀/DRL真循环.md)
- [E1铁律.md](file:///d:/1/xiyouji/docs/10-方法论沉淀/E1铁律.md)
- [CHANGELOG.md](file:///d:/1/xiyouji/CHANGELOG.md) v2.2.24 W201 段
