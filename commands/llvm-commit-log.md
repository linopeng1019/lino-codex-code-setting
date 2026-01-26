幫我為 git tree 上最後一個 commit 寫合適的 commit message，針對 LLVM 專案的規範：

格式要求：
- 每行不超過 79 字元（程式碼、指令、路徑、網址除外）
- 使用英文，簡潔口語化表達
- 禁用 emoji 或非 ASCII 字元
- 採用 LLVM 慣用格式：[Component] Brief description

LLVM 專案特定規範：
- 組件標識：使用方括號標示相關組件，如：
  [clang], [llvm], [mlir], [flang], [lld], [lldb], [openmp]
  [CodeGen], [X86], [AArch64], [RISCV], [WebAssembly]
  [SelectionDAG], [GlobalISel], [MC], [IR], [Analysis]
- 描述格式：簡潔描述變更內容，避免冗餘詞彙
- 技術術語：可使用 LLVM 領域專用術語（如 DAG, ISel, BB 等）
- 測試相關：標示為 [test] 或在組件後加 test

內容指引：
- 動詞原形開頭，描述具體變更
- 優先說明功能影響而非實作細節
- 提及相關 bug 修復時使用 "Fix" 開頭
- 新功能使用 "Add" 或 "Implement" 開頭

參考現有內容：
- 若該 commit 已有 commit message，分析其組件歸類和描述方式
- 保留重要的 issue 引用、PR 號碼或相關討論連結
- 維持原始技術重點，但符合 LLVM 格式規範

工作流程：
1. 檢查是否已有 commit message，若有則先展示原始內容
2. 分析變更文件，識別相關 LLVM 組件
3. 提供 2-3 個符合 LLVM 風格的 commit message 選項
4. 等待我選擇或提供修改意見
5. 收到 "ok" 確認後才寫入 git tree
6. 若變更跨多個組件，建議是否拆分 commit

範例格式：
- [clang] Add support for C++23 auto deduction in lambdas
- [CodeGen] Fix register allocation bug in loop unrolling
- [X86] Implement AVX-512 instruction selection patterns
- [test] Add regression tests for ARM64 atomic operations
