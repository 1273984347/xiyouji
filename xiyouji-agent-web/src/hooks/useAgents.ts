import { useState, useEffect, useCallback } from 'react';
import { CustomAgent } from '../types';
import { v4 as uuidv4 } from 'uuid';

const STORAGE_KEY = 'customAgents';

// 默认的 Agent —— 适配「详解西游记」xiyouji 项目
const DEFAULT_AGENT: CustomAgent = {
  id: 'default',
  name: '西游记·渡口问津',
  description: '详解西游记（xiyouji）项目专属助手：解读、检索、运行分析脚本、撰写文档',
  systemPrompt: `你是「详解西游记」项目的专属智能助手，代号「渡口问津」。

【项目背景】
本项目（位于 D:/1/xiyouji）是一座关于《西游记》的混合型解读知识库，以「一源多形」方式组织：
- docs/：Markdown 文档主体，含十大学生板块（01 全书逐回解读、02 人物深度分析、03 主题与情节专题、04 文化与历史背景、05 诗词歌赋、06 个人随笔、07 学以致用、08 提升认知、09 精神塑造、10 方法论沉淀），以及 00-导读（项目说明、阅读指南、术语表）。
- source/：原著全文、分回文本、引用与网络解读、学术论文索引。
- site/：D3.js 驱动的可浏览 HTML 站点（dashboard、chapters、characters、themes、data 可视化页）。
- scripts/：Python 文本分析与可视化脚本（按 A–AH 共 34 类组织），含词频、人物共现、八十一难、关系网络、心性曲线等。
- dataset/：多个结构化 JSON（八十一难明细、章节元数据、元气图谱三元映射等）。
- timeline/：取经路线、大事年表、人物时间线。

【你的职责】
1. 项目向导：帮用户快速定位某回解读、某个人物分析、某个主题专题或某张可视化页面，给出可对照的文件路径（如 docs/01-全书逐回解读/...）。
2. 研究助手：基于 docs/ 与 source/ 原文回答情节、人物、佛道思想、明代隐喻、诗词、内丹术语（心猿/木母/黄婆等）问题，引用时注明来源路径。
3. 工程助手：可阅读并运行 scripts/ 下的 Python 脚本做文本分析，将结果写入 dataset/ 或生成可视化；运行脚本前先说明用途与预期。
4. 写作助手：协助撰写/修订 docs/ 下的解读文档，遵循 docs/00-导读/文档规范.md 的防膨胀与归档规则。

【行为准则】
- 优先引用项目内已有文档与原文，给出可对照路径。
- 涉及诗词、术语时参考 source/ 与 docs/00-导读/术语表.md。
- 文件操作前先确认意图；写入新内容遵循项目文档规范。
- 语气可带古典雅致，但表达务必清晰、准确、可操作。
- 当前项目版本 v2.3.9（详见 README.md 顶部与 CHANGELOG.md）。`,
  icon: 'BookOpen',
  color: '#c8463a',
  permissionMode: 'acceptEdits',  // P0-1 修复：默认不做 bypassPermissions（高危操作需人工确认）
  createdAt: new Date(),
  updatedAt: new Date(),
};

export function useAgents() {
  const [agents, setAgents] = useState<CustomAgent[]>(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        return [DEFAULT_AGENT, ...parsed.map((a: any) => ({
          ...a,
          createdAt: new Date(a.createdAt),
          updatedAt: new Date(a.updatedAt),
        }))];
      }
    } catch (e) {
      console.error('Failed to load agents:', e);
    }
    return [DEFAULT_AGENT];
  });

  // 保存到 localStorage（排除默认 agent）
  const saveAgents = useCallback((newAgents: CustomAgent[]) => {
    const toSave = newAgents.filter(a => a.id !== 'default');
    localStorage.setItem(STORAGE_KEY, JSON.stringify(toSave));
  }, []);

  const addAgent = useCallback((agent: Omit<CustomAgent, 'id' | 'createdAt' | 'updatedAt'>) => {
    const newAgent: CustomAgent = {
      ...agent,
      id: uuidv4(),
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    setAgents(prev => {
      const updated = [...prev, newAgent];
      saveAgents(updated);
      return updated;
    });
    return newAgent;
  }, [saveAgents]);

  const updateAgent = useCallback((id: string, updates: Partial<Omit<CustomAgent, 'id' | 'createdAt'>>) => {
    setAgents(prev => {
      const updated = prev.map(a => 
        a.id === id ? { ...a, ...updates, updatedAt: new Date() } : a
      );
      saveAgents(updated);
      return updated;
    });
  }, [saveAgents]);

  const deleteAgent = useCallback((id: string) => {
    if (id === 'default') return; // 不能删除默认 agent
    setAgents(prev => {
      const updated = prev.filter(a => a.id !== id);
      saveAgents(updated);
      return updated;
    });
  }, [saveAgents]);

  const getAgent = useCallback((id: string) => {
    return agents.find(a => a.id === id);
  }, [agents]);

  return {
    agents,
    addAgent,
    updateAgent,
    deleteAgent,
    getAgent,
    defaultAgent: DEFAULT_AGENT,
  };
}
