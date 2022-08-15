# ordenamelo
> Una app cli para renombrar y mover esos odiosos comprobantes de pago mensuales!

![license](https://img.shields.io/badge/license-Apache-orange)
![made_with](https://img.shields.io/badge/Made%20with-Python-blue)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/gonzalezgbr/sachagrilla/graphs/commit-activity)


Si haces muchos pagos por home banking y guardas los comprobantes pero no tienes ganas de ordenarlos, esta es tu solución!

Con `ordenamelo` puedes renombrar los archivos pdf de comprobantes de pago o transferencias con un solo comando. 
Opcionalmente, se pueden mover a una carpeta pre-definida.

## Instalación

> ⚠️ *Por el momento, `ordenamelo` solo se puede instalar como un paquete Python, es decir, tienes que tener Python y pip instalado en tu sistema.*   

1. Descargar `.whl` de la carpeta `dist/` de este repo.
2. En una terminal ejecutar: 

- OS X & Linux:

```shell
python3 -m pip install nombre_del_wheel_.whl
```
   
- Windows:

```shell
py -m pip install nombre_del_wheel.whl 
```

## Como usar

La primera vez vas a tener que configurar tus carpetas, palabras clave y reglas.

> ⚠️ *Actualmente, `ordenamelo` solo funciona con comprobantes de los bancos Nación y Santander de Argentina.* 

### Configurar

```shell
ordenamelo --config 
```

![config](docs/config.png)

- Sección `paths`:
  - `origin` carpeta donde buscar los comprobantes. Usualmente será *descargas*.
  - `dest` carpeta a donde mover los comprobantes. Tener en cuenta que dentro de esta carpeta:
    - se crea una carpeta por año para guardar los comprobantes
    - se crea una carpeta `transferencias` dentro de la anual para guardar los comprobantes de transferencias

- Sección `keywords`:
  - Se deben incluir las palabras que identifican a los archivos. Usualmente `pago` y `transferencia` son suficientes.
  - Deben ir una por línea y con signo = al final.

- Sección `rules`: contiene las reglas para renombrar los archivos.
  - El formato general del nombre es AÑO-MES-textoDerechaRule.pdf
    - El año y el mes se toman automáticamente el día del pago (cuando se genera el pdf del comprobante).
    - Las claves (texto a la izquierda) deben identificar de forma única ese tipo de comprobante, por ejemplo, número de cliente o de cuenta.

### Uso

Para renombrar y mover todos los archivos que se encuentran:

```shell
ordenamelo 
```

Solo renombrar, sin mover:

```shell
ordenamelo -ro
```

Mientras se ejecuta se imprimen mensajes indicando los archivos, encontrados, renombrados, movidos, etc.

![ordenamelo-run](docs/ordenamelo.png)


## Release History

* 0.1.0
    * Primer release


## Meta

By GG - [@GargaraG](https://twitter.com/GargaraG) 

Distribuido bajo licencia Apache. Ver ``LICENSE`` para más información.

[https://github.com/gonzalezgbr/](https://github.com/gonzalezgbr/)



