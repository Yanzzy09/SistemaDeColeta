import os

from dotenv import load_dotenv

# Esta configuração carrega as variáveis locais em um único lugar para que o restante do backend não leia o arquivo .env.
load_dotenv()

# A origem exata do React é usada pelo CORS para permitir chamadas do navegador durante o desenvolvimento.
ORIGEM_FRONTEND = os.getenv("FRONTEND_ORIGIN", "")
ORIGENS_FRONTEND = [origem for origem in {
    ORIGEM_FRONTEND,
    "http://localhost:5173",
    "http://127.0.0.1:5173",
} if origem]

# Este endereço informa ao SQLAlchemy como encontrar o banco PostgreSQL deste ambiente.
URL_DO_BANCO = os.getenv(
    "URL_DO_BANCO",
    "postgresql+psycopg://postgres:senha@localhost:5432/Sistema_de_coleta",
)

# Esta chave assina os tokens e deve existir somente no .env de cada ambiente.
CHAVE_DO_TOKEN = os.getenv("CHAVE_DO_TOKEN", "troque-esta-chave-no-env")
