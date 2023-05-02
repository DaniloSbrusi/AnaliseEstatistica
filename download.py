import basedosdados as bd
import pandas as pd

df_frota = bd.read_table(dataset_id='br_denatran_frota', table_id='municipio_tipo', billing_project_id="cnpj-377823")
df_populacao = bd.read_table(dataset_id='br_ibge_populacao', table_id='municipio', billing_project_id="cnpj-377823")

df_frota.to_csv('frota.csv', index=False)
df_populacao.to_csv('populacao.csv', index=False)
