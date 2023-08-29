import pandas as pd
import unicodedata
import re
import numpy as np
import streamlit as st
import glob


st.subheader("医科在宅アプリ")
file_upload = st.file_uploader("厚労省データ", type={"xlsx"})

if st.button("変換スタート"):
    df = pd.read_excel(file_upload, skiprows=3, usecols=[0, 7, 9, 14])  # 要らない行も引数で削除
    df.columns = ["ID", "医療機関名称", "医療機関所在地", "受理記号"]  # カラム名変更（念のため

    df_zaikansinjitu = df[df["受理記号"] == "在緩診実"]
    df_shiensin_1 = df[df["受理記号"] == "支援診１"]
    df_shiensin_2 = df[df["受理記号"] == "支援診２"]
    df_shiensin_3 = df[df["受理記号"] == "支援診３"]
    df_zaiisoukan = df[df["受理記号"] == "在医総管"]
    df_zaisou = df[df["受理記号"] == "在総"]
    df_zaikansinbyou = df[df["受理記号"] == "在緩診病"]
    df_shienbyou1 = df[df["受理記号"] == "支援病１"]
    df_shienbyou2 = df[df["受理記号"] == "支援病２"]
    df_shienbyou3 = df[df["受理記号"] == "支援病３"]

    df_test = pd.DataFrame(
        {"ID": [0], "医療機関名称": ["テスト"], "医療機関所在地": ["テスト"], "受理記号": ["〇"]},
    )

    df_zaikansinjitu = pd.concat([df_zaikansinjitu, df_test])

    df_shiensin_1 = pd.concat([df_shiensin_1, df_test])
    df_1 = pd.merge(df_zaikansinjitu, df_shiensin_1, on="ID", how="outer")
    df_1["導入_flag"] = df_1["医療機関名称_x"].isna()

    ##名称と住所をインポート
    query_str = "導入_flag == 1"
    df_subset = df_1.query(query_str)
    df_1.loc[df_subset.index, "医療機関名称_x"] = df_1["医療機関名称_y"]
    df_1.loc[df_subset.index, "医療機関所在地_x"] = df_1["医療機関所在地_y"]
    df_1.drop(df_1.columns[[4, 5, 7]], axis=1, inplace=True)
    df_1.rename(
        columns={
            "医療機関名称_x": "医療機関名称",
            "医療機関所在地_x": "医療機関所在地",
            "受理記号_x": "在緩診実",
            "受理記号_y": "支援診１",
        },
        inplace=True,
    )

    df_shiensin_2 = pd.concat([df_shiensin_2, df_test])
    df_2 = pd.merge(df_1, df_shiensin_2, on="ID", how="outer")
    df_2["導入_flag"] = df_2["医療機関名称_x"].isna()
    query_str = "導入_flag == 1"
    df_subset = df_2.query(query_str)
    df_2.loc[df_subset.index, "医療機関名称_x"] = df_2["医療機関名称_y"]
    df_2.loc[df_subset.index, "医療機関所在地_x"] = df_2["医療機関所在地_y"]
    df_2.drop(df_2.columns[[5, 6, 8]], axis=1, inplace=True)
    df_2.rename(
        columns={"医療機関名称_x": "医療機関名称", "医療機関所在地_x": "医療機関所在地", "受理記号": "支援診２"},
        inplace=True,
    )
    df_shiensin_3 = pd.concat([df_shiensin_3, df_test])
    df_3 = pd.merge(df_2, df_shiensin_3, on="ID", how="outer")
    df_3["導入_flag"] = df_3["医療機関名称_x"].isna()
    query_str = "導入_flag == 1"
    df_subset = df_3.query(query_str)
    df_3.loc[df_subset.index, "医療機関名称_x"] = df_3["医療機関名称_y"]
    df_3.loc[df_subset.index, "医療機関所在地_x"] = df_3["医療機関所在地_y"]
    df_3.drop(df_3.columns[[6, 7, 9]], axis=1, inplace=True)
    df_3.rename(
        columns={"医療機関名称_x": "医療機関名称", "医療機関所在地_x": "医療機関所在地", "受理記号": "支援診３"},
        inplace=True,
    )

    df_zaiisoukan = pd.concat([df_zaiisoukan, df_test])
    df_4 = pd.merge(df_3, df_zaiisoukan, on="ID", how="outer")
    df_4["導入_flag"] = df_4["医療機関名称_x"].isna()
    query_str = "導入_flag == 1"
    df_subset = df_4.query(query_str)
    df_4.loc[df_subset.index, "医療機関名称_x"] = df_4["医療機関名称_y"]
    df_4.loc[df_subset.index, "医療機関所在地_x"] = df_4["医療機関所在地_y"]
    df_4.drop(df_4.columns[[7, 8, 10]], axis=1, inplace=True)
    df_4.rename(
        columns={"医療機関名称_x": "医療機関名称", "医療機関所在地_x": "医療機関所在地", "受理記号": "在医総管"},
        inplace=True,
    )

    df_zaisou = pd.concat([df_zaisou, df_test])
    df_5 = pd.merge(df_4, df_zaisou, on="ID", how="outer")
    df_5["導入_flag"] = df_5["医療機関名称_x"].isna()
    query_str = "導入_flag == 1"
    df_subset = df_5.query(query_str)
    df_5.loc[df_subset.index, "医療機関名称_x"] = df_5["医療機関名称_y"]
    df_5.loc[df_subset.index, "医療機関所在地_x"] = df_5["医療機関所在地_y"]
    df_5.drop(df_5.columns[[8, 9, 11]], axis=1, inplace=True)
    df_5.rename(
        columns={"医療機関名称_x": "医療機関名称", "医療機関所在地_x": "医療機関所在地", "受理記号": "在総"},
        inplace=True,
    )

    df_zaikansinbyou = pd.concat([df_zaikansinbyou, df_test])
    df_6 = pd.merge(df_5, df_zaikansinbyou, on="ID", how="outer")
    df_6["導入_flag"] = df_6["医療機関名称_x"].isna()
    query_str = "導入_flag == 1"
    df_subset = df_6.query(query_str)
    df_6.loc[df_subset.index, "医療機関名称_x"] = df_6["医療機関名称_y"]
    df_6.loc[df_subset.index, "医療機関所在地_x"] = df_6["医療機関所在地_y"]
    df_6.drop(df_6.columns[[9, 10, 12]], axis=1, inplace=True)
    df_6.rename(
        columns={"医療機関名称_x": "医療機関名称", "医療機関所在地_x": "医療機関所在地", "受理記号": "在緩診病"},
        inplace=True,
    )

    df_shienbyou1 = pd.concat([df_shienbyou1, df_test])
    df_7 = pd.merge(df_6, df_shienbyou1, on="ID", how="outer")
    df_7["導入_flag"] = df_7["医療機関名称_x"].isna()
    query_str = "導入_flag == 1"
    df_subset = df_7.query(query_str)
    df_7.loc[df_subset.index, "医療機関名称_x"] = df_7["医療機関名称_y"]
    df_7.loc[df_subset.index, "医療機関所在地_x"] = df_7["医療機関所在地_y"]
    df_7.drop(df_7.columns[[10, 11, 13]], axis=1, inplace=True)
    df_7.rename(
        columns={"医療機関名称_x": "医療機関名称", "医療機関所在地_x": "医療機関所在地", "受理記号": "支援病１"},
        inplace=True,
    )
    df_shienbyou2 = pd.concat([df_shienbyou2, df_test])
    df_8 = pd.merge(df_7, df_shienbyou2, on="ID", how="outer")
    df_8["導入_flag"] = df_8["医療機関名称_x"].isna()
    query_str = "導入_flag == 1"
    df_subset = df_8.query(query_str)
    df_8.loc[df_subset.index, "医療機関名称_x"] = df_8["医療機関名称_y"]
    df_8.loc[df_subset.index, "医療機関所在地_x"] = df_8["医療機関所在地_y"]
    df_8.drop(df_8.columns[[11, 12, 14]], axis=1, inplace=True)
    df_8.rename(
        columns={"医療機関名称_x": "医療機関名称", "医療機関所在地_x": "医療機関所在地", "受理記号": "支援病２"},
        inplace=True,
    )

    df_shienbyou3 = pd.concat([df_shienbyou3, df_test])
    df_9 = pd.merge(df_8, df_shienbyou3, on="ID", how="outer")
    df_9["導入_flag"] = df_9["医療機関名称_x"].isna()
    query_str = "導入_flag == 1"
    df_subset = df_9.query(query_str)
    df_9.loc[df_subset.index, "医療機関名称_x"] = df_9["医療機関名称_y"]
    df_9.loc[df_subset.index, "医療機関所在地_x"] = df_9["医療機関所在地_y"]
    df_9.drop(df_9.columns[[12, 13, 15]], axis=1, inplace=True)
    df_9.rename(
        columns={"医療機関名称_x": "医療機関名称", "医療機関所在地_x": "医療機関所在地", "受理記号": "支援病３"},
        inplace=True,
    )

    df_9 = df_9.sort_values("ID")
    df_9 = df_9[df_9["ID"] != 0]

    chack_name = df_9["在緩診実"] == "在緩診実"
    if chack_name.sum() > 0:
        df_9["在緩診実"] = df_9["在緩診実"].str.replace("在緩診実", "〇")
    else:
        pass

    chack_name = df_9["支援診１"] == "支援診１"
    if chack_name.sum() > 0:
        df_9["支援診１"] = df_9["支援診１"].str.replace("支援診１", "〇")
    else:
        pass

    chack_name = df_9["支援診２"] == "支援診２"
    if chack_name.sum() > 0:
        df_9["支援診２"] = df_9["支援診２"].str.replace("支援診２", "〇")
    else:
        pass

    chack_name = df_9["支援診３"] == "支援診３"
    if chack_name.sum() > 0:
        df_9["支援診３"] = df_9["支援診３"].str.replace("支援診３", "〇")
    else:
        pass

    chack_name = df_9["在医総管"] == "在医総管"
    if chack_name.sum() > 0:
        df_9["在医総管"] = df_9["在医総管"].str.replace("在医総管", "〇")
    else:
        pass

    chack_name = df_9["在総"] == "在総"
    if chack_name.sum() > 0:
        df_9["在総"] = df_9["在総"].str.replace("在総", "〇")
    else:
        pass

    chack_name = df_9["在緩診病"] == "在緩診病"
    if chack_name.sum() > 0:
        df_9["在緩診病"] = df_9["在緩診病"].str.replace("在緩診病", "〇")
    else:
        pass

    chack_name = df_9["支援病１"] == "支援病１"
    if chack_name.sum() > 0:
        df_9["支援病１"] = df_9["支援病１"].str.replace("支援病１", "〇")
    else:
        pass

    chack_name = df_9["支援病２"] == "支援病２"
    if chack_name.sum() > 0:
        df_9["支援病２"] = df_9["支援病２"].str.replace("支援病２", "〇")
    else:
        pass

    chack_name = df_9["支援病３"] == "支援病３"
    if chack_name.sum() > 0:
        df_9["支援病３"] = df_9["支援病３"].str.replace("支援病３", "〇")
    else:
        pass

    st.download_button(
        label="変換リストCSV",
        data=df_9.to_csv(index=False).encode("utf-8-sig"),
        file_name="ika_list.csv",
        mime="text/csv",
    )
