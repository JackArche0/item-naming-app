import streamlit as st
import pandas as pd
from PIL import Image
import openai
import os

openai.api_key = st.secrets["OPENAI_API_KEY"]

def generate_name(description):
    prompt = f"""
ゲームに登場するアイテムアイコンにふさわしい名前を考えてください。
以下はそのアイコンの説明（中国語）です：
「{description}」

この説明に基づいて、ゲーム内で使われるような日本語のアイテム名を1つ作成してください。
名前は**漢字・ひらがな・カタカナ**を使って構成してください。
ファンタジー的な雰囲気があって、覚えやすく、ユニークなものにしてください。
英語やローマ字は使わないでください。
"""
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50,
        temperature=0.9
    )
    return response['choices'][0]['message']['content'].strip()

st.title("ゲームアイテム名 自動生成ツール")

uploaded_file = st.file_uploader("Excelファイルをアップロード（画像パスと中国語説明）", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    if "画像パス" not in df.columns or "説明" not in df.columns:
        st.error("列名は『画像パス』と『説明』である必要があります。")
    else:
        names = []
        for idx, row in df.iterrows():
            description = row["説明"]
            name = generate_name(description)
            names.append(name)

        df["生成された名前"] = names
        st.dataframe(df)

        output_file = "output_with_names.xlsx"
        df.to_excel(output_file, index=False)
        with open(output_file, "rb") as f:
            st.download_button("生成結果をダウンロード", f, file_name=output_file)
