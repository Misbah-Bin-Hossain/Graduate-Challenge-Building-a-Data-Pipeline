Set-Location "C:\Github\The challenge\Graduate-Challenge-Building-a-Data-Pipeline"
docker-compose up -d
python ".\Get Data.py" *>> ".\pipeline.log"