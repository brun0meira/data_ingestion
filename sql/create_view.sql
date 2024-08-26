CREATE VIEW IF NOT EXISTS character_info_view AS
SELECT
    data_ingestao,
    JSONExtractString(dado_linha, 'name') AS name,
    JSONExtractString(dado_linha, 'status') AS status,
    JSONExtractString(dado_linha, 'species') AS species,
    JSONExtractString(dado_linha, 'gender') AS gender,
    toDateTime(JSONExtractInt(dado_linha, 'data_ingestao') / 1000) AS data_ingestao_datetime
FROM working_data;