# ジャパンオープン2026（50m）エントリー確認

2026年12月4日(金)〜6日(日)・東京アクアティクスセンター。
日本水泳連盟が公開したエントリー受付情報（2026/11/21 11:43 時点・更新版）をもとにした非公式の確認アプリです。

- 選手・チーム検索／種目別一覧（公式エントリーランキング順）／リレー／鹿児島タブ／日程・標準記録
- `index.html` 1ファイルで動作します
- 正式な内容は必ず公式PDFでご確認ください: https://aquatics.or.jp/tournament/57943/

## 表示・検索の修正（2026-11-24）

- 320px／375px向けに種目カードの氏名・記録を上下へ配置。操作領域は48px以上。
- 男女の指定色・左5pxラインと男女別名簿を選手、種目、リレー、鹿児島に適用。
- リレーは団体数と延べエントリー件数を分けて表示。
- 男子800m／女子1500m自由形は他種目の標準記録による参加条件を表示。
- 検索専用の漢字読み候補を追加。候補は公式ふりがなではなく、画面には表示しません。
- Abacusの大会専用名前空間で閲覧数を表示。同じブラウザでは日本時間で1日1回、公開ページでのみ加算します。

### 検索用辞書の帰属と再生成

[Electronic Dictionary Research and Development Group (EDRDG)](https://www.edrdg.org/) の
[KANJIDIC2](https://www.edrdg.org/wiki/index.php/KANJIDIC_Project) を利用しています。
辞書由来の `KANJI_READINGS` データは [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) です。
本アプリで使用する漢字のみ抽出し、仮名の正規化・連濁・促音の候補を加え、1文字の名乗り読みは除外しています。

再生成: `python3 tools/build-kana.py /path/to/kanjidic2.xml.gz`
