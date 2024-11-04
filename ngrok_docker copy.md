# Using ngrok with Docker
ngrok provides pre-built Docker images for the ngrok Agent with instructions for getting started. An example command for starting a tunnel to port 80 on the host machine looks like this:
```bash

docker run --net=host -it -e NGROK_AUTHTOKEN=xyz ngrok/ngrok:latest http 80
```
  
Note: the Docker version of ngrok follows the same convention as the agent, for example:

  
```
docker run -it -e NGROK_AUTHTOKEN=xyz ngrok/ngrok:latest http 80                            _# secure public URL for port 80 web server_

docker run -it -e NGROK_AUTHTOKEN=xyz ngrok/ngrok:latest http --url=baz.ngrok.dev 8080      _# port 8080 available at baz.ngrok.dev_

docker run -it -e NGROK_AUTHTOKEN=xyz ngrok/ngrok:latest http foo.dev:80                    _# tunnel to host:port instead of localhost_

docker run -it -e NGROK_AUTHTOKEN=xyz ngrok/ngrok:latest http https://localhost:5001        _# expose a local https server running on port 5001_

docker run -it -e NGROK_AUTHTOKEN=xyz ngrok/ngrok:latest tcp 22                             _# tunnel arbitrary TCP traffic to port 22_

docker run -it -e NGROK_AUTHTOKEN=xyz ngrok/ngrok:latest tls --url=foo.com 443              _# TLS traffic for foo.com to port 443_

docker run -it -e NGROK_AUTHTOKEN=xyz ngrok/ngrok:latest start foo bar baz                  _# start tunnels from the configuration file_

```

**Note:**

For MacOS or Windows users, the --net=host option will not work. You will need to use the special URL host.docker.internal as described in the Docker networking documentation.
```
docker run -it -e NGROK_AUTHTOKEN=xyz ngrok/ngrok:latest http host.docker.internal:80
```
  
This also applies to the upstream addr in your ngrok config file. For example:
```
tunnels:
  test:
    proto: http
    addr: http://host.docker.internal:80
```

**Using ngrok with Docker Compose**
If you’re more comfortable using Docker Compose, you can use the following as a starting point. Copy the contents below into a new file named docker-compose.yaml, then run docker compose up in that directory. This Docker compose file assumes that you have an ngrok.yml file in the same directory with at least one tunnel defined. Check out the ngrok agent config file documentation for help creating a configuration file with a tunnel definition. If you want to use the same configuration file as your local ngrok agent, you can view the location of the default config file using ngrok config check.
```
services:
  ngrok:
    image: ngrok/ngrok:latest
    restart: unless-stopped
    command:
      - "start"
      - "--all"
      - "--config"
      - "/etc/ngrok.yml"
    volumes:
      - ./ngrok.yml:/etc/ngrok.yml
    ports:
      - 4040:4040
  ```

If you’re defining your tunnels directly in docker-compose.yaml rather than using an ngrok.yml file, the configuration will look a little different. Your command will be running an ngrok http command, and you’ll be using the special URL host.docker.internal as mentioned in the note above. The following is an example of using ngrok along with the dockersamples/static-site image.

```
services:
  static-site:
    image: dockersamples/static-site
    build: .
    ports:
      - "80:80"
    restart: always
  ngrok:
    image: ngrok/ngrok:latest
    command:
      - "http"
      - "http://host.docker.internal:80"
    environment:
      NGROK_AUTHTOKEN: ${NGROK_AUTHTOKEN}
    ports:
      - 4040:4040