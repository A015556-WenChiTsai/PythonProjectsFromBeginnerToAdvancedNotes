import streamlit as st
import re

# --- 核心邏輯 (完全沒變) ---
def deidentify_logic(report_content):
    patterns = [
        r".{2,3}醫師\(放診專", r"姓名", r"病歷號", r"醫囑醫師",
        r"新光吳火獅紀念醫院", r"病患姓名"
    ]
    ignore_pattern = re.compile("|".join(patterns))
    lines = report_content.splitlines()
    clean_lines = [line for line in lines if not ignore_pattern.search(line)]
    return "\n".join(clean_lines)

# --- 網頁介面 ---
st.title("🏥 病歷報告去識別化工具")
st.write("這是一個基於 Web 的工具，不用擔心 Linux 字型亂碼問題。")

# 建立兩欄版面
col1, col2 = st.columns(2)

with col1:
    req_no = st.text_input("檢查單號 (ExaRequestNo)")
    raw_content = st.text_area("原始報告內容", height=300, placeholder="請在此貼上報告...")

    if st.button("執行去識別化", type="primary"):
        if not raw_content:
            st.warning("請輸入報告內容！")
        else:
            result = deidentify_logic(raw_content)
            # 將結果存入 Session State 以便在右欄顯示
            st.session_state['result'] = result
            st.session_state['req_no'] = req_no

with col2:
    st.subheader("處理結果")
    if 'result' in st.session_state:
        st.text_input("確認單號", value=st.session_state['req_no'], disabled=True)
        st.text_area("去識別化內容", value=st.session_state['result'], height=300)
    else:
        st.info("請在左側輸入資料並點擊執行。")