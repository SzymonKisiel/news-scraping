# create network

# build
docker build -t test/scraper ./scraper
docker build -t test/command-handler ./command-handler
docker build -t test/sentiment-analyser ./sentiment-analyser

# run
docker run -it --rm --network news_scraping_net -p 5002:5002 --name scraper test/scraper
docker run -it --rm --network news_scraping_net -p 5001:5001 --name command-handler test/command-handler
docker run -it --rm --network news_scraping_net -p 5003:5003 --name sentiment-analyser test/sentiment-analyser

docker run --rm -d -v mysql:/var/lib/mysql -v mysql_config:/etc/mysql -p 3306:3306 --network news_scraping_net --name scraper_db -e MYSQL_ROOT_PASSWORD=p@ssw0rd1 mysql
docker stop scraper_db

# clean




# test
# Just create interactive container. No start but named for future reference.
# Use your own image.
docker create -it --name new-container test/sentiment-analyser

# Now start it.
docker start new-container

# Now attach bash session.
docker exec -it new-container bash