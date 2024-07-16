# gradio-sample

## Setup(for Windows)

```cmd
copy .env.example .env
```

.envファイルのOPENAI_API_KEYに発行したキーを設定
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

```cmd
docker compose up -d
```

## Access

[Open](http://localhost:7860/)

## All Delete

```
docker compose down --rmi all --volumes --remove-orphans
```
