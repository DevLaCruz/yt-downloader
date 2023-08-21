import os
import streamlit as st
from pytube import YouTube

# Función para descargar el video
@st.cache(allow_output_mutation=True)
def download_video(video_url, selected_stream):
    try:
        yt = YouTube(video_url)
        video_stream = yt.streams.get_by_itag(selected_stream.itag)

        download_path = os.path.expanduser("~") + os.path.sep + "Downloads"
        video_stream.download(output_path=download_path)
        return download_path, yt.thumbnail_url
    except Exception as e:
        return None, None

def main():
    st.title("YouTube Video Downloader")

    # Crear un input para ingresar la URL del video
    video_url = st.text_input("Ingresa la URL del video de YouTube")

    if video_url:
        selected_stream = None

        try:
            yt = YouTube(video_url)
            st.image(yt.thumbnail_url, caption="Miniatura del video")

            # Obtener las resoluciones disponibles
            video_streams = yt.streams.filter(file_extension="mp4").order_by("resolution").desc()

            # Crear un select para elegir la calidad del video
            video_qualities = [f"{stream.resolution}" for stream in video_streams]
            selected_quality = st.selectbox("Selecciona la calidad del video:", video_qualities)

            selected_stream = video_streams[video_qualities.index(selected_quality)]

        except Exception as e:
            st.error("Ocurrió un error: " + str(e))

        if selected_stream and st.button("Descargar"):
            download_path, thumbnail_url = download_video(video_url, selected_stream)

            if download_path:
                st.success("Descarga completada. El video se encuentra en: " + download_path)
                st.markdown(f"**[Descargar aquí]({download_path})**")
            else:
                st.error("Ocurrió un error durante la descarga.")

if __name__ == "__main__":
    main()
