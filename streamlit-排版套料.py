import streamlit as st
import json
import pandas as pd
import random
from streamlit_utils import Rectangle, main_process


# 用于生成矩形数据的函数
def generate_rectangles(width, height, count, rect_type):
    return [{"type": rect_type, "width": width, "height": height} for _ in range(count)]

# 处理数据的函数
def process_rectangles():
    # 简单模拟检测处理逻辑，可以在这里加入复杂算法
    result = main_process(
        sheet_rectangle_config=st.session_state.sheet_rectangles,
        rect_rectangle_config=st.session_state.component_rectangles,
        over_rate=0.5
    )
    return result

st.set_page_config(layout="wide")
# Streamlit 界面布局
st.title("矩形检测系统")

# cache
if 'sheet_rectangles' not in st.session_state:
    st.session_state.sheet_rectangles = []
if 'component_rectangles' not in st.session_state:
    st.session_state.component_rectangles = []
# 配置超投比例
if 'over_rate' not in st.session_state:
    st.session_state.over_rate = 0.03
col1, col2 = st.columns(2)
with col1:
    # 母版矩形输入
    st.header("输入母版矩形的大小和数量")
    master_width = st.number_input("母版矩形宽度", min_value=100)
    master_height = st.number_input("母版矩形高度", min_value=200)
    master_count = st.number_input("母版矩形数量", min_value=5, step=1)

    if st.button("添加母版"):
        st.session_state.sheet_rectangles.append(
            {
                "width": master_width,
                "height": master_height,
                "count": master_count,
                'gap': 0,
                'type': len(st.session_state.sheet_rectangles) + 1,
            }
        )
    if st.button('随机母版'):
        
        st.session_state.sheet_rectangles.append(
            {
                "width": random.randint(100, 300),
                "height": random.randint(200, 700),
                "count": random.randint(1, 10),
                'gap': 0,
                'type': len(st.session_state.sheet_rectangles) + 1,
            }
        )

    # 元件矩形输入
    st.header("输入元件矩形的大小和数量")
    component_width = st.number_input("元件矩形宽度", min_value=5)
    component_height = st.number_input("元件矩形高度", min_value=5)
    component_gap = st.number_input("元件矩形间距", min_value=0.0, step=0.01)
    component_count = st.number_input("元件矩形数量", min_value=10, step=5)
    if st.button("添加元件"):
        st.session_state.component_rectangles.append(
            {
                "width": component_width,
                "height": component_height,
                "gap": component_gap,
                'count': component_count,
                'type': len(st.session_state.component_rectangles) + 1,
            } 
        )
    if st.button('随机元件'):
        st.session_state.component_rectangles.append(
            {
                "width": random.randint(5, 10),
                "height": random.randint(5, 50),
                "gap": 1.6,
                'count': random.randint(100, 200),
                'type': len(st.session_state.component_rectangles) + 1,
            } 
        )

with col2:
    st.subheader("母版信息")
    st.dataframe(pd.DataFrame(st.session_state.sheet_rectangles))
    st.subheader("元件信息")
    st.dataframe(pd.DataFrame(st.session_state.component_rectangles))

# 提交按钮
if st.button("提交检测请求"):
    
    # 处理矩形数据
    result = process_rectangles()
    
    # 显示 JSON 数据
    st.subheader("处理结果")

    for arrs in result:
        # st.json(open(arrs[0], 'r', encoding='utf-8').read())
        st.image(arrs[-1])
        for arr in arrs[1:-1]:
            st.dataframe(pd.read_excel(arr))
    
    # 将 JSON 结果以可读格式显示
    st.subheader("报告")
    st.json(result,)
