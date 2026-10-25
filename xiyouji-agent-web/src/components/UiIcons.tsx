/**
 * W947 · 界面内联图标（东方线描·与静态站 site/static/icons/ui 同一套图形）
 *
 * 替代此前用 emoji 充当图标的位置（⚠️ / 📝 / 🔗）：
 *   · emoji 跨平台字形不一致、暗色模式不可控、屏幕阅读器读出「thumbs up」而非语义。
 *   · 本组件用内联 SVG（fill:none + stroke:currentColor）⇒ 颜色跟随 currentColor，
 *     随主题自动适配，且零外域依赖（不引入新的图标包依赖）。
 *
 * 图形与静态站资产逐字同源（site/static/icons/ui/{warn,note,link}.svg）。
 */
import type { CSSProperties } from 'react';

const BASE: CSSProperties = {
  width: '1em',
  height: '1em',
  verticalAlign: '-0.14em',
  flexShrink: 0,
};

function Svg({ d, style }: { d: string; style?: CSSProperties }) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={1.5}
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      focusable="false"
      style={{ ...BASE, ...style }}
    >
      <path d={d} />
    </svg>
  );
}

/** 警示三角（危险操作提示） */
export function WarnIcon({ style }: { style?: CSSProperties }) {
  return <Svg d="M12 3.4l9.4 16.2H2.6zM12 9.4v4.8M12 16.8v.6" style={style} />;
}

/** 折角纸页（文件修改提示） */
export function NoteIcon({ style }: { style?: CSSProperties }) {
  return <Svg d="M6 3.6h8l4 4v12.8H6zM14 3.6v4h4M9.2 12h5.6M9.2 15.4h3.6" style={style} />;
}

/** 双环链条（链接） */
export function LinkIcon({ style }: { style?: CSSProperties }) {
  return (
    <Svg
      d="M9.7 14.3a3.5 3.5 0 0 0 5 0l2.6-2.6a3.5 3.5 0 0 0-5-5l-1.3 1.3M14.3 9.7a3.5 3.5 0 0 0-5 0l-2.6 2.6a3.5 3.5 0 0 0 5 5l1.3-1.3"
      style={style}
    />
  );
}
