# start by pulling the python image
FROM python:3.8-alpine

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install flask
RUN pip install requests




RUN pip install chardet
RUN pip install pdfkit


RUN pip install spotipy
RUN pip install python-dotenv

# copy every content from the local file to the image
COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]
