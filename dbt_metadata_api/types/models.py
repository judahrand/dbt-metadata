from typing import Optional

import strawberry

from ..interfaces import NodeInterface
from .common import CatalogColumn
from .sources import SourceNode
from .metrics import MetricNode


@strawberry.type
class ModelNode(NodeInterface):

    def __post_init__(self) -> None:
        if self.node.resource_type.value != "model":
            raise TypeError("That unique_id is not a model.")

    @strawberry.field
    def alias(self) -> Optional[str]:
        return self.node().alias

    @strawberry.field
    def children_l1(self) -> Optional[list[str]]:
        return self.manifest.child_map[self.unique_id]

    @strawberry.field
    def columns(self) -> Optional[list[CatalogColumn]]:
        return [
            CatalogColumn(
                name=col.name,
                index=idx,
                description=col.description,
                meta=col.meta,
                tags=col.tags,
                type=col.data_type,
            )
            for idx, col
            in enumerate(self.node.columns.values())
        ]

    @strawberry.field
    def compiled_code(self) -> Optional[str]:
        return self.node.compiled_code

    @strawberry.field
    def compiled_sql(self) -> Optional[str]:
        if getattr(self.ndoe, "language", "sql") == "sql":
            return self.compiled_code()
        return None

    @strawberry.field
    def database(self) -> Optional[str]:
        return self.node.database

    @strawberry.field
    def depends_on(self) -> Optional[list[str]]:
        return [
            node
            for node_type in self.node.depends_on.values()
            for node in node_type
        ]

    @strawberry.field
    def materialized_type(self) -> Optional[str]:
        return self.node.config.materialized

    @strawberry.field
    def metrics(self) -> Optional[list[MetricNode]]:
        if hasattr(self.node, "metrics"):
            return [
                MetricNode(
                    manifest=self.manifest,
                    unique_id=unique_id,
                )
                for unique_id in
                self.node.metrics
            ]

    @strawberry.field
    def parents_models(self) -> Optional[list["ModelNode"]]:
        parents = self.manifest.parent_map[self.unique_id]
        return [
            self.manifest.nodes[unique_id]
            for unique_id in parents
            if self.manifest.nodes[unique_id].resource_type.value == "model"
        ]

    @strawberry.field
    def parents_sources(self) -> Optional[list[SourceNode]]:
        parents = self.manifest.parent_map[self.unique_id]
        return [
            SourceNode(
                manifest=self.manifest,
                unique_id=unique_id,
            )
            for unique_id in parents
            if self.manifest.nodes[unique_id].resource_type.value == "source"
        ]

    @strawberry.field
    def raw_code(self) -> Optional[str]:
        return self.node.raw_code

    @strawberry.field
    def raw_sql(self) -> Optional[str]:
        if getattr(self.ndoe, "language", "sql") == "sql":
            return self.raw_code()
        return None

    @strawberry.field
    def schema(self) -> Optional[str]:
        return self.node.schema_
