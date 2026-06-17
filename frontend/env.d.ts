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