Feedly
===

# How to Test
###### Note: You can visit these links for instructions on installing docker and docker-compose: [docker](https://linuxize.com/post/how-to-install-and-use-docker-on-ubuntu-18-04/), [docker-compose](https://linuxize.com/post/how-to-install-and-use-docker-compose-on-ubuntu-18-04/)
After having docker and docker-compose installed go through these steps:

1. Clone the repository:

    ```bash
    git clone git@github.com:borouny/feedly.git && cd feedly
    ```
 2. Create env file from [example](env.example) and fill the required variables in it:
 
    ```bash
    cp env.example .env
    ```
  3. Build the project with ssh key (in order to install requirements from private git repo
  
    ```bash
    sudo docker-compose build
    ```
  4. Start the project:
  
    ```bash
    sudo docker-compose up -d
    ```
  5. Open http://localhost:8000/swagger/ or http://localhost:8000/redoc/ on the browser
  
  6. Run test cases
  
    ```bash
    docker exec -it web  python manage.py test
    ```
  
