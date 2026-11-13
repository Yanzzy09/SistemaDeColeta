import React from 'react';
import { createRoot } from 'react-dom/client';
import Aplicativo from './Aplicativo.jsx';
import './estilos.css';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, mensagem: '' };
  }

  static getDerivedStateFromError(erro) {
    return { hasError: true, mensagem: erro?.message || 'Erro ao carregar a aplicação.' };
  }

  componentDidCatch(erro) {
    console.error('Erro no frontend:', erro);
  }

  render() {
    if (this.state.hasError) {
      return (
        <main style={{
          minHeight: '100vh',
          display: 'grid',
          placeItems: 'center',
          padding: '24px',
          background: '#f7f8f4',
          color: '#244531',
          fontFamily: 'sans-serif',
          textAlign: 'center',
        }}>
          <div style={{ maxWidth: '440px', background: '#fff', border: '1px solid #e7ece5', borderRadius: '16px', padding: '28px 24px', boxShadow: '0 18px 40px rgba(27, 58, 42, 0.08)' }}>
            <h1 style={{ margin: '0 0 12px', fontSize: '24px' }}>Não foi possível abrir o app.</h1>
            <p style={{ margin: 0, lineHeight: 1.6, color: '#475d51' }}>
              {this.state.mensagem}
            </p>
            <button
              type="button"
              onClick={() => window.location.reload()}
              style={{
                marginTop: '20px',
                border: 'none',
                borderRadius: '10px',
                background: '#287650',
                color: '#fff',
                fontWeight: 700,
                padding: '12px 18px',
                cursor: 'pointer',
              }}
            >
              Recarregar
            </button>
          </div>
        </main>
      );
    }

    return this.props.children;
  }
}

const raiz = document.getElementById('raiz');

if (!raiz) {
  document.body.innerHTML = '<main style="min-height:100vh;display:grid;place-items:center;background:#f7f8f4;color:#244531;font-family:sans-serif;text-align:center;padding:24px"><div style="background:#fff;border:1px solid #e7ece5;border-radius:16px;padding:28px 24px;max-width:440px"><h1 style="margin:0 0 12px;font-size:24px">Não foi possível abrir o app.</h1><p style="margin:0;line-height:1.6;color:#475d51">Elemento raiz não encontrado.</p></div></main>';
} else {
  createRoot(raiz).render(
    <React.StrictMode>
      <ErrorBoundary>
        <Aplicativo />
      </ErrorBoundary>
    </React.StrictMode>,
  );
}
