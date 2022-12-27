# Lenguaje Luyer

Proyecto para la materia de diseño de compiladores del semestre Agosto-Diciembre 2022.

## Setup

Luyer es un lenguaje hecho en Python, por lo que este se necesita para ejecutarlo.

Además, ya con python instalado, se necesitan descargar e instalar dos librerías, LARK y NumPy. Para instalarla ejecuta los siguiente en tu terminal.

`pip install lark`  
`pip install numpy`

Después clona este repositorio

`git clone https://github.com/Luyer74/Compilador`

## Sintaxis y ejecución

La estructura de un programa hecho en Luyer es
`Globales -> Funciones -> Main `

### Variables

Las variables en Luyer se pueden declarar localmente o globalmente. Como se vió en la estructura anterior, las globales son lo primero. Las variables locales se declaran al inicio de main o de cada función para ser accesadas ahí mismo. Las variables se pueden declarar sin valor

`int : i`

o con valor asignado

`int : i = 0`

### Condiciones

Las condiciones siguen la sintaxis estándar

```
    if (i != 0){
      out(i);
    } else{
      out("fin");
    }
```

### Ciclos

Se cuentan con ciclos de tipo while

```
  while (i < 100){
    out(i);
    i = i + 1;
  }
```

### Funciones

Para funciones, se sigue el siguiente formato

```
  func int : suma(int : x, int : y){
    ret x + y;
  }
```

### Variables con Dimensiones

Luyer maneja variables de N dimensiones.

```
int : a[10, 5, 2];
```

### Funciones estadísticas

Luyer cuenta con funciones auxiliares.

`fill(método, arreglo)`: Llena un arreglo con el método especificado.

- "zeros", arreglo: llena con ceros
- "ones", arreglo: llena con unos
- "arange", arreglo: llena con números de 0 al tamaño del arreglo en orden
- "random", arreglo: llena con números aleatorios en un rango de 0 al tamaño del arreglo

`min(arreglo)` : Regresa el valor mínimo de un arreglo

`max(arreglo)` : Regresa el valor máximo de un arreglo

`mean(arreglo)` : Regresa el valor promedio de un arreglo

`std(arreglo)` : Regresa el valor de desviación estándar de un arreglo

`len(arreglo)` : Regresa la longitud de un arreglo

### Ejecución

Para ejecutar un programa en Luyer, debemos reemplezar una parte del archivo `compilador.py`

En la sección de
`input = open("./pruebas/array_test.ly", "r").read()` se reemplaza el archivo actual por tu propio archivo, el cual puede tener cualquier terminación.
