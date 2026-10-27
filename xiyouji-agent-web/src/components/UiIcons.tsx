/**
 * W950 · 界面内联图标（东方线描·与静态站 site/static/icons/ui 同一套图形）
 *
 * 替代此前用 emoji 充当图标的位置（⚠️ / 📝 / 🔗）：
 *   · emoji 跨平台字形不一致、暗色模式不可控、屏幕阅读器读出「thumbs up」而非语义。
 *   · 本组件用内联 SVG（fill:none + stroke:currentColor）⇒ 颜色跟随 currentColor，
 *     随主题自动适配，且零外域依赖（不引入新的图标包依赖）。
 *
 * ⚠️ 本文件由 scripts/_w950_refresh_icon_paths.py 从 site/static/icons/ui/*.svg 重建
 *    （W950 起：图标资产是唯一事实源·此处不得手抄 path）。
 * 图形：warn = 警示三角 · note = 折角纸页 · link = 双环链条
 */
import type { CSSProperties } from 'react';

const BASE: CSSProperties = {
  width: '1em',
  height: '1em',
  verticalAlign: '-0.14em',
  flexShrink: 0,
};

function Svg({ children, style }: { children: React.ReactNode; style?: CSSProperties }) {
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
      {children}
    </svg>
  );
}

/** 警示三角（危险操作提示） */
export function WarnIcon({ style }: { style?: CSSProperties }) {
  return (
    <Svg style={style}>
      <path d="M12 3.4l9.4 16.2H2.6zM12 9.4v4.8M12 16.8v.6" transform="translate(0.2353 0.7255) scale(0.9804)" />
    </Svg>
  );
}

/** 折角纸页（文件修改提示） */
export function NoteIcon({ style }: { style?: CSSProperties }) {
  return (
    <Svg style={style}>
      <path d="M6 3.6h8l4 4v12.8H6zM14 3.6v4h4M9.2 12h5.6M9.2 15.4h3.6" transform="translate(-1.0435 -1.0435) scale(1.087)" />
    </Svg>
  );
}

/** 双环链条（链接） */
export function LinkIcon({ style }: { style?: CSSProperties }) {
  return (
    <Svg style={style}>
      <path d="M8.4 12.2a3.4 3.4 0 0 0 2.4 5.9l1.6-1.6a3.4 3.4 0 0 0 0-4.8M15.6 11.8a3.4 3.4 0 0 0-2.4-5.9l-1.6 1.6a3.4 3.4 0 0 0 0 4.8M9.9 14.1l4.2-4.2" transform="translate(-5.3913 -5.3913) scale(1.4493)" />
    </Svg>
  );
}
