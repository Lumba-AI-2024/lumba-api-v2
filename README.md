# LumbaAI API V2

A revamp of the old LumbaAI API 
https://github.com/MKM-EAI/backend.git

## Cara clone dan menjalankan project
1. Clone project  
   ```
   git clone https://github.com/MKM-EAI/backend.git
   ```  
2. Buat virtual environment  
   ```
   python virtualenv venv
   ```  
3. Aktifkan virtual environment  
   ```
   source venv/bin/activate
   ```  
4. Install library yang terdokumentasi di requirements.txt  
   ```
   pip install -r requirements.txt
   ```
5. Buat file `.env` pada root dengan format:
   ```shell
   ENV= # Prod or  Dev
   DEBUG= # True for devs
   DJANGO_SECRET_KEY= # https://djecrety.ir/
   
   # POSTGRES CREDENTIALS
   PSQL_DB_NAME=
   PSQL_USER=
   PSQL_PASSWORD=
   PSQL_HOST=
   
   #lumba-model API
   TRAINING_API_URL=
   
   # Credentials for MinIO instance
   AWS_ACCESS_KEY_ID=
   AWS_SECRET_ACCESS_KEY=
   AWS_S3_ENDPOINT_URL=
   ```
6. Buat migrasi model ke database  
   ```
   python ./manage.py makemigrations
   ```  
   ```
   python ./manage.py migrate
   ``` 
7. Jalankan server  
   ```
   python ./manage.py runserver
   ```  

### Running in Docker
1. Build image
    ```shell
    docker build . -t lumba_api_v2 -f .\Kubernetes\build.Dockerfile
    ```
2. Run
    ```shell
    docker run -d -p 8000:8000 --name lumba_api --env-file=.env  lumba_api_v2
    ```
    Should be accessible from http://localhost:8000/

## Jangan lupa dokumentasikan library sebelum push
`pip freeze > requirements.txt`
