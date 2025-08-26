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
    
    // FormDataオブジェクトを作成してファイルを追加
    const formData = new FormData();
    formData.append('image_file', selectedFile);

    try {
        const response = await fetch('/analyze_image', {
            method: 'POST',
            body: formData, // FormDataを使う場合、headersは自動で設定される
        });
        if (!response.ok) throw new Error('サーバーエラー');
        const data = await response.json();
        displayResults(data);
    } catch (error) {
        displayError('画像分析中にエラーが発生しました。');
    }
});

// 3. 画像ドロップゾーンのイベント
dropZone.addEventListener('click', () => fileInput.click()); // クリック時にファイル選択ダイアログを開く

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault(); // ブラウザのデフォルト動作を無効化
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

// 4. ファイルインプットの変更イベント
fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        handleFile(fileInput.files[0]);
    }
});


// --- 補助関数 ---

/** ファイルが選択されたときの共通処理 */
function handleFile(file) {
    // 画像ファイルかどうかの簡易チェック
    if (!file.type.startsWith('image/')) {
        displayError('画像ファイルを選択してください。');
        return;
    }
    
    selectedFile = file;

    // 画像プレビューを表示
    const reader = new FileReader();
    reader.onload = () => {
        imagePreviewContainer.innerHTML = `<img src="${reader.result}" alt="選択された画像">`;
    };
    reader.readAsDataURL(file);
    
    // 画像分析ボタンを有効化
    analyzeImageButton.disabled = false;
}

/** 分析結果を表示する共通関数 */
function displayResults(data) {
    if (data.error) {
        displayError(data.error);
        return;
    }
    
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
}

/** エラーメッセージを表示する共通関数 */
function displayError(message) {
    resultArea.innerHTML = `<p style="color: red;">${message}</p>`;
}