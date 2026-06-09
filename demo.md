colima start

docker stop $(docker ps -aq) && docker rm $(docker ps -aq)

docker compose -f docker-compose-pragent.yml up -d

/api/v1/github_webhooks
https://439a-118-69-122-34.ngrok-free.app/api/v1/github_webhooks
choose-a-random-secret-here

https://github.com/thanhlamvo-ogilvy/cicd-with-ai/settings/hooks

docker compose -f docker-compose-pragent.yml logs -f pr-agent

docker compose -f docker-compose-pragent.yml up -d --force-recreate pr-agent