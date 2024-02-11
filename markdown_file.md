\setstretch{1.25} % Define o espaçamento entre linhas para 1.25

###  Contexto

A energização de um banco de capacitores (Figura \ref{fig:picture1}) pelo fechamento de um disjuntor resultará em uma alta corrente de pico transitória (Figura \ref{fig:picture2}), denominada inrush. A magnitude e frequência desta corrente de pico transitória são funções:


* 	da tensão aplicada (ponto na onda de tensão no fechamento);
* 	da capacitância equivalente do circuito;
* 	da indutância no circuito (quantidade e localização);
* 	da carga no banco de capacitores no instante de fechamento;
* 	de qualquer amortecimento do circuito devido a resistores de fechamento ou outra resistência no circuito.

	
###  Dados de entrada do banco



* 	Potencia reativa  = 401 MVAr
* 	Tensão trifásica  = 230 kV
* 	Tensão monofásica  = 133 kV
* 	Corrente de curto-circuito  = 63 kA


\begin{center}
	\begin{tabular}{lllllllllll}
\toprule
 & $Q_{3\phi}$ & $Q_{1\phi}$ & $V_{3\phi}$ & $V_{1\phi}$ & $I_{1\phi}$ & $X_{1\phi}$ & $C_{1\phi}$ & $L_{1\phi}$ & $I_{p}/I_{n}$ & $f_{0}$ \\\\
\midrule
0 & 100 MVAr & 33 MVAr & 230 kV & 133 kV & 251 A & 529.0 $\Omega$ & 5.01 µF & 100 µH & 22.0 & 942 Hz \\\\
1 & 111 MVAr & 37 MVAr & 230 kV & 133 kV & 279 A & 476.6 $\Omega$ & 5.57 µF & 100 µH & 74.8 & 7 kHz \\\\
2 & 95 MVAr & 32 MVAr & 230 kV & 133 kV & 238 A & 556.8 $\Omega$ & 4.76 µF & 100 µH & 114.1 & 7 kHz \\\\
3 & 95 MVAr & 32 MVAr & 230 kV & 133 kV & 238 A & 556.8 $\Omega$ & 4.76 µF & 100 µH & 127.8 & 7 kHz \\\\
\bottomrule
\end{tabular}

\end{center}



	
	
###  Considerações Iniciais


A corrente \textit{inrush} transitória não é um fator limitante em aplicações de bancos de capacitores isolados. Contudo, quando os bancos de capacitores são comutados \textit{back-to-back}, ou seja, quando um banco é acionado enquanto outro banco está conectado ao mesmo barramento, correntes transitórias de altas magnitude e frequência natural irão fluir entre o banco acionado e os que já estavam acionados.

	
\begin{figure}[!hbp]
	\centering
	\includegraphics{figs/Picture1}
	\caption{Sistema de banco de capacitores.}
	\label{fig:picture1}
\end{figure}


Essa corrente oscilatória é limitada apenas pela impedância do banco de capacitores e pelo circuito entre o banco ou bancos energizados e o banco comutado (Banco \#0), que geralmente decai para zero em uma fração de um ciclo da frequência do sistema. No caso de comutação \textit{back-to-back}, o componente fornecido pela fonte está em uma frequência mais baixa (60 Hz) e tão pequena quando comparada a corrente \textit{inrush}, que pode ser desprezada \href{https://ieeexplore.ieee.org/document/7035261}{[ANSI/IEEE C37.012-1979]}.



###  Resultados

\begin{figure}[!hbp]
	\centering
	\includegraphics{figs/Correntes.png}
	\caption{Corrente instantânea no banco de capacitores acionado em um ciclo da frequência fundamental.}
	\label{fig:picture2}
\end{figure}

São os valores obtidos com o reator escolhido ($L_{reator} = 100.0 \, \mu \rm{H} $):


* 	Corrente de pico: 43 kA;
* 	Frequência de Oscilação: 6.9 kHz;
* 	Corrente inrush / Corrente nominal: 127.8


###  Conclusão

Reator n\~{a}o adequado, conforme IEEE Std C37.012, p\'{a}gina 16.

###  Referências


\noindent
\begin{tabular}{p{0.2cm} p{15.8cm}}
    \href{https://ieeexplore.ieee.org/document/7035261}{[1]} &
    \begin{minipage}[t]{15.8cm}
        IEEE Application Guide for Capacitance Current Switching for AC High-Voltage Circuit Breakers Rated on a Symmetrical Current Basis, in ANSI/IEEE C37.012-1979, vol., no., pp.1-54, 6 Feb. 1979, doi: 10.1109/IEEESTD.1979.7035261.
    \end{minipage} \\\\

    \href{https://ieeexplore.ieee.org/document/9574631}{[2]} &
    \begin{minipage}[t]{15.8cm}
        IEEE Approved Draft Standard Requirements for Capacitor Switches for AC Systems (1 kV to 38 kV), in IEEE PC37.66/D10, October 2021, vol., no., pp.1-35, 13 Dec. 2021.
    \end{minipage} \\\\

    \href{https://ieeexplore.ieee.org/document/5318709}{[3]} &
    \begin{minipage}[t]{15.8cm}
        IEEE Standard for AC High-Voltage Circuit Breakers Rated on a Symmetrical Current Basis--Preferred Ratings and Related Required Capabilities for Voltages Above 1000 V, in IEEE Std C37.06-2009, vol., no., pp.1-56, 6 Nov. 2009, doi: 10.1109/IEEESTD.2009.5318709.
    \end{minipage} \\\\

    \href{https://cdn.standards.iteh.ai/samples/101972/4e7e06bd66d2443da668b8e0c6c60512/IEC-62271-100-2021.pdf}{[4]} &
    \begin{minipage}[t]{15.8cm}
        IEC 62271-100 High-voltage switchgear and controlgear – Part 100: Alternating-current circuit-breakers.
    \end{minipage} \\\\

    \href{https://www.normas.com.br/autorizar/visualizacao-nbr/313/identificar/visitante}{[5]} &
    \begin{minipage}[t]{15.8cm}
        NBR 5282 Capacitores de potência em derivação para sistema de tensão nominal acima de 1000 V.
    \end{minipage} \\\\
\end{tabular}



% Espaço para assinaturas
\noindent % Evita a indentação
\begin{minipage}[t]{0.5\textwidth} % Inicia a primeira coluna para assinatura
	\centering % Alinha o texto ao centro
	\vspace{5cm} % Espaço reservado para a assinatura
	\rule{6cm}{0.4pt}\\ % Linha para assinatura
	**Angelo A. Hafner**\\ % Nome
	Engenheiro Eletricista\\ % Título
	CONFEA: 2.500.821.919\\ % Número do registro
	CREA/SC: 045.776-5\\ % Outro número do registro
	aah@dax.energy % E-mail
\end{minipage}%
\hfill % Espaço entre as colunas
\begin{minipage}[t]{0.5\textwidth} % Inicia a segunda coluna para assinatura
	\centering % Alinha o texto ao centro
	\vspace{5cm} % Espaço reservado para a assinatura
	\rule{6cm}{0.4pt}\\ % Linha para assinatura
	**Tiago Machado**\\ % Nome
	Business Manager\\ % Título
	Mobile: +55 41 99940-3744\\ % Contato
	tm@dax.energy % E-mail
\end{minipage}