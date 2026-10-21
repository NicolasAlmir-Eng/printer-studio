
Printer Studio Pro (Linux Edition)

O Printer Studio é uma interface gráfica avançada desenvolvida em Python (Tkinter) pensada para preencher a lacuna de bons softwares de gerenciamento de impressoras e scanners no ecossistema Linux (Ubuntu/Debian). O aplicativo consolida ferramentas de impressão fotográfica, digitalização assistida e manutenção de hardware em uma única UI limpa.

Principais Integrações e Dependências do Sistema

O software atua como uma interface inteligente por cima de poderosas ferramentas Linux:

CUPS (lp, cancel, cupsenable): Gerenciamento da fila de impressão.

SANE (scanimage, airscan-discover): Captura de scanners na rede via protocolo eSCL.

Tesseract OCR: Extração de texto a partir de imagens digitalizadas.

ImageMagick (convert, mogrify): Tratamento de imagem, auto-trim de bordas brancas e masterização para impressões fotográficas.

Escputil: Utilitário para limpeza de cabeçotes e verificação de tintas via cabo USB.

Funcionalidades

Digitalização (Scanner)

Descoberta automática de scanners na rede (Wi-Fi).

Suporte a múltiplas resoluções (150 a 4800 DPI) e modo de cor.

Extração com IA (OCR): Lê o documento escaneado e gera um arquivo .txt automático.

Múltiplas Páginas: Escaneia sucessivamente e une tudo em um único .pdf.

Recorte de bordas automático.

Impressão Fotográfica e de Documentos

Controle total de qualidade (Draft, Normal, High, Ultra), papéis (Glossy, Matte) e cópias.

Masterização de Imagem: Um pipeline que ajusta nitidez, saturação e densidade de pixels (600ppi) antes da foto ir para o CUPS.

Animação visual em tempo real acompanhando o progresso da impressão lendo sensores do CUPS.

Modo Borderless (sem bordas) nativo.

Manutenção e Ferramentas

Atalhos rápidos para o painel CUPS (Localhost:631) e UI nativa do Ubuntu.

Execução de testes de bico (Nozzle Check) via USB.

Limpeza forçada de cabeçote de impressão.

Como Instalar e Rodar

Certifique-se de ter os pacotes de sistema necessários instalados no Ubuntu:

sudo apt update
sudo apt install sane-utils cups-client sane-airscan tesseract-ocr tesseract-ocr-por tesseract-ocr-eng imagemagick img2pdf escputil


Instale as dependências Python (caso não existam):

pip install Pillow


Execute o programa:

python3 main.py


