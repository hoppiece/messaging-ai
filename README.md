## Developing

- Prepare `ngrok.yml` on project root
  ```yaml
    version: "2"
    authtoken: **********************
    tunnels:
    api:
        proto: http
        addr: api:8000
        host_header: rewrite
  ```

- `docker compose up`
  - http://localhost:8000 -- Local API endpoint
  - http://localhost:4040 -- ngrok console that show public URL of local API


### Local DB Initialization

```
docker compose exec -it api bash
cd repositories
python init_db.py
```

### Cheat sheet for local MySQL
```
docker compose exec -it mysql bash
mysql -u user -p
```
```
USE hygeia;
SHOW TABLES;

```

### Troubleshooting
- `Error response from daemon: network a10b89ed703a0d642faf5af93abc2ac3a767574d1af4b9236d5628092cf72377 not found`
  - `docker network prune -f`
- Failure while installing `mysqlclient`:
  - `brew install mysql` 
