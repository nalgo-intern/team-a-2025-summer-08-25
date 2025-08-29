# メッセージの感情評価アプリケーション

## 目的
SNSのメッセージでは、意図せず自分の想定と異なる印象を与えてしまうことがある。  
こういった事態を避けるために、本プロジェクトでは **テキストおよび画像内の文章から感情と極性を分析** し、  
その結果を **Web上で分かりやすく可視化するシステム** を構築した。


## 実行環境

- Python 3.9.5
- 依存ライブラリは `requirements.txt` に記載
- 以下のコマンドでアプリを起動可能:

pip install -r requirements.txt
python app.py



## お借りしたデータ
- [LoneWolfgang/bert-for-japanese-twitter-sentiment](https://huggingface.co/LoneWolfgang/bert-for-japanese-twitter-sentiment)
- [Mizuiro-sakura/luke-japanese-large-sentiment-analysis-wrime](https://huggingface.co/Mizuiro-sakura/luke-japanese-large-sentiment-analysis-wrime)  
- 東北大学 乾・岡崎研究室. [日本語評価極性辞書](https://www.cl.ecei.tohoku.ac.jp/Open_Resources-Japanese_Sentiment_Polarity_Dictionary.html)

## 参考文献
- 小林のぞみ，乾健太郎，松本裕治，立石健二，福島俊一. 意見抽出のための評価表現の収集. 自然言語処理，Vol.12, No.3, pp.203-222, 2005.  
  *Nozomi Kobayashi, Kentaro Inui, Yuji Matsumoto, Kenji Tateishi. Collecting Evaluative Expressions for Opinion Extraction, Journal of Natural Language Processing 12(3), 203-222, 2005.*

- 東山昌彦, 乾健太郎, 松本裕治. 述語の選択選好性に着目した名詞評価極性の獲得. 言語処理学会第14回年次大会論文集, pp.584-587, 2008.  
  *Masahiko Higashiyama, Kentaro Inui, Yuji Matsumoto. Learning Sentiment of Nouns from Selectional Preferences of Verbs and Adjectives, Proceedings of the 14th Annual Meeting of the Association for Natural Language Processing, pp.584-587, 2008.*
