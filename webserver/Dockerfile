FROM python:3.8.16


WORKDIR /app

COPY ./requirements.txt ./requirements.txt
COPY ./app.py ./app.py

COPY ./templates/create_new_password.html ./templates/create_new_password.html
COPY ./templates/home.html ./templates/home.html
COPY ./templates/login.html ./templates/login.html
COPY ./templates/reset_password_mail.html ./templates/reset_password_mail.html
COPY ./templates/reset_password.html ./templates/reset_password.html

COPY ./static/img/applausi.gif ./static/img/applausi.gif
COPY ./static/img/logo.png ./static/img/logo.png

COPY ./static/styles/bootstrap.min.css ./static/styles/bootstrap.min.css
COPY ./static/styles/bootstrap.min.css.map ./static/styles/bootstrap.min.css.map
COPY ./static/styles/bootstrap.rtl.min.css ./static/styles/bootstrap.rtl.min.css
COPY ./static/styles/bootstrap.rtl.min.css.map ./static/styles/bootstrap.rtl.min.css.map
COPY ./static/styles/sign-in.css ./static/styles/sign-in.css

EXPOSE 80

RUN pip3 install -r requirements.txt
CMD gunicorn --bind 0.0.0.0:80 app:app