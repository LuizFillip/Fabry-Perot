# Análise e redução dos dados de Interferômetro Fabry-Perot (FPI)


# Filtro e Cálculo das Componentes Zon e Med


* Separação de cada direção (Norte, Leste, Oeste, Sul)
    * Norte ($\alpha  = 45, \theta = 0$)
    * Leste ($\alpha  = 45, \theta = 90$)
    * Sul ($\alpha  = 45, \theta = 180$)
    * Oeste ($\alpha  = 45, \theta = 270$)
    
    
* Fórmula geral:
    
    $V_{LOS} = w \sin(\alpha) + [v \cos(\theta) + u \sin(\theta)]\cos(\alpha)$
  
    Onde, $\alpha$ é o angulo de elvação (0 horizontal e 90 no zenite) e $\theta$ é ângulo azimute (0 para o Norte e 90 para o Leste). 

* Que nos permite estimar a componente vertical (Zenite)
    
    $w = \frac{V_{LOS}}{\sin(\alpha = 90)} = V_{LOS}$
    
* Leste e Oeste LOS podem ser usados para calcular a componente zonal 

    $u = \frac{V_{LOS}}{\sin(\theta) \cos(\alpha)}$ 

* Norte e Sul LOS podem ser usados para calcular a componente Meridional 

    $v = \frac{V_{LOS}}{\cos(\theta) \cos(\alpha)}$ 
