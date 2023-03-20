FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN apt-get update && apt-get install -y unixodbc unixodbc-dev
RUN pip install -r requirements.txt
EXPOSE 80
RUN mkdir ~/.streamlit
RUN cp config.toml ~/.streamlit/config.toml
RUN cp credentials.toml ~/.streamlit/credentials.toml
WORKDIR /app
ENTRYPOINT ["streamlit", "run"]
CMD ["GBG_Pingis.py"]