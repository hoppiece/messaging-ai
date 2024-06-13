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
