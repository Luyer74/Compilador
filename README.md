# Compilador

Proyecto para la clase de Diseño de Compiladores

### Avance semana 1

- Se implementó análisis léxico y sintáctico con LARK.

### Avance semana 2

- Se agregó el cubo semántico

### Avance semana 3

- Se agregó semántica inicial para funciones y main, junto con el directorio de funciones y tablas de variables correspondientes
- Se implementaron puntos neurálgicos para operaciones aritméticas de suma, resta, multiplicación y división
- Se creó un objeto para cuádruplos y se empezaron a imprimir los primeros con los puntos anteriores

### Avance semana 4

- Se agregó la semántica para asignaciones, condiciones y ciclo while.
- Los valores de las variables ahora son manejados correctamente por el directorio
- Se agregaron errores comunes como variables duplicadas o valores inválidos
- Se agregaron variables globales

### Avance semana 5

- Se agregó la semántica para funciones
- Se agregó la tabla de párametros
- Se creó la clase Memoria mediante varias estructuras
- Se manejan direcciones de memoria para todas las variables correctamente
- Se guardan los cuádruplos de inicio de cada función y del main
- Se inició la implementación de cuádruplos de funciones, return aun sin funcionar

### Avance semana 6

- Se modificó la sintáxis para el uso de return, funciones void y con tipo
- Se creó la tabla de constantes
- Se agregó la tabla de parámetros
- Los parámetros se verifican, con su tipo y orden
- Las funciones void y return se manejan correctamente
- Se manejan llamadas dentro de llamadas con una pila de llamadas

### Avance semana 7

- Se maneja la declaración de arreglos de n dimensiones utilizando indexado de tipo C
- Se maneja el acceso de arreglos y su uso en operaciones
- La memoria se aparta correctamente para los arreglos
- Se maneja la asignación en arreglos
- Se creó la máquina virtual con una clase
- La máquina virtual lee cuádruplos en el orden correcto
- La máquina virtual realiza operaciones aritméticas y de asignación
- La clase memoria maneja asignaciones de valores correctamente
- La máquina virtual ejecuta estatutos condicionales y ciclos
- La máquina virtual ejecuta funciones correctamente
- La máquina virtual maneja la recursividad correctamente con una pila de IP
- Se agregaron funciones predefinidas
