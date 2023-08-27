# コーディングルール

このプロジェクトでのコーディングルールは特にありません。

docstring は Googleスタイル それ以外は標準ルールへ従う必要があります。

コーダーのにより適合しないことも許されています。

きれいなコードは見やすいのでフォーマットをお願いします。

```shell
black --ipynb dev.ipynb
isort .
pnpm fix
```

## フォーマットツールインストール

```sehll
pip install black
pip install "black[jupyter]"
pip install isort
```

JavaScript の 依存関係は `package.json` に記載されています。

```shell
pnpm i
```
