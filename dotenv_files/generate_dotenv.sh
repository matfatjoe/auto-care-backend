#!/bin/bash

# Caminho do arquivo base e destino
EXAMPLE_ENV_FILE="dotenv_files/.env_example"
OUTPUT_ENV_FILE="dotenv_files/.env"

# Geração dos valores para desenvolvimento
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(64))')
POSTGRES_PASSWORD=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')
POSTGRES_HOST="psql"
POSTGRES_PORT="5432"
ALLOWED_HOSTS="127.0.0.1, localhost, psql"
POSTGRES_DB="autocare-db"
POSTGRES_USER="dev-autocare"

# Verifica se o arquivo exemplo existe
if [ ! -f "$EXAMPLE_ENV_FILE" ]; then
  echo "Arquivo exemplo não encontrado: $EXAMPLE_ENV_FILE"
  exit 1
fi

# Verifica se o .env já existe
if [ -f "$OUTPUT_ENV_FILE" ]; then
  echo "O arquivo .env já existe. Não será sobrescrito."
  exit 1
fi

# Copia o conteúdo original
cp "$EXAMPLE_ENV_FILE" "$OUTPUT_ENV_FILE"

# Substitui os valores no novo arquivo (.env)
sed -i "s|^SECRET_KEY=.*|SECRET_KEY=\"$SECRET_KEY\"|" "$OUTPUT_ENV_FILE"
sed -i "s|^ALLOWED_HOSTS=.*|ALLOWED_HOSTS=\"$ALLOWED_HOSTS\"|" "$OUTPUT_ENV_FILE"
sed -i "s|^POSTGRES_DB=.*|POSTGRES_DB=\"$POSTGRES_DB\"|" "$OUTPUT_ENV_FILE"
sed -i "s|^POSTGRES_USER=.*|POSTGRES_USER=\"$POSTGRES_USER\"|" "$OUTPUT_ENV_FILE"
sed -i "s|^POSTGRES_PASSWORD=.*|POSTGRES_PASSWORD=\"$POSTGRES_PASSWORD\"|" "$OUTPUT_ENV_FILE"
sed -i "s|^POSTGRES_HOST=.*|POSTGRES_HOST=\"$POSTGRES_HOST\"|" "$OUTPUT_ENV_FILE"
sed -i "s|^POSTGRES_PORT=.*|POSTGRES_PORT=\"$POSTGRES_PORT\"|" "$OUTPUT_ENV_FILE"

# Ajusta as permissões do arquivo
chmod 600 "$OUTPUT_ENV_FILE"

echo ".env de desenvolvimento gerado com sucesso em: $OUTPUT_ENV_FILE"
