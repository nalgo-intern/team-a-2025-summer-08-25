// --- DOM要素の取得 ---
const textInput = document.getElementById('text-input');
const analyzeTextButton = document.getElementById('analyze-text-button');
const resultArea = document.getElementById('result-area');

// 画像関連のDOM要素
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const imagePreviewContainer = document.getElementById('image-preview-container');
const analyzeImageButton = document.getElementById('analyze-image-button');

// グローバル変数で選択されたファイルを保持
let selectedFile = null;

// 表示順を固定するための配列
const emotionOrder = [
    "喜び", "悲しみ", "怒り", "驚き", "恐怖", "嫌悪", "信頼", "期待"
];


// --- イベントリスナーの設定 ---

// 1. テキスト分析ボタンのクリックイベント
analyzeTextButton.addEventListener('click', async () => {
    const inputText = textInput.value;
    if (!inputText.trim()) {
        displayError('文章を入力してください。');
        return;
    }

    textInput.value = '';

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: inputText }),
        });
        if (!response.ok) throw new Error('サーバーエラー');
        const data = await response.json();
        displayResults(data);
    } catch (error) {
        displayError('テキスト分析中にエラーが発生しました。');
    }
});

// 2. 画像分析ボタンのクリックイベント
analyzeImageButton.addEventListener('click', async () => {
    if (!selectedFile) {
        displayError('画像ファイルを選択してください。');
        return;
    }

    // 画像プレビューのsrcを取得
    const previewImageSrc = imagePreviewContainer.querySelector('img')?.src;
    
    // FormDataオブジェクトを作成してファイルを追加
    const formData = new FormData();
    formData.append('image_file', selectedFile);

    // 送信前にUIをリセット
    imagePreviewContainer.innerHTML = '';
    selectedFile = null;
    fileInput.value = ''; // 同じファイルを選択できるようにリセット
    analyzeImageButton.disabled = true;


    try {
        const response = await fetch('/analyze_image', {
            method: 'POST',
            body: formData,
        });
        if (!response.ok) throw new Error('サーバーエラー');
        const data = await response.json();
        displayResults(data, previewImageSrc);
    } catch (error) {
        displayError('画像分析中にエラーが発生しました。');
    }
});

// 3. 画像ドロップゾーンのイベント
dropZone.addEventListener('click', () => fileInput.click());
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) handleFile(files[0]);
});

// 4. ファイルインプットの変更イベント
fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) handleFile(fileInput.files[0]);
});


// --- 補助関数 ---

/** ファイルが選択されたときの共通処理 */
function handleFile(file) {
    if (!file.type.startsWith('image/')) {
        displayError('画像ファイルを選択してください。');
        return;
    }
    selectedFile = file;
    const reader = new FileReader();
    reader.onload = () => {
        imagePreviewContainer.innerHTML = `<img src="${reader.result}" alt="選択された画像">`;
    };
    reader.readAsDataURL(file);
    analyzeImageButton.disabled = false;
}

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
function displayResults(data, imageSrc = null) {
    if (data.error) {
        displayError(data.error);
        return;
    }

    const pol_pred = data.polarity.pred;
    const pol_detail = data.polarity.detail;
    const emo_detail = data.emotion.detail;

    let htmlContent = '<h2>分析結果</h2>';

    if (imageSrc) {
        htmlContent += `<img src="${imageSrc}" alt="分析対象の画像" class="result-image">`;
    }

    htmlContent += `
        <div class="result-section">
            <h3>▼ 入力文</h3>
            <p class="input-text-result">${data.text}</p>
        </div>

        <div class="result-section">
            <h3>▼ 感情（8種類）</h3>
            <ul class="detail-list">
                ${emo_detail.map(d => `<li><span>${d.icon} ${d.ja}:</span> ${pct(d.prob)} (${d.degree})</li>`).join('')}
            </ul>
        </div>

        <div class="result-section">
            <h3>▼ 極性（ネガ・ニュートラル・ポジ）</h3>
            <p><strong>予測:</strong> ${pol_pred.icon} ${pol_pred.ja} / <strong>確率:</strong> ${pct(pol_pred.prob)} / <strong>程度:</strong> ${pol_pred.degree}</p>
            <h4>内訳:</h4>
            <ul class="detail-list">
                ${pol_detail.map(d => `<li><span>${d.icon} ${d.ja}:</span> ${pct(d.prob)} (${d.degree})</li>`).join('')}
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