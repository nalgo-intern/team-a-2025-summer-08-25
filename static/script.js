const textInput = document.getElementById('text-input');
const analyzeButton = document.getElementById('analyze-button');
const resultArea = document.getElementById('result-area');

// 表示順を固定するための配列を定義
const emotionOrder = [
    "喜び", "悲しみ", "怒り", "驚き", "恐怖", "嫌悪", "信頼", "期待"
];

console.log('操作対象の要素:', resultArea);

// 「分析する」ボタンがクリックされたら非同期処理を実行
analyzeButton.addEventListener('click', async () => {
    // ... (以降の処理は変更ありません) ...
    const inputText = textInput.value;

    if (!inputText.trim()) {
        resultArea.innerHTML = '<p>文章を入力してください。</p>';
        return;
    }

    textInput.value = '';

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: inputText }),
        });

        if (!response.ok) {
            throw new Error('サーバーからの応答が正常ではありません。');
        }

        const data = await response.json();
        displayResults(data);

    } catch (error) {
        displayError('テキスト分析中にエラーが発生しました。');
    }
});

/**
 * 確率をパーセント表示にフォーマットするヘルパー関数
 * @param {number} p - 確率 (0.0 to 1.0)
 * @returns {string} - "xx.x%" 形式の文字列
 */
const pct = (p) => (p * 100).toFixed(1) + '%';

/**
 * 分析結果を詳細に表示する関数
 * @param {object} data - バックエンドから返された分析結果オブジェクト
 */
function displayResults(data) {
    if (data.error) {
        displayError(data.error);
        return;
    }

    const pol_pred = data.polarity.pred;
    const pol_detail = data.polarity.detail;
    const emo_detail = data.emotion.detail;

    let htmlContent = `
        <h2>分析結果</h2>
        
        <div class="result-section">
            <h3>▼ 入力文</h3>
            <p class="input-text-result">${data.text}</p>
        </div>

        <div class="result-section">
            <h3>▼ 極性（ネガ・ニュートラル・ポジ）</h3>
            <p><strong>予測:</strong> ${pol_pred.label} / <strong>確率:</strong> ${pct(pol_pred.prob)} / <strong>程度:</strong> ${pol_pred.degree}</p>
            <h4>内訳:</h4>
            <ul class="detail-list">
                ${pol_detail.map(d => `<li><span>${d.label}:</span> ${pct(d.prob)} (${d.degree})</li>`).join('')}
            </ul>
        </div>

        <div class="result-section">
            <h3>▼ 感情（8種類）</h3>
            <ul class="detail-list">
                ${emo_detail.map(d => `<li><span>${d.label}:</span> ${pct(d.prob)} (${d.degree})</li>`).join('')}
            </ul>
        </div>
    `;

    resultArea.innerHTML = htmlContent;
    resultArea.scrollIntoView({ behavior: 'smooth' });
}

/** エラーメッセージを表示する共通関数 */
function displayError(message) {
    resultArea.innerHTML = `<p style="color: red;">${message}</p>`;
    resultArea.scrollIntoView({ behavior: 'smooth' });
}