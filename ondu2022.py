import streamlit as st
import numpy as np
import pandas as pd
import datetime
import os
import base64
import io
import openpyxl

def dt_change(dt):
  return '{:0=4}{:0=2}{:0=2}'.format(dt.year, dt.month, dt.day)
now = datetime.datetime.now()
end = dt_change(now)

def BEFORE14(dt):
  dt_ = f'{dt[0:4]}-{dt[4:6]}-{dt[6:8]}'
  dt_ = datetime.datetime.strptime(dt_, '%Y-%m-%d')
  return dt_ - datetime.timedelta(days=13)
  
def dt_change2(dt):
  return '{}/{}'.format(dt.month, dt.day)

def data_shaping(df): 
  # カラムを限定
  df_ = df[["'氏名'", "'日付・時刻'", "'体温(体調情報)'"]]
  
  # カラムの名前を変更
  df_ = df_.rename(columns={"'氏名'":"氏名", 
          "'日付・時刻'":"日付",
          "'体温(体調情報)'":"体温"})
  
  #日付型に変更
  df_['日付'] = pd.to_datetime(df_['日付'])
  # 日付を直近14日に限定
  df_ = df_[df_['日付'] >= BEFORE14(end)]

  # 日付をわかりやすい形に変換
  f = lambda x: str(x.month) + '/' + str(x.day)
  df_['日付'] = df_['日付'].map(f)

  # 引用符をなくす
  for c in ['氏名', '体温']:
    df_[c] = df_[c].str[1:-1]
      
  return df_.reset_index(drop=True)

def data_merging(df3, df4):
    for i in df4['氏名'].unique():
        if i in df3['氏名'].unique():
            df4 = df4[df4['氏名']!=i]
    return pd.concat([df3, df4])

# 1年生：
year1 =[
'天野 聖乃',
'丸山 幸恵',
'渡部 雪歩',
'野地 志織',
'大塚 菜々美',
# 1年生(前期のみ)
'Laura Susanne Klug', 
'イーゼンベルク ザブリーナ',]
# 2年生:
year2 = [
'笹子 恵利',
'大田 小夏',
'牧本 武蔵',
'角 晴香',
'小山 杏奈',
'山地 沙蘭',
'水谷 文音',
'荻 真優子',
'朱 博瑄',
'梶原 城太',
# '藤枝 美帆',
'吉永 晴香',
'北野 志保',
# '近藤 彩加',
# '長谷川 紗希',
'谷渕 晴哉',
'櫻井 俊太郎']
# 3年生:
year3 = [
'佐久間 悠斗',
'車谷 郁実',
'田嶋 悠楽々',
'青木 日花',
'村崎 咲良',
'鴻巣 遥香',
'米谷 はづき',
'小泉 ときわ',
'天草 萌々',
'高柳 菜月',
'西村 篤朗',
'星野 明日美',
'齊藤 由理',
'佐光 未帆',
'加藤 大輝',
'萩原 怜央',
'花井 菜々子',
# '水野 隼',
# '寄川 淳聖',
]
# 4年生 
year4 = [
# '大竹 叶望',
'春日 崇伸',
'片岡 弓澄',
# '川邊 笑',
# '黒川 夕鶴',
'小林 優太',
'齋藤 真衣子',
# '櫻井 藍花里',
'佐藤 綾香',
# '佐藤 由',
# '塩入 翔也',
'下仲 咲穂',
'島 沙也加',
# '田岡 佑基',
# '谷口 萌',
'戸井田 風音',
'中西 映人',
'原田 秦冴',
'細谷 なつみ',
# '眞鍋 礼子',
]
# 院1年
grad = [
# '大坂 実旺',
# '小澤 政貴',
# '加来 祐子',
'齋藤 亘佑',
# '孫 辰希',
# '田中 大輔',
# '鍋山 雄樹',
# '本田 拓海',

# 院2年:4(累計65)
'川端 航平',
'二宮 功伎',
'吉澤 秀俊',
]
# 社会人さん
social = [
# '澁澤 薫',
'小澤 政貴',
'若木 良太',
'赤根 大介',
'赤根 たか子',
# '赤根 寛',
'井上 百合子',
'加園 真愛',
# '後坊 健太',
'齊藤 憲二',
# '齊藤 裕希也',
'佐藤 恵美子',
'鈴木 悠斗',
'中村 雅子',
'中村 公祐',
'坂東 香代子',
'坂東 正樹',
'松本 朔弥',
'安田 清美',
'飯村 良枝',
'土井原 良美',
'宮澤 美幸',
'北條 海織',
# 'Sesso Bruno',
]

members = year1+year2+year3+year4+grad+social

def name_day(df, members=members):  
  # 日付一覧
  days = [d for d in df['日付'].unique()]

  A = pd.DataFrame(index=members, columns=days)
  A.insert(0, '未記録数','')
  A.insert(0, '属性','')
  
  # 37.5度以上あったら★を付ける
  f = lambda x: '★'+x if float(x) > 37.4 else x
  for m in members:
    df_m = df[df['氏名']==m]
    df_m.loc[:,'体温'].map(f)

    n = 0
    for d in days:
      day_data = df_m[df_m['日付']==d]

      # 一日に複数回入れている場合を削除
      if len(day_data) > 1:
        day_data = day_data.iloc[-1:]
      
      if day_data.empty is False:
        A.loc[m][d] = day_data.iloc[0]['体温']
        n += 1

    # 未記録数
    # if n ==14: A.at[m, '未記録数'] = '〇'
    # else:      
    A.at[m, '未記録数'] = 14-n

    # 属性
    if   m in year1: A.at[m, '属性'] = '筑波大1年'
    elif m in year2: A.at[m, '属性'] = '筑波大2年'
    elif m in year3: A.at[m, '属性'] = '筑波大3年'
    elif m in year4: A.at[m, '属性'] = '筑波大4年'
    elif m in grad : A.at[m, '属性'] = '筑波大院生'
    else:            A.at[m, '属性'] = '社会人' 

  return A

atts = ['筑波大1年', '筑波大2年', '筑波大3年', '筑波大4年', '筑波大院生', '社会人']
atts_ = ['1年', '2年', '3年', '4年', '院生', '社会人さん']

zero = []
def attr(i):
  a = atts[i]
  a_ = atts_[i]
  B2 = B[B['属性']==a]
  lst1 = []
  lst2 = []
  for i in B2.index:
    if B2.at[i, '未記録数'] == 0:
      lst1.append(i)
    elif B2.at[i, '未記録数'] == 14:
      zero.append(i)
    else: 
      b = B2.at[i, '未記録数']
      lst2.append(f'{i}({b})')

  txt1 = f"【{a_}({len(lst1)})】{', '.join(lst1)}"
  txt2 = f"【{a_}({len(lst2)})】{', '.join(lst2)}"
  
  if len(lst1) == len(B2):
    txt1 = f"【{a_} 全員】"

  return txt1, txt2

def text1():
  for txt in can:
    st.write(txt)
  st.write()
  st.write('今日の名簿です。検温の記入漏れ等ありましたらご連絡ください。')

def text2():
  # st.write('出してない人リスト')
  st.write()
  for txt in cant:
    st.write(txt)
  st.write()
  st.write('【2週間1回も出していない人リスト】')
  st.write(', '.join(zero))

def download():
  towrite = io.BytesIO()
  downloaded_file = A.to_excel(towrite, encoding='utf-8', index=True, header=True) # write to BytesIO buffer
  towrite.seek(0)  # reset pointer
  b64 = base64.b64encode(towrite.read()).decode() 
  linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="斬桐舞体温記録_{end}.xlsx">ファイルをダウンロード</a>'
  st.markdown(linko, unsafe_allow_html=True)     



# MAIN
st.title("OND'U管理")

if st.checkbox('日付を入力する(自動でうまくいかないとき)'):
    end = st.text_input('今日の日付を入力して下さい (例：20211107)')

"ファイルをアップロードしてください"
file1 = st.file_uploader("【筑波大学　斬桐舞】", type='csv') 
file2 = st.file_uploader("【つくば　斬桐舞】", type='csv') 


if file1 is not None:
    if file2 is not None:
        "ファイルのアップロードが完了しました"
        st.write('-'*50)
        st.write('しばらくお待ちください')
        bar = st.progress(0) 
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)
        df3 = data_shaping(df1)
        df4 = data_shaping(df2)
        df5 = data_merging(df3, df4)
        bar.progress(50)
        A = name_day(df5, members=members)

        B = A.iloc[:, :2]
        y1, y1_ = attr(0)
        y2, y2_ = attr(1)
        y3, y3_ = attr(2)
        y4, y4_ = attr(3)
        gr, gr_ = attr(4)
        so, so_ = attr(5)
        can  = [y1, y2, y3, y4, gr, so]
        cant = [y1_, y2_, y3_, y4_, gr_, so_]

        st.write('-'*50)
        text1()
        st.write('-'*50)
        bar.progress(100)

        button1 = st.button('出してない人リストを表示する')
        if button1:
          text2()
        st.write('-'*50)

        button2 = st.button('Excelデータを出力する')
        if button2:
          download()
          st.write('ファイルの出力が完了しました')


        

