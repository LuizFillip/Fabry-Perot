{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Análise e redução dos dados de Interferômetro Fabry-Perot (FPI)\n",
    "\n",
    "O interferômetro Fabry-Perot MiniME Doppler Imaging localizado em Cariri no nordeste do Brasil é operado pela Universidade Federal de Campina Grande em colaboração com a Universidade de Illinois em Urbana-Champaign e Clemson University. O instrumento está hospedado em um site operado pelo Instituto Nacional de Pesquisas Espaciais localizado na latitude 7.38S e longitude 36.52W. \n",
    "\n",
    "O FPI utiliza um diâmetro de 42 mm Etalon de diâmetro C com espaçamento fixo de 1,5 cm. A refletividade do etalon é ~77% a 630,0 nm. Um filtro de interferência de banda estreita centrado em 630,0 nm isola a emissão termoférica redline decorrente da recombinação dissociativa de O2+. Aproximadamente 11 anéis C do padrão de interferência são visualizados em um circuito termoelétrico CCD refrigerado. Um sistema de varredura do céu de espelho duplo é usado para especificar o direção de cada observação. Este instrumento faz parte do Observatório Equatorial Noturno Relocável de Regiões Ionosféricas (RENOIR) e muitas vezes opera em conjunto com um segundo instrumento FPI localizado em Cajazeiras, Brasil. \n",
    "\n",
    "Dados disso também estão contidos no banco de dados Madrigal. Descrição de Procedimento de Análise: As medições de vento e temperatura são derivadas a partir de imagens capturadas por um CCD de várias ordens de um Fabry-Perot Padrão de franja C de airglow atmosférico. Intercalado com airglow fazemos medições de uma frequência difusa estabilizada laser para monitorar a deriva do instrumento durante a noite. Como o laser é uma fonte monocromática conhecida, essas medições fornece a função de instrumento, que é o kernel que usamos para deconvolve as medidas do céu."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Filtro e Cálculo das Componentes Zon e Med\n",
    "\n",
    "\n",
    "* Fórmula geral:\n",
    "    \n",
    "    $V_{LOS} = w \\sin(\\alpha) + [v \\cos(\\theta) + u \\sin(\\theta)]\\cos(\\alpha)$\n",
    "  \n",
    "    Onde, $\\alpha$ é o angulo de elvação (0 horizontal e 90 no zenite) e $\\theta$ é ângulo azimute (0 para o Norte e 90 para o Leste). \n",
    "\n",
    "* Que nos permite estimar a componente vertical (Zenite)\n",
    "    \n",
    "    $w = \\frac{V_{LOS}}{\\sin(\\alpha = 90)} = V_{LOS}$\n",
    "\n",
    "* Separação de cada direção (Norte, Leste, Oeste, Sul)\n",
    "    * Norte ($\\alpha  = 45, \\theta = 0$)\n",
    "    * Leste ($\\alpha  = 45, \\theta = 90$)\n",
    "    * Sul ($\\alpha  = 45, \\theta = 180$)\n",
    "    * Oeste ($\\alpha  = 45, \\theta = 270$)\n",
    "    \n",
    "* Leste e Oeste LOS podem ser usados para calcular a componente zonal \n",
    "\n",
    "    $u = \\frac{V_{LOS}}{\\sin(\\theta) \\cos(\\alpha)}$ \n",
    "\n",
    "* Norte e Sul LOS podem ser usados para calcular a componente Meridional \n",
    "\n",
    "    $v = \\frac{V_{LOS}}{\\cos(\\theta) \\cos(\\alpha)}$ "
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
