// 声明所有的 .css 文件
declare module '*.css' {
  const content: { [className: string]: string };
  export default content;
}

// 顺便把 .scss 也声明了，以后用到就不会报错
declare module '*.scss' {
  const content: { [className: string]: string };
  export default content;
}

// vite/client.d.ts（Vite 内置），为了识别env文件
interface ImportMeta {
  readonly env: ImportMetaEnv  // ✅ 补上了 env
}