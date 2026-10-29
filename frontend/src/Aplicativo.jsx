import React, { useEffect, useMemo, useState } from 'react';

// A URL vem do ambiente: desenvolvimento chama a API local e produção usa o proxy /api.
const URL_API_CONFIGURADA = import.meta.env.VITE_URL_DA_API;
const API_BASE_URL = (URL_API_CONFIGURADA && URL_API_CONFIGURADA !== '/api'
  ? URL_API_CONFIGURADA
  : 'https://sistema-de-coleta-vert.vercel.app').replace(/\/$/, '');
const MATERIAIS = ['Papel', 'Vidro', 'Plástico', 'Metal'];
const PONTOS_POR_QUILO = { Papel: 1, Vidro: 1, Plástico: 2, Metal: 4 };

// Estes dados iniciais mostram os estados principais do fluxo na primeira visita.
const COLETAS_INICIAIS = [
  {
    id: 'VC-1042', morador: 'Joana Martins', endereco: 'Rua das Palmeiras, 128 · Vila Mariana',
    dia: dataRelativa(2), materiais: ['Papel', 'Plástico'], situacao: 'Agendada', pontos: 0, pesagens: [],
  },
  {
    id: 'VC-1041', morador: 'Joana Martins', endereco: 'Rua das Palmeiras, 128 · Vila Mariana',
    dia: dataRelativa(-3), materiais: ['Papel', 'Metal'], situacao: 'Coletada', pontos: 26,
    pesagens: [{ material: 'Papel', quilos: 10 }, { material: 'Metal', quilos: 4 }],
  },
  {
    id: 'VC-1040', morador: 'Marcos Silva', endereco: 'Rua Harmonia, 45 · Vila Madalena',
    dia: dataRelativa(2), materiais: ['Vidro', 'Papel'], situacao: 'Agendada', pontos: 0, pesagens: [],
  },
  {
    id: 'VC-1039', morador: 'Ana Costa', endereco: 'Av. dos Ipês, 903 · Saúde',
    dia: dataRelativa(2), materiais: ['Plástico', 'Metal'], situacao: 'Agendada', pontos: 0, pesagens: [],
  },
];

// Este helper gera datas de demonstração sem fixar o calendário do aplicativo.
function dataRelativa(dias) {
  const data = new Date();
  data.setDate(data.getDate() + dias);
  const ano = data.getFullYear();
  const mes = String(data.getMonth() + 1).padStart(2, '0');
  const dia = String(data.getDate()).padStart(2, '0');
  return `${ano}-${mes}-${dia}`;
}

// Esta função transforma a data salva em uma legenda simples para os cartões.
function formatarData(valor, curto = false) {
  if (!valor) return 'Escolha uma data';
  const data = new Date(`${valor}T12:00:00`);
  return new Intl.DateTimeFormat('pt-BR', curto
    ? { day: '2-digit', month: 'short' }
    : { weekday: 'long', day: '2-digit', month: 'long' }).format(data);
}

// Este componente mostra o símbolo da marca feito com formas simples em SVG.
function Marca() {
  return <a className="marca" href="#inicio" aria-label="Volta, início">
    <span className="marca-simbolo" aria-hidden="true"><svg viewBox="0 0 36 36" fill="none"><path d="M27.9 10.7A12.4 12.4 0 0 0 7.6 14M8.1 7.8v6.8h6.8M8.1 25.3a12.4 12.4 0 0 0 20.3-3.3m-.5 6.2v-6.8h-6.8" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round"/><circle cx="18" cy="18" r="3.1" fill="currentColor"/></svg></span>
    <span>volta<span className="marca-ponto">.</span></span>
  </a>;
}

// Este componente padroniza pequenos ícones decorativos e mantém os botões acessíveis.
function Icone({ nome, tamanho = 18 }) {
  const caminhos = {
    casa: <><path d="m3 10 9-7 9 7"/><path d="M5 9v11h14V9M9 20v-6h6v6"/></>,
    calendario: <><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18"/></>,
    caixa: <><path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 8 9 5 9-5M3 8v10l9 5 9-5V8M12 13v10"/></>,
    seta: <><path d="M5 12h14M13 6l6 6-6 6"/></>,
    mais: <><path d="M12 5v14M5 12h14"/></>,
    local: <><path d="M20 10c0 5-8 11-8 11S4 15 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/></>,
    peso: <><path d="M6 7h12l2 14H4L6 7Z"/><path d="M9 7a3 3 0 0 1 6 0M12 12l2 2"/></>,
    check: <path d="m5 12 4 4L19 6"/>,
    relogio: <><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></>,
    estrela: <path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1.1 6.2-5.6-3-5.6 3 1.1-6.2L3 9.6l6.2-.9L12 3Z"/>,
    chevron: <path d="m9 18 6-6-6-6"/>,
    reciclavel: <><path d="m10 3 2-1 4 6-2 1M6 13l-3 1 2 7h7v-3M18 13l3 1-2 7h-7v-3"/><path d="m8 8 3-5M16 8l3 5M8 15h8"/></>,
  };
  return <svg className="icone" width={tamanho} height={tamanho} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{caminhos[nome] || caminhos.caixa}</svg>;
}

// Este componente mantém a navegação entre os dois perfis simples e visível.
function SeletorPerfil({ perfil, aoSair, modoDemo, aoAlternarDemo }) {
  return <div className="seletor-perfil" role="group" aria-label="Escolha o perfil">
    <span className="perfil-logado"><span className={`perfil-avatar ${perfil === 'moradora' ? 'avatar-moradora' : 'avatar-cooperativa'}`}>{perfil === 'moradora' ? 'J' : 'O'}</span><span>{perfil === 'moradora' ? 'Moradora' : 'Cooperativa'}</span></span>
    {modoDemo && <button className="botao-alternar-demo" onClick={aoAlternarDemo}>{perfil === 'moradora' ? 'Ver Osmar' : 'Ver Joana'}</button>}<button className="botao-sair" onClick={aoSair}>Sair</button>
  </div>;
}

// Esta tela autentica a pessoa antes de liberar as telas e as requisições protegidas.
function TelaLogin({ aoEntrar }) {
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [mensagem, setMensagem] = useState('');
  const [enviando, setEnviando] = useState(false);

  // Esta função envia o formulário OAuth2 e guarda somente o token no navegador.
  function entrar(evento) {
    evento.preventDefault();
    setEnviando(true);
    setMensagem('');
    const corpo = new URLSearchParams({ username: email, password: senha });
    fetch(`${API_BASE_URL}/login`, { method: 'POST', body: corpo })
      .then((resposta) => {
        if (!resposta.ok) throw new Error('E-mail ou senha incorretos.');
        return resposta.json();
      })
      .then((dados) => {
        localStorage.setItem('volta-token', dados.access_token);
        aoEntrar(dados.access_token);
      })
      .catch((erro) => setMensagem(erro.message))
      .finally(() => setEnviando(false));
  }

  function abrirDemonstracao() {
    localStorage.setItem('volta-token', 'demo');
    aoEntrar('demo');
  }

  return <main className="tela-login"><section className="cartao-login"><Marca /><span className="sobretitulo">ACESSO AO VOLTA</span><h1>Seu cuidado<br /><em>continua daqui.</em></h1><p>Entre para agendar coletas, acompanhar pontos e cuidar da rota.</p><form onSubmit={entrar}><label className="campo-label" htmlFor="login-email">E-mail</label><input className="campo-login" id="login-email" type="email" required value={email} onChange={(evento) => setEmail(evento.target.value)} placeholder="voce@exemplo.com" /><label className="campo-label" htmlFor="login-senha">Senha</label><input className="campo-login" id="login-senha" type="password" required value={senha} onChange={(evento) => setSenha(evento.target.value)} placeholder="Sua senha" />{mensagem && <p className="mensagem-erro" role="alert">{mensagem}</p>}<button className="botao-principal botao-login" disabled={enviando}>{enviando ? 'Entrando...' : 'Entrar'} <Icone nome="seta" tamanho={17} /></button></form><div className="divisor-login"><span>ou</span></div><button type="button" className="botao-secundario botao-demo" onClick={abrirDemonstracao}>Ver demonstração</button><p className="legenda-demo">A demonstração usa dados fictícios e não precisa do banco.</p></section></main>;
}

// Este formulário reúne os dados necessários para marcar uma coleta em poucos passos.
function FormularioAgendamento({ aoSalvar, aoCancelar }) {
  const [endereco, setEndereco] = useState('');
  const [dia, setDia] = useState(dataRelativa(1));
  const [materiais, setMateriais] = useState([]);
  const [erro, setErro] = useState('');

  // Esta função verifica os campos essenciais antes de incluir a coleta na lista.
  function enviar(evento) {
    evento.preventDefault();
    if (!endereco.trim() || !dia || materiais.length === 0) {
      setErro('Preencha o endereço, escolha o dia e selecione ao menos um material.');
      return;
    }
    aoSalvar({
      id: `VC-${Math.floor(1000 + Math.random() * 8999)}`,
      morador: 'Joana Martins', endereco: endereco.trim(), dia, materiais,
      situacao: 'Agendada', pontos: 0, pesagens: [],
    });
  }

  // Esta função alterna um material sem apagar as outras escolhas da moradora.
  function alternarMaterial(material) {
    setMateriais((atuais) => atuais.includes(material)
      ? atuais.filter((item) => item !== material)
      : [...atuais, material]);
    setErro('');
  }

  return <div className="modal-fundo" role="presentation" onMouseDown={(evento) => evento.target === evento.currentTarget && aoCancelar()}>
    <section className="modal" role="dialog" aria-modal="true" aria-labelledby="titulo-agendamento">
      <div className="modal-cabecalho"><div className="modal-icone"><Icone nome="reciclavel" tamanho={23} /></div><button className="fechar-modal" onClick={aoCancelar} aria-label="Fechar">×</button></div>
      <p className="sobretitulo">UMA NOVA COLETA</p><h2 id="titulo-agendamento">Vamos buscar seu material?</h2>
      <p className="texto-modal">Escolha um dia e conte pra gente o que você separou.</p>
      <form onSubmit={enviar}>
        <label className="campo-label" htmlFor="endereco">Endereço da coleta</label>
        <div className="campo-com-icone"><Icone nome="local" tamanho={18} /><input id="endereco" value={endereco} onChange={(evento) => { setEndereco(evento.target.value); setErro(''); }} placeholder="Rua, número e bairro" autoFocus /></div>
        <label className="campo-label" htmlFor="dia">Qual dia fica melhor?</label>
        <input className="campo-data" id="dia" type="date" min={dataRelativa(0)} value={dia} onChange={(evento) => setDia(evento.target.value)} />
        <span className="campo-label">O que você separou?</span>
        <div className="opcoes-materiais">{MATERIAIS.map((material, indice) => <button key={material} type="button" className={`opcao-material ${materiais.includes(material) ? 'opcao-selecionada' : ''}`} onClick={() => alternarMaterial(material)}><span className={`bolinha-material material-${indice}`}><Icone nome="caixa" tamanho={17} /></span><span>{material}</span><span className="marca-selecao">{materiais.includes(material) ? '✓' : '+'}</span></button>)}</div>
        {erro && <p className="mensagem-erro" role="alert">{erro}</p>}
        <div className="acoes-modal"><button type="button" className="botao-secundario" onClick={aoCancelar}>Agora não</button><button type="submit" className="botao-principal">Agendar coleta <Icone nome="seta" tamanho={17} /></button></div>
      </form>
    </section>
  </div>;
}

// Este cartão transforma o estado e o resultado de cada coleta em informação fácil de localizar.
function CartaoColeta({ coleta, aoSelecionar, compacto = false }) {
  const concluida = coleta.situacao === 'Coletada';
  return <button className={`cartao-coleta ${compacto ? 'cartao-compacto' : ''}`} onClick={() => aoSelecionar(coleta)}>
    <span className={`mini-icone-coleta ${concluida ? 'mini-concluida' : ''}`}><Icone nome={concluida ? 'check' : 'caixa'} tamanho={19} /></span>
    <span className="cartao-conteudo"><span className="cartao-linha-superior"><span className="codigo-coleta">{coleta.id}</span><span className={`selo-status ${concluida ? 'status-concluida' : 'status-agendada'}`}><i />{coleta.situacao}</span></span><strong>{compacto ? coleta.morador : formatarData(coleta.dia)}</strong><span className="cartao-detalhe">{compacto ? formatarData(coleta.dia) : coleta.endereco}</span>{!compacto && <span className="etiquetas-materiais">{coleta.materiais.map((material) => <span key={material}>{material}</span>)}</span>}{coleta.pesagens.length > 0 && <span className="linha-pontos"><Icone nome="estrela" tamanho={14} /> {coleta.pontos} pontos conquistados</span>}</span>
    <Icone nome="chevron" tamanho={18} />
  </button>;
}

// Este painel abre o histórico da coleta para mostrar cada material pesado e seus pontos.
function DetalheColeta({ coleta, aoFechar }) {
  return <div className="modal-fundo" role="presentation" onMouseDown={(evento) => evento.target === evento.currentTarget && aoFechar()}><section className="modal modal-detalhe" role="dialog" aria-modal="true" aria-labelledby="titulo-detalhe">
    <div className="modal-cabecalho"><span className={`mini-icone-coleta detalhe-icone ${coleta.situacao === 'Coletada' ? 'mini-concluida' : ''}`}><Icone nome={coleta.situacao === 'Coletada' ? 'check' : 'caixa'} tamanho={20} /></span><button className="fechar-modal" onClick={aoFechar} aria-label="Fechar">×</button></div>
    <p className="sobretitulo">COLETA {coleta.id}</p><h2 id="titulo-detalhe">{formatarData(coleta.dia)}</h2><p className="texto-modal">{coleta.endereco}</p>
    <div className="detalhe-status"><span className={`selo-status ${coleta.situacao === 'Coletada' ? 'status-concluida' : 'status-agendada'}`}><i />{coleta.situacao}</span><span>{coleta.materiais.join(' · ')}</span></div>
    <div className="secao-pesagem"><div className="secao-titulo"><h3>O que foi pesado</h3><span>{coleta.pesagens.length} {coleta.pesagens.length === 1 ? 'material' : 'materiais'}</span></div>{coleta.pesagens.length ? <>{coleta.pesagens.map((pesagem, indice) => <div className="linha-pesagem" key={`${pesagem.material}-${indice}`}><span><span className="bolinha-peso"><Icone nome="peso" tamanho={15} /></span><strong>{pesagem.material}</strong></span><span>{pesagem.quilos} kg <b>·</b> {pesagem.pontos} pts</span></div>)}<div className="total-pontos"><span><Icone nome="estrela" tamanho={18} /> Total da entrega</span><strong>{coleta.pontos} <small>pontos</small></strong></div></> : <div className="sem-pesagens"><span className="sem-peso-icone"><Icone nome="relogio" tamanho={19} /></span><div><strong>Ainda não foi pesada</strong><p>Os pontos aparecem aqui depois da coleta.</p></div></div>}</div>
    <button className="botao-secundario botao-largo" onClick={aoFechar}>Fechar</button>
  </section></div>;
}

// Esta tela permite à moradora agendar uma busca e acompanhar seus resultados.
function TelaMoradora({ coletas, aoAgendar, aoSelecionar, nomeMoradora = 'Joana Martins' }) {
  const minhas = coletas.filter((coleta) => coleta.morador === nomeMoradora).sort((a, b) => a.dia.localeCompare(b.dia));
  const pontos = minhas.reduce((soma, coleta) => soma + coleta.pontos, 0);
  return <main className="conteudo conteudo-moradora" id="inicio">
    <section className="boas-vindas"><div><span className="saudacao">OLÁ, JOANA <span className="emoji-ola">✳</span></span><h1>Um cuidado de cada vez.<br /><em>O planeta agradece.</em></h1><p>Separe o que puder. A gente busca e transforma em novos começos.</p><button className="botao-principal botao-agendar" onClick={aoAgendar}><Icone nome="mais" tamanho={18} /> Agendar coleta</button></div><div className="ilustracao-boas-vindas" aria-hidden="true"><div className="sol-ilustrado" /><div className="folha folha-um" /><div className="folha folha-dois" /><div className="vaso"><span>↟</span></div><span className="ponto-voando ponto-a">✳</span><span className="ponto-voando ponto-b">✦</span><span className="ponto-voando ponto-c">✳</span><span className="selo-ilustrado">cada gesto<br />faz diferença</span></div></section>
    <section className="resumo-moradora"><div className="resumo-item"><span className="resumo-icone"><Icone nome="calendario" /></span><div><small>SUAS COLETAS</small><strong>{minhas.length.toString().padStart(2, '0')} <span>agendadas e feitas</span></strong></div></div><span className="resumo-divisor" /><div className="resumo-item"><span className="resumo-icone resumo-estrela"><Icone nome="estrela" /></span><div><small>SEUS PONTOS</small><strong>{pontos} <span>pontos acumulados</span></strong></div></div><div className="mensagem-resumo"><span>✳</span> Cada quilo conta. Obrigada por separar!</div></section>
    <section className="secao-coletas"><div className="cabecalho-secao"><div><span className="sobretitulo">SEU HISTÓRICO</span><h2>Suas coletas</h2></div><button className="link-acao" onClick={aoAgendar}>Nova coleta <Icone nome="seta" tamanho={16} /></button></div>
      {minhas.length ? <div className="lista-coletas">{minhas.map((coleta) => <CartaoColeta key={coleta.id} coleta={coleta} aoSelecionar={aoSelecionar} />)}</div> : <div className="estado-vazio"><span className="vazio-icone"><Icone nome="caixa" tamanho={23} /></span><strong>Sua primeira coleta começa aqui</strong><p>Quando você agendar, vamos acompanhar tudo por aqui.</p><button className="botao-secundario" onClick={aoAgendar}>Agendar minha coleta</button></div>}</section>
  </main>;
}

// Este painel calcula uma prévia de pontos antes de Osmar confirmar a pesagem.
function FormularioPesagem({ coleta, aoSalvar, aoCancelar }) {
  const [material, setMaterial] = useState(MATERIAIS[0]);
  const [quilos, setQuilos] = useState('');
  const [erro, setErro] = useState('');
  const pontos = Number(quilos || 0) * PONTOS_POR_QUILO[material];

  // Esta função valida o peso e passa ao aplicativo a pesagem pronta para registrar.
  function registrar(evento) {
    evento.preventDefault();
    if (!Number(quilos) || Number(quilos) <= 0) {
      setErro('Informe um peso maior que zero para continuar.');
      return;
    }
    aoSalvar({ material, quilos: Number(quilos), pontos });
  }

  return <div className="modal-fundo" role="presentation" onMouseDown={(evento) => evento.target === evento.currentTarget && aoCancelar()}><section className="modal" role="dialog" aria-modal="true" aria-labelledby="titulo-pesagem">
    <div className="modal-cabecalho"><div className="modal-icone modal-icone-verde"><Icone nome="peso" tamanho={22} /></div><button className="fechar-modal" onClick={aoCancelar} aria-label="Fechar">×</button></div>
    <p className="sobretitulo">REGISTRO DE PESAGEM · {coleta.id}</p><h2 id="titulo-pesagem">O que chegou na balança?</h2><p className="texto-modal">{coleta.morador} <span>·</span> {coleta.endereco}</p>
    <form onSubmit={registrar}><label className="campo-label" htmlFor="material-peso">Tipo de material</label><select id="material-peso" className="campo-select" value={material} onChange={(evento) => setMaterial(evento.target.value)}>{MATERIAIS.map((item) => <option key={item} value={item}>{item} · {PONTOS_POR_QUILO[item]} {PONTOS_POR_QUILO[item] === 1 ? 'ponto' : 'pontos'} por kg</option>)}</select>
      <label className="campo-label" htmlFor="quilos">Peso registrado</label><div className="campo-quilos"><input id="quilos" type="number" min="0.1" step="0.1" placeholder="0,0" value={quilos} onChange={(evento) => { setQuilos(evento.target.value); setErro(''); }} /><span>kg</span></div>
      <div className="previa-pontos"><span><Icone nome="estrela" tamanho={17} /> Pontos desta pesagem</span><strong>{pontos} <small>pts</small></strong></div>
      {erro && <p className="mensagem-erro" role="alert">{erro}</p>}<div className="acoes-modal"><button type="button" className="botao-secundario" onClick={aoCancelar}>Cancelar</button><button type="submit" className="botao-principal">Salvar pesagem <Icone nome="check" tamanho={17} /></button></div>
    </form>
  </section></div>;
}

// Esta tela organiza a rota do dia e dá acesso direto ao registro de cada pesagem.
function TelaCooperativa({ coletas, aoPesagem }) {
  const [dia, setDia] = useState(dataRelativa(2));
  const [busca, setBusca] = useState('');
  const doDia = coletas.filter((coleta) => coleta.dia === dia && `${coleta.morador} ${coleta.endereco}`.toLocaleLowerCase('pt-BR').includes(busca.toLocaleLowerCase('pt-BR')));
  const pendentes = doDia.filter((coleta) => coleta.situacao === 'Agendada').length;
  const pontosDoDia = doDia.reduce((total, coleta) => total + coleta.pontos, 0);
  return <main className="conteudo conteudo-cooperativa" id="inicio">
    <section className="cabecalho-cooperativa"><div><span className="saudacao">PAINEL DA COOPERATIVA <span className="ponto-verde">●</span></span><h1>Bom dia, Osmar.</h1><p>A operação do dia começa com uma boa rota.</p></div><div className="data-hoje"><span className="data-dia">{new Date(`${dia}T12:00:00`).getDate()}</span><span>{new Intl.DateTimeFormat('pt-BR', { month: 'short', weekday: 'short' }).format(new Date(`${dia}T12:00:00`))}</span><Icone nome="calendario" tamanho={17} /></div></section>
    <section className="metricas-rota"><article className="metrica metrica-destaque"><span className="metrica-icone"><Icone nome="local" /></span><small>PARADAS NA ROTA</small><strong>{doDia.length.toString().padStart(2, '0')}</strong><span className="metrica-legenda">coletas para visitar</span><div className="barras-decorativas"><i /><i /><i /><i /><i /><i /><i /></div></article><article className="metrica"><span className="metrica-icone metrica-icone-ambar"><Icone nome="relogio" /></span><small>AGUARDANDO COLETA</small><strong>{pendentes.toString().padStart(2, '0')}</strong><span className="metrica-legenda">precisam de pesagem</span></article><article className="metrica"><span className="metrica-icone metrica-icone-lilas"><Icone nome="estrela" /></span><small>PONTOS REGISTRADOS</small><strong>{pontosDoDia}</strong><span className="metrica-legenda">pontos neste dia</span></article></section>
    <section className="secao-rota"><div className="cabecalho-secao cabecalho-rota"><div><span className="sobretitulo">ORGANIZAÇÃO DO CAMINHÃO</span><h2>Coletas da rota</h2></div><label className="seletor-data"><Icone nome="calendario" tamanho={17} /><input type="date" aria-label="Filtrar coletas por dia" value={dia} onChange={(evento) => setDia(evento.target.value)} /></label></div>
      <div className="filtros-rota"><label className="campo-busca"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"><circle cx="11" cy="11" r="7"/><path d="m16 16 4 4"/></svg><input value={busca} onChange={(evento) => setBusca(evento.target.value)} placeholder="Buscar morador ou endereço" /></label><span className="contador-rota">{doDia.length} {doDia.length === 1 ? 'parada' : 'paradas'}</span></div>
      {doDia.length ? <div className="lista-rota">{doDia.map((coleta, indice) => <div className="parada-rota" key={coleta.id}><div className="ordem-parada"><span>{String(indice + 1).padStart(2, '0')}</span><i /></div><CartaoColeta coleta={coleta} compacto aoSelecionar={() => {}} /><div className="acao-parada">{coleta.situacao === 'Agendada' ? <button className="botao-pesagem" onClick={() => aoPesagem(coleta)}><Icone nome="peso" tamanho={16} /> Registrar peso</button> : <div className="acoes-coleta-feita"><span className="peso-concluido"><Icone nome="check" tamanho={16} /> {coleta.pontos} pts</span><button className="botao-pesagem botao-pesagem-secundario" onClick={() => aoPesagem(coleta)}><Icone nome="mais" tamanho={14} /> Adicionar material</button></div>}</div></div>)}</div> : <div className="estado-vazio"><span className="vazio-icone"><Icone nome="calendario" tamanho={23} /></span><strong>Nenhuma coleta para este dia</strong><p>Escolha outra data ou ajuste sua busca.</p></div>}
    </section><p className="nota-pontos"><Icone nome="estrela" tamanho={15} /> Pontuação automática: papel e vidro 1 pt/kg · plástico 2 pts/kg · metal 4 pts/kg</p>
  </main>;
}

// Este componente reúne os perfis e mantém as coletas sincronizadas entre as telas.
function PainelAplicativo() {
  const [token, setToken] = useState(() => localStorage.getItem('volta-token'));
  const [usuario, setUsuario] = useState(null);
  const [perfil, setPerfil] = useState('moradora');
  const [coletas, setColetas] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erroApi, setErroApi] = useState('');
  const [modalAgendamento, setModalAgendamento] = useState(false);
  const [coletaAtiva, setColetaAtiva] = useState(null);
  const [coletaPesagem, setColetaPesagem] = useState(null);
  const coletasOrdenadas = useMemo(() => coletas, [coletas]);

  // Este efeito carrega a mesma lista usada pelo backend para sincronizar os dois perfis.
  useEffect(() => {
    if (!token) {
      setCarregando(false);
      return;
    }
    if (token === 'demo') {
      setUsuario({ nome: 'Joana Martins', tipo: 'morador' });
      setPerfil('moradora');
      setColetas(COLETAS_INICIAIS);
      setCarregando(false);
      return;
    }
    fetch(`${API_BASE_URL}/coletas`, { headers: { Authorization: `Bearer ${token}` } })
      .then((resposta) => {
        if (!resposta.ok) throw new Error('Não foi possível carregar as coletas.');
        return resposta.json();
      })
      .then((dados) => setColetas(dados.map((coleta) => ({ ...coleta, pesagens: coleta.pesagens || [] })) ))
      .catch(() => {
        setErroApi('A API não respondeu. Confira se o backend está ligado.');
        setColetas(COLETAS_INICIAIS);
      })
      .finally(() => setCarregando(false));
  }, [token]);

  // Este efeito busca o perfil do token e impede que a pessoa escolha outro papel manualmente.
  useEffect(() => {
    if (!token || token === 'demo') return;
    fetch(`${API_BASE_URL}/usuarios/eu`, { headers: { Authorization: `Bearer ${token}` } })
      .then((resposta) => {
        if (!resposta.ok) throw new Error('Sessão inválida.');
        return resposta.json();
      })
      .then((dados) => {
        setUsuario(dados);
        setPerfil(dados.tipo === 'morador' ? 'moradora' : 'cooperativa');
      })
      .catch(() => {
        localStorage.removeItem('volta-token');
        setToken(null);
      });
  }, [token]);

  // Esta função inclui uma nova coleta e fecha o formulário depois do agendamento.
  async function salvarAgendamento(novaColeta) {
    if (token === 'demo') {
      setColetas((atuais) => [{ ...novaColeta }, ...atuais]);
      setErroApi('');
      setModalAgendamento(false);
      return;
    }
    try {
      const resposta = await fetch(`${API_BASE_URL}/coletas`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({
          // O perfil da Joana é escolhido sem login e, nesta etapa, usa o usuário de demonstração 1.
          endereco: novaColeta.endereco,
          dia: novaColeta.dia,
          materiais: novaColeta.materiais,
        }),
      });
      if (!resposta.ok) throw new Error('Não foi possível agendar a coleta.');
      const coletaCriada = await resposta.json();
      setColetas((atuais) => [{ ...coletaCriada, pesagens: coletaCriada.pesagens || [] }, ...atuais]);
      setErroApi('');
      setModalAgendamento(false);
    } catch {
      setErroApi('Não foi possível agendar agora. Confira se o backend está ligado.');
    }
  }

  // Esta função registra uma pesagem, atualiza os pontos e conclui a coleta.
  async function salvarPesagem(pesagem) {
    if (token === 'demo') {
      setColetas((atuais) => atuais.map((coleta) => coleta.id === coletaPesagem.id
        ? { ...coleta, situacao: 'Coletada', pontos: coleta.pontos + pesagem.pontos, pesagens: [...(coleta.pesagens || []), pesagem] }
        : coleta));
      setErroApi('');
      setColetaPesagem(null);
      return;
    }
    try {
      const resposta = await fetch(`${API_BASE_URL}/coletas/${coletaPesagem.id}/pesagens`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({ material: pesagem.material, quilos: pesagem.quilos }),
      });
      if (!resposta.ok) throw new Error('Não foi possível registrar a pesagem.');
      const pesagemCriada = await resposta.json();
      setColetas((atuais) => atuais.map((coleta) => coleta.id === coletaPesagem.id
        ? { ...coleta, situacao: 'Coletada', pontos: coleta.pontos + pesagemCriada.pontos, pesagens: [...(coleta.pesagens || []), pesagemCriada] }
        : coleta));
      setErroApi('');
      setColetaPesagem(null);
    } catch {
      setErroApi('Não foi possível registrar a pesagem. Confira se o backend está ligado.');
    }
  }

  function alternarPerfilDemo() {
    setPerfil((atual) => atual === 'moradora' ? 'cooperativa' : 'moradora');
    setUsuario((atual) => atual?.tipo === 'morador' ? { nome: 'Osmar Coordenador', tipo: 'cooperativa' } : { nome: 'Joana Martins', tipo: 'morador' });
  }

  return <div className="aplicativo"><header className="barra-superior"><div className="barra-interior"><Marca /><div className="navegacao-centro"><span className="navegacao-ponto" />{perfil === 'moradora' ? 'Seu cantinho sustentável' : 'Operação de coleta'}</div><SeletorPerfil perfil={perfil} modoDemo={token === 'demo'} aoAlternarDemo={alternarPerfilDemo} aoSair={() => { localStorage.removeItem('volta-token'); window.location.reload(); }} /></div></header>
    {erroApi && <div className="aviso-api" role="status"><span>!</span>{erroApi}<button onClick={() => setErroApi('')} aria-label="Fechar aviso">×</button></div>}
    {carregando ? <main className="estado-carregamento"><span className="carregando-spinner" />Carregando suas coletas...</main> : perfil === 'moradora' ? <TelaMoradora coletas={coletasOrdenadas} nomeMoradora={usuario?.nome} aoAgendar={() => setModalAgendamento(true)} aoSelecionar={setColetaAtiva} /> : <TelaCooperativa coletas={coletasOrdenadas} aoPesagem={setColetaPesagem} />}
    <footer className="rodape"><Marca /><span>Pequenas atitudes, um futuro que volta.</span><span className="rodape-direitos">Feito com cuidado <span>✳</span></span></footer>
    {modalAgendamento && <FormularioAgendamento aoSalvar={salvarAgendamento} aoCancelar={() => setModalAgendamento(false)} />}
    {coletaAtiva && <DetalheColeta coleta={coletaAtiva} aoFechar={() => setColetaAtiva(null)} />}
    {coletaPesagem && <FormularioPesagem coleta={coletaPesagem} aoSalvar={salvarPesagem} aoCancelar={() => setColetaPesagem(null)} />}
  </div>;
}

// Este componente decide se a pessoa vê a tela de login ou o painel do perfil autenticado.
export default function Aplicativo() {
  const [token, setToken] = useState(() => localStorage.getItem('volta-token'));
  if (!token) return <TelaLogin aoEntrar={setToken} />;
  return <PainelAplicativo key={token} />;
}
