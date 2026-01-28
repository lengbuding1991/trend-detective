import streamlit as st
import requests
from datetime import datetime

# ==========================================
# 1. 页面配置 & CSS 注入 (整容的核心)
# ==========================================
st.set_page_config(page_title="DeepInsight Pro", page_icon="🦁", layout="wide")

# 自定义 CSS：把 Streamlit 原生的丑头部去掉，增加卡片阴影
st.markdown("""
<style>
    /* 隐藏右上角菜单和页脚 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 全局背景微调 */
    .stApp {
        background-color: #0e1117;
    }
    
    /* 卡片容器样式 */
    .css-card {
        border-radius: 10px;
        padding: 20px;
        background-color: #1e2130;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        margin-bottom: 20px;
        border: 1px solid #303340;
    }
    
    /* 标题样式增强 */
    h1 {
        color: #f0f2f6;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
    }
    
    /* 侧边栏美化 */
    section[data-testid="stSidebar"] {
        background-color: #161924;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 初始化记忆
# ==========================================
if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_report' not in st.session_state:
    st.session_state.current_report = None

# ==========================================
# 3. 侧边栏：极简风格
# ==========================================
with st.sidebar:
    st.markdown("### 🦁 DeepInsight Pro")
    st.caption("Institutional Grade AI Analysis")
    st.markdown("---")
    
    for i, item in enumerate(reversed(st.session_state.history)):
        # 使用 emoji 区分
        if st.button(f"🕒 {item['time']} | {item['keyword']}", key=f"hist_{i}", use_container_width=True):
            st.session_state.current_report = item
            st.rerun()
            
    st.markdown("---")
    if st.button("🗑️ 清空历史", use_container_width=True):
        st.session_state.history = []
        st.session_state.current_report = None
        st.rerun()

# ==========================================
# 4. 主界面：仪表盘布局
# ==========================================

# 顶部标题栏
col_logo, col_input, col_btn = st.columns([1, 4, 1])

with col_logo:
    st.title("🦁") # 用 Emoji 做个简单的 Logo

with col_input:
    keyword = st.text_input("", placeholder="输入代码或关键词 (e.g. Tesla, 存量房贷利率)", label_visibility="collapsed")

with col_btn:
    start_btn = st.button("🚀 深度分析", type="primary", use_container_width=True)

st.markdown("---")

# 逻辑处理
if start_btn and keyword:
    with st.spinner(f"正在穿透全网数据分析【{keyword}】..."):
        try:
            # ---------------------------
            # ⚠️ 记得换成你的 ngrok 地址
            # ---------------------------
            n8n_url = "https://n8n.lbuding.com/webhook/search"
            
            response = requests.post(n8n_url, json={"keyword": keyword})
            if response.status_code == 200:
                result = response.json()
                content = result.get("report", str(result))
                
                # 存入历史
                record = {
                    "keyword": keyword, 
                    "content": content, 
                    "time": datetime.now().strftime("%H:%M")
                }
                st.session_state.history.append(record)
                st.session_state.current_report = record
                st.rerun()
        except Exception as e:
            st.error(f"系统连接中断: {e}")

# ==========================================
# 5. 报告展示区 (卡片式设计)
# ==========================================
if st.session_state.current_report:
    report = st.session_state.current_report
    
    # 使用 HTML 容器模拟卡片效果
    st.markdown(f"""
    <div class="css-card">
        <h2 style="margin-top:0;">📡 {report['keyword']} 深度研报</h2>
        <p style="color:#888;">生成时间: {report['time']} | 数据源: 全网实时检索</p>
    </div>
    """, unsafe_allow_html=True)

    # 左右分栏：左边主要内容，右边可以放（假装的）指标
    main_col, metric_col = st.columns([3, 1])
    
    with main_col:
        st.markdown(report['content'])
    
    with metric_col:
        # 这里为了美观，我们加几个“装饰性”的指标卡片
        # 未来你可以让 n8n 真的返回这些数字
        st.markdown('<div class="css-card"><h5>🔥 市场热度</h5><h2>High</h2></div>', unsafe_allow_html=True)
        st.markdown('<div class="css-card"><h5>⚖️ 情绪倾向</h5><h2 style="color:#4caf50;">Neutral</h2></div>', unsafe_allow_html=True)
        
        st.download_button(
            "📥 导出 PDF (Markdown)",
            data=report['content'],
            file_name=f"{report['keyword']}_report.md",
            mime="text/markdown",
            use_container_width=True
        )

else:
    # 空状态页
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 50px;">
        <h3>👋 欢迎回到指挥中心</h3>
        <p>输入关键词，启动 AI 投资分析引擎</p>
    </div>
    """, unsafe_allow_html=True)
