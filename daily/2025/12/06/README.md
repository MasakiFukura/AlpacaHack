# Writeup for simpleoverflow

## 概要

スタックバッファオーバーフローにより、隣接する変数を書き換える問題。

## 解析

### フラグ取得条件の確認

cファイルを確認すると、`is_admin`が`TRUE`になればフラグの値が表示されることがわかる。

```c
  if (!is_admin) {
    puts("You are not admin. bye");
  } else {
    system("/bin/cat ./flag.txt");
  }
```

### 書き換え対象の特定

`is_admin`を`TRUE`にする方法を探るため、`is_admin`の変数宣言を確認する。

```c
  char buf[10] = {0};
  int is_admin = 0;
```

`buf`配列の次に`is_admin`が配置されているため、
`buf`をスタックバッファオーバーフローさせ、`is_admin`に0以外を入れれば良いと考えられる。
一般的に`int`が4バイトの環境に配置されるため、アラインメントにより`buf`10バイト + パディング2バイトの後に`is_admin`が置かれている可能性が高い。

### 書き換え方法の特定

`buf`をスタックバッファオーバーフローさせるため、`buf`に値を入力している箇所を探す。

```c
  read(0, buf, 0x10);
```

`buf`は10バイトしか確保されていないにもかかわらず16バイト読み込まれるため、
後続の `is_admin` を上書きできる。

## Exploit

`is_admin`の位置までのオフセットは12バイトと推定されるため、
12バイト分のダミーデータの後に、`is_admin` を上書きする値を書き込むコマンドを用意する。
今回はリトルエンディアンを考慮し、`\x01\x00\x00\x00`とした。
標準入力からペイロードを送り、リモートサーバに接続する。
`python3 -c 'import sys; sys.stdout.buffer.write(b"A"*12 + b"\x01\x00\x00\x00")' | nc 34.170.146.252 36920`
（`nc`以降は`Spawn Challenge Server`にて生成されたものに置き換えること）

## Flag

`ctf4b{0n_y0ur_m4rk}`
