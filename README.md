# Ejercicio de postulación a Fintual

**Autor**: Gustavo Truan

**Esta solución está implementada en Python 3.9.6**

Pese a ser heavy user de AI, me tomé el tiempo de hacer el código y el ejemplo de ejecución completamente a mano para demostrar mejor la estructura de mi solución y mi *thought process* ya que considero que este es un problema lo suficientemente simple en implementación. 

Tanto el código como la documentación están en inglés y explican muy a grandes rasgos la estructura de mi código y la forma de rebalancear el portafolio, junto con mis supuestos y limitaciones. 

Evité hacer over-engineering dado el scope del problema por lo que todo está dispuesto en un archivo `main.py` sin requirements, para llegar y ejecutar. En la parte de ejecución (al final del archivo) se puede declarar la *allocation* del portafolio y los stocks de este. Los precios y tipos de stocks se declaran al principio del archivo.

Al correr la solución, se debería imprimir el output en consola de la siguiente forma:
```plaintext
Portfolio value: $2800
Allocations:
META | 30.0%
AAPL | 60.0%
NVDA | 10.0%
Current stocks:
META (price=100) | 3 shares
AAPL (price=150) | 0 shares
NVDA (price=250) | 10 shares
Buy 5.4 shares of META
Buy 11.2 shares of AAPL
Sell 8.88 shares of NVDA
```

Saludos.