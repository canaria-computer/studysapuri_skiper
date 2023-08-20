# studysapuri_skiper

## 目的

[Selenium](https://www.selenium.dev/ja/documentation/) ライブラリを使って [スタサプ](https://studysapuri.jp/) を自動化する試み

## 使用環境

* Win10 Home
* [Google Chrome](https://www.google.com/intl/ja_jp/chrome/) / [Mozilla Firefox](https://www.mozilla.org/ja-jp/firefox/new/)

## 簡易アプリケーション

ブックマークウォレットして コードを公開します。
ブックマークに 分かりやすい名前を付けてリンク先に以下のコードを記述します。

すべての選択肢をランダムに選ぶ

```javascript
javascript:Array.from(document.querySelectorAll(`button[class^="QuizDropdown"]`)).sort((a,b)=>Math.random()-Math.random()).forEach(el=>el.click());document.querySelector(`button[class^="RaisedButton"]`).click();
```

### ブックマークウォレットに関わる問題FAQ

#### Q.確かにコピーしましたが張り付けることができません

A.リンク先に最初`//`を入力した後に貼り付けます。これは、Webブラウザセキュリティによるものと考えられます。

#### Q.ブックマークバーが表示されない

##### A1-解決策1(ショートカットキー)

`Ctrl` + `Shift` + `B` を同時に押し表示させます。

##### A2-解決策2(ブラウザの設定から)

* Google chrome をお使いの場合 [Google chromeの設定画面 chrome://settings/appearance](chrome://settings/appearance) から [ブックマーク バーを表示する] のトグルスイッチを ON にします。
* Microsoft edge をお使いの場合 [Microsoft edgeの設定画面 edge://settings/appearance](edge://settings/appearance#:~:text=%E7%A7%BB%E5%8B%95%E3%81%97%E3%81%BE%E3%81%99-,%E3%83%84%E3%83%BC%E3%83%AB%20%E3%83%90%E3%83%BC%E3%81%AE%E3%82%AB%E3%82%B9%E3%82%BF%E3%83%9E%E3%82%A4%E3%82%BA,-%E3%82%BF%E3%83%96%E6%93%8D%E4%BD%9C%E3%83%A1%E3%83%8B%E3%83%A5%E3%83%BC)下部にある [お気に入りバーの表示] を [常に表示] に切り替えます。
* Brave をお使いの場合 [Brave の設定画面 brave://settings/appearance](brave://settings/appearance) の [ブックマーク バーを表示する] を [常に表示] に切り替えます。
* Firefox及びWaterfox,Tor browser,LibreWolf など派生ブラウザをお使いの場合 [firefoxのヘルプ](https://support.mozilla.org/ja/kb/bookmarks-toolbar-display-favorite-websites#w_butsukumakutsurubawobiao-shi-matahafei-biao-shi-nisuru)を参考にしてください。

### 余裕があれば実装する環境

* [Brave](https://brave.com/ja/)
* [Waterfox](https://www.waterfox.net/)
* [Opera](https://www.opera.com/ja)
* [Microsoft Edge](https://www.microsoft.com/ja-jp/edge)
* [Tor browser](https://www.torproject.org/ja/download/)
* [LibreWolf](https://librewolf.net/)

## 更新(2023-07-15)

JavaScript ファイルを分離し Selenium から挿入します。
再利用性が高まりました。

JavaScript による自動処理の ボタン連打に緊急停止機能を持たせました。

### 緊急停止

* `F8`key 再開可能な緊急停止
  * 2回押すとプログラムが再開します
  * 一次的な停止はこれを使うことをおすすめします
* `F9`key 手動で コンソールラインから 再呼び出しが必要な停止
  * 処理を完全殺す処理を実行します
  * デバック用として提供しています
  * 再開の必要がないときに使うこともできます

## ライセンス

MIT License

    The MIT License
    Copyright (c) 2023 canaria-computer

    以下に定める条件に従い、本ソフトウェアおよび関連文書のファイル（以下「ソフトウェア」）の複製を取得するすべての人に対し、ソフトウェアを無制限に扱うことを無償で許可します。これには、ソフトウェアの複製を使用、複写、変更、結合、掲載、頒布、サブライセンス、および/または販売する権利、およびソフトウェアを提供する相手に同じことを許可する権利も無制限に含まれます。

    上記の著作権表示および本許諾表示を、ソフトウェアのすべての複製または重要な部分に記載するものとします。

    ソフトウェアは「現状のまま」で、明示であるか暗黙であるかを問わず、何らの保証もなく提供されます。ここでいう保証とは、商品性、特定の目的への適合性、および権利非侵害についての保証も含みますが、それに限定されるものではありません。 作者または著作権者は、契約行為、不法行為、またはそれ以外であろうと、ソフトウェアに起因または関連し、あるいはソフトウェアの使用またはその他の扱いによって生じる一切の請求、損害、その他の義務について何らの責任も負わないものとします。

## 下準備

### モジュールインストール

```shell
pip install selenium
pip install webdriver-manager
pip install python-dotenv
```

### .env ファイルの作成

カレントディレクトリに .env を作成する必要があります。
内容は以下の通り。

```plantext
LOGIN_URL="https://learn.studysapuri.jp/ja/login"
EMAIL_ADDRESS=<Your address>
PASSWORD=<Your password>
```

## 要件

* Mozilla Firefox version 114
* Python 3.11(Python 3.7前後以降で動くはずですがテストはしていません。)

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
