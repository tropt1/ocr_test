import streamlit as st
import easyocr
import cv2
import numpy as np

from PIL import Image
from PIL import ImageDraw


def draw_boxes(image, bounds, color='yellow', width=2):
    image = Image.open(image)

    draw = ImageDraw.Draw(image)

    for bound in bounds:
        p0, p1, p2, p3 = bound[0]
        draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)

    return st.image(image)


if __name__ == '__main__':
    st.markdown('''<h1 style='text-align: center; color: white;'>
                Распознавание текста на изображениях by Sysoeva Daria</h1>''',
                unsafe_allow_html=True)

    languages = ['ar', 'az', 'be', 'bg', 'ch_tra', 'che', 'cs', 'de', 'en', 'es',
                 'fr', 'hi', 'hu', 'it', 'ja', 'la', 'pl', 'ru', 'tr', 'uk', 'vi']

    choose_lang = st.multiselect('Выберите язык для распознавания:', languages)
    uploaded_img = st.file_uploader("Ниже загрузите изображение с текстом", type=['jpg', 'jped', 'png'])

    if uploaded_img is not None:
        st.image(uploaded_img, use_column_width='auto', caption=f'Загруженное изображение {uploaded_img}')
        file_bytes = np.asarray(bytearray(uploaded_img.read()), dtype=np.uint8)
        bytearray_img = cv2.imdecode(file_bytes, 1)

    if st.button('Распознать текст с загруженного изображения'):

        if not choose_lang or not uploaded_img:

            st.write('_Обработка приостановлена: загрузите изображение и/или выберите язык для распознавания._')

        else:
            reader = easyocr.Reader(choose_lang)
            bounds = reader.readtext(bytearray_img)
            draw_boxes(uploaded_img, bounds)

            result = reader.readtext(bytearray_img, detail=0, paragraph=True)

            st.markdown('#### Распознанный текст:')

            for string in result:
                st.write(string)

            result_as_str = ' '.join(result)

            st.download_button(label='Загрузить результат в формате txt', data=result_as_str,
                               file_name='SysoevaProject.txt', mime='text/csv')
