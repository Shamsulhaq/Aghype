import json
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator

async def paginate(
    model: type[Model],
    start: int = 0,
    limit: int = 10,
    filters: dict | None = None,
    order_by: list[str] | None = None,
):
    """
    Generic paginator for any Tortoise ORM model.
    """
    queryset = model.all()

    if filters:
        print("Applying filters:", filters)
        queryset = queryset.filter(**filters)

    if order_by:
        queryset = queryset.order_by(*order_by)

    total = await queryset.count()
    next = True if (start + 1) * limit < total else False
    previous = True if start > 0 else False

    # Apply pagination without awaiting
    queryset = queryset.offset(start).limit(limit)

    # Dynamically create Pydantic model
    PydanticModel = pydantic_model_creator(model)

    # from_queryset works directly on QuerySet
    results = await PydanticModel.from_queryset(queryset)

    return {
        "count": total,
        "next": next,
        "previous": previous,
        "results": results,
    }


async def paginate_queryset(
    queryset,
    start: int = 0,
    limit: int = 10,
):
    """
    Generic paginator for any Tortoise ORM QuerySet.
    """
    # Apply pagination without awaiting
    pg_queryset = queryset.offset(start).limit(limit)

    return pg_queryset