from typing import Annotated
from fastapi import FastAPI, Path, Request
from fastapi.responses import RedirectResponse
from .dao import get_samples as dao_get_samples
from .dao import get_taxa as dao_get_taxa
from .dao import get_bugs_by_sample as dao_get_bugs_by_sample
from pydantic import BaseModel

app = FastAPI()


@app.middleware("http")
async def get_real_ip(request: Request, call_next):
    # Get the real IP from X-Forwarded-For or X-Real-IP headers
    client_ip = (
        request.headers.get("X-Forwarded-For")
        or request.headers.get("X-Real-IP")
        or request.client.host
    )

    # Optional: you can add this to the request state if you want to use it later
    request.state.client_ip = client_ip

    response = await call_next(request)
    return response


class Samples(BaseModel):
    sample_ids: list[str]


class Taxa(BaseModel):
    tax_ids: list[str]


class MetaphlanBug(BaseModel):
    sample_id: str
    tax_id_string: str
    clade_name: str
    rel_abundance: float


class MetaphlanBugsList(BaseModel):
    bugs: list[MetaphlanBug]


@app.get("/", include_in_schema=False)
async def root():
    # redirect to the docs
    return RedirectResponse(url="/docs")


@app.get("/samples", response_model=Samples)
async def get_samples() -> Samples:
    """List the unique sample IDs in the database!"""
    res = await dao_get_samples()
    return Samples(**res)


@app.get("/taxa", response_model=Taxa)
async def get_taxa() -> Taxa:
    """List the unique taxonomic IDs in the database."""
    res = await dao_get_taxa()
    return Taxa(**res)


@app.get("/metaphlan/{sample_id}", response_model=MetaphlanBugsList)
async def get_bugs_by_sample(
    sample_id: Annotated[
        str,
        Path(
            description="The sample ID to query. This typically looks like 'SAMEA10739627'.",
            example="SAMEA10739627",
        ),
    ],
) -> MetaphlanBugsList:
    """Metaphlan results by sample id."""
    res = await dao_get_bugs_by_sample(sample_id)
    retres = []
    for bug in res:
        new_bug = MetaphlanBug(
            sample_id=bug[0],
            clade_name=bug[1],
            tax_id_string=bug[2],
            rel_abundance=bug[3],
        )
        retres.append(new_bug)
    return MetaphlanBugsList(bugs=retres)
