document.addEventListener('DOMContentLoaded', () => {

    // ==========================================
    // 1. MÁSCARA DO CPF (Apenas na página de Login)
    // ==========================================
    const cpfInput = document.getElementById('cpf');
    if (cpfInput) {
        cpfInput.addEventListener('input', (e) => {
            let value = e.target.value.replace(/\D/g, "").slice(0, 11);
            value = value.replace(/^(\d{3})(\d)/, "$1.$2");
            value = value.replace(/^(\d{3})\.(\d{3})(\d)/, "$1.$2.$3");
            value = value.replace(/^(\d{3})\.(\d{3})\.(\d{3})(\d{1,2})$/, "$1.$2.$3-$4");
            e.target.value = value;
        });
    }

    // ==========================================
    // 2. LÓGICA DA URNA ELETRÔNICA (Telas de Votação)
    // ==========================================
    const formUrna = document.getElementById('form-urna');
    
    if (formUrna) {
        const digitos = document.querySelectorAll('.digito');
        const campoVoto = document.getElementById('campo-voto');
        const botoesTeclas = document.querySelectorAll('.teclas');
        const btnBranco = document.getElementById('branco');
        const btnCorrigir = document.getElementById('corrigir');
        const btnConfirmar = document.getElementById('confirmar');

        let posicaoAtual = 0;
        let eVotoBranco = false;

        // Clique nos botões numéricos (1 a 0)
        botoesTeclas.forEach(botao => {
            botao.addEventListener('click', () => {
                if (posicaoAtual < digitos.length && !eVotoBranco) {
                    digitos[posicaoAtual].value = botao.innerText.trim();
                    posicaoAtual++;
                }
            });
        });

        // Botão BRANCO
        if (btnBranco) {
            btnBranco.addEventListener('click', () => {
                limparDigitos();
                eVotoBranco = true;
                if (campoVoto) campoVoto.value = "BRANCO";
                formUrna.submit(); // Envia o formulário automaticamente ao clicar em BRANCO
            });
        }

        // Botão CORRIGIR
        if (btnCorrigir) {
            btnCorrigir.addEventListener('click', () => {
                limparDigitos();
            });
        }

        // Envio/Confirmação do Formulário
        formUrna.addEventListener('submit', (e) => {
            if (eVotoBranco) return;

            // Coleta os valores digitados nos campos
            let numeroCompleto = "";
            digitos.forEach(input => {
                numeroCompleto += input.value;
            });

            // Valida se todos os dígitos foram preenchidos
            if (numeroCompleto.length < digitos.length) {
                e.preventDefault();
                alert("Preencha todos os dígitos ou clique em BRANCO para votar.");
                return;
            }

            // Armazena no input hidden para o Flask receber
            if (campoVoto) {
                campoVoto.value = numeroCompleto;
            }
        });

        function limparDigitos() {
            digitos.forEach(input => input.value = "");
            posicaoAtual = 0;
            eVotoBranco = false;
            if (campoVoto) campoVoto.value = "";
        }
    }
});