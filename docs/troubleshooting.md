# Troubleshooting

## SHIR: `JreNotFound` / no puede cargar `jvm.dll` al escribir Parquet

**Síntoma**

Al ejecutar el pipeline `pl_sqlserver_to_bronze` con destino Parquet en ADLS Gen2, la actividad Copy Data falla en el Self-Hosted Integration Runtime (`shir-acmesim-dev`) con un error del tipo `JreNotFound`, indicando que no puede localizar/cargar `jvm.dll` (necesaria porque la escritura de Parquet internamente depende de un runtime Java).

**Causa raíz**

El SHIR localiza el JRE instalado mediante una clave de registro **legacy**:

```
HKEY_LOCAL_MACHINE\SOFTWARE\JavaSoft\Java Runtime Environment
```

Las distribuciones modernas de Java (JDK/JRE 17+, incluyendo Eclipse Adoptium/Temurin) **ya no crean esa clave por defecto** — usan `JavaSoft\JDK` en su lugar. Como resultado, aunque Java esté instalado y funcional, el SHIR no lo encuentra.

**Solución**

1. Instalar **Eclipse Temurin JRE 8** (no una versión moderna).
2. Durante la instalación, elegir **instalación personalizada** ("Custom install").
3. Marcar explícitamente la opción **"Set JAVA_HOME variable"** / **"Claves de registro JavaSoft"** — esta opción es la que crea la clave legacy `JavaSoft\Java Runtime Environment` que el SHIR necesita.
4. Reiniciar el servicio "Integration Runtime Service" (o reiniciar Windows) para que el SHIR vuelva a detectar el JRE.
5. Re-ejecutar el pipeline.

**Por qué JRE 8 y no una versión moderna:** el mecanismo de detección del SHIR es el legacy, así que la vía más simple es usar la versión de Java que todavía crea esa clave por defecto con la opción marcada, en vez de intentar crear la clave de registro manualmente para una versión moderna.

---

## SQL Server vía SHIR: usar `localhost`, no `host.docker.internal`

**Síntoma**

El Linked Service `ls_sqlserver_onprem` no conecta si se configura el server como `host.docker.internal,1433`.

**Causa raíz**

`host.docker.internal` solo tiene sentido cuando el proceso que intenta conectar corre **dentro** de un contenedor Docker y necesita alcanzar el host. El SHIR corre **nativo en Windows** (no dentro de Docker) — el que está en un contenedor es el propio SQL Server. Desde el SHIR, el contenedor de SQL Server es simplemente accesible en `localhost` porque Docker Desktop en Windows publica el puerto `1433` en el host.

**Solución**

Configurar el Linked Service con `server = localhost,1433`.

---

## Operación diaria: reinicios de Windows

Docker Desktop y el servicio "Integration Runtime Service" **no arrancan solos** tras un reinicio de Windows (salvo que se configure inicio automático). Antes de correr el pipeline hay que verificar/activar manualmente:

1. Docker Desktop está corriendo y el contenedor `sqlserver-onprem-dev` está `up`.
2. El servicio Windows "Integration Runtime Service" está iniciado (se puede verificar desde la app "Microsoft Integration Runtime" o `services.msc`).
