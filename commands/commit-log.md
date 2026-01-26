幫我為 git tree 上最後一個 commit 寫合適的 commit message，規則如下：

格式要求：
- 每行不超過 79 字元（程式碼、指令、路徑、網址除外）
- 使用英文，簡潔口語化表達
- 禁用 emoji 或非 ASCII 字元
- 採用 Conventional Commits 格式：<type>(<scope>): <description>

內容指引：
- 動詞原形開頭，描述「做了什麼」
- 常用類型：feat, fix, docs, style, refactor, test, chore
- 必要時在空行後添加詳細說明

參考現有內容：
- 若該 commit 已有 commit message，請分析其內容和意圖
- 保留有價值的資訊，改善格式和表達方式
- 維持原始語調和重點，但符合上述規範

工作流程：
1. 檢查是否已有 commit message，若有則先展示原始內容
2. 分析程式碼變更，提供 2-3 個改進的 commit message 選項
3. 等待我選擇或提供修改意見
4. 收到 "ok" 確認後才寫入 git tree
5. 若變更複雜，詢問是否需要拆分多個 commit
