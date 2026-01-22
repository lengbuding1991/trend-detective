import streamlit as st
import requests
import time
from datetime import datetime

# ==========================================
# 1. 页面配置 (必须是第一行代码)
# ==========================================
st.set_page_config(
    page_title="热点侦探 Pro",
    page_icon="🕵️‍♂️",
    layout="centered",  # 居中布局，阅读体验更好
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. 侧边栏装修 (Settings & About)
# ==========================================
with st.sidebar:
    st.header("⚙️ 控制台")
    st.info("当前版本：v2.0 (Pro)")
    
    st.markdown("### 💡 使用指南")
    st.markdown(
        """
        1. 在右侧输入关键词
        2. 点击“开始侦查”
        3. 等待 AI 全网搜索
        4. **下载报告**并分享
        """
    )
    
    st.divider()
    st.caption("Build with ❤️ by 一人AI公司")
    st.caption(f"Today: {datetime.now().strftime('%Y-%m-%d')}")

# ==========================================
# 3. 主界面设计
# ==========================================
st.title("🕵️‍♂️ 全网热点侦探")
st.markdown("#### 🚀 你的私人 AI 商业情报官")

# 搜索框区域
with st.container():
    # 使用表单 (Form) 可以让用户按回车键也能提交，体验更顺滑
    with st.form(key='search_form'):
        col1, col2 = st.columns([4, 1])
        with col1:
            keyword = st.text_input("请输入关键词", placeholder="例如：DeepSeek / 2026年AI趋势 / 美联储降息")
        with col2:
            # 把按钮放低一点，对齐输入框
            st.write("") 
            st.write("") 
            submit_button = st.form_submit_button(label='🚀 开始侦查', use_container_width=True)

# ==========================================
# 4. 核心逻辑 (点击后触发)
# ==========================================
if submit_button:
    if not keyword:
        st.toast("⚠️ 请先输入关键词再点搜索！", icon="⚠️")
    else:
        # 进度条效果
        progress_text = "AI 正在全网搜集情报..."
        my_bar = st.progress(0, text=progress_text)
        
        start_time = time.time()
        
        try:
            # -------------------------------------------------------
            # 【注意】这里记得换回你的 n8n 真实地址
            # -------------------------------------------------------
            n8n_webhook_url = "https://n8n.lbuding.com/webhook/search"
            
            # 模拟一点进度条走动，让用户感觉“正在努力工作”
            for percent_complete in range(100):
                time.sleep(0.01)
                if percent_complete < 60: # 假装走到60%，剩下等接口返回
                    my_bar.progress(percent_complete + 1, text=progress_text)

            # 发送真实请求
            response = requests.post(n8n_webhook_url, json={"keyword": keyword})
            
            # 接口返回后，进度条拉满
            my_bar.progress(100, text="侦查完成！整理报告中...")
            time.sleep(0.5)
            my_bar.empty() # 隐藏进度条

            if response.status_code == 200:
                result = response.json()
                report_content = result.get("report", str(result))
                
                # 计算耗时
                duration = time.time() - start_time
                
                # 成功提示
                st.success(f"✅ 成功生成报告，耗时 {duration:.2f} 秒")

                # === 结果展示区 (使用标签页) ===
                tab1, tab2 = st.tabs(["📄 核心简报", "🔍 原始数据"])
                
                with tab1:
                    st.markdown("---")
                    st.markdown(report_content)
                    st.markdown("---")
                    
                    # === 导出功能 ===
                    # 生成一个文件名
                    file_name = f"{keyword}_report_{datetime.now().strftime('%Y%m%d')}.md"
                    st.download_button(
                        label="📥 下载 Markdown 报告",
                        data=report_content,
                        file_name=file_name,
                        mime="text/markdown",
                        type="primary" # 醒目的按钮颜色
                    )
                    
                with tab2:
                    st.json(result) # 也就是把 JSON 打印出来给极客看
                    
            else:
                st.error(f"❌ 连接工厂失败，状态码: {response.status_code}")
                
        except Exception as e:
            st.error(f"❌ 发生系统错误: {e}")