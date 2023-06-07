# ConstellationLines Generator v0.1

## 概要

PixInsight (https://pixinsight.com/)のスクリプト AnnotateImage の星座線を好みの繋ぎ方に変更するためのツールです。シンプルに記述できるプレーンテキスト形式の星座線定義ファイルを作成して、このツールで AnnotateImage の設定ファイル(`ConstellationLines.json`)を生成します。既存の設定にある特定の星座の星座線だけを差し替えることもできます。

## 動作環境

Python 3 が動く環境で動作します。以下の環境で動作確認しています。

- Ubuntu 20.04 LTS
- Anaconda 4.12.0
  - python 3.7.13
  - astropy 4.3.1
  - astroquery 0.4.6

## 星座線定義ファイル

星座線定義ファイルは以下のような書式のテキストを UTF-8 エンコーディングで保存したファイルです。

```
# constellation lines in Japan

Cnc:
ι-γ
γ-η-θ-δ-γ
θ-β
δ-α

Gem:
31-24-43-55-78-66-46-27-13-7-1
55-54
46-34
```

- `#` で始まる行はコメントです。
- 空行または空白文字のみからなる行は無視されます。
- 行末が `:` の行は星座の略号(アルファベット3文字)を指定する行です。
  - 以下次の略号の行が出現するまで、ここで指定した略号に対応する星座の星座線の定義になります。
- `-` で区切られた整数またはギリシャ文字からなる行は星座線を表す行です。
  - 各整数またはギリシャ文字は星座線で繋がれる恒星を表します。
  - 整数はフラムスティード番号です。
  - ギリシャ文字はバイエル名です。

## ConstellationLines.json の保存場所

AnnotateImage の星座線設定ファイル `ConstellationLines.json` は以下のディレクトリにあります。

- Linux: /opt/PixInsight/src/scripts/AdP/
- macOS: /Applications/PixInsight/src/scripts/AdP/
- Windows: C:\Program Files\PixInsight\src\scripts\AdP\

ConstellationLines.json はこのツールの出力で上書きされるため、あらかじめオリジナルのファイルをバックアップしておいてください。

また、AnnotateImage がアップデートされると ConstellationLines.json が元に戻る(または新しいバージョンに置き換えられる)可能性があります。ツールが出力した  ConstellationLines.json も必要に応じてバックアップしておいてください。

## 使用方法

### ConstellationLines.json の生成

星座線定義ファイルが `lines.txt`, 出力ファイルが `ConstellationLines.json` の場合、以下のコマンドラインを実行します。

```sh
python clg.py lines.txt ConstellationLines.json
```

この場合、`ConstellationLines.json` の内容はすべて削除され、`lines.txt` で定義した星座線で上書きされます。

既存の `ConstellationLines.json` に `lines.txt` で定義した星座線をマージする場合は `-m` オプションを指定します。

```sh
python clg.py -m lines.txt ConstellationLines.json
```

この場合、`ConstellationLines.json` にあった星座線のうち、`lines.txt` に含まれる星座の線のみが削除され、残った星座線に `lines.txt` で定義した星座線が追加されます。

### 生成した ConstellationLines.json の使用

生成した ConstellationLines.json は上述の保存場所に上書きコピーすると、次の AnnotateImage の実行時から反映されます。PixInsight の再起動は必要ありません。

## ライセンス

MITライセンスです。