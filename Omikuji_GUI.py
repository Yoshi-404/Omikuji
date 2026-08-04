import random
import tkinter as tk

def draw_omikuji():
    fortunes = {
        "大吉" : [
            "今日は最高の一日になるでしょう！",
            "あなたの努力が報われる日です。",
            "素晴らしいチャンスが訪れるでしょう。"
        ],
        "吉" : [
            "今日は良い日になるでしょう。",
            "幸運が訪れるかもしれません。",
            "良い結果が得られるでしょう。"
        ],
        "中吉" : [
            "今日は少し運が良い日です。",
            "小さな幸運が訪れるでしょう。",
            "前向きな気持ちで過ごすと良いことがあります。"
        ],
        "小吉" : [
            "今日は普通の日です。",
            "少し注意が必要な日かもしれません。",
            "無理をせず、穏やかに過ごしましょう。"
        ],
        "末吉" : [
            "今日は少し運が悪い日かもしれません。",
            "慎重に行動することが大切です。",
            "小さな困難があるかもしれませんが、前向きに対処しましょう。"
        ],
        "凶" : [
            "今日は注意が必要な日です。",
            "無理をせず、慎重に行動しましょう。",
            "困難なことがあるかもしれませんが、冷静に対処しましょう。"
        ],
        "大凶" : [
            "今日は非常に注意が必要な日です。",
            "無理をせず、慎重に行動しましょう。",
            "困難なことがあるかもしれませんが、冷静に対処しましょう。"
        ]
    }

    result_omikuji = random.choice(list(fortunes.keys()))
    result_message = random.choice(fortunes[result_omikuji])

    # 運勢に合わせた色を決める
    colors = {
        "大吉": "red",      # 赤
        "吉": "orange",     # オレンジ
        "中吉": "green",    # 緑
        "小吉": "blue",     # 青
        "末吉": "purple",   # 紫
        "凶": "gray",       # グレー
        "大凶": "black"     # 黒
    }
    result_color = colors.get(result_omikuji, "black")

    # 画面の文字と色を更新する
    result_label.config(text=f"運勢: {result_omikuji}", fg=result_color)
    message_label.config(text=f"お告げ: {result_message}")

# --- ここからGUI（画面）の設定 ---

# メインウィンドウの作成
root = tk.Tk()
root.title("おみくじアプリ")
root.geometry("600x400") # 画面のサイズ

# タイトルラベル
title_label = tk.Label(root, text="今日のおみくじ", font=("", 16))
title_label.pack(pady=20)

# おみくじを引くボタン
# command=draw_omikuji で、ボタンが押された時に上の関数を呼び出す
draw_button = tk.Button(root, text="おみくじを引く", command=draw_omikuji, font=("", 14))
draw_button.pack(pady=10)

# 結果を表示するラベル
result_label = tk.Label(root, text="運勢: ?", font=("", 24, "bold"), fg="red")
result_label.pack(pady=15)

# メッセージを表示するラベル
message_label = tk.Label(root, text="お告げ: ...", font=("", 14))
message_label.pack(pady=5)

# アプリを起動して画面を表示し続ける
if __name__ == "__main__":
    root.mainloop()