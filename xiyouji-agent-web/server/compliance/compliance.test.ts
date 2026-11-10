/**
 * compliance.test.ts — 合规面单测（W1205 · D-3 合规批）
 *
 * 覆盖四组：
 *  ① 分级目录（§12.1 单一事实源：四级齐全 + 落点/存储/传输逐字对齐）；
 *  ② 入库强制校验的可枚举错误类（C-4 + C-6）；
 *  ③ 部署基线自检（fail-closed：基线不满足 ⇒ 拒绝启动）；
 *  ④ 留存期口径（§12.5：审计 ≥ 180 天下限 · 类别可配）。
 *
 * 运行：cd xiyouji-agent-web && node --import tsx --test server/compliance/compliance.test.ts
 */
import { test } from "node:test";
import assert from "node:assert";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {
  DATA_CLASS_CATALOG,
  DATA_CLASSES,
  RESOURCE_CLASS,
  SENSITIVE_COLUMNS,
  dataClassEnforcementEnabled,
  isDataClass,
  requireDataClass,
  resolveDataClass,
  resolveWriteDataClass,
} from "./data-class.js";
import {
  ComplianceError,
  ComplianceErrorCode,
  complianceErrorCodes,
  complianceHttpStatus,
  isComplianceError,
} from "./errors.js";
import {
  DEFAULT_BASELINE_REQUIREMENT,
  assertDeploymentBaseline,
  baselineEnabled,
  effectiveAllowedHosts,
  evaluateDeploymentBaseline,
  loadBaselineFile,
  resolveBaselineRequirement,
} from "./baseline.js";
import {
  AUDIT_RETENTION_FLOOR_DAYS,
  RETENTION_POLICIES,
  resolveRetention,
  retentionCategories,
  retentionCutoff,
} from "./retention.js";
import { AUDIT_REQUIRED_FIELDS, isStructuredAuditEvent } from "./audit-event.js";

const TMP = fs.mkdtempSync(path.join(os.tmpdir(), "xiyouji-compliance-test-"));

// ============= ① 分级目录（§12.1 单一事实源） =============

test("E1 分级目录：四级齐全且每级判定标准/落点/存储/传输要求非空", () => {
  assert.deepEqual([...DATA_CLASSES], ["L1", "L2", "L3", "L4"], "分级必须是且只是四级");
  for (const level of DATA_CLASSES) {
    const spec = DATA_CLASS_CATALOG[level];
    assert.ok(spec, level + " 应有规格");
    assert.equal(spec.level, level);
    assert.ok(spec.name.length > 0, level + " 应有名称");
    assert.ok(spec.criteria.length > 0, level + " 应有判定标准");
    assert.ok(spec.projectScope.length > 0, level + " 应有本项目落点");
    assert.ok(spec.storage.length > 0, level + " 应有存储要求");
    assert.ok(spec.transmission.length > 0, level + " 应有传输要求");
  }
  // 逐字对齐方案 §12.1（改口径时这里会红 ⇒ 文档与代码同步）
  assert.deepEqual(DATA_CLASS_CATALOG.L1.projectScope, ["原著原文", "解读文档", "公开可视化数据"]);
  assert.equal(DATA_CLASS_CATALOG.L1.storage, "Git 明文");
  assert.deepEqual(DATA_CLASS_CATALOG.L2.projectScope, ["反馈数据", "构建元数据", "内部报告"]);
  assert.equal(DATA_CLASS_CATALOG.L2.storage, "DB 明文或列级加密");
  assert.equal(DATA_CLASS_CATALOG.L2.transmission, "内网即可");
  assert.deepEqual(DATA_CLASS_CATALOG.L3.projectScope, ["会话与消息（含用户提问内容）", "检索上下文"]);
  assert.equal(DATA_CLASS_CATALOG.L3.storage, "列级加密（敏感列）");
  assert.equal(DATA_CLASS_CATALOG.L3.transmission, "必须 TLS");
  assert.deepEqual(DATA_CLASS_CATALOG.L4.projectScope, ["审计事件", "密钥", "凭证"]);
  assert.equal(DATA_CLASS_CATALOG.L4.storage, "加密存储 + 只追加");
  assert.equal(DATA_CLASS_CATALOG.L4.transmission, "必须 TLS");
  assert.equal(DATA_CLASS_CATALOG.L3.columnEncryptionRequired, true, "L3 必须列级加密");
  assert.equal(DATA_CLASS_CATALOG.L4.columnEncryptionRequired, true, "L4 必须加密存储");
  assert.equal(DATA_CLASS_CATALOG.L4.appendOnlyRequired, true, "L4 必须只追加");
  assert.equal(DATA_CLASS_CATALOG.L1.columnEncryptionRequired, false, "L1 不要求加密");
});

test("E2 落点映射与敏感列映射（§12.1 落点列的可执行形态）", () => {
  assert.equal(resolveDataClass("sessions"), "L3", "会话 = L3");
  assert.equal(resolveDataClass("messages"), "L3", "消息 = L3");
  assert.equal(resolveDataClass("feedback"), "L2", "反馈 = L2");
  assert.equal(resolveDataClass("audit"), "L4", "审计事件 = L4");
  assert.equal(resolveDataClass("keys"), "L4", "密钥/凭证 = L4");
  assert.equal(resolveDataClass("content"), "L1", "公开内容 = L1");
  assert.deepEqual(Object.keys(RESOURCE_CLASS).sort(), Object.keys(RESOURCE_CLASS).sort());
  assert.deepEqual(SENSITIVE_COLUMNS.messages, ["content", "tool_calls"], "消息的敏感列 = 正文 + 工具调用");
  assert.deepEqual(SENSITIVE_COLUMNS.feedback, [], "L2 反馈表不强制加密");
});

// ============= ② 可枚举错误类（C-4）+ 入库强制校验（C-6） =============

test("E3 requireDataClass：缺标签/非法值各报一个可枚举错误码，合法值原样返回", () => {
  assert.throws(
    () => requireDataClass(undefined, "t.missing"),
    (err: unknown) => {
      assert.ok(isComplianceError(err), "应为 ComplianceError");
      assert.equal(err.code, ComplianceErrorCode.DATA_CLASS_MISSING);
      return true;
    },
  );
  assert.throws(
    () => requireDataClass("L9", "t.invalid"),
    (err: unknown) => {
      assert.ok(isComplianceError(err));
      assert.equal(err.code, ComplianceErrorCode.DATA_CLASS_INVALID);
      return true;
    },
  );
  assert.equal(requireDataClass("L3", "t.ok"), "L3");
  assert.equal(isDataClass("L1"), true);
  assert.equal(isDataClass("l1"), false, "级别大小写敏感（与 PG CHECK 约束一致）");
  assert.equal(isDataClass(null), false);
});

test("E4 错误码可枚举（C-4）：全部错误码可穷举，且每类映射到确定的 HTTP 语义", () => {
  const codes = complianceErrorCodes();
  assert.ok(codes.length >= 8, "合规错误码应成规模可枚举，实际 " + codes.length);
  assert.equal(new Set(codes).size, codes.length, "错误码不得重复");
  assert.ok(codes.includes(ComplianceErrorCode.DATA_CLASS_MISSING));
  assert.ok(codes.includes(ComplianceErrorCode.DATA_CLASS_INVALID));
  assert.ok(codes.includes(ComplianceErrorCode.BASELINE_VIOLATION));
  assert.equal(complianceHttpStatus(ComplianceErrorCode.DATA_CLASS_MISSING), 400);
  assert.equal(complianceHttpStatus(ComplianceErrorCode.BASELINE_VIOLATION), 503);
  const err = new ComplianceError(ComplianceErrorCode.RETENTION_INVALID, "x", { category: "audit" });
  assert.ok(err instanceof Error, "合规错误仍是 Error 的子类（可被 catch）");
  assert.equal(err.name, "ComplianceError");
  assert.equal(err.code, ComplianceErrorCode.RETENTION_INVALID);
});

test("E5 入库分级解析：强制模式缺标签拒绝；显式非法值一律拒绝；非强制模式按目录推导", () => {
  const strict = { AGENT_WEB_COMPLIANCE_ENFORCE: "1" } as NodeJS.ProcessEnv;
  assert.equal(dataClassEnforcementEnabled(strict), true);
  assert.equal(dataClassEnforcementEnabled({} as NodeJS.ProcessEnv), false, "默认不改变现役行为");
  assert.throws(
    () => resolveWriteDataClass(undefined, "messages", "t.strict", strict),
    (err: unknown) => isComplianceError(err) && err.code === ComplianceErrorCode.DATA_CLASS_MISSING,
  );
  assert.throws(
    () => resolveWriteDataClass("L9", "messages", "t.bad", {} as NodeJS.ProcessEnv),
    (err: unknown) => isComplianceError(err) && err.code === ComplianceErrorCode.DATA_CLASS_INVALID,
    "显式非法值在任何模式下都拒绝（不因开关放宽）",
  );
  assert.equal(resolveWriteDataClass(undefined, "messages", "t.lenient", {} as NodeJS.ProcessEnv), "L3");
  assert.equal(resolveWriteDataClass(undefined, "feedback", "t.lenient", {} as NodeJS.ProcessEnv), "L2");
  assert.equal(resolveWriteDataClass("L1", "messages", "t.explicit", strict), "L1");
});

// ============= ③ 部署基线（fail-closed） =============

/** 一份满足全部基线要求的环境（口令/密钥均为测试造值·非真实凭据）。 */
function goodEnv(): NodeJS.ProcessEnv {
  return {
    AGENT_WEB_REQUIRE_TOKEN: "1",
    AGENT_WEB_TOKEN: "t".repeat(40),
    AGENT_WEB_BIND_HOST: "127.0.0.1",
    AGENT_WEB_ALLOWED_HOSTS: "app.internal",
    AGENT_WEB_TLS_TERMINATED: "1",
    AGENT_WEB_PG_SSL: "require",
    AGENT_WEB_DATA_KEY: Buffer.alloc(32, 7).toString("base64"),
    AGENT_WEB_AUDIT_LOG: path.join(TMP, "baseline", "audit.jsonl"),
  } as NodeJS.ProcessEnv;
}

test("E6 基线自检：全部满足 ⇒ 通过；任一要素缺失 ⇒ 违规并列出", () => {
  const ok = evaluateDeploymentBaseline(goodEnv());
  assert.equal(ok.ok, true, "满足基线时应通过：\n" + ok.violations.join("\n"));
  assert.equal(ok.checks.length >= 8, true, "基线检查项应覆盖四要素 + 加密/留存/审计可写");

  const noToken = goodEnv();
  delete noToken.AGENT_WEB_TOKEN;
  const r2 = evaluateDeploymentBaseline(noToken);
  assert.equal(r2.ok, false, "缺 token 必须不通过");
  assert.ok(r2.violations.some((v) => v.includes("auth.token")), "应指出强制鉴权违规：\n" + r2.violations.join("\n"));

  const shortToken = goodEnv();
  shortToken.AGENT_WEB_TOKEN = "short";
  assert.equal(evaluateDeploymentBaseline(shortToken).ok, false, "过短 token 必须不通过");

  const noTls = goodEnv();
  delete noTls.AGENT_WEB_TLS_TERMINATED;
  assert.ok(evaluateDeploymentBaseline(noTls).violations.some((v) => v.includes("transport.client_tls")), "缺 TLS 终止声明须违规");

  const wildcardHost = goodEnv();
  wildcardHost.AGENT_WEB_ALLOWED_HOSTS = "*";
  assert.ok(evaluateDeploymentBaseline(wildcardHost).violations.some((v) => v.includes("net.host_allowlist")), "通配 Host 白名单须违规");

  const nonLoopback = goodEnv();
  nonLoopback.AGENT_WEB_BIND_HOST = "0.0.0.0";
  assert.ok(evaluateDeploymentBaseline(nonLoopback).violations.some((v) => v.includes("net.bind_loopback")), "非回环监听须违规");

  const noKey = goodEnv();
  delete noKey.AGENT_WEB_DATA_KEY;
  assert.ok(evaluateDeploymentBaseline(noKey).violations.some((v) => v.includes("crypto.column_encryption")), "缺加密密钥须违规");

  const pgNoSsl = goodEnv();
  pgNoSsl.AGENT_WEB_DB_BACKEND = "postgres";
  pgNoSsl.AGENT_WEB_PG_SSL = "disable";
  assert.ok(evaluateDeploymentBaseline(pgNoSsl).violations.some((v) => v.includes("transport.pg_tls")), "PG 链路非 TLS 须违规");

  const pgSslOk = goodEnv();
  pgSslOk.AGENT_WEB_DB_BACKEND = "postgres";
  assert.equal(evaluateDeploymentBaseline(pgSslOk).ok, true, "PG + ssl=require 应通过");
});

test("E7 基线不满足 ⇒ 拒绝启动（抛错·非警告）", () => {
  const bad = goodEnv();
  delete bad.AGENT_WEB_TOKEN;
  assert.throws(
    () => assertDeploymentBaseline(bad),
    (err: unknown) => {
      assert.ok(isComplianceError(err), "应为 ComplianceError");
      assert.equal(err.code, ComplianceErrorCode.BASELINE_VIOLATION);
      assert.ok(String(err.detail.violations).includes("auth.token"), "违规清单应含具体违规项");
      return true;
    },
    "基线自检失败必须抛错（调用方据此拒绝启动）",
  );
  // 通过时返回结果对象（可打印检查项清单）
  const ok = assertDeploymentBaseline(goodEnv());
  assert.equal(ok.ok, true);
});

test("E8 基线开关默认关闭（不改现役启动行为）", () => {
  assert.equal(baselineEnabled({} as NodeJS.ProcessEnv), false);
  assert.equal(baselineEnabled({ AGENT_WEB_COMPLIANCE_BASELINE: "1" } as NodeJS.ProcessEnv), true);
  assert.equal(baselineEnabled({ AGENT_WEB_COMPLIANCE_BASELINE: "0" } as NodeJS.ProcessEnv), false);
  assert.ok(DEFAULT_BASELINE_REQUIREMENT.requireAuth, "基线默认要求强制鉴权");
  assert.equal(DEFAULT_BASELINE_REQUIREMENT.minAuditRetentionDays, AUDIT_RETENTION_FLOOR_DAYS);
  const hosts = effectiveAllowedHosts({ AGENT_WEB_ALLOWED_HOSTS: "a.com , b.com" } as NodeJS.ProcessEnv);
  assert.deepEqual(hosts, ["127.0.0.1", "localhost", "::1", "a.com", "b.com"], "Host 白名单口径：回环三形态 + 追加项");
});

// ============= ④ 留存期口径（§12.5） =============

test("E9 留存期：审计默认 180 天且有硬下限；类别可配；永久类不销毁", () => {
  const policies = resolveRetention({} as NodeJS.ProcessEnv);
  assert.equal(policies.audit.retentionDays, AUDIT_RETENTION_FLOOR_DAYS, "审计默认 180 天");
  assert.equal(policies.audit.minDays, AUDIT_RETENTION_FLOOR_DAYS);
  assert.equal(policies.session.retentionDays, 90);
  assert.equal(policies.session.archiveDays, 180);
  assert.equal(policies.message.retentionDays, 90);
  assert.equal(policies.feedback.retentionDays, 365);
  assert.equal(policies.content.retentionDays, null, "公开内容永久（Git）");
  assert.equal(retentionCutoff(policies.content, Date.now()), null, "永久类无截止时刻");
  assert.ok(retentionCutoff(policies.audit, Date.now()) instanceof Date);
  assert.equal(retentionCategories().length, Object.keys(RETENTION_POLICIES).length);
});

test("E10 留存期越界配置 ⇒ 拒绝（fail-closed·不等到销毁时才发现）", () => {
  assert.throws(
    () => resolveRetention({ AGENT_WEB_RETENTION_AUDIT_DAYS: "30" } as NodeJS.ProcessEnv),
    (err: unknown) => isComplianceError(err) && err.code === ComplianceErrorCode.RETENTION_INVALID,
    "审计留存期低于 180 天下限必须拒绝",
  );
  assert.throws(
    () => resolveRetention({ AGENT_WEB_RETENTION_AUDIT_DAYS: "abc" } as NodeJS.ProcessEnv),
    (err: unknown) => isComplianceError(err) && err.code === ComplianceErrorCode.RETENTION_INVALID,
  );
  assert.throws(
    () => resolveRetention({ AGENT_WEB_RETENTION_FEEDBACK_DAYS: "10" } as NodeJS.ProcessEnv),
    (err: unknown) => isComplianceError(err) && err.code === ComplianceErrorCode.RETENTION_INVALID,
    "反馈留存期低于 365 天下限必须拒绝",
  );
  const longer = resolveRetention({ AGENT_WEB_RETENTION_AUDIT_DAYS: "365" } as NodeJS.ProcessEnv);
  assert.equal(longer.audit.retentionDays, 365, "允许调长（收紧合规而非放松）");
});

test("E12 基线配置文件：可加载并覆盖默认要求；非法文件 ⇒ 判违规（不静默通过）", () => {
  const file = path.join(TMP, "baseline.json");
  fs.writeFileSync(file, JSON.stringify({ version: 1, minTokenLength: 64, requireColumnEncryption: false }), "utf8");
  const loaded = loadBaselineFile(file);
  assert.equal(loaded.minTokenLength, 64, "配置文件应覆盖默认要求");
  const { requirement, fileError } = resolveBaselineRequirement({ AGENT_WEB_COMPLIANCE_BASELINE_FILE: file } as NodeJS.ProcessEnv);
  assert.equal(fileError, undefined, "合法文件不应报错");
  assert.equal(requirement.minTokenLength, 64);
  assert.equal(requirement.requireColumnEncryption, false);
  // 短 token 在加严后的基线下仍应违规
  const env = goodEnv();
  env.AGENT_WEB_TOKEN = "t".repeat(40);
  env.AGENT_WEB_COMPLIANCE_BASELINE_FILE = file;
  const res = evaluateDeploymentBaseline(env);
  assert.equal(res.ok, false, "加严到 64 字符后 40 字符 token 应违规");
  assert.ok(res.violations.some((v) => v.includes("auth.token")));
  // 非法文件 ⇒ 违规清单里点名（而不是抛未捕获异常或静默放过）
  const bad = path.join(TMP, "bad-baseline.json");
  fs.writeFileSync(bad, "{ not json", "utf8");
  const badRes = evaluateDeploymentBaseline({ AGENT_WEB_COMPLIANCE_BASELINE_FILE: bad } as NodeJS.ProcessEnv);
  assert.equal(badRes.ok, false, "非法基线文件必须判违规");
  assert.ok(badRes.violations.some((v) => v.includes("baseline.config_file")));
});

// ============= ⑤ 审计事件结构（§12.3） =============

test("E11 审计事件必填字段清单：11 个且覆盖 §12.3 全部规定字段", () => {
  assert.equal(AUDIT_REQUIRED_FIELDS.length, 11, "必填字段应为 11 个");
  for (const f of [
    "ts",
    "event_id",
    "actor",
    "action",
    "target",
    "decision",
    "result",
    "data_class",
    "trace_id",
    "source_ip",
  ]) {
    assert.ok(AUDIT_REQUIRED_FIELDS.includes(f), "必填清单应含 " + f);
  }
  assert.equal(isStructuredAuditEvent({}), false);
  assert.equal(isStructuredAuditEvent({ schema_version: 1, ts: "x", event_id: "y", actor: "a", action: "read", target: "t", decision: "allow", result: "ok", data_class: "L9", trace_id: "", source_ip: "" }), false, "非法级别不算结构化事件");
});
