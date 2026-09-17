# Diário de leitura: a contradição entre os três estudos

**Objetivo.** Entender por que os três estudos discordam sobre IA e produtividade.

**Material.** Peng et al. (2023), METR (2025), Anthropic (2026) — leitura dos três, ~2h.

**O que os números diziam.** 55,8% mais rápido no Copilot. 19% mais lento na METR. Sucesso subindo de 15% para 33% com expertise na Anthropic.

**Onde a contradição se desfez.** O ambiente. Servidor HTTP novo com testes visíveis contra repositório de 1,1 milhão de linhas e dez anos de convenção não escrita. A METR admite que seu resultado é compatível com ganho em projeto greenfield.

**Onde ela não se desfez.** A METR acha mais lentidão onde há mais familiaridade; a Anthropic, mais sucesso onde há mais expertise. Medem "experiência" de formas diferentes.

## O que aprendi

O número da manchete não é comparável entre os três porque nenhum deles mede a mesma grandeza. Peng e METR medem tempo até a tarefa ficar pronta, com grupo de controle — sabem o que teria acontecido sem IA. A Anthropic mede taxa de sucesso dentro de sessões que já existiam, sem contrafactual: mostra quem extrai mais do agente, não se alguém ficou mais rápido. Colocar os três lado a lado como se fossem a mesma régua é o que produz a impressão de contradição.

A segunda coisa é o quanto o contexto pesa mais do que a capacidade do modelo. A METR usou Claude 3.5 e 3.7, bem mais capazes que o Codex de 2022 do estudo do Copilot, e o resultado inverteu. O que mudou foi a tarefa: de código novo com teste explícito para código velho com convenção implícita. Em repositório maduro, boa parte do tempo vai para revisar e readequar a saída, e não para produzi-la.

A terceira é a mais desconfortável. Os desenvolvedores da METR estimaram que a IA os acelerou em 20%, depois de terem sido desacelerados em 19% — e 69% continuaram usando o Cursor depois do estudo. Percepção de ganho e ganho medido são coisas separadas, e no caso deles andaram em direções opostas. Isso vale como aviso para qualquer avaliação da própria produtividade feita sem cronômetro.

A quarta é que "experiência" precisa ser desambiguada antes de qualquer comparação. Anos de carreira (Peng), convivência com aquele repositório (METR) e domínio do problema (Anthropic) são três variáveis diferentes, e cada estudo mediu uma. Nada impede que apontem em direções opostas ao mesmo tempo.

## Fontes

- Peng, Kalliamvakou, Cihon e Demirer, *The Impact of AI on Developer Productivity: Evidence from GitHub Copilot* (arXiv:2302.06590)
- Becker, Rush, Barnes e Rein, *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity*, METR (arXiv:2507.09089v2)
- Hitzig, Massenkoff, Lyubich, Heller e McCrory, *Agentic coding and persistent returns to expertise*, Anthropic, 16/06/2026

> *Autores: Antonio Morais e Polyana Moraes*