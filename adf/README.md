# Recursos de ADF

Los recursos ya están exportados y saneados en este repo (linked services con `encryptedCredential` reemplazado por un placeholder — ese valor es una credencial encriptada local al Integration Runtime y no es portable ni reutilizable fuera de esa máquina/tenant, pero se redactó igual por buena práctica).

Si necesitas re-exportarlos tras un cambio, pasos manuales desde `adf-acmesim-dev`:

## Opción A — Desde el portal de ADF Studio (recomendado, más simple)

Para cada recurso (Linked Service, Dataset, Pipeline):

1. Abrir [ADF Studio](https://adf.azure.com) → seleccionar `adf-acmesim-dev`.
2. En el panel de autor (lápiz), clic derecho sobre el recurso → **Export template** (o abrir el recurso → botón `{ }` / "Edit as JSON" según la vista).
3. Guardar el JSON resultante en la carpeta correspondiente con el nombre del recurso:
   - `adf/linkedServices/ls_sqlserver_onprem.json`
   - `adf/linkedServices/ls_adls_gen2.json`
   - `adf/datasets/ds_sqlserver_customers.json`
   - `adf/datasets/ds_adls_bronze_customers.json`
   - `adf/pipelines/pl_sqlserver_to_bronze.json`

**Importante:** el JSON de `ls_adls_gen2` puede incluir el Account Key en texto plano si se exporta directo desde el recurso. Antes de commitear, reemplazar cualquier secreto/connection string por un placeholder (ej. `"<ACCOUNT_KEY>"`), igual que se hace con `.env` vs `.env.example`.

## Opción B — Vía ARM template completo (más "production-like")

1. En ADF Studio → **ARM Template** (ícono en la barra superior) → **Export ARM Template**.
2. Descarga un `.zip` con `arm_template.json` y `arm_template_parameters.json` para todo el factory.
3. Extraer solo las definiciones relevantes (linkedServices, datasets, pipelines) o dejar el ARM template completo en `adf/arm_template/` si prefieres esa granularidad en vez de archivos sueltos por recurso.

## Opción C — Vía Azure CLI / az datafactory

```bash
az datafactory linked-service show --factory-name adf-acmesim-dev --resource-group rg-acmesim-dev --name ls_sqlserver_onprem > adf/linkedServices/ls_sqlserver_onprem.json
az datafactory linked-service show --factory-name adf-acmesim-dev --resource-group rg-acmesim-dev --name ls_adls_gen2 > adf/linkedServices/ls_adls_gen2.json
az datafactory dataset show --factory-name adf-acmesim-dev --resource-group rg-acmesim-dev --name ds_sqlserver_customers > adf/datasets/ds_sqlserver_customers.json
az datafactory dataset show --factory-name adf-acmesim-dev --resource-group rg-acmesim-dev --name ds_adls_bronze_customers > adf/datasets/ds_adls_bronze_customers.json
az datafactory pipeline show --factory-name adf-acmesim-dev --resource-group rg-acmesim-dev --name pl_sqlserver_to_bronze > adf/pipelines/pl_sqlserver_to_bronze.json
```

Antes de commitear, revisa cada archivo y reemplaza cualquier secreto por un placeholder.
