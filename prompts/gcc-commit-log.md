幫我為 git tree 上最後一個 commit 寫合適的 commit message，針對 GCC 專案的規範：

格式要求：
- 每行不超過 79 字元（程式碼、指令、路徑、網址除外）
- 使用英文，簡潔口語化表達
- 禁用 emoji 或非 ASCII 字元
- 採用 GCC 標準格式：component: Brief description

GCC 專案特定規範：
- 組件標識：使用小寫組件名，如：
  c++, c, fortran, ada, go, objc, objc++, jit
  tree-optimization, rtl-optimization, middle-end
  target (或具體架構如 i386, aarch64, rs6000, RISC-V)
  libstdc++, libgcc, libgomp, libgfortran, libobjc
  testsuite, docs, build-system, driver
- 多組件：使用逗號分隔，如 "c++, middle-end:"
- 子組件：使用斜線，如 "libstdc++/ranges:"
- 必須要有符合 GCC 專案規範的 ChangeLog

ChangeLog 格式：
- 每個受影響的目錄需要對應的 ChangeLog 條目
- 空行後列出變更項目，使用 tab 縮進
- 每個文件的變更用 "* filename (function): Description." 格式
- 新增檔案使用 "* filename: New file."
- 刪除檔案使用 "* filename: Removed."

描述風格：
- 首字母大寫，句末不加句號
- 優先描述用戶可見的行為變更
- 修復使用 "Fix"，新功能使用 "Add" 或 "Implement"
- 效能改進使用 "Improve" 或 "Optimize"
- 程式碼清理使用 "Clean up" 或 "Refactor"

技術規範：
- 可使用 GCC 術語（如 gimple, RTL, IPA, LTO 等）
- 提及 PR 號碼："PR c++/12345" 或 "PR target/67890"
- 回歸測試：明確標示 "PR regression/xxxxx"
- ABI 變更：務必在描述中提及

參考現有內容：
- 若該 commit 已有 commit message，分析其組件分類方式
- 保留重要的 PR 引用和 bug 報告號碼
- 維持原始技術重點，但符合 GCC 格式規範

工作流程：
1. 檢查是否已有 commit message，若有則先展示原始內容
2. 分析變更文件，識別相關 GCC 組件和子系統
3. 根據變更文件自動生成對應的 ChangeLog 條目
4. 提供 2-3 個符合 GCC 風格的完整 commit message 選項（包含 ChangeLog）
5. 等待我選擇或提供修改意見
6. 收到 "ok" 確認後，先寫入 git tree
7. 立即執行 `contrib/gcc-changelog/git_check_commit.py` 驗證最新 commit 的格式正確性
8. 若驗證通過則完成；若驗證失敗則：
   - 顯示錯誤訊息並分析問題
   - 根據錯誤提示修正 commit message
   - 使用 `git commit --amend` 更新 commit message
   - 重新執行驗證直到通過為止
9. 若變更影響多個組件，建議是否拆分 commit

範例完整格式：
```
c++: Implement C++23 consteval if feature

gcc/cp/ChangeLog:

	* parser.cc (cp_parser_selection_statement): Add consteval if parsing.
	* semantics.cc (finish_if_stmt): Handle consteval conditions.
gcc/testsuite/ChangeLog:

	* g++.dg/cpp23/consteval-if1.C: New test.
```
