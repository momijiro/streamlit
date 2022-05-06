# 0.import
from cgitb import text
import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import time

st.title('My app')
st.write('DataFrame')

# 1.基本的な使い方
# 1.1 df
df = pd.DataFrame(
    np.random.rand(20, 3),
   columns = ['a', 'b', 'c']
    )

# st.write(df)
# st.dataframe(df.style.highlight_max(axis=1), width=200, height=200)
# st.table(df)

# 1.2 markdown
# """
# # 章
# ## 節
# ### 項
# ```python
# import streamlit as st
# ```
# """

# 1.3 plot
# st.line_chart(df)
# st.area_chart(df)
# st.bar_chart(df)

# 1.4 map
# df = pd.DataFrame(
#     np.random.rand(100, 2)/[50,50] + [35.69, 139.70],
#     columns = ['lat', 'lon']
#     )
# st.map(df)

# 1.5 image
# img = Image.open('sample.jpg')
# st.image(img, caption='pen')

# 2.インタラクティブ(動的)な操作
# 2.1 checkboc
# if st.checkbox('show Image'):
#     img = Image.open('sample.jpg')
#     st.image(img, caption='pen', use_column_width=True)

# 2.2 select box
# option = st.selectbox(
#     'please enter a favorable number',
#     list(range(1, 11))
# )

# 'あなたの好きな数字は', option, 'です'

# 2.3 enter text
# st.write('Interactive Widgets')
# text = st.text_input(
#     'please enter your hobby')

# 'あなたの趣味は', text, 'です'

# # 2.4 slider
# condition = st.slider('あなたの今の調子は？', 0, 100, 50)

# 'コンディション：', condition

# 3.レイアウト
# 3.1 サイドバー
# ちなみに、ctrl + Dで同じものを選択できる
# text = st.sidebar.text_input('please enter your hobby')
# condition = st.sidebar.slider('あなたの今の調子は？', 0, 100, 50)

# 'あなたの趣味は', text, 'です'
# 'コンディション：', condition

# 3.2 ボタン
# left_column, right_column = st.columns(2)
# button = left_column.button('右カラムに文字を表示する')
# if button:
#     right_column.write('ここは右カラム')

# # 3.3 expander
# expander1 = st.expander('問い合わせ1')
# expander1.write('問い合わせ1の回答')
# expander2 = st.expander('問い合わせ2')
# expander2.write('問い合わせ2の回答')

# 4.プログレスバー
'Start!!'

latest_iteration = st.empty()
bar = st.progress(0) 

for i in range(100):
    latest_iteration.text(f'Iteration {i+1}')
    bar.progress(i + 1)
    time.sleep(0.1)

'Done!!'

# 5.Web上に登録
# 5.1 Stramlit Sharingの登録

