# studysapuri_skiper

## 目的

[Selenium](https://www.selenium.dev/ja/documentation/) ライブラリを使って [スタサプ](https://studysapuri.jp/) を自動化する試み

## 使用環境

* Win10 Home
* [Google Chrome](https://www.google.com/intl/ja_jp/chrome/) / [Mozilla Firefox](https://www.mozilla.org/ja-jp/firefox/new/)

### 余裕があれば実装する環境

* [Brave](https://brave.com/ja/)
* [Waterfox](https://www.waterfox.net/)
* [Opera](https://www.opera.com/ja)
* [Microsoft Edge](https://www.microsoft.com/ja-jp/edge)
* [Tor browser](https://www.torproject.org/ja/download/)
* [LibreWolf](https://librewolf.net/)


## ライセンス

MIT License

    The MIT License
    Copyright (c) 2023

    以下に定める条件に従い、本ソフトウェアおよび関連文書のファイル（以下「ソフトウェア」）の複製を取得するすべての人に対し、ソフトウェアを無制限に扱うことを無償で許可します。これには、ソフトウェアの複製を使用、複写、変更、結合、掲載、頒布、サブライセンス、および/または販売する権利、およびソフトウェアを提供する相手に同じことを許可する権利も無制限に含まれます。

    上記の著作権表示および本許諾表示を、ソフトウェアのすべての複製または重要な部分に記載するものとします。

    ソフトウェアは「現状のまま」で、明示であるか暗黙であるかを問わず、何らの保証もなく提供されます。ここでいう保証とは、商品性、特定の目的への適合性、および権利非侵害についての保証も含みますが、それに限定されるものではありません。 作者または著作権者は、契約行為、不法行為、またはそれ以外であろうと、ソフトウェアに起因または関連し、あるいはソフトウェアの使用またはその他の扱いによって生じる一切の請求、損害、その他の義務について何らの責任も負わないものとします。

## 下準備

```
pip install selenium
pip install webdriver-manager
```

## システム概要

1. 自動ログイン
   * `.env` ファイルによって設定される ログイン情報 を使ってログインを実行する
2. アクティブな課題の実行
3. 期限切れの課題の実行
4. 半手動で 特定の講座を読み込み再生し続けます。

### 課題の実行

1. 動画を自動再生する
2. 動画の再生終了後ページ遷移する
3. 演習問題は 選択肢をランダムに行います