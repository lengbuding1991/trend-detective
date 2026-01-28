import streamlit as st
import requests
import time
from datetime import datetime

# ==========================================
# 1. 页面配置 & 记忆初始化
# ==========================================
st.set_page_config(
    page_title="热点侦探 V3.0",
    page_icon="🧠",
    layout="wide",  # 宽屏模式，看报告更舒服
    initial_sidebar_state="expanded"
)

# --- 核心：初始化“记忆” ---
# 如果这是用户第一次打开，先给他个空的笔记本
if 'history' not in st.session_state:
    st.session_state.history = [] 

if 'current_report' not in st.session_state:
    st.session_state.current_report = None

# ==========================================
# 2. 侧边栏：历史记录控制台
# ==========================================
with st.sidebar:
    st.title("🧠 侦探记忆库")
    st.caption("本次会话的历史查询")
    
    # 遍历历史记录，生成按钮
    # reversed() 是为了让最新的记录排在最上面
    for i, item in enumerate(reversed(st.session_state.history)):
        col_btn, col_time = st.columns([3, 1])
        # 如果点击了某个历史关键词
        if st.button(f"📄 {item['keyword']}", key=f"history_{i}", use_container_width=True):
            st.session_state.current_report = item # 把当年的报告调出来
            st.rerun() # 重新刷新页面显示

    st.divider()
    
    # 清空按钮
    if st.button("🗑️ 清空记忆", type="primary"):
        st.session_state.history = []
        st.session_state.current_report = None
        st.rerun()

# ==========================================
# 3. 主界面逻辑
# ==========================================
st.title("🕵️‍♂️ 全网热点侦探 (记忆版)")

# --- 搜索区 ---
with st.container():
    col1, col2 = st.columns([5, 1])
    with col1:
        # 如果是从历史记录点的，自动填入关键词
        default_kw = st.session_state.current_report['keyword'] if st.session_state.current_report else ""
        keyword = st.text_input("输入关键词", value=default_kw, placeholder="例如：2026年养老金政策 / 英伟达财报")
    with col2:
        st.write("") 
        st.write("") 
        start_btn = st.button("🚀 新侦查", type="primary", use_container_width=True)

# --- 核心处理逻辑 ---
if start_btn and keyword:
    # 进度条
    progress_text = f"正在全网搜查关于【{keyword}】的情报..."
    my_bar = st.progress(0, text=progress_text)
    
    try:
        # -------------------------------------------------------
        # 【请修改】这里填你那个能用的 ngrok 地址
        # -------------------------------------------------------
        n8n_webhook_url = "https://n8n.lbuding.com/webhook/search"
        
        # 模拟进度
        for percent in range(60):
            time.sleep(0.01)
            my_bar.progress(percent + 1, text=progress_text)

        # 发送请求
        response = requests.post(n8n_webhook_url, json={"keyword": keyword})
        
        if response.status_code == 200:
            my_bar.progress(100, text="报告生成完毕！")
            result = response.json()
            report_content = result.get("report", str(result))
            
            # --- 关键步骤：存入记忆 ---
            # 把这次成功的报告，打包存进 session_state
            record = {
                "keyword": keyword,
                "content": report_content,
                "time": datetime.now().strftime("%H:%M:%S"),
                "raw": result
            }
            st.session_state.history.append(record)
            st.session_state.current_report = record # 设为当前显示
            
            time.sleep(0.5)
            my_bar.empty()
            st.rerun() # 刷新页面展示结果
            
        else:
            st.error(f"工厂报错: {response.status_code}")
            
    except Exception as e:
        st.error(f"连接错误: {e}")

# ==========================================
# 4. 报告展示区
# ==========================================
if st.session_state.current_report:
    data = st.session_state.current_report
    
    st.divider()
    st.markdown(f"### 📊 关于 “{data['keyword']}” 的侦查简报")
    st.caption(f"生成时间: {data['time']}")
    
    tab1, tab2 = st.tabs(["精读简报", "原始数据"])
    
    with tab1:
        st.markdown(data['content'])
        
        # 导出功能
        st.download_button(
            label="📥 下载当前报告",
            data=data['content'],
            file_name=f"{data['keyword']}_report.md",
            mime="text/markdown"
        )
        
    with tab2:
        st.json(data['raw'])

else:
    # 还没搜索时的欢迎页
    st.info("👈 左侧是你的历史记录，上方输入关键词开始新的侦查。")
