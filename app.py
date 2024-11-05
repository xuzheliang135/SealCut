import streamlit as st
from PIL import Image
import os
from seal_processor import process_seal_complete

def reset_state():
    """重置所有状态"""
    st.session_state.processed = False
    st.session_state.result = None
    if 'last_uploaded_file' in st.session_state:
        del st.session_state.last_uploaded_file

def main():
    st.title("印章图片处理工具")
    st.write("上传一张带有印章的图片，自动提取印章")

    # 初始化 session_state
    if 'processed' not in st.session_state:
        st.session_state.processed = False
    if 'result' not in st.session_state:
        st.session_state.result = None

    # 文件上传
    uploaded_file = st.file_uploader("选择图片文件", type=['png', 'jpg', 'jpeg'], on_change=reset_state)
    
    if uploaded_file is not None:
        # 显示原始图片
        st.subheader("原始图片")
        image = Image.open(uploaded_file)
        st.image(image, caption="上传的图片")
        
        # 处理按钮
        if st.button("开始处理") or st.session_state.processed:
            if not st.session_state.processed:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                with st.spinner("正在处理中..."):
                    try:
                        # 创建临时文件夹
                        temp_dir = "temp_results"
                        if not os.path.exists(temp_dir):
                            os.makedirs(temp_dir)
                        else:
                            # 清理临时文件
                            for file in os.listdir(temp_dir):
                                os.remove(os.path.join(temp_dir, file))
                        
                        progress_bar.progress(30)
                        status_text.text("正在保存上传文件...")
                        
                        # 保存上传文件
                        input_path = os.path.join(temp_dir, "input.png")
                        image.save(input_path)
                        
                        progress_bar.progress(60)
                        status_text.text("正在处理图片...")
                        
                        # 处理图片
                        process_seal_complete(input_path, temp_dir)
                        
                        # 保存结果到 session_state
                        st.session_state.result = Image.open(os.path.join(temp_dir, "extracted_seal.png"))
                        st.session_state.processed = True
                        
                        progress_bar.progress(100)
                        status_text.text("处理完成！")
                        
                    except Exception as e:
                        st.error(f"处理出错：{str(e)}")
                        reset_state()
                    finally:
                        progress_bar.empty()
                        status_text.empty()
            
            # 显示处理结果
            if st.session_state.processed and st.session_state.result:
                st.subheader("处理结果")
                st.image(st.session_state.result, caption="提取的印章")
                
                # 下载按钮
                result_path = os.path.join("temp_results", "extracted_seal.png")
                with open(result_path, "rb") as file:
                    btn = st.download_button(
                        label="下载处理结果",
                        data=file,
                        file_name="extracted_seal.png",
                        mime="image/png"
                    )

if __name__ == "__main__":
    main()