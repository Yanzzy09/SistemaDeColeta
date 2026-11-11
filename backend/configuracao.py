import os
from pathlib import Path

from dotenv import load_dotenv

# Esta configuração carrega as variáveis locais em um único lugar para que o restante do backend não leia o arquivo .env.
load_dotenv()

# A origem exata do React é usada pelo CORS para permitir chamadas do navegador durante o desenvolvimento.
ORIGEM_FRONTEND = os.getenv("FRONTEND_ORIGIN", "")
ORIGENS_FRONTEND = [origem for origem in {
    ORIGEM_FRONTEND,
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://sistema-de-coleta-v1vz.vercel.app",
} if origem]

# Este endereço informa ao SQLAlchemy como encontrar o banco PostgreSQL deste ambiente.
_url_banco_configurada = os.getenv("URL_DO_BANCO", "").strip()
# Produção usa o PostgreSQL informado pelo ambiente. Sem essa variável no
# desenvolvimento, usamos o SQLite local já existente para permitir o login.
_url_de_exemplo = "usuario:senha@localhost" in _url_banco_configurada or "postgres:senha@localhost" in _url_banco_configurada
# O .env local pode conter uma URL remota antiga/inacessível. O deploy da
# Vercel mantém o PostgreSQL; fora dele, o SQLite local garante o fluxo de
# autenticação e desenvolvimento sem mascarar a falha como senha incorreta.
_url_remota_fora_da_vercel = "supabase.com" in _url_banco_configurada and not os.getenv("VERCEL")
URL_DO_BANCO = (
    f"sqlite:///{Path(__file__).resolve().parent / 'volta.db'}"
    if not _url_banco_configurada or _url_de_exemplo or _url_remota_fora_da_vercel
    else _url_banco_configurada
)

# Esta chave assina os tokens e deve existir somente no .env de cada ambiente.
CHAVE_DO_TOKEN = os.getenv("CHAVE_DO_TOKEN", "troque-esta-chave-no-env")
