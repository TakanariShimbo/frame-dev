// アプリのモード（題材）。ホームで選び、以降の画面の文言を切り替える。
// 画面構成・機能は共通で、変わるのは文言だけ（useModeT が hanabi.* キーを優先して引く）。
export type AppMode = "mountain" | "hanabi";

let mode: AppMode = "mountain";

export function setAppMode(m: AppMode): void {
  mode = m;
}

export function getAppMode(): AppMode {
  return mode;
}
