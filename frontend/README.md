# Frontend

Interface React responsiva do sistema Volta. Para executar em desenvolvimento, com Node.js e npm instalados:

```powershell
npm install
npm run dev
```

O ambiente de desenvolvimento usa `.env.development`, que aponta `VITE_URL_DA_API` para a API local na porta 8000. O seletor no cabeçalho alterna entre os fluxos da moradora e da cooperativa. Os dados de demonstração e as alterações feitas nas telas ficam salvos no navegador.

Para gerar os arquivos que o servidor web entregará em produção:

```powershell
npm run build
```

O build usa `.env.production`, com `VITE_URL_DA_API=/api`. O servidor web deve entregar `dist/` e encaminhar `/api` para a API interna.
