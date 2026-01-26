# PR Review Comment 自動處理

請幫我處理 PR #$ARGUMENTS 的最新 review comment 並進行相應修改。請按照以下步驟執行：

## 步驟 0: 確認 PR 存在
1. 首先確認指定的 PR 是否存在並可訪問：
   ```bash
   gh pr view <pr-number>
   ```
   - 檢查 PR 狀態（Open/Closed/Merged）
   - 確認 PR 標題和描述
   - 檢查是否有權限訪問該 PR
   - 如果 PR 不存在或無法訪問，請停止執行並報告錯誤

## 步驟 1: 設置工作環境
1. 創建新的 git worktree 避免污染當前分支：
   ```bash
   git worktree add pr<pr-number>
   cd pr<pr-number>
   ```

2. 切換到指定的 PR 分支：
   ```bash
   gh pr checkout <pr-number>
   ```

## 步驟 2: 獲取 Repository 資訊
1. 從 git remote 獲取 owner 和 repo 資訊：
   ```bash
   git remote -v
   ```
   請解析輸出並提取 `<owner>/<repo>` 格式的資訊。

## 步驟 3: 獲取 Review Comments
1. 獲取 PR 的所有 reviews：
   ```bash
   gh api repos/<owner>/<repo>/pulls/<pr-number>/reviews
   ```

2. 從返回的 JSON 中找到最後一個 review 的 ID（通常是數組中的最後一個元素）

3. 使用該 review ID 獲取具體的 review comments：
   ```bash
   gh api repos/<owner>/<repo>/pulls/<pr-number>/reviews/<review-id>/comments
   ```

4. 檢查並獲取回覆串內容（如果存在）：
   - 檢查每個 review comment 是否包含 `in_reply_to_id` 欄位
   - 如果 `in_reply_to_id` 欄位存在，則使用以下指令獲取原始 comment 的內容：
     ```bash
     gh api repos/<owner>/<repo>/pulls/comments/<in_reply_to_id>
     ```
   - 這能幫助理解 comment 的完整上下文和討論脈絡

## 步驟 4: 分析並執行修改
1. 仔細分析 review comments 的內容，包括：
   - 建議的修改點
   - 相關的檔案路徑
   - 具體的程式碼位置（如果有行號資訊）
   - 修改建議的性質（bug 修復、程式碼品質改善、功能調整等）
   - **上下文分析**：如果該 comment 有 `in_reply_to_id`，請同時分析：
     - 原始 comment 的內容和建議
     - 回覆 comment 與原始 comment 的關係
     - 討論的演進和最終結論
     - 確保理解完整的討論脈絡再進行修改決策
   - 根據 comment 的內容和上下文來判斷該 comment 的重要性和優先級

2. 根據 comments 在當前 worktree 中進行相應的程式碼修改

## 步驟 5: 總結報告
修改完成後，請提供詳細的總結報告，包括：

### 已完成的修改：
- 列出每個 review comment 對應的修改
- 說明修改的具體內容和原因
- 標註修改的檔案和大致的變更範圍
- **上下文考量**：如果該 comment 是回覆串的一部分，說明如何考慮整個討論脈絡來做出修改決策

### 未修改的項目（如果有）：
- 列出沒有處理的 review comments
- 說明未修改的原因，例如：
  - 需要更多上下文資訊
  - 建議與現有架構衝突
  - 需要與團隊討論的設計決策
  - 技術限制或相依性問題
  - **討論串衝突**：如果回覆串中有相互矛盾的建議，建議暫緩修改並尋求澄清

### 注意事項：
- 確保所有修改都符合專案的程式碼風格和慣例
- 如果有任何不確定的地方，請明確指出並建議後續行動
- 檢查修改是否可能影響其他功能，如有需要請提醒進行相關測試

請開始執行以上步驟，並在每個階段提供進度更新。
