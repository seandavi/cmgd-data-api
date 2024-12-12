from .db import get_clickhouse_client


async def get_samples():
    client = await get_clickhouse_client()
    result = await client.query(
        "SELECT distinct sample_id FROM src_cmgd__metaphlan_bugs"
    )
    result_cols = result.result_columns
    return {"sample_ids": result_cols[0]}


async def get_taxa():
    client = await get_clickhouse_client()
    result = await client.query(
        "SELECT distinct tax_id_string FROM src_cmgd__metaphlan_bugs"
    )
    result_cols = result.result_columns
    return {"tax_ids": result_cols[0]}


async def get_bugs_by_sample(sample_id: str):
    client = await get_clickhouse_client()
    result = await client.query(
        """SELECT sample_id, clade_name, tax_id_string, relative_abundance  
        FROM src_cmgd__metaphlan_bugs WHERE sample_id = %(sample_id)s""",
        {"sample_id": sample_id},
    )
    return result.result_rows
