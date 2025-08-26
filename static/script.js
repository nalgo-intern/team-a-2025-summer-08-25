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
        resultArea.innerHTML = ''; 
        let htmlContent = '<h2>分析結果</h2>';

        if (data["入力された文章"]) {
            htmlContent += `<p><strong>入力された文章:</strong> ${data["入力された文章"]}</p>`;
        }

        emotionOrder.forEach(emotion => {
            if (data.hasOwnProperty(emotion)) {
                htmlContent += `<p><strong>${emotion}:</strong> ${data[emotion]}</p>`;
            }
        });
        
        resultArea.innerHTML = htmlContent;

        resultArea.scrollIntoView({ behavior: 'smooth' });

    } catch (error) {
        console.error('エラー:', error);
        resultArea.innerHTML = `<p style="color: red;">分析中にエラーが発生しました。</p>`;
    }
});