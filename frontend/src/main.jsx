import React from 'react';
import { createRoot } from 'react-dom/client';
import Aplicativo from './Aplicativo.jsx';
import './estilos.css';

// Este ponto inicia a interface React no elemento principal da página.
createRoot(document.getElementById('raiz')).render(
  <React.StrictMode>
    <Aplicativo />
  </React.StrictMode>,
);
